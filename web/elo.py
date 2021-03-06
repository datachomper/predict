#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)
from data.models import Box
from numpy import std, average
import sys
import types
import re
from urllib import urlopen
from datatable import datatable
from datetime import date

tally = {}
delta = []
rating = {}

def distance(x, y):
    if (x <= 0) and (y >= 0):
        return y + abs(x)
    if (y <= 0) and (x >= 0):
        return x + abs(y)
    if (y < 0) and (x < 0):
        return abs(abs(y) - abs(x))
    return abs(x - y)

class Stat():
    def __unicode__(self):
        return self.rate

    def __init__(self):
        self.win = 0
        self.loss = 0
        self.rate = 1500

year = date.today().year

# Find number of weeks of data that are available
num_weeks_avail = Box.objects.filter(year=year).order_by('-week')[0].week

# Pre-fetch NFL.com score feed
url = "http://www.nfl.com/liveupdate/scorestrip/scorestrip.json"
raw = urlopen(url).read()

# Iterate over each week's games
for week in range(1, num_weeks_avail+1):
    datamatrix = []
    win = loss = 0
    matches = Box.objects.filter(week=week, year=year)
    for match in matches:
        # Create a stat object for teams
        if not match.home in tally:
            tally[match.home] = Stat()
        if not match.road in tally:
            tally[match.road] = Stat()

        # Keep win/loss ratio tally per week
        winloss = Stat()

        # The Casino's are much smarter than I am so we pre-seed our ratings
        # by reverse engineering their spread predictions
        if week == 1:
            tally[match.home].rate = 1500 - int((match.line * 100/7)/2)
            tally[match.road].rate = 1500 + int((match.line * 100/7)/2)

        match.hrate = tally[match.home].rate
        match.rrate = tally[match.road].rate

        # Find accuracy of curent ELO
        prediction = (tally[match.road].rate - tally[match.home].rate)*7/100
        match.prediction = prediction

        # Figure out who to bet on
        if (distance(prediction, match.line) <= 1):
            # Skip bets that are too close
            match.bet = None
        # Don't bet on this game
        elif (prediction == 0):
            match.bet = None
        # We favor the home team
        elif (prediction < 0):
            # Home team will make their spread
            if (match.line - prediction > 0):
                match.bet = match.home
            # Home team will not make their spread
            else:
                match.bet = match.road
        # We favor the road team
        else:
            # Road team will make their spread
            if (prediction - match.line > 0):
                match.bet = match.road
            # Road team will not make their spread
            else:
                match.bet = match.home

        # We have three states, we're either pre-games, during-games, or post games
        if type(match.hscore) is types.NoneType:
            # No final score data yet, check if we're mid-games
            #print "%s(%d) vs %s(%d) : predicted %d : line %d" % (match.home, tally[match.home].rate, match.road, tally[match.road].rate, prediction, match.line)

            # If there is nfl json data, we're mid game
            if raw:
                # Replace empty csv values with "None"
                # Here we have to use a positive lookahead assertion "(?=,)"
                # which means that we match any two commas together ",," and
                # replace it with ",None,"
                m = re.compile(",(?=,)")
                formatted = m.sub(",None", raw)
                
                # A well formatted JSON string can be eval'd into a python dictionary
                data = eval(formatted)
                
                # NFL uses different abbreviations than we do
                remap = {"SF":"SFO", "NE":"NWE", "SD":"SDG", "GB":"GNB", "TB":"TAM", "NO":"NOR", "KC":"KAN"}

                # Find this match's live data
                for x in data['ss']:
                    # If this game is currently running
                    if x[2] != 'Pregame':
                        # Remap the NFL.com's team acronyms
                        try:
                            x[4] = remap[x[4]]
                        except:
                            pass

                        # We found our game
                        if (x[4] == match.road) and (x[12] == "REG%s"%match.week):
                            # Load up the status member
                            match.status = x[2]
                            try:
                                if (int(match.status) > 0 and int(match.status) < 6):
                                    match.status = "Q"+match.status+" "+x[3]
                            except:
                                pass

                            if(match.status == "final overtime"):
                                match.status = "Final OT"

                            match.hscore = int(x[7])
                            match.rscore = int(x[5])
                            # Add our predicted line to the home team score and compare
                            hscore = match.hscore + match.line
                            rscore = match.rscore

                            # Figure out if we're winning
                            if (match.bet == match.home):
                                # Is the home team beating the vegas spread?
                                if ((hscore - rscore) > 0):
                                    win += 1
                                    match.betresult = "win"
                                elif (hscore - rscore == 0):
                                    match.betresult = "push"
                                else:
                                    loss += 1
                                    match.betresult = "loss"
                            elif (match.bet == match.road):
                                # Is the road team beating the vegas spread?
                                if ((rscore - hscore) > 0):
                                    # Bet the home team
                                    win += 1
                                    match.betresult = "win"
                                elif (rscore - hscore == 0):
                                    match.betresult = "push"
                                else:
                                    loss += 1
                                    match.betresult = "loss"

        # Game is not live
        else:
            match.status = "Final"
            # Add our predicted line to the home team score and compare
            hscore = match.hscore + match.line
            rscore = match.rscore

            # Figure out if we're winning
            if (match.bet == match.home):
                # Is the home team beating the vegas spread?
                if ((hscore - rscore) > 0):
                    win += 1
                    match.betresult = "win"
                elif (hscore - rscore == 0):
                    match.betresult = "push"
                else:
                    loss += 1
                    match.betresult = "loss"
            elif (match.bet == match.road):
                # Is the road team beating the vegas spread?
                if ((rscore - hscore) > 0):
                    # Bet the home team
                    win += 1
                    match.betresult = "win"
                elif (rscore - hscore == 0):
                    match.betresult = "push"
                else:
                    loss += 1
                    match.betresult = "loss"

        datamatrix.append(match)
        continue

        # If we have the scores, calculate the results
        diff = match.rscore - match.hscore
        spreaddiff = diff - prediction
        d = distance(prediction, diff)
        if (match.hscore + match.line) > match.rscore :
            winloss.win += 1
        else:
            winloss.loss += 1

        # Print match info
#       print "%s:%d vs %s:%d" % (match.home, match.hscore, match.road, match.rscore)
#       print " > pre-game:  home: %d road: %d" % (tally[match.home].rate, tally[match.road].rate)
#       print " > predicted %d, spread %d, actual %d, delta %d" % (prediction, match.line, diff, d)
#       print " > %s" % (match.bet)
#       if week > 1:
#           delta.append(d)

        # Take scores for current week and adjust ELO
        # We add 100 ELO for every 7 point difference
        # each team gets or loses half the total ELO points
        hrate = tally[match.home].rate - (spreaddiff * 100/7)/2
        rrate = tally[match.road].rate + (spreaddiff * 100/7)/2
        tally[match.home].rate = (tally[match.home].rate * week + hrate) / (week + 1)
        tally[match.road].rate = (tally[match.road].rate * week + rrate) / (week + 1)
#       print " > post-game: home: %d road: %d" % (tally[match.home].rate, tally[match.road].rate)

    print ""
        
    cols = ['week', 'home', 'road', 'prediction', ' line', ' bet', 'hscore', 'rscore', 'betresult', 'status']
    colormap = {'win' : 'green', 'loss' : 'red'}
        
    datatable(datamatrix, cols, colormap)

print "------"
#print "Accuracy: %f Std Dev: %f" % (average(delta), std(delta))
print "Win: %s | Loss: %s" % (win, loss)
