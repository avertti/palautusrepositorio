# Kivi-Paperi-Sakset Web App

A web-based Rock-Paper-Scissors game built with Flask and Poetry.

## Features

- **Player vs Player**: Two players can play on the same device
- **Player vs Computer (Easy)**: Play against a random AI
- **Player vs Computer (Hard)**: Play against an AI that learns from your moves
- Score tracking across rounds
- Beautiful, responsive UI

## Installation

1. Make sure you have Python 3.8+ and Poetry installed
2. Navigate to the project directory
3. Install dependencies:
   ```
   poetry install
   ```

## Running the Application

Start the Flask server:
```
poetry run python app.py
```

The application will be available at: http://localhost:5000

## Game Rules

- Rock (🪨) beats Scissors (✂️)
- Scissors (✂️) beats Paper (📄)
- Paper (📄) beats Rock (🪨)

## Code Structure

- `app.py` - Main Flask application with routes and game logic
- `tuomari.py` - Judge class for keeping score
- `tekoaly.py` - Simple random AI opponent
- `tekoaly_parannettu.py` - Advanced AI that learns from player patterns
- `templates/` - HTML templates for the web interface
- `pyproject.toml` - Poetry dependency configuration

## Credits

This web app reuses game logic from the original console-based Kivi-Paperi-Sakset game.
