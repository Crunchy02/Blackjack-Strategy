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

if __name__ == '__main__':
    startTime = time.time()

    #Opening excel file to store stats in
    wb = openpyxl.load_workbook('Black Jack Data.xlsx')
    ws = wb['Player Stats']

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

    playerHittingStats = [[0 for cols in range(20)] for rows in range(15)]
    playerBustingStats = [[0 for cols in range(20)] for rows in range(3)]

    columnTotals = [0 for j in range(20)]

    for i in range(10000000):
        reshuffle = False

        if deck[0] == 0:
            deck = deck[1:]
            reshuffle = True
        if deck[1] == 0:
            deck = [deck[0]] + deck[2:]
            reshuffle = True

        playersHand = deck[:2]
        deck = deck[2:] + playersHand

        score = 0
        for j in range(2):
            score += playersHand[j]

        if score == 22:
            playersHand = [1, 1]
            score = 2

        if score == 13 and (playersHand[0] == 2 or playersHand[1] == 2):
            playersHand = [2, 1]
            score = 3

        column = score - 2
        columnTotals[column] += 1

        for cardsDrawn in range(3):
            if deck[0] == 0:
                deck = deck[1:]
                reshuffle = True

            playersHand.append(deck.pop(0))
            deck.append(playersHand[-1])

            if playersHand[-1] == 11 and score + playersHand[-1] > 21:
                playersHand[-1] = 1

            score += playersHand[-1]

            if score > 21:
                playerBustingStats[cardsDrawn][column] += 1
            elif score > 16:
                playerHittingStats[cardsDrawn * 5 + score - 17][column] += 1

            if reshuffle:
                deck = preparingDeck(deck)
                reshuffle = False

    for cols in range(20):
        for rows in range(15):
            ws.cell(row=3 + rows + rows // 5 * 2, column=cols + 3).value = playerHittingStats[rows][cols] / columnTotals[cols] * 100

    for cols in range(20):
        for rows in range(3):
            ws.cell(row=3 + rows * 7, column=cols + 26).value = playerBustingStats[rows][cols] / columnTotals[cols] * 100

    wb.save('Black Jack Data.xlsx')

    print(columnTotals)
    print(time.time() - startTime)
