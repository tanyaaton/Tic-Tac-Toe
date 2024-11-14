
from flask import Flask, request, jsonify
import random
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Initialize an empty board (3x3 grid)
board = [""] * 9  # Each cell is empty initially

def check_winner():
    """Check if there is a winner or if the game is a draw."""
    # Winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
            print(board[combo[0]])
            return board[combo[0]]  # Return "X" or "O" as the winner

    if all(cell != "" for cell in board):  # If all cells are filled
        return "Draw"  # Game is a draw

    return None  # No winner or draw yet

def get_computer_move():
    """Select a random available cell for the computer's move."""
    available_cells = [i for i in range(9) if board[i] == ""]
    return random.choice(available_cells) if available_cells else None

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    player_move = int(data['cellId'])

    # Update board with player's move
    if board[player_move] == "":
        board[player_move] = "X"
    else:
        return jsonify({"error": "Cell already taken"}), 400

    # Check if player won
    winner = check_winner()
    if winner:
        return jsonify({"winner": winner, "board": board})

    # Make computer's move
    computer_move = get_computer_move()
    if computer_move is not None:
        board[computer_move] = "O"

    # Check if computer won after its move
    winner = check_winner()
    if winner:
        return jsonify({"winner": winner, "board": board})

    # Return the updated game state to the frontend
    return jsonify({"computerMove": computer_move, "board": board})
    # return {"computerMove": 1, "board": board}

@app.route('/reset', methods=['GET'])
def reset_game():
    global board
    board = [""] * 9
    return jsonify({"message": "Game reset successfully!"})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
