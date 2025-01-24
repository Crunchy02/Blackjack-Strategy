# Blackjack-Strategy
Code to generate the statistics involved with Blackjack and test the efficacy of different strategies.

Question to answer: What is the best strategy for the player?

Current State:
 - Unrefined code to produce the percent chance of a dealer hitting 17-21 or busting based on the card shown (2-Ace)
 - Unrefined code to produce the percent chance of a player reaching 17-21 or busting based off what value their hand is (2-21) and how many cards they have drawn (1-3)

Next Step Ideas:
 - Comment both "Dealer's Stats" and "Player's Stats" codes
 - Create different strategies that can be read in to create different "players" and test how each strategy performs
 - Create a "place" where multiple people play blackjack: this is where the strategies will be tested
 - Look into the pattern of wins/losses for each strategy to see if there is any predictable "steakiness" seen, which could be potentially added into a strategy
 - Go through the current statistics to develop a table of how likely a player is to win a hand based on the player and dealer statistics already found
 - Find a way to determine the overall winning percentage of the player provided a certain strategy (how high can we get this?)
 - Implement counting cards into some stategies
 - Add hitting on a soft 17 into the "Dealer's Stats" code
     - Run stats again to see how this impacts them
