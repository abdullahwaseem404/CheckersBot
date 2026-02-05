import streamlit as st
import copy

EMPTY = 0
PLAYER = 1
AI = 2
BOARD_SIZE = 8

class Checkers:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for row in range(3):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1: board[row][col] = PLAYER
        for row in range(5, 8):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1: board[row][col] = AI
        return board

    def get_valid_moves(self, player):
        moves = []
        directions = [(1, -1), (1, 1)] if player == PLAYER else [(-1, -1), (-1, 1)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == player:
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and self.board[nr][nc] == EMPTY:
                            moves.append(((r, c), (nr, nc)))
                        if 0 <= r + 2*dr < BOARD_SIZE and 0 <= c + 2*dc < BOARD_SIZE:
                            if self.board[nr][nc] not in [EMPTY, player] and self.board[r + 2*dr][c + 2*dc] == EMPTY:
                                moves.append(((r, c), (r + 2*dr, c + 2*dc)))
        return moves

    def make_move(self, move):
        (r1, c1), (r2, c2) = move
        piece = self.board[r1][c1]
        self.board[r1][c1] = EMPTY
        self.board[r2][c2] = piece
        if abs(r2 - r1) == 2:
            self.board[(r1 + r2)//2][(c1 + c2)//2] = EMPTY

    def evaluate(self):
        p1_pieces = sum(row.count(PLAYER) for row in self.board)
        ai_pieces = sum(row.count(AI) for row in self.board)
        return ai_pieces - p1_pieces

def minimax(board, depth, maximizing_player):
    if depth == 0: return board.evaluate(), None
    current_player = AI if maximizing_player else PLAYER
    moves = board.get_valid_moves(current_player)
    if not moves: return board.evaluate(), None

    if maximizing_player:
        best_value = float('-inf')
        best_move = None
        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.make_move(move)
            val, _ = minimax(new_board, depth-1, False)
            if val > best_value:
                best_value, best_move = val, move
        return best_value, best_move
    else:
        best_value = float('inf')
        best_move = None
        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.make_move(move)
            val, _ = minimax(new_board, depth-1, True)
            if val < best_value:
                best_value, best_move = val, move
        return best_value, best_move

st.set_page_config(page_title="Streamlit Checkers", layout="centered")

st.markdown("""
    <style>
    div.stButton > button {
        width: 60px !important;
        height: 60px !important;
        border-radius: 0px !important;
        padding: 0px !important;
        font-size: 25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'game' not in st.session_state:
    st.session_state.game = Checkers()
    st.session_state.selected = None
    st.session_state.turn = "Player"

st.title("🔴 Checkers vs AI")
st.write(f"Current Turn: **{st.session_state.turn}**")

game = st.session_state.game

def handle_click(r, c):
    if st.session_state.selected is None:
        if game.board[r][c] == PLAYER:
            st.session_state.selected = (r, c)
    else:
        move = (st.session_state.selected, (r, c))
        if move in game.get_valid_moves(PLAYER):
            game.make_move(move)
            st.session_state.selected = None
            st.session_state.turn = "AI thinking..."
            _, ai_move = minimax(game, 3, True)
            if ai_move:
                game.make_move(ai_move)
            st.session_state.turn = "Player"
        else:
            st.session_state.selected = None

for r in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for c in range(BOARD_SIZE):
        piece = game.board[r][c]
        label = "🔴" if piece == PLAYER else ("⚫" if piece == AI else "")
        
        if (r, c) == st.session_state.selected:
            btn_key = f"select-{r}-{c}" 
        
        if cols[c].button(label, key=f"btn-{r}-{c}"):
            handle_click(r, c)
            st.rerun()

if st.button("Reset Game"):
    st.session_state.clear()
    st.rerun()