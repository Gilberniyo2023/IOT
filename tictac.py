import tkinter as tk
from tkinter import messagebox
import random


def get_empty_cells(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']


def check_win(board, player):
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    # Check diagonals
    return (board[0][0] == board[1][1] == board[2][2] == player) or \
           (board[0][2] == board[1][1] == board[2][0] == player)


def is_board_full(board):
    return all(board[r][c] != ' ' for r in range(3) for c in range(3))


def minimax(board, depth, is_maximizing):
    if check_win(board, 'X'):
        return 10 - depth
    if check_win(board, 'O'):
        return -10 + depth
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r, c in get_empty_cells(board):
            board[r][c] = 'X'
            score = minimax(board, depth + 1, False)
            board[r][c] = ' '
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for r, c in get_empty_cells(board):
            board[r][c] = 'O'
            score = minimax(board, depth + 1, True)
            board[r][c] = ' '
            best_score = min(best_score, score)
        return best_score


def find_best_move(board):
    best_move = None
    best_score = -float('inf')
    for r, c in get_empty_cells(board):
        board[r][c] = 'X'
        score = minimax(board, 0, False)
        board[r][c] = ' '
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move


class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tic-Tac-Toe")

        self.board = [[' '] * 3 for _ in range(3)]
        self.buttons = []
        self.player_turn = 'O'
        self.game_mode = 1

        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        for r in range(3):
            row_buttons = []
            for c in range(3):
                button = tk.Button(self.master, text=' ', font=('Arial', 24), width=5, height=2,
                                   command=lambda r=r, c=c: self.handle_click(r, c))
                button.grid(row=r, column=c)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.mode_frame = tk.Frame(self.master)
        self.mode_frame.grid(row=3, columnspan=3)

        tk.Button(self.mode_frame, text="Player vs AI", command=lambda: self.set_mode(1)).pack(side=tk.LEFT)
        tk.Button(self.mode_frame, text="AI vs AI", command=lambda: self.set_mode(2)).pack(side=tk.RIGHT)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=4, columnspan=3)

        self.status_label = tk.Label(self.master, text="Player (O) turn", font=('Arial', 12))
        self.status_label.grid(row=5, columnspan=3)

    def set_mode(self, mode):
        self.game_mode = mode
        if mode == 1:
            self.status_label.config(text="Player (O) turn")
        else:
            self.status_label.config(text="AI vs AI mode")
        self.reset_game()

    def handle_click(self, row, col):
        if self.board[row][col] == ' ' and self.game_mode == 1:
            self.board[row][col] = 'O'
            self.buttons[row][col].config(text='O')
            self.player_turn = 'X'
            self.status_label.config(text="AI (X) turn")
            self.update_board()
            if not check_win(self.board, 'O') and not is_board_full(self.board):
                self.master.after(500, self.ai_move)

    def ai_move(self):
        if check_win(self.board, 'O') or check_win(self.board, 'X') or is_board_full(self.board):
            return

        move = find_best_move(self.board)
        if move:
            row, col = move
            self.board[row][col] = self.player_turn
            self.buttons[row][col].config(text=self.player_turn)
            self.player_turn = 'O' if self.player_turn == 'X' else 'X'
            status = f"{'AI (X)' if self.player_turn == 'X' else 'AI (O)'} turn"
            self.status_label.config(text=status)
            self.update_board()

        if self.game_mode == 2 and not check_win(self.board, 'X') and not check_win(self.board, 'O') and not is_board_full(self.board):
            self.master.after(500, self.ai_move)

    def update_board(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=self.board[r][c])

        if check_win(self.board, 'O'):
            self.show_game_over("Player (O) wins!")
        elif check_win(self.board, 'X'):
            self.show_game_over("AI (X) wins!")
        elif is_board_full(self.board):
            self.show_game_over("It's a tie!")

    def show_game_over(self, message):
        messagebox.showinfo("Game Over", message)
        self.reset_game()

    def reset_game(self):
        self.board = [[' '] * 3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=' ')
        self.player_turn = 'O'
        self.status_label.config(text="Player (O) turn" if self.game_mode == 1 else "AI vs AI mode")
        if self.game_mode == 2:
            self.master.after(500, self.ai_move)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()
