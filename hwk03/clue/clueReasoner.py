'''ClueReasoner.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED FOR THIS HOMEWORK".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant

Copyright (C) 2008 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import SATSolver

# Initialize important variables
caseFile = "cf"
players = ["sc", "mu", "wh", "gr", "pe", "pl"]
extendedPlayers = players + [caseFile]
suspects = ["mu", "pl", "gr", "pe", "sc", "wh"]
weapons = ["kn", "ca", "re", "ro", "pi", "wr"]
rooms = ["ha", "lo", "di", "ki", "ba", "co", "bi", "li", "st"]
cards = suspects + weapons + rooms

def getPairNumFromNames(player,card):
    global extendedPlayers
    global cards
    return getPairNumFromPositions(extendedPlayers.index(player),
           cards.index(card))

def getPairNumFromPositions(player,card):
     global cards
     return player*len(cards) + card + 1

# TO BE IMPLEMENTED FOR THIS HOMEWORK
def initialClauses():
    clauses = []
    global cards
    global extendedPlayers
    global suspects
    global weapons
    global rooms
    global caseFile
    # Each card is in at least one place (including case file).
    for c in cards:
        clauses.append([getPairNumFromNames(p,c) for p in extendedPlayers])

    # A card cannot be in two places.
    for c in cards:
        for p in extendedPlayers:
            for q in extendedPlayers:
                if q is not p:
                    clauses.append([(-1)*getPairNumFromNames(p,c), (-1)*getPairNumFromNames(q,c)])
    # At least one card of each category is in the case file.
    clauses.append([getPairNumFromNames(caseFile, c) for c in suspects])
    clauses.append([getPairNumFromNames(caseFile, c) for c in weapons])
    clauses.append([getPairNumFromNames(caseFile, c) for c in rooms])
    # No two cards in each category can both be in the case file.
    for c in suspects:
        for d in suspects:
            if c is not d:
                clauses.append([(-1)*getPairNumFromNames(caseFile, c), (-1)*getPairNumFromNames(caseFile,d)])
    for c in weapons:
        for d in weapons:
            if c is not d:
                clauses.append([(-1)*getPairNumFromNames(caseFile, c), (-1)*getPairNumFromNames(caseFile,d)])
    for c in rooms:
         for d in rooms:
             if c is not d:
                clauses.append([(-1)*getPairNumFromNames(caseFile, c), (-1)*getPairNumFromNames(caseFile,d)])
    return clauses

# TO BE IMPLEMENTED FOR THIS HOMEWORK
def hand(player,cards):
    clauses = []
    for c in cards:
        clauses.append([getPairNumFromNames(player,c)])
    return clauses


# TO BE IMPLEMENTED FOR THIS HOMEWORK
def suggest(suggester,card1,card2,card3,refuter,cardShown):
    global players
    clauses = []
    if refuter is None:
        for p in players:
            if p is not suggester:
                clauses.append([(-1)*getPairNumFromNames(p, card1)])
                clauses.append([(-1)*getPairNumFromNames(p, card2)])
                clauses.append([(-1)*getPairNumFromNames(p, card3)])
    else:
        p = (players.index(suggester) + 1)%len(players)
        while p is not players.index(refuter):
            clauses.append([(-1)*getPairNumFromNames(players[p], card1)])
            clauses.append([(-1)*getPairNumFromNames(players[p], card2)])
            clauses.append([(-1)*getPairNumFromNames(players[p], card3)])
            p = (p+1)%len(players)

        if cardShown is None:
            clauses.append([getPairNumFromNames(players[p], card1), getPairNumFromNames(players[p], card2), getPairNumFromNames(players[p], card3)])
        else:
            clauses.append([getPairNumFromNames(players[p], cardShown)])
    return clauses

# TO BE IMPLEMENTED FOR THIS HOMEWORK
def accuse(accuser,card1,card2,card3,isCorrect):
    global caseFile
    clauses = []
    if isCorrect:
        clauses.append([getPairNumFromNames(caseFile, card1)])
        clauses.append([getPairNumFromNames(caseFile, card2)])
        clauses.append([getPairNumFromNames(caseFile, card3)])
    else:
        clauses.append([(-1)*getPairNumFromNames(caseFile, card1), (-1)*getPairNumFromNames(caseFile, card2), (-1)*getPairNumFromNames(caseFile, card3)])

    clauses.append([(-1)*getPairNumFromNames(accuser, card1)])
    clauses.append([(-1)*getPairNumFromNames(accuser, card2)])
    clauses.append([(-1)*getPairNumFromNames(accuser, card3)])


    return clauses




# HELPER METHODS FOR YOUR BENEFIT
def query(player,card,clauses):
    return SATSolver.testLiteral(getPairNumFromNames(player,card),clauses)

def queryString(returnCode):
    if returnCode == True:
        return 'Y'
    elif returnCode == False:
        return 'N'
    else:
        return '-'

def printNotepad(clauses):
    for player in players:
        print '\t', player,
    print '\t', caseFile
    for card in cards:
        print card,'\t',
        for player in players:
            print queryString(query(player,card,clauses)),'\t',
        print queryString(query(caseFile,card,clauses))

def playClue():
    clauses = initialClauses()
    clauses.extend(hand("sc",["wh", "li", "st"]))
    clauses.extend(suggest("sc", "sc", "ro", "lo", "mu", "sc"))
    clauses.extend(suggest("mu", "pe", "pi", "di", "pe", None))
    clauses.extend(suggest("wh", "mu", "re", "ba", "pe", None))
    clauses.extend(suggest("gr", "wh", "kn", "ba", "pl", None))
    clauses.extend(suggest("pe", "gr", "ca", "di", "wh", None))
    clauses.extend(suggest("pl", "wh", "wr", "st", "sc", "wh"))
    clauses.extend(suggest("sc", "pl", "ro", "co", "mu", "pl"))
    clauses.extend(suggest("mu", "pe", "ro", "ba", "wh", None))
    clauses.extend(suggest("wh", "mu", "ca", "st", "gr", None))
    clauses.extend(suggest("gr", "pe", "kn", "di", "pe", None))
    clauses.extend(suggest("pe", "mu", "pi", "di", "pl", None))
    clauses.extend(suggest("pl", "gr", "kn", "co", "wh", None))
    clauses.extend(suggest("sc", "pe", "kn", "lo", "mu", "lo"))
    clauses.extend(suggest("mu", "pe", "kn", "di", "wh", None))
    clauses.extend(suggest("wh", "pe", "wr", "ha", "gr", None))
    clauses.extend(suggest("gr", "wh", "pi", "co", "pl", None))
    clauses.extend(suggest("pe", "sc", "pi", "ha", "mu", None))
    clauses.extend(suggest("pl", "pe", "pi", "ba", None, None))
    clauses.extend(suggest("sc", "wh", "pi", "ha", "pe", "ha"))
    clauses.extend(suggest("wh", "pe", "pi", "ha", "pe", None))
    clauses.extend(suggest("pe", "pe", "pi", "ha", None, None))
    clauses.extend(suggest("sc", "gr", "pi", "st", "wh", "gr"))
    clauses.extend(suggest("mu", "pe", "pi", "ba", "pl", None))
    clauses.extend(suggest("wh", "pe", "pi", "st", "sc", "st"))
    clauses.extend(suggest("gr", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(suggest("pe", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(suggest("pl", "pe", "pi", "ki", "gr", None))
    print 'Before accusation: should show a single solution.'
    printNotepad(clauses)
    print
    clauses.extend(accuse("sc", "pe", "pi", "bi", True))
    print 'After accusation: if consistent, output should remain unchanged.'
    printNotepad(clauses)

if __name__ == '__main__':
    playClue()
