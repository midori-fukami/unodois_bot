import telebot
import random

# Create a new Telegram bot using your bot token
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Dictionary to store game sessions
games = {}

# UNO deck
deck = [
    "Red 0", "Red 1", "Red 2", "Red 3", "Red 4", "Red 5", "Red 6", "Red 7", "Red 8", "Red 9", "Red Skip", "Red Reverse", "Red +2",
    "Blue 0", "Blue 1", "Blue 2", "Blue 3", "Blue 4", "Blue 5", "Blue 6", "Blue 7", "Blue 8", "Blue 9", "Blue Skip", "Blue Reverse", "Blue +2",
    "Green 0", "Green 1", "Green 2", "Green 3", "Green 4", "Green 5", "Green 6", "Green 7", "Green 8", "Green 9", "Green Skip", "Green Reverse", "Green +2",
    "Yellow 0", "Yellow 1", "Yellow 2", "Yellow 3", "Yellow 4", "Yellow 5", "Yellow 6", "Yellow 7", "Yellow 8", "Yellow 9", "Yellow Skip", "Yellow Reverse", "Yellow +2",
    "+4 Wild", "+4 Wild", "+4 Wild", "+4 Wild",
    "+4 Wild +2", "+4 Wild +2", "+4 Wild +2", "+4 Wild +2"
]

# Command handler for starting a new game
@bot.message_handler(commands=['start'])
def start_game(message):
    chat_id = message.chat.id
    if chat_id not in games:
        # Start a new game session
        games[chat_id] = {
            'players': {},
            'deck': [],
            'discard': [],
            'current_player': None,
            'current_card': None,
            'direction': 1,  # 1 for forward, -1 for reverse
            'active_color': None,
            'uno_calls': {},
            'penalty_cards': 0
        }
        bot.reply_to(message, 'New game started! Use /join to join the game.')
    else:
        bot.reply_to(message, 'There is already a game in progress.')

# Command handler for joining a game
@bot.message_handler(commands=['join'])
def join_game(message):
    chat_id = message.chat.id
    if chat_id in games:
        player_id = message.from_user.id
        game = games[chat_id]
        if player_id not in game['players']:
            game['players'][player_id] = {
                'username': message.from_user.username,
                'hand': []
            }
            bot.reply_to(message, 'You joined the game.')
            if len(game['players']) == 1:
                game['current_player'] = player_id
                bot.send_message(chat_id, 'Game started! You are the first player.')
        else:
            bot.reply_to(message, 'You have already joined the game.')
    else:
        bot.reply_to(message, 'There is no game in progress. Start a new game with /start.')

# Command handler for playing a card
@bot.message_handler(commands=['play'])
def play_card(message):
    chat_id = message.chat.id
    player_id = message.from_user.id
    game = games.get(chat_id)
    
    if game:
        if player_id == game['current_player']:
            # Extract the card information from the message text
            card_info = message.text.split()[1]
            # Validate the card and check if it can be played
            if validate_card(card_info, game):
                # Update the game state
                update_game_state(card_info, game)
                # Broadcast the played card to all players
                bot.send_message(chat_id, f"{message.from_user.username} played {card_info}.")
                # Check for a winner or next player
                check_winner_or_next_player(game)
            else:
                bot.reply_to(message, "Invalid move. Please try again.")
        else:
            bot.reply_to(message, "It's not your turn.")
    else:
        bot.reply_to(message, "There is no game in progress.")

# Command handler for drawing a card
@bot.message_handler(commands=['draw'])
def draw_card(message):
    chat_id = message.chat.id
    player_id = message.from_user.id
    game = games.get(chat_id)
    
    if game:
        if player_id == game['current_player']:
            # Draw a card from the deck or from the discard pile if the deck is empty
            card = draw_card_from_deck(game) if game['deck'] else draw_card_from_discard(game)
            # Add the card to the player's hand
            game['players'][player_id]['hand'].append(card)
            # Send the drawn card to the player
            bot.send_message(player_id, f"You drew {card}.")
            # Check for penalties and handle UNO calls
            handle_penalties_and_uno_calls(player_id, game)
        else:
            bot.reply_to(message, "It's not your turn.")
    else:
        bot.reply_to(message, "There is no game in progress.")

# Command handler for skipping a turn
@bot.message_handler(commands=['skip'])
def skip_turn(message):
    chat_id = message.chat.id
    player_id = message.from_user.id
    game = games.get(chat_id)
    
    if game:
        if player_id == game['current_player']:
            # Update the current player to the next player
            game['current_player'] = get_next_player(game)
            bot.send_message(chat_id, f"{message.from_user.username} skipped their turn.")
        else:
            bot.reply_to(message, "It's not your turn.")
    else:
        bot.reply_to(message, "There is no game in progress.")

# Function to validate if a card can be played
def validate_card(card_info, game):
    current_card = game['current_card']
    active_color = game['active_color']
    
    if card_info in game['players'][game['current_player']]['hand']:
        card_color, card_value = card_info.split()
        current_color, current_value = current_card.split()
        
        if card_color == active_color or card_value == current_value or card_color == current_color:
            return True
    
    return False

# Function to update the game state after a card is played
def update_game_state(card_info, game):
    current_card = game['current_card']
    card_color, card_value = card_info.split()
    game['active_color'] = None
    
    if card_color.startswith("+4"):
        game['active_color'] = random.choice(['Red', 'Blue', 'Green', 'Yellow'])
        game['penalty_cards'] += 4
    
    game['current_card'] = card_info
    game['players'][game['current_player']]['hand'].remove(card_info)
    game['discard'].append(card_info)

# Function to check if there is a winner or update the current player to the next player
def check_winner_or_next_player(game):
    current_player_id = game['current_player']
    current_player_hand = game['players'][current_player_id]['hand']
    
    if len(current_player_hand) == 0:
        bot.send_message(current_player_id, "Congratulations! You won the game!")
        end_game(game)
    else:
        game['current_player'] = get_next_player(game)

# Function to draw a card from the deck
def draw_card_from_deck(game):
    card = game['deck'].pop()
    
    if len(game['deck']) == 0:
        game['deck'] = game['discard']
        game['discard'] = []
        random.shuffle(game['deck'])
    
    return card

# Function to draw a card from the discard pile
def draw_card_from_discard(game):
    card = game['discard'].pop()
    return card

# Function to get the next player's ID
def get_next_player(game):
    current_player_id = game['current_player']
    current_player_index = list(game['players']).index(current_player_id)
    next_player_index = (current_player_index + game['direction']) % len(game['players'])
    return list(game['players'])[next_player_index]

# Function to handle penalties and UNO calls
def handle_penalties_and_uno_calls(player_id, game):
    penalty_cards = game['penalty_cards']
    
    if penalty_cards > 0:
        bot.send_message(player_id, f"You have {penalty_cards} penalty card(s). Use /penalty to draw them.")
    else:
        check_uno_call(player_id, game)

# Command handler for penalty card drawing
@bot.message_handler(commands=['penalty'])
def draw_penalty_cards(message):
    chat_id = message.chat.id
    player_id = message.from_user.id
    game = games.get(chat_id)
    
    if game:
        if player_id == game['current_player']:
            penalty_cards = game['penalty_cards']
            if penalty_cards > 0:
                for _ in range(penalty_cards):
                    card = draw_card_from_deck(game)
                    game['players'][player_id]['hand'].append(card)
                
                game['penalty_cards'] = 0
                bot.send_message(player_id, f"You drew {penalty_cards} penalty card(s).")
                check_uno_call(player_id, game)
            else:
                bot.reply_to(message, "There are no penalty cards to draw.")
        else:
            bot.reply_to(message, "It's not your turn.")
    else:
        bot.reply_to(message, "There is no game in progress.")

# Function to check UNO calls
def check_uno_call(player_id, game):
    uno_calls = game['uno_calls']
    if player_id in uno_calls:
        uno_calls[player_id] += 1
    else:
        uno_calls[player_id] = 1
    
    if len(game['players'][player_id]['hand']) == 1 and uno_calls[player_id] == 1:
        bot.send_message(player_id, "Don't forget to call UNO!")

# Command handler for calling UNO
@bot.message_handler(commands=['uno'])
def call_uno(message):
    chat_id = message.chat.id
    player_id = message.from_user.id
    game = games.get(chat_id)
    
    if game:
        if player_id == game['current_player']:
            uno_calls = game['uno_calls']
            if player_id in uno_calls and uno_calls[player_id] == 1:
                bot.send_message(chat_id, f"{message.from_user.username} called UNO!")
            else:
                bot.reply_to(message, "Invalid UNO call.")
        else:
            bot.reply_to(message, "It's not your turn.")
    else:
        bot.reply_to(message, "There is no game in progress.")

# Function to end the game and clean up the game session
def end_game(game):
    del games[game['chat_id']]

# Start the bot
bot.polling()