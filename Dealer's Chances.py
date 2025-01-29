import numpy as np
import random
import time
import openpyxl

#Shuffles and cuts the deck and places a placeholder in it
def preparingDeck(deck):
    # Shuffling the deck
    random.shuffle(deck)

    # Cutting the deck
    #cutPoint = random.randint(50, 275)
    #deck = deck[cutPoint:] + deck[:cutPoint]

    # Inserting placeholder to indicate when to reshuffle deck
    placeholderLoc = random.randint(150, 250)
    deck = deck[:placeholderLoc] + [0] + deck[placeholderLoc:]

    return deck

    

#The actions of the dealer drawing until reaching at least 17 or busting
def dealerActions(deck, dealersCards, reshuffle):
    #Checking the score of the cards dealt to the dealer
    score = 0
    for i in range(len(dealersCards)):
        score += dealersCards[i]

    #Checking if the dealer got two aces and making one of them worth 1
    if dealersCards[-1] == 11 and score + dealersCards[-1] > 21:
        dealersCards[-1] = 1

    #Making dealer hit on soft 17
    if score == 17:
        if dealersCards[0] == 11:
            dealersCards[0] = 1
            score = 7
        if dealersCards[1] == 11:
            dealersCards[1] = 1
            score = 7   

    #Having the dealer draw until score is at least 17
    while score < 17:
        #Checking if the next card is the placeholder card
        if deck[0] == 0:
            deck = deck[1:]
            reshuffle = True

        #Drawing top card of the deck into the dealer's hand (placing it at the bottom of the overall deck)
        dealersCards = dealersCards[:] + [deck[0]]
        deck = deck[1:] + [deck[0]]

        if dealersCards[-1] == 11 and score + dealersCards[-1] > 21:
            dealersCards[-1] = 1

        score = 0
        for i in range(len(dealersCards)):
            score += dealersCards[i]

    if score > 21:
        bust = True
    else:
        bust = False

    return deck, bust, score, reshuffle

if __name__ == '__main__':
    startTime = time.time()

    #Opening excel file to store stats in
    wb = openpyxl.load_workbook('Blackjack Data.xlsx')
    ws = wb['Dealer Stats']

    #Makes a deck consisting of 6 standard 52 card decks
    deck = [0 for i in range(52)]
    for normalCards in range(2,10):
        for numOfDuplicates in range(4):
             deck[numOfDuplicates + (normalCards - 2)*4] = normalCards
    for faceCards in range(1,17):
        deck[31 + faceCards] = 10
    for aces in range(1,5):
        deck[47 + aces] = 11

    deck = deck*6

    deck = preparingDeck(deck)
    bust = True

    #Initializing the array to store stats in
    dealerCardStats = [[0 for cols in range(10)] for rows in range (6)]

    #This is the primary loop where the dealer will be dealt two cards and then draw (if necessary) to at least 17 or till bust
    for i in range(130000000):
        if (i % 1300000) == 0:
            print('|', end="")

        reshuffle = False

        #Checking if either of the next two cards are the placeholder card
        if deck[0] == 0:
            deck = deck[1:]
            reshuffle = True
        if deck[1] == 0:
            deck = [deck[0]] + deck[2:]
            reshuffle = True
        
        dealersHand = deck[:2]
        deck = deck[2:] + deck[:2]
        column = dealersHand[0] - 2

        score = 0
        for i in range(len(dealersHand)):
            score += dealersHand[i]
        
        #Checking if dealer has blackjack
        if score != 21:
            deck, bust, score, reshuffle = dealerActions(deck, dealersHand, reshuffle)

            #Recording the outcome of this particular hand
            if bust:
                row = 5
                dealerCardStats[row][column] += 1
            else:
                row = score - 17
                dealerCardStats[row][column] += 1

        if reshuffle:
            deck = preparingDeck(deck)

    #Turning the data into percentages and exporting it to excel file
    columnTotals = [0 for cols in range(10)]
    for cols in range(10):
        for rows in range(6):
            columnTotals[cols] += dealerCardStats[rows][cols]
    print(columnTotals)
    for cols in range(10):
        for rows in range(6):
            ws.cell(row=rows + 3, column=cols + 2).value = dealerCardStats[rows][cols] / columnTotals[cols] * 100

    wb.save('Blackjack Data.xlsx')

    print(time.time() - startTime)
