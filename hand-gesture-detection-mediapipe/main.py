# Main game loop
board = [" " for _ in range(9)]
from minimax_tictactoe import display_board, check_winner, is_board_full, computer_move
from UR3e_control import robot_move, human_move, play_position, home, UR_set_up, position, position_X

import socket, struct, time
from pymodbus.client import ModbusTcpClient
import numpy,time
import math
from gripper import Gripper

# from minimax_tictactoe import display_board, check_winner, is_board_full, board, computer_move



def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print("The board positions are as follows:")
    play_position()  
    print("Done sending play_postion")  
    display_board()
    while True:
        # Player's turn
        while True:
            try:
                user_pos = int(input("Choose your position (1-9): ")) - 1
                if user_pos in range(9) and board[user_pos] == " ":
                    board[user_pos] = "X"
                    break
                else:
                    print("Position already taken or invalid. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")
        
        print("user_pos", user_pos)
        human_move(user_pos, 'X"')
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
        print("a")
        UR_set_up()
        print("b")
        home()
        play_game()
