#!/usr/bin/env python
# To sort through the nonsense, each page has to be kept in a list where the list holds an element of a person
from os import path
from ParserUtilities import *
import sys, operator

DEBUG=False
    
def allocateKonaSlots(numOfSlots):
    konaSlotDict = dict()
    participantPercentages = dict() # list of tuples
    slotsLeft = numOfSlots
    for ag in AgeGroupOrder:
        if len(MasterAgeGroup[ag]) == 0:
            # No slot goes to this group
            if DEBUG: print "%s gets no slot"%ag
        else:
            konaSlotDict[ag] = 1
            slotsLeft -= 1
            participantPercentages[ag] = (len(MasterAgeGroup[ag]) * 1.0)/TotalEntrants
    
    # Done with singlular allocation of slots
    if DEBUG: print "Number of slots after mandatory 1 is %d"%slotsLeft
    firstCutSlotsLeft = slotsLeft
    
    ## -- Go Through and divy these bitches up --
    ## Round up, give base to each category...
    for ag, percent in participantPercentages.iteritems():
        slots = round(firstCutSlotsLeft*percent)
        participantPercentages[ag] = (percent*firstCutSlotsLeft) - slots
        if (slotsLeft - slots) < 0:
            slots = slotsLeft
            print "Had an issue allocating in algorithm. A number is slightly too large..."
        if DEBUG: print "Allocating %d slots to age group %s"%(slots, ag)
        konaSlotDict[ag] += slots
        slotsLeft -= slots
            
    # went through each category once
    if DEBUG: print "After initial divy up, %d are left"%slotsLeft
    
    # Find max leftover percentage and allocate one to that, then once to the next, then one to the next
    while (slotsLeft > 0):
        maxPercentageGroup = max(participantPercentages.iteritems(), key=operator.itemgetter(1))[0]
        participantPercentages[maxPercentageGroup] -= 1.0
        if DEBUG: print "Allocating slot to %s"%maxPercentageGroup
        konaSlotDict[maxPercentageGroup] += 1
        slotsLeft -= 1
        
    print "\n\n================================================================================="
    for ag in AgeGroupOrder:
        if ag in konaSlotDict:
            print "Age Group %s Kona Slots: %d"%(ag, konaSlotDict[ag])
    
def printAgeGroupBreakdown(agroup):
    agList = MasterAgeGroup[agroup]
    print "Age Group %s: %d participants, %.2f percent of total entrants"%(agroup, len(agList), (len(agList)*100.0)/(TotalEntrants*1.0))

def printMasterAgeGroupBreakdown():
    print "Total Entrants: %d\n\n"%TotalEntrants
    for agroup in AgeGroupOrder:
        printAgeGroupBreakdown(agroup)

def printAgeGroups():
    for agroup in AgeGroupOrder:
        printAgeGroup(agroup)
        
def printAgeGroup(agKey):
    print "\n\n=========================================\nAge Group: %s (%d Participants)\n-----------------------------------------"%(agKey, len(MasterAgeGroup[agKey]))
    for agParticpant in MasterAgeGroup[agKey]:
        agParticpant.printParticipant()
    
def printStatistics(aGroup = None):
    if aGroup is None:
        printAgeGroups()
    else:
        try:
            printAgeGroup(aGroup)
        except:
            print "Unable to print with that age group, printing all"
            printAgeGroups()

# ==========================================================
# File Parsing - Non Statistical
# ==========================================================
    
def saveParticipant(partic):
    global TotalEntrants
    participantAge = partic.getAge()
    gender = partic.getGender()
    if gender == FEMALE:
        for agName, agRange in FemaleAgeGroups.iteritems():
            if participantAge in agRange:
                # Found a participant in this age group
                MasterAgeGroup[agName].append(partic)
                TotalEntrants += 1
    elif gender == MALE:
        for agName, agRange in MaleAgeGroups.iteritems():
            if participantAge in agRange:
                # Found a participant in this age group
                MasterAgeGroup[agName].append(partic)
                TotalEntrants += 1
            
def readFile(fileToParse):
    fin = open(fileToParse, 'r')
    lines = fin.read().splitlines()
    if DEBUG: print "Read in %d lines from file %s"%(len(lines), TEXT_FILE)
    return lines

def goToNextColumn(currentColumn):
    nextColumn = (FORMAT.index(currentColumn) + 1) % (len(FORMAT))
    return FORMAT[nextColumn]

def getNumberOfParticipantsInPage(linesInPage):
    # Go through and look for the first 'M' or 'F' character, and last
    numOfParticipants = 0
    for line in linesInPage:
        if line == MALE or line == FEMALE:
            numOfParticipants += 1
    
    return numOfParticipants
    
def parsePage(linesInPage, pageNo = -1):
    pageParticipants = list()
    currentFormat = FORMAT[0]
    currentColumnParticipant = 0
    currentLine = 0
    
    ## Get number of participants in this page -> look for M or F
    numOfParticipants = getNumberOfParticipantsInPage(linesInPage)
    if DEBUG: print "Number of participants in page %d is %d"%(pageNo+1, numOfParticipants)
    while (currentLine < len(linesInPage)):
        singleLine = linesInPage[currentLine]
        
        # -- Seperator case is special, handle error case and new page/column case -- 
        if (singleLine == COLUMN_SEPERATOR):
            if (currentColumnParticipant >= numOfParticipants):
                currentFormat = goToNextColumn(currentFormat)
                currentColumnParticipant = 0
                if currentFormat == FIRST_NAME:
                    # We moved to new page...return out of this loop
                    for part in pageParticipants:
                        saveParticipant(part)
            elif (currentLine == (len(linesInPage) -1)):
                # New Page is coming!!!
                for part in pageParticipants:
                    saveParticipant(part)
        ## -- Wasn't a seperator, its real data --
        else:
            # What column are we in?
            if currentFormat == FIRST_NAME:
                newParticipant = Participant(singleLine)    # Initializes with first name
                pageParticipants.append(newParticipant)
            else:
                # Add data to participant in list.
                theParticipant = pageParticipants[currentColumnParticipant]
                theParticipant.setField(currentFormat, singleLine)
            currentColumnParticipant += 1
            
        currentLine += 1

def parseLines(rawLines):
    # First get rid of header...look for 'State/Province' then skip line.
    firstLines = rawLines[:30]
    skipLines = 0
    if STATE_PROVINCE in firstLines:
        if DEBUG: print "Got state province on line %d"%firstLines.index(STATE_PROVINCE)
        # Names now start on the next non-blank space
        skipLines = firstLines.index(STATE_PROVINCE)

    rawLines = rawLines[skipLines+2:]

    ## OKAY! Lines are now correct.
    pageNum = 0
    whichLine = 0
    tally = 0
    firstLineOfPage = 0
    badPages = list()
    # Find the page seperator and parse each page individually...
    while (whichLine < len(rawLines)):
        singleLine = rawLines[whichLine]
        if singleLine.find(NEW_PAGE_DELIMITER) != -1:
            # Found a new page...
            if DEBUG: print "New page, %s:%d. Parsing from %s to it"%(singleLine.lstrip(NEW_PAGE_DELIMITER), \
                            whichLine, rawLines[firstLineOfPage].lstrip(NEW_PAGE_DELIMITER))
            try:
                rawLines[firstLineOfPage] = rawLines[firstLineOfPage].lstrip(NEW_PAGE_DELIMITER)
                parsePage(rawLines[firstLineOfPage:whichLine], pageNum)
            except:
                if DEBUG: print "Unable to parse page %d"%(pageNum + 1)
                badPages.append(str(pageNum+1))
            firstLineOfPage = whichLine
            pageNum += 1

        whichLine += 1
    
    print "Failed to retrieve entrants from pages %s."%(", ".join(badPages))
    
    return
    
if __name__ == "__main__":
    fileToParse = sys.argv[1]
    if DEBUG: print "Looking for file %s"%fileToParse
    initializeDictionary()
    if path.exists(fileToParse):
        rawLines = readFile(fileToParse)
        parseLines(rawLines)
        #printAgeGroup(M18_24)
        printMasterAgeGroupBreakdown()
        if len(sys.argv) >= 3:
            allocateKonaSlots(int(sys.argv[2]))
