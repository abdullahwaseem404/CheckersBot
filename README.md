# ♟️ CheckersBot – AI Game Engine

A web-based Checkers game built using **Python** and **Streamlit**, where a human player competes against an AI powered by a **hybrid decision system (Minimax + Reinforcement Learning Q-learning style agent)**.

---

## 🚀 Features

* 🎮 Interactive 8×8 Checkers board built with Streamlit
* 🤖 Player vs AI gameplay
* 🧠 AI powered by **Minimax algorithm (depth-limited search)**
* 🧪 Hybrid decision system combining:
  * Minimax (strategic planning)
  * Q-learning style RL agent (state-action learning)
* ⚡ Capture mechanics and valid move validation
* 🖥️ Clean and minimal Streamlit UI
* 🔄 Reset game functionality

---

## 🧠 How the AI Works

The AI uses a **hybrid intelligence system**:

### 1. Minimax Algorithm

* Explores possible future game states
* Evaluates board positions using a simple heuristic:
  * AI pieces – Player pieces
* Chooses optimal move assuming optimal opponent play

### 2. Reinforcement Learning Agent (Q-Learning Style)

* Stores state-action values in a Q-table
* Learns from rewards after each move
* Uses:
  * Exploration (random moves)
  * Exploitation (best known move)

### 3. Hybrid Strategy

AI randomly switches between:
* Minimax decision-making
* Q-learning based decision-making

This creates a balance between:
* Strategic planning
* Adaptive learning behavior

---

## 🛠️ Tech Stack

* Python 🐍
* Streamlit 🌐
* Minimax Algorithm ♟️
* Q-learning (simplified DQN-style agent) 🧠
  
---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/abdullahwaseem404/CheckersBot.git
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

---

## 🎮 Controls

* Click a **🔴 red piece** to select it
* Click a valid square to move
* AI (⚫) automatically plays after your turn

---

## 🧪 AI Behavior

* AI evaluates board state using piece advantage
* Uses Minimax for optimal decision search
* Uses Q-table memory for learning from past moves
* Switches strategy randomly for dynamic gameplay

---

## 🔄 Reset Game

Click the **“♻️ Reset Game”** button to restart anytime.

---
