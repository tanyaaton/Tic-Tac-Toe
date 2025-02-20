# 🎮 Tic-Tac-Toe with UR3e Robotic Arm

## Overview
This project implements a Tic-Tac-Toe game controlled using hand gestures, with a UR3e robotic arm executing moves. The system uses computer vision for gesture recognition and AI for game logic.

## Features
- Hand gesture recognition usign MediaPipe library for player's move selection.
- AI opponent using the Minimax algorithm.
- UR3e robotic arm for physically marking moves on a real board.
- Data logging and visualization.

## File Structure
```
main/
│── image/                         # Image assets for the game
│
│── model/                          # Machine learning models
│   ├── keypoint_classifier/         # Model for hand keypoint classification
│   ├── point_history_classifier/    # Model for tracking hand motion
│   ├── __init__.py                  # Initialization file
│
│── utils/                          # Utility scripts
│   ├── __init__.py                  # Initialization file
│   ├── cvfpscalc.py                 # FPS calculation helper
│   ├── UR3e_control.py              # UR3e robotic arm control script
│   ├── app.py                       # Application entry point (GUI/web-based interaction)
│   ├── df_export.py                 # Data export utilities
│   ├── gripper.py                   # Gripper control functions for UR3e
│   ├── main.py                      # Main game logic
│   ├── minimax_tictactoe.py         # AI opponent using Minimax algorithm
│
│── test/                            # Test scripts
│
│── .gitignore                       # Git ignore file
│── AWSCLIV2.pkg                      # AWS CLI installation package (if needed)
│── requirements.txt                  # Python dependencies
│── tictactoe.db                      # Database file (if used)
```

## Setup Instructions
### Prerequisites
- Required Python packages (install via `requirements.txt`):
  ```bash
  pip install -r requirements.txt
  ```

