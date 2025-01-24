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

def dealerActions(deck, dealersCards, reshuffle):
    score = 0
    for i in range(len(dealersCards)):
        score += dealersCards[i]

    if dealersCards[-1] == 11 and score + dealersCards[-1] > 21:
        dealersCards[-1] = 1

    while score < 17:
        if deck[0] == 0:
            deck = deck[1:]
            reshuffle = True

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
    wb = openpyxl.load_workbook('Black Jack Data.xlsx')
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

    dealerCardStats = [[0 for cols in range(10)] for rows in range (6)]

    for i in range(130000000):
        if (i % 1300000) == 0:
            print('|', end="")

        reshuffle = False

        if deck[0] == 0:
            deck = deck[1:]
            reshuffle = True
        if deck[1] == 0:
            deck = [deck[0]] + deck[2:]
            reshuffle = True

        dealersHand = deck[:2]
        deck = deck[2:] + deck[:2]
        column = dealersHand[0] - 2
        deck, bust, score, reshuffle = dealerActions(deck, dealersHand, reshuffle)

        if bust:
            row = 5
            dealerCardStats[row][column] += 1
        else:
            row = score - 17
            dealerCardStats[row][column] += 1

        if reshuffle:
            deck = preparingDeck(deck)

    columnTotals = [0 for cols in range(10)]
    for cols in range(10):
        for rows in range(6):
            columnTotals[cols] += dealerCardStats[rows][cols]
    print(columnTotals)
    for cols in range(10):
        for rows in range(6):
            ws.cell(row=rows + 3, column=cols + 2).value = dealerCardStats[rows][cols] / columnTotals[cols] * 100

    wb.save('Black Jack Data.xlsx')

    print(time.time() - startTime)