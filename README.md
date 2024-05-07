# Tic Tac Toe with Mini-Max Algorithm

## Key Commands:
- `r`: Reset Game.
- `g`: Toggle AI Opponent for 2 human players.
- `0`: Set AI opponent to random square selection.
- `1`: Set AI opponent to Mini-Max algorithm.

## Game Overview:
- **State Space**: 3x3 grid with empty, 'X', or 'O' cells.
- **Initial State**: Empty 3x3 grid.
- **Actions**: Place 'X' or 'O' in an empty cell.
- **Transition Model**: New state after action.
- **Goal Test**: 3 in a row/column/diagonal.
- **Path Cost**: Not considered.

## PEAS:
- **Performance**: Win, Block, Grid utilization.
- **Environment**: Opponent, Move, Board.
- **Actuators**: 'X', 'O', Draw.
- **Sensors**: Score, Turn, Game State.

## ODESA:
- **Observability**: Fully Observable.
- **Dynamics**: Deterministic.
- **Episodic/Sequential**: Sequential.
- **Static/Dynamic**: Semi-Dynamic.
- **Single/Multi-agent**: Multi-agent.

## Mini-Max Algorithm:
A recursive depth-first search algorithm maximizing the AI player's minimum gain.

**[YouTube Video](https://youtu.be/l-hh51ncgDI?feature=shared)**
