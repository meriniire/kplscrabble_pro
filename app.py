import streamlit as st
import random
import csv

# Load valid dictionary words from CSV
valid_words = set()
with open('dic.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        valid_words.add(row[0].strip().upper())  # Add words to set and convert to uppercase

# Set page configuration
st.set_page_config(page_title="Scrabble Game", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    body {
        background-color: #f5f5f5;
        color: #333;
        font-family: 'Arial', sans-serif;
    }
    .header {
        background-color: #4caf50;
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .sidebar {
        background-color: #333;
        color: white;
    }
    .stButton, .stTextInput, .stNumberInput {
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .stButton:hover {
        background-color: #45a049;
        color: white;
    }
    .stTextInput:focus {
        border-color: #4caf50;
        outline: none;
    }
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Function to calculate word score based on Scrabble letter values
def calculate_word_score(word):
    letter_values = {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1,
        'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8,
        'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1,
        'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1,
        'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4,
        'Z': 10
    }
    return sum(letter_values.get(letter.upper(), 0) for letter in word)

# Initialize session state variables
if 'player_names' not in st.session_state:
    st.session_state.player_names = []
if 'scores' not in st.session_state:
    st.session_state.scores = {}
if 'current_player_index' not in st.session_state:
    st.session_state.current_player_index = 0
if 'tiles' not in st.session_state:
    st.session_state.tiles = random.sample(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 7)

# Main Menu
def main_menu():
    st.markdown("<div class='header'><h1>Development of a Computerized Scrabble Game</h1></div>", unsafe_allow_html=True)
    st.sidebar.header("Navigation")
    option = st.sidebar.selectbox("Select an Option:", ["Home", "Register Players", "Game Menu"])

    if option == "Home":
        splash_screen()
    elif option == "Register Players":
        register_players()
    elif option == "Game Menu":
        game_menu()
    elif option == "Game Restore":
        game_restore()

# Splash Screen
def splash_screen():
    st.header("Welcome")
    st.write("Test your word formation skills and compete for the highest score!")
    if st.button("Start Game"):
        register_players()

# Register Players
def register_players():
    st.header("Player Registration")
    num_players = st.number_input("Enter the number of players:", min_value=1, max_value=10, value=1)
    player_names = []

    for i in range(num_players):
        name = st.text_input(f"Enter name of Player {i + 1}:")
        if name:
            player_names.append(name)

    if st.button("Save Players"):
        if player_names:
            st.session_state.player_names = player_names
            st.session_state.scores = {name: 0 for name in player_names}
            st.success("Players registered successfully!")
            st.session_state.current_player_index = 0  # Reset to the first player
            st.session_state.tiles = random.sample(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 7)  # New tiles for each game
            game_menu()
        else:
            st.warning("Please enter player names.")

# Game Menu
def game_menu():
    st.header("Game Menu")
    if 'player_names' not in st.session_state or not st.session_state.player_names:
        st.warning("Please register players first!")
        return

    current_player = st.session_state.player_names[st.session_state.current_player_index]
    st.write(f"Current Player: {current_player}")
    st.write("Your Tiles: " + ', '.join(st.session_state.tiles))

    # Button to fetch new tiles
    if st.button("Fetch New Tiles"):
        st.session_state.tiles = random.sample(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 7)
        st.success("New tiles fetched!")

    letters_input = st.text_input("Input letters to form a word:", key="word_input")

    if st.button("Submit Word"):
        if letters_input:
            input_word = letters_input.upper()

            # Check if the input word can be formed with the available tiles
            if all(input_word.count(letter) <= st.session_state.tiles.count(letter) for letter in input_word):
                if input_word in valid_words:
                    score = calculate_word_score(letters_input)
                    st.session_state.scores[current_player] += score
                    st.success(f"Word '{letters_input}' submitted! Score: {score}")
                    update_tiles(letters_input)  # Update tiles after submission
                    # Randomize tiles immediately after a successful word submission
                    st.session_state.tiles = random.sample(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 7)
                    display_scores()
                    st.session_state.current_player_index = (st.session_state.current_player_index + 1) % len(st.session_state.player_names)
                else:
                    st.error(f"Word '{letters_input}' is not valid according to the dictionary.")
            else:
                st.error(f"You do not have enough tiles to form the word '{letters_input}'.")
        else:
            st.warning("Please enter a valid word.")

    # Check for any valid words that can be formed with current tiles
    possible_words = [word for word in valid_words if all(word.count(letter) <= st.session_state.tiles.count(letter) for letter in word)]
    if not possible_words:
        st.info("No valid words can be formed with the current tiles. Try rearranging or drawing new tiles.")

    display_scores()  # Display scores after each submission

# Update tiles after a valid word is submitted
def update_tiles(word):
    for letter in word.upper():
        if letter in st.session_state.tiles:
            st.session_state.tiles.remove(letter)

# Replenish tiles to ensure the player has 7 tiles if possible
def replenish_tiles():
    available_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') - set(st.session_state.tiles)
    # Convert available_letters to a list
    available_letters_list = list(available_letters)
    new_tiles = random.sample(available_letters_list, min(7 - len(st.session_state.tiles), len(available_letters_list)))
    st.session_state.tiles.extend(new_tiles)

# Display Scores
def display_scores():
    st.header("Current Scores")
    for player, score in st.session_state.scores.items():
        st.write(f"{player}: {score} points")

# Game Restore (placeholder)
def game_restore():
    st.header("Game Restore")
    st.write("Game restore functionality will be implemented here.")

# Run the app
if __name__ == "__main__":
    main_menu()
