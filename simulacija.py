import random

# Define the card types and subtypes
card_types = ["x", "y", "z"]
card_subtypes = ["x", "y", "z", "xy", "xz", "yz", "xyz"]

# Function to check if a card's type is present in another card's subtype
def is_valid_play(prev_card_subtype, played_card_type):
    return played_card_type in prev_card_subtype

# Function to create a deck with 100 cards with random type-subtype combinations
def create_deck():
    deck = []
    for _ in range(100):
        card_type = random.choice(card_types)
        card_subtype = random.choice(card_subtypes)
        card = f"{card_type} ({card_subtype})"
        deck.append(card)
    return deck

# Function to distribute cards to players
def deal_cards(deck, players, cards_per_player):
    for player in players:
        player.extend(deck[:cards_per_player])
        del deck[:cards_per_player]

# Function to simulate a player's turn
def play_turn(player, deck, prev_card_subtype, player_number, turn_count):
    if player:
        # Draw a card from the deck
        if deck:
            drawn_card = deck.pop()
            print(f"Player {player_number + 1} draws: {drawn_card}")
            # Add the drawn card to the player's hand
            player.append(drawn_card)
        else:
            print("No cards left in the deck.")
            return None, prev_card_subtype, turn_count

        random.shuffle(player)
        played_card = None

        # Attempt to play a valid card from the player's hand
        for card in player:
            card_parts = card.split()
            card_type = card_parts[0]
            card_subtype = card_parts[-1][1:-1]  # Extract subtype correctly

            if is_valid_play(prev_card_subtype, card_type):
                played_card = card
                player.remove(played_card)
                break

        if played_card:
            print(f"Player {player_number + 1} plays: {played_card}")
            # Extract the type and subtype from the played card
            played_card_parts = played_card.split()
            played_card_type = played_card_parts[0]
            played_card_subtype = played_card_parts[-1][1:-1]  # Extract subtype correctly
            if is_valid_play(prev_card_subtype, played_card_type):
                prev_card_subtype = played_card_subtype
                turn_count += 1
            else:
                print("Invalid play! The played card type is not in the previous card's subtype.")
        else:
            print(f"Player {player_number + 1} has no more valid cards to play.")
            return None, prev_card_subtype, turn_count

        return played_card, prev_card_subtype, turn_count
    else:
        print(f"Player {player_number + 1} has no more cards to play.")
        return None, prev_card_subtype, turn_count

# Create the deck
deck = create_deck()

# Display the initial deck
print("Initial deck:")
print(deck)

# Define the number of players and initial hand size
num_players = 2
initial_hand_size = 5

# Create players
players = [[] for _ in range(num_players)]

# Deal initial cards to players
deal_cards(deck, players, initial_hand_size)

# Initialize previous card subtype
prev_card_subtype = "xyz"

# Initialize turn count
turn_count = 0

# Main game loop
while all(players) and deck:
    for i, player in enumerate(players):
        print(f"\nPlayer {i + 1}'s turn:")
        played_card, prev_card_subtype, turn_count = play_turn(player, deck, prev_card_subtype, i, turn_count)
        print(f"Player {i + 1}'s hand: {player}")
        if not deck:
            break

# Determine the winner
winning_player = max(enumerate(players), key=lambda x: len(x[1]))[0]
print(f"\nPlayer {winning_player + 1} wins!")

# Print the number of turns played
print(f"Total turns played: {turn_count}")
