import numpy as np
from collections import Counter
from scipy.spatial import distance
import tkinter as tk
from tkinter import messagebox

# Convert board state to a numerical format
def board_to_numeric(board):
    mapping = {'': 0, 'X': 1, 'O': 2}
    return [mapping[cell] for cell in board]

# Example dataset: (board state, next move)
dataset = [
    (['X', 'O', 'X', 'O', 'X', 'O', '', '', ''], 6),
    (['O', 'X', 'O', 'X', 'O', 'X', '', '', ''], 6),
    (['X', 'X', 'O', 'O', 'X', '', 'O', '', ''], 5),
    (['X', 'O', 'X', 'O', 'X', 'O', 'X', '', 'O'], 7),
    # Add more examples for a comprehensive dataset
]

# Convert dataset to numerical format
numeric_dataset = [(board_to_numeric(data[0]), data[1]) for data in dataset]

def check_two_in_a_row(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        values = [board[pos] for pos in condition]
        if values.count(player) == 2 and values.count('') == 1:
            return condition[values.index('')]
    return None

def knn_predict(board, dataset, k=3):
    print(f"Board state: {board}")
    
    # Check for a winning move
    winning_move = check_two_in_a_row(board, 'O')
    if winning_move is not None:
        print(f"AI winning move: {winning_move}")
        return winning_move

    # Check for a blocking move
    blocking_move = check_two_in_a_row(board, 'X')
    if blocking_move is not None:
        print(f"AI blocking move: {blocking_move}")
        return blocking_move

    numeric_board = board_to_numeric(board)
    # Calculate the distance between the input board and all boards in the dataset
    dists = sorted([(distance.euclidean(numeric_board, data[0]), data[1]) for data in dataset], key=lambda x: x[0])
    print(f"Distances: {dists}")

    # Ensure we have at least k neighbors
    if len(dists) < k:
        k = len(dists)

    nearest_neighbors = [move for _, move in dists[:k]]

    # Filter out moves that are not valid (i.e., those that target already occupied cells)
    valid_moves = [move for move in nearest_neighbors if board[move] == '']

    if not valid_moves:
        print("No valid moves found by k-NN. Falling back to the first available move.")
        valid_moves = [i for i, cell in enumerate(board) if cell == '']
        if not valid_moves:
            raise ValueError("No valid moves available for AI.")
        return valid_moves[0]

    print(f"Valid moves: {valid_moves}")
    # Return the most common move among the valid nearest neighbors
    return Counter(valid_moves).most_common(1)[0][0]

def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != '':
            return board[condition[0]]
    return None

def is_board_full(board):
    return '' not in board

def on_button_click(index):
    global board, current_player
    if board[index] == '':
        board[index] = current_player
        buttons[index].config(text=current_player, state='disabled')
        
        winner = check_winner(board)
        if winner:
            messagebox.showinfo("Tic Tac Toe", f"Player {winner} wins!")
            reset_game()
            return
        elif is_board_full(board):
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            reset_game()
            return
        
        current_player = 'O' if current_player == 'X' else 'X'
        
        if current_player == 'O':
            try:
                move = knn_predict(board, numeric_dataset)
                on_button_click(move)
            except ValueError as e:
                messagebox.showinfo("Tic Tac Toe", str(e))
                reset_game()

def reset_game():
    global board, current_player, buttons
    board = [''] * 9
    current_player = 'X'
    for button in buttons:
        button.config(text='', state='normal')

def create_gui():
    global buttons
    root = tk.Tk()
    root.title("Tic Tac Toe")

    buttons = []
    for i in range(9):
        button = tk.Button(root, text='', width=10, height=3,
                           command=lambda i=i: on_button_click(i))
        button.grid(row=i//3, column=i%3)
        buttons.append(button)

    root.mainloop()

if __name__ == "__main__":
    board = [''] * 9
    current_player = 'X'
    buttons = []
    create_gui()