import random
import numpy as np

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
def play_turn(player, deck, prev_card_subtype, turn_count):
    if player:
        # Draw a card from the deck
        if deck:
            drawn_card = deck.pop()
            # Add the drawn card to the player's hand
            player.append(drawn_card)
        else:
            return None, prev_card_subtype, turn_count

        random.shuffle(player)
        played_card = None

        # Attempt to play a valid card from the player's hand
        for card in player:
            card_parts = card.split()
            card_type = card_parts[0]

            if is_valid_play(prev_card_subtype, card_type):
                played_card = card
                player.remove(played_card)
                break

        if played_card:
            # Extract the type and subtype from the played card
            played_card_parts = played_card.split()
            played_card_type = played_card_parts[0]
            played_card_subtype = played_card_parts[-1][1:-1]  # Extract subtype correctly
            if is_valid_play(prev_card_subtype, played_card_type):
                prev_card_subtype = played_card_subtype
                turn_count += 1

        return played_card, prev_card_subtype, turn_count
    else:
        return None, prev_card_subtype, turn_count


# Function to play the game with a given deck and initial hand size
def play_game(deck, initial_hand_size):
    players = [[] for _ in range(2)]
    deal_cards(deck, players, initial_hand_size)
    prev_card_subtype = "xyz"
    turn_count = 0

    while all(players) and deck:
        for i, player in enumerate(players):
            played_card, prev_card_subtype, turn_count = play_turn(player, deck, prev_card_subtype, turn_count)
            if not deck:
                break

    return turn_count


# Function to print unique cards and their counts in a deck
def print_unique_cards(deck):
    unique_cards = {}
    for card in deck:
        if card in unique_cards:
            unique_cards[card] += 1
        else:
            unique_cards[card] = 1

    # Sort unique cards by descending number of copies
    sorted_unique_cards = sorted(unique_cards.items(), key=lambda x: x[1], reverse=True)

    for card, count in sorted_unique_cards:
        print(f"{card}: {count}")


# Function to compute the fitness of a set
def compute_fitness(initial_hand_size, deck, num_games):
    total_turns = 0
    num_unique_cards = len(set(deck))  # Count the number of unique cards in the deck
    possible_unique_cards = len(card_types) * len(card_subtypes)  # Total possible unique cards

    for _ in range(num_games):
        deck_copy = deck.copy()
        total_turns += play_game(deck_copy, initial_hand_size)

    # Calculate the fitness as average turns played, multiplied by unique cards ratio
    fitness = (total_turns / num_games) * (num_unique_cards / possible_unique_cards)

    return fitness


# Function to create a random set of initial hand size and deck
def create_random_set():
    initial_hand_size = random.randint(5, 10)
    deck = create_deck()
    return initial_hand_size, deck


# Function to perform crossover between two sets
def crossover(set1, set2):
    crossover_point = round(np.random.normal(50, 15))  # Gaussian distribution around 50
    crossover_point = max(1, min(100, crossover_point))  # Ensure it's within [1, 100]

    # Randomly exchange cards between the two sets
    new_set1 = set1[:crossover_point] + set2[crossover_point:]
    new_set2 = set2[:crossover_point] + set1[crossover_point:]

    return new_set1, new_set2


# Function to evolve the population
def evolve_population(population, population_size):
    population.sort(key=lambda x: x[1])  # Sort by fitness
    survivors = population[:len(population) // 2]

    new_population = survivors.copy()
    while len(new_population) < population_size:
        parent1, parent2 = random.choices(survivors, k=2, weights=[1 / x[1] for x in survivors])
        child1, child2 = crossover(parent1[0], parent2[0])
        new_population.extend([(child1, 0), (child2, 0)])

    return new_population


# Number of generations, population size, number of games, and number of decks to display
num_generations = 10
population_size = 100  # Adjustable population size
num_games_per_deck = 200  # Adjustable number of games per deck
num_top_decks_to_display = 10  # Number of top decks to display

# Initialize the best fitness
best_fitness = float('inf')

# Store the top different best decks
top_decks = []

for generation in range(num_generations):
    print(f"Generation {generation + 1}...")

    population = [create_random_set() for _ in range(population_size)]
    for i, (initial_hand_size, deck) in enumerate(population):
        fitness = compute_fitness(initial_hand_size, deck, num_games_per_deck)
        population[i] = ((initial_hand_size, deck), fitness)

    population = evolve_population(population, population_size)
    best_in_generation = min(population, key=lambda x: x[1])

    if best_in_generation[1] < best_fitness:
        best_fitness = best_in_generation[1]
        best_deck = best_in_generation[0]
        top_decks.append(best_deck)

# Sort the top decks by fitness
top_decks.sort(key=lambda x: x[1])

# Print the top different best decks along with unique cards and counts
print(f"\nTop {num_top_decks_to_display} different best decks:")
for i, (initial_hand_size, deck) in enumerate(top_decks[:num_top_decks_to_display]):
    print(f"\nDeck {i + 1} (Fitness: {compute_fitness(initial_hand_size, deck, num_games_per_deck)}):")
    print_unique_cards(deck)