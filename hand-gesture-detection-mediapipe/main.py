# Main game loop
board = [" " for _ in range(9)]
from minimax_tictactoe import display_board, urarm_move, check_winner, is_board_full
from UR3e_control import computer_move, human_move

def play_game():
    print("Welcome to Tic-Tac-Toe!")
    display_board()

    print('hello')
    
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
        
        human_move('human',user_pos)
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
        urarm_move('robot',computer_pos)
        display_board()
        
        # Check if computer wins
        if check_winner("O"):
            print("Computer wins! Better luck next time!")
            break
        
        # Check if it's a tie
        if is_board_full():
            print("It's a tie!")
            break

# Start the game
play_game()