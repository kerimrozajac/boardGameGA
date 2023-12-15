import random

# Define the card quantities
card_quantities = {
    ('z', 'xz'): 8,
    ('x', 'y'): 8,
    ('y', 'z'): 7,
    ('x', 'yz'): 6,
    ('y', 'xz'): 6,
    ('y', 'xyz'): 6,
    ('z', 'z'): 6,
    ('z', 'xy'): 6,
    ('y', 'yz'): 6,
    ('z', 'x'): 5,
    ('z', 'y'): 5,
    ('x', 'xz'): 5,
    ('x', 'xy'): 5,
    ('y', 'y'): 4,
    ('x', 'z'): 4,
    ('y', 'xy'): 3,
    ('z', 'yz'): 3,
    ('x', 'xyz'): 2,
    ('y', 'x'): 2,
    ('x', 'x'): 2,
    ('z', 'xyz'): 1
}

# Generate the deck based on the quantities
deck = [(card[0], card[1]) for card, quantity in card_quantities.items() for _ in range(quantity)]

# Initialize the discard pile
discard_pile = []


# Function to shuffle the deck
def shuffle_deck(deck):
    random.shuffle(deck)


# Function to simulate the game with adjustable number of players and initial hand size
def simulate_game(num_players, initial_hand_size):
    # Initialize the game
    shuffle_deck(deck)
    player_hands = [[] for _ in range(num_players)]
    players_in_game = list(range(num_players))

    # Initialize the counters
    cards_played = 0
    cards_left_in_deck = len(deck)

    # Deal initial cards to players
    for _ in range(initial_hand_size * num_players):
        player_hands[_ % num_players].append(deck.pop())

    # Simulate the game
    current_player = 0
    played_card = None
    while len(players_in_game) > 1:
        # Check if the current player is still in the game
        if current_player not in players_in_game:
            current_player = (current_player + 1) % num_players
            continue

        # Current player's turn
        drawn_card = None

        # Draw a card at the beginning of the player's turn
        if deck:
            drawn_card = deck.pop()
            player_hands[current_player].append(drawn_card)

        # Print the turn information
        print(f"Player {current_player + 1}'s turn:")
        if drawn_card:
            print(f"  - Drew card: {drawn_card}")
            print(f"  - Hand after drawing: {player_hands[current_player]}")

        valid_cards = [card for card in player_hands[current_player] if
                       played_card is None or card[0] in played_card[1]]

        if valid_cards:
            played_card = random.choice(valid_cards)
            player_hands[current_player].remove(played_card)
            print(f"  - Played card: {played_card}")
            print(f"  - Hand after playing: {player_hands[current_player]}")
            cards_played += 1
            cards_left_in_deck = len(deck)
            print(f"  - Cards played so far: {cards_played}")
            print(f"  - Cards left in the deck: {cards_left_in_deck}\n")
        else:
            print(f"Player {current_player + 1} cannot make a move and is out of the game.\n")

            # Add the player's hand to the bottom of the discard pile
            discard_pile.extend(player_hands[current_player])
            player_hands[current_player] = []

            players_in_game.remove(current_player)

        current_player = (current_player + 1) % num_players

    # Determine the winner
    if len(players_in_game) == 1:
        winner = players_in_game[0]
        print(f"Player {winner + 1} is the winner!")


# Adjust the number of players and initial hand size here
num_players = 5
initial_hand_size = 4
simulate_game(num_players, initial_hand_size)
