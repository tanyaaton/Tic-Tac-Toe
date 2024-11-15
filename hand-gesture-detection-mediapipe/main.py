# Main game loop
board = [" " for _ in range(9)]
from UR3e_control import robot_move, human_move, play_position, home, UR_set_up, test, grid
from minimax_tictactoe import display_board, check_winner, is_board_full, board, computer_move
from pymodbus.client import ModbusTcpClient

import socket, struct, time
import numpy,time
from gripper import Gripper

def server_connection():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to the server.")

def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print("The board positions are as follows:")
    play_position()  
    print("Done sending play_postion")  
    display_board()
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
        display_board()
        
        # Check if player wins
        if check_winner("X"):
            print("Congratulations! You win!")
            break
        
        # Check if it's a tie
        if is_board_full():
            print("It's a tie!")
            break
        
        # Computer's turn
        computer_pos = computer_move()
        robot_move(computer_pos, 'O')
        display_board()
        
        # Check if computer wins
        if check_winner("O"):
            print("Computer wins! Better luck next time!")
            break
        
        # Check if it's a tie
        if is_board_full():
            print("It's a tie!")
            break


if __name__ == '__main__':
        server_connection()
        UR_set_up()
        home()
        # grid()
        # test()
        # play_position()
        play_game()
        # robot_move(1, 'X')
        