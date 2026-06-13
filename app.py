import streamlit as st
import copy
import random

EMPTY = 0
PLAYER = 1
AI = 2
BOARD_SIZE = 8

class Checkers:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for r in range(3):
            for c in range(BOARD_SIZE):
                if (r + c) % 2 == 1:
                    board[r][c] = PLAYER

        for r in range(5, 8):
            for c in range(BOARD_SIZE):
                if (r + c) % 2 == 1:
                    board[r][c] = AI

        return board

    def get_valid_moves(self, player):
        moves = []
        directions = [(1, -1), (1, 1)] if player == PLAYER else [(-1, -1), (-1, 1)]

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == player:
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc

                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                            if self.board[nr][nc] == EMPTY:
                                moves.append(((r, c), (nr, nc)))

                        if 0 <= r + 2*dr < BOARD_SIZE and 0 <= c + 2*dc < BOARD_SIZE:
                            if self.board[nr][nc] not in [EMPTY, player]:
                                if self.board[r + 2*dr][c + 2*dc] == EMPTY:
                                    moves.append(((r, c), (r + 2*dr, c + 2*dc)))

        return moves

    def make_move(self, move):
        (r1, c1), (r2, c2) = move
        piece = self.board[r1][c1]

        self.board[r1][c1] = EMPTY
        self.board[r2][c2] = piece

        if abs(r2 - r1) == 2:
            self.board[(r1 + r2) // 2][(c1 + c2) // 2] = EMPTY

    def evaluate(self):
        return sum(row.count(AI) for row in self.board) - sum(row.count(PLAYER) for row in self.board)


class DQNAgent:
    def __init__(self):
        self.q_table = {}

    def get_state(self, board):
        return str(board)

    def choose_action(self, game, moves):
        state = self.get_state(game.board)

        if state not in self.q_table:
            self.q_table[state] = {}

        if random.random() < 0.2:
            return random.choice(moves)

        q_values = self.q_table[state]

        best_move = None
        best_value = float("-inf")

        for move in moves:
            if move not in q_values:
                q_values[move] = 0

            if q_values[move] > best_value:
                best_value = q_values[move]
                best_move = move

        return best_move or random.choice(moves)

    def update(self, state, action, reward):
        if state not in self.q_table:
            self.q_table[state] = {}

        self.q_table[state][action] = self.q_table[state].get(action, 0) + 0.1 * reward


agent = DQNAgent()


def minimax(board, depth, maximizing):
    if depth == 0:
        return board.evaluate(), None

    player = AI if maximizing else PLAYER
    moves = board.get_valid_moves(player)

    if not moves:
        return board.evaluate(), None

    best_move = None

    if maximizing:
        best_score = float("-inf")

        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.make_move(move)

            score, _ = minimax(new_board, depth - 1, False)

            if score > best_score:
                best_score = score
                best_move = move

        return best_score, best_move

    else:
        best_score = float("inf")

        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.make_move(move)

            score, _ = minimax(new_board, depth - 1, True)

            if score < best_score:
                best_score = score
                best_move = move

        return best_score, best_move


st.set_page_config(page_title="CheckersBot AI", layout="centered")

st.title("🔴 CheckersBot – AI Engine")


if "game" not in st.session_state:
    st.session_state.game = Checkers()
    st.session_state.selected = None

game = st.session_state.game

def ai_move():
    moves = game.get_valid_moves(AI)
    if not moves:
        return

    if random.random() < 0.5:
        _, move = minimax(game, 3, True)
    else:
        move = agent.choose_action(game, moves)

    if move:
        state = str(game.board)
        game.make_move(move)
        agent.update(state, move, game.evaluate())


def handle_click(r, c):
    if st.session_state.selected is None:
        if game.board[r][c] == PLAYER:
            st.session_state.selected = (r, c)
        return

    move = (st.session_state.selected, (r, c))

    if move in game.get_valid_moves(PLAYER):
        game.make_move(move)
        st.session_state.selected = None
        ai_move()
    else:
        st.session_state.selected = None


for r in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)

    for c in range(BOARD_SIZE):
        piece = game.board[r][c]

        label = ""
        if piece == PLAYER:
            label = "🔴"
        elif piece == AI:
            label = "⚫"

        if cols[c].button(label, key=f"{r}-{c}"):
            handle_click(r, c)
            st.rerun()


if st.button("♻️ Reset Game"):
    st.session_state.clear()
    st.rerun()