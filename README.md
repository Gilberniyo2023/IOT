===========================
IOT Projects
===========================

Project 1: AI-Powered Password Generator
project 2: (name/; password.py) more adanvaced than the first one 
----------------------------------------

Description:
-------------
This is an advanced password manager application that not only generates strong, random passwords based on customizable user settings, but also uses machine learning (ML) to evaluate and enhance the strength of the passwords in real time.

Key Features:
-------------
- GUI interface built using tkinter.
- Custom settings: length, character types (uppercase, lowercase, digits, special characters), and ambiguous character filters.
- Uses a trained neural network (MLPClassifier from scikit-learn) to classify password strength.
- Dynamically improves weak passwords by injecting stronger elements (digits/symbols).
- Password features are extracted using entropy, character diversity, and length metrics.
- Machine Learning model is trained on synthetic data and saved using `joblib` for reuse.
- Model auto-trains if not found, making the system adaptive and self-healing.

AI/ML Concepts Used:
---------------------
- Feature extraction (entropy, character count).
- Training a neural network with `MLPClassifier`.
- Model persistence with `joblib`.
- Real-time prediction and password optimization based on ML inference.


How to Use:
------------
1. Run the program.
2. Choose password length and character options.
3. Click “Generate Password”.
4. A strong, AI-evaluated password will be shown.
5. Exit with the "Exit" button.

Required Libraries:
-------------------
- tkinter
- sklearn
- numpy
- joblib
- secrets
- string
- random


Project 2: Tic Tac Toe Game (2-Player GUI Version)
--------------------------------------------------

Description:
-------------
A classic 2-player  and AI VS AI Tic Tac Toe game built using Python’s tkinter GUI library. Players alternate turns marking “X” or “O” on a 3x3 grid until one wins or the game ends in a draw.

Key Features:
-------------
- Interactive GUI with buttons for each cell.
- Turn-based input from Player 1 (X) and Player 2 (O).
- Automatic win/draw detection.
- End-of-game message alerts for win or draw.
- Reset after each game.

How to Play:
-------------
1. Run the game script.
2. Click a grid button to place your mark.
3. The system will announce the winner or a draw.
4. A new game starts automatically.

Required Libraries:
-------------------
- tkinter (standard with Python)

---------------------------
Developed by G_klay8
---------------------------
best wishes in navigating through them
