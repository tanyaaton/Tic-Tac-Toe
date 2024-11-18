# Main game loop
board = [" " for _ in range(9)]
from UR3e_control import robot_move, human_move, play_position, home, UR_set_up, test, grid, gripper_connection,gripper_open,gripper_close, draw_end_line
from minimax_tictactoe import display_board, check_winner, is_board_full, board, computer_move

import socket, struct, time
import time
from gripper import Gripper
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
    st.title("🌷Welcome")
    st.markdown('''
    This is your Tic-Tac-Toe game.
    You can play with ROBOT!!!!
    ''')

empty_path = 'image/empty.png'
x_path = 'image/x.png'
o_path = 'image/o.png'

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
            st.image(path_list[0], width=200, use_column_width=True)
        with col2:
            st.image(path_list[1], width=200, use_column_width=True)
        with col3:
            st.image(path_list[2], width=200, use_column_width=True)

        # Second row
        col4, col5, col6 = st.columns(3)
        with col4:
            st.image(path_list[3], width=200, use_column_width=True)
        with col5:
            st.image(path_list[4], width=200, use_column_width=True)
        with col6:
            st.image(path_list[5], width=200, use_column_width=True)

        # Third row
        col7, col8, col9 = st.columns(3)
        with col7:
            st.image(path_list[6], width=200, use_column_width=True)
        with col8:
            st.image(path_list[7], width=200, use_column_width=True)
        with col9:
            st.image(path_list[8], width=200, use_column_width=True)

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

def play_game():
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
        human_move(user_pos+1, 'X')
        play_position()
        streamlit_remove_table()
        update_path_list(user_pos, 'X')
        streamlit_display_table(path_list)
        display_board()
        
        # Check if player wins
        if check_winner("X"):
            draw_end_line("X")
            print("Congratulations! You win!")
            break
        
        # Check if it's a tie
        if is_board_full():
            print("It's a tie!")
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
            print("Computer wins! Better luck next time!")
            break
        
        # Check if it's a tie
        if is_board_full():
            print("It's a tie!")
            play_position()
            home()
            break


if __name__ == '__main__':
        server_connection()
        # gripper_init()
        UR_set_up()
        home()
        # grid()
        # test()
        play_position()
        play_game()
        # robot_move(1, 'X')
