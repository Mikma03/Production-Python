import random

# Define the suits and ranks
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Create a list of cards
deck = [f'{rank} of {suit}' for suit in suits for rank in ranks]

# Create an empty set to store the shuffled deck
shuffled_deck = set()

# Keep adding random cards to the set until all cards are added
while deck:
    card = random.choice(deck)
    shuffled_deck.add(card)
    deck.remove(card)

# Print the shuffled deck
for card in shuffled_deck:
    print(card)