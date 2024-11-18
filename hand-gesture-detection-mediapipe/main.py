# Main game loop
board = [" " for _ in range(9)]
from UR3e_control import robot_move, human_move, play_position, home, UR_set_up, test, grid, gripper_connection,gripper_open,gripper_close, draw_end_line
from minimax_tictactoe import display_board, check_winner, is_board_full, board, computer_move
# from pymodbus.client import ModbusTcpClient

import socket, struct, time
import time
from gripper import Gripper
import boto3
from uuid import uuid4
from minimax_tictactoe import display_board, check_winner, is_board_full, board, computer_move

#-------fill in this part after we have front end-------
#receivee player name from front end
#player_name = ???? 
import pandas as pd
import numpy as np

import streamlit as st

st.set_page_config(
    page_title="Retrieval Augmented Generation",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.header("Tic-Tac-Toe 🎮")

with st.sidebar:
    st.title(f"Welcome")
    st.markdown('''
    This is your Tic-Tac-Toe game.
    You can play with ROBOT!
    
    🎥💌🤖✨
    ''')     
    st.title('''To play:''')
    st.markdown('''          
    point your index finder to the position you want to play
    The robot will draw the symbol for you ;)
    ''')

empty_path = 'image/empty.png'
x_path = 'image/x.png'
o_path = 'image/o.png'

#------initialize dynamodb client------
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')  
table = dynamodb.Table('TicTacToeGameHistory')

if 'player_name' not in st.session_state:
    st.session_state.player_name = None
if 'table_container' not in st.session_state:
    st.session_state.table_container = st.empty()

path_list = [empty_path, empty_path, empty_path, empty_path, empty_path, empty_path, empty_path, empty_path, empty_path]

def update_path_list(index, symbol):
    if symbol == 'X':
        path_list[index] = x_path
    elif symbol == 'O':
        path_list[index] = o_path

def streamlit_display_table(path_list):
    with st.session_state.table_container.container():
        col_width = 1
        # First row
        col1, col2, col3 = st.columns([col_width, col_width, col_width])
        with col1:
            st.image(path_list[0], width=200)
        with col2:
            st.image(path_list[1], width=200)
        with col3:
            st.image(path_list[2], width=200)

        # Second row
        col4, col5, col6 = st.columns(3)
        with col4:
            st.image(path_list[3], width=200)
        with col5:
            st.image(path_list[4], width=200)
        with col6:
            st.image(path_list[5], width=200)

        # Third row
        col7, col8, col9 = st.columns(3)
        with col7:
            st.image(path_list[6], width=200)
        with col8:
            st.image(path_list[7], width=200)
        with col9:
            st.image(path_list[8], width=200)

def streamlit_remove_table():
    """Clear the existing table display to prepare for a new one"""
    st.session_state.table_container.empty()

def server_connection():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to the server.")

def gripper_init():
    gripper_connection()
    gripper_open()
    time.sleep(3)
    gripper_close()

# Player name input form
def get_player_name():
    if st.session_state.player_name is None:
        with st.form("player_name_form"):
            player_name = st.text_input("Enter your name to start playing:", "")
            submit_button = st.form_submit_button("Start Game")
            if submit_button and player_name:
                st.session_state.player_name = player_name
                st.success(f"Welcome, {player_name}! Let's play Tic-Tac-Toe.")


def play_game():
    move_count = 0
    print("Welcome to Tic-Tac-Toe!")
    print("The board positions are as follows:")
    # play_position()  
    print("Done sending play_postion")  
    display_board()
    streamlit_display_table(path_list)
    while True:
        # Player's turn
        command = client_socket.recv(1024).decode() # Receive command from server(Flush)
        while True:
            try:
                command = client_socket.recv(1024).decode()
                while not(command[-1].isdigit()):
                    command = client_socket.recv(1024).decode()
                print(f"Received Command: {command[-1]}")
                user_pos = int(command[-1]) - 1
                # user_pos = int(input("Choose your position (1-9): ")) - 1
                if user_pos in range(9) and board[user_pos] == " ":
                    board[user_pos] = "X"
                    break
                else:
                    print("Position already taken or invalid. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")
        
        print("user_pos", user_pos+1)
        move_count += 1 #add 1 move to player's record
        display_board()
        streamlit_remove_table()
        update_path_list(user_pos, 'X')
        streamlit_display_table(path_list)
        human_move(user_pos+1, 'X')
        play_position()
        
        # Check if player wins
        if check_winner("X"):
            draw_end_line("X")
            st.header("Congratulations! You win!")
            #player win computer by int(move) moves
            save_game_history(st.session_state.player_name,"Robot",st.session_state.player_name,move_count)
            break
        
        # Check if it's a tie
        if is_board_full():
            st.header("It's a tie!")
             #player ties computer by int(move) moves
            save_game_history(st.session_state.player_name,"Robot","Draw",move_count)
            play_position()
            home()
            break
        
        # Computer's turn
        computer_pos = computer_move()
        streamlit_remove_table()
        update_path_list(computer_pos-1, 'O')
        streamlit_display_table(path_list)
        robot_move(computer_pos, 'O')
        display_board()
        
        # Check if computer wins
        if check_winner("O"):
            draw_end_line("O")
            st.header("Computer wins! Better luck next time!")
            save_game_history(st.session_state.player_name,"Robot","Robot",move_count)
            break
        
        # Check if it's a tie
        if is_board_full():
            st.header("It's a tie!")
            play_position()
            home()
            break

# Function to save win/loss history and total moves
def save_game_history(player1, player2, winner, total_moves):
    game_id = str(uuid4())  # Generate a unique game ID
    item = {
        'GameID': game_id,
        'Player1': player1,
        'Player2': player2,
        'Winner': winner,
        'TotalMoves': total_moves
    }
    
    try:
        table.put_item(Item=item)
        print(f"Game {game_id} saved successfully.")
    except Exception as e:
        print(f"Error saving game history: {e}")


if __name__ == '__main__':
    get_player_name()
    if st.session_state.player_name:
        st.header("player: "+st.session_state.player_name)
        server_connection()
        # gripper_init()
        UR_set_up()
        home()
        # grid()
        # test()
        # play_position()
        play_position()
        play_game()
        # robot_move(1, 'X')