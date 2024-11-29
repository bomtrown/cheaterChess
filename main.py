import matplotlib.pyplot as plt
import numpy as np

# Define a mapping from chess piece names to Unicode symbols
CHESS_PIECES = {
    "king": "\u265A",   # White King
    "queen": "\u265B",  # White Queen
    "rook": "\u265C",   # White Rook
    "bishop": "\u265D", # White Bishop
    "knight": "\u265E", # White Knight
    "pawn": "\u265F",   # White Pawn
}

# Set up the figure
fig, ax = plt.subplots(figsize=(8, 8))

# Create a chessboard pattern with two shades of gray
chessboard_pattern = np.zeros((8, 8))
chessboard_pattern[1::2, ::2] = 1  # Light gray squares
chessboard_pattern[::2, 1::2] = 1  # Light gray squares

start_pos = None  # Track the user's selected positions
turn = "white"  # Track the current turn

class ChessPiece:
    def __init__(self, type, color):
        self.type = type
        self.color = color

    def move(self, board, start_pos, end_pos, turn):
        """Move the piece if valid and if it is the correct player's turn."""
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        piece = board[start_x][start_y]

        if piece is None or piece.color != turn:
            print(f"It's {turn}'s turn!")
            return False

        # Move the piece
        board[start_x][start_y] = None
        board[end_x][end_y] = piece
        return True

# Helper function to create the initial chessboard
def create_initial_board():
    initial_board = [
        [ChessPiece("rook", "black"), ChessPiece("knight", "black"), ChessPiece("bishop", "black"),
         ChessPiece("queen", "black"), ChessPiece("king", "black"), ChessPiece("bishop", "black"),
         ChessPiece("knight", "black"), ChessPiece("rook", "black")],
        [ChessPiece("pawn", "black") for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [ChessPiece("pawn", "white") for _ in range(8)],
        [ChessPiece("rook", "white"), ChessPiece("knight", "white"), ChessPiece("bishop", "white"),
         ChessPiece("queen", "white"), ChessPiece("king", "white"), ChessPiece("bishop", "white"),
         ChessPiece("knight", "white"), ChessPiece("rook", "white")],
    ]
    return initial_board

def update_pieces(board):
    """Update the displayed chessboard with the current state of the board."""
    ax.clear()
    ax.imshow(chessboard_pattern, cmap="Greys", interpolation="nearest", vmin=-1, vmax=2)
    ax.set_xticks(np.arange(8))
    ax.set_yticks(np.arange(8))
    ax.set_xticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    ax.set_yticklabels(['8', '7', '6', '5', '4', '3', '2', '1'])
    ax.grid(False)
    ax.set_xticks([], minor=True)
    ax.set_yticks([], minor=True)
    ax.invert_yaxis()

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece:
                symbol = CHESS_PIECES.get(piece.type, "")
                text_color = "white" if piece.color == "white" else "black"
                ax.text(j, i, symbol, ha="center", va="center", fontsize=24, color=text_color)

    plt.draw()


def is_within_board(x, y):
    """Check if the given position is within the chessboard boundaries."""
    return 0 <= x < 8 and 0 <= y < 8

def get_valid_moves(type, color, pos):
    """
    Get valid moves for a given chess piece, considering the current board state.
    :param type: Piece type ('king', 'queen', 'rook', 'bishop', 'knight', 'pawn')
    :param color: Piece color ('white', 'black')
    :param pos: Tuple (row, column) representing the current position
    :param board: 2D list representing the chessboard with ChessPiece objects or None
    :return: A 2D numpy array where 1 represents a valid move
    """
    global chessboard
    valid_moves = np.zeros((8, 8), dtype=int)
    x, y = pos  # Current position

    def is_enemy_piece(px, py):
        """Check if a position contains an enemy piece."""
        if not is_within_board(px, py) or not chessboard[px][py]:
            return False
        return chessboard[px][py].color != color

    def is_empty_square(px, py):
        """Check if a position is empty."""
        return is_within_board(px, py) and chessboard[px][py] is None

    if type == 'king':
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_within_board(nx, ny) and (is_empty_square(nx, ny) or is_enemy_piece(nx, ny)):
                valid_moves[nx][ny] = 1

    elif type == 'queen':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dx, dy in directions:
            for step in range(1, 8):
                nx, ny = x + step * dx, y + step * dy
                if is_empty_square(nx, ny):
                    valid_moves[nx][ny] = 1
                elif is_enemy_piece(nx, ny):
                    valid_moves[nx][ny] = 1
                    break  # Stop after capturing an enemy
                else:
                    break  # Blocked by another piece

    elif type == 'rook':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            for step in range(1, 8):
                nx, ny = x + step * dx, y + step * dy
                if is_empty_square(nx, ny):
                    valid_moves[nx][ny] = 1
                elif is_enemy_piece(nx, ny):
                    valid_moves[nx][ny] = 1
                    break
                else:
                    break

    elif type == 'bishop':
        directions = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dx, dy in directions:
            for step in range(1, 8):
                nx, ny = x + step * dx, y + step * dy
                if is_empty_square(nx, ny):
                    valid_moves[nx][ny] = 1
                elif is_enemy_piece(nx, ny):
                    valid_moves[nx][ny] = 1
                    break
                else:
                    break

    elif type == 'knight':
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_within_board(nx, ny) and (is_empty_square(nx, ny) or is_enemy_piece(nx, ny)):
                valid_moves[nx][ny] = 1

    elif type == 'pawn':
        if color == 'white':
            # Move forward
            if is_empty_square(x - 1, y):
                valid_moves[x - 1][y] = 1
                if x == 6 and is_empty_square(x - 2, y):  # Double move from starting row
                    valid_moves[x - 2][y] = 1
            # Captures
            if is_enemy_piece(x - 1, y - 1):
                valid_moves[x - 1][y - 1] = 1
            if is_enemy_piece(x - 1, y + 1):
                valid_moves[x - 1][y + 1] = 1
        elif color == 'black':
            # Move forward
            if is_empty_square(x + 1, y):
                valid_moves[x + 1][y] = 1
                if x == 1 and is_empty_square(x + 2, y):  # Double move from starting row
                    valid_moves[x + 2][y] = 1
            # Captures
            if is_enemy_piece(x + 1, y - 1):
                valid_moves[x + 1][y - 1] = 1
            if is_enemy_piece(x + 1, y + 1):
                valid_moves[x + 1][y + 1] = 1

    return valid_moves

def show_valid_moves(type, color, pos):
    """
    Highlight valid moves for a given piece type and position on the chessboard.
    """
    # Get valid moves for the piece
    valid_moves = get_valid_moves(type, color, pos)

    # Iterate over the valid_moves matrix
    for i in range(8):
        for j in range(8):
            if valid_moves[i][j] == 1:  # If the move is valid
                # Draw a semi-transparent rectangle on the valid square
                rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color='yellow', alpha=0.4)
                ax.add_patch(rect)

    plt.draw()

def is_valid_move(type, color, start_pos, end_pos):
    if get_valid_moves(type, color, start_pos)[end_pos[0]][end_pos[1]] == 1:
        return True
    else:
        return False

# Handle user clicks
def on_click(event):
    global start_pos, selected_type, selected_color, turn

    # Convert click coordinates to chessboard indices
    if event.inaxes == ax:
        col = int(event.xdata + 0.5)
        row = int(event.ydata + 0.5)

        # click 1 - if start_pos == None, it is a piece, the piece is on the right team and the piece can move
        if start_pos == None:
            # Ensure it is a piece
            if chessboard[row][col] is not None:
                # Ensure it is on the right team
                if chessboard[row][col].color == turn:
                    # Ensure the piece can move
                    if sum(sum(row) for row in get_valid_moves(chessboard[row][col].type, chessboard[row][col].color, [row, col])) != 0:
                        # Set start_pos
                        start_pos = (row, col)
                        selected_type = chessboard[row][col].type
                        selected_color = chessboard[row][col].color
                        print(selected_color, selected_type, 'on', start_pos)
                        show_valid_moves(selected_type, selected_color, start_pos)
                    else: print("This piece is not able to move")
                else: print("Not the correct colour")
            else: print("Not a piece")
        # click 2 - if start_pos != None and the piece can move to the location
        else:
            # Ensure it is a place the piece can move to
            if is_valid_move(selected_type, selected_color, start_pos, [row, col]):
                end_pos = (row, col)
                piece = chessboard[start_pos[0]][start_pos[1]]

                if piece and piece.move(chessboard, start_pos, end_pos, turn):
                    turn = "black" if turn == "white" else "white"
                    update_pieces(chessboard)
                else:
                    print("Invalid move! Try again.")

                # Reset for the next move
                start_pos = None
                selected_color = None
                selected_type = None
            else: print("Selected piece cannot move here")

# Initialize the game
chessboard = create_initial_board()
update_pieces(chessboard)

# Connect the click handler
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()