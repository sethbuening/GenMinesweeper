# GenMinesweeper
Genetic algorithm to play minesweeper; created for the Hello World 2025 hackathon at Purdue West Lafayette

## Minesweeper Game

This repository includes a simple terminal-based minesweeper game implementation in Python.

### How to Play

Run the game:
```bash
python3 minesweeper.py
```

**Commands:**
- `r x y` - Reveal cell at coordinates (x, y)
- `f x y` - Toggle flag at coordinates (x, y)  
- `q` - Quit game

**Game Rules:**
- The goal is to reveal all cells that don't contain mines
- Numbers show how many mines are adjacent to that cell
- Use flags to mark cells you think contain mines
- If you reveal a mine, the game ends

### Example Game Session

```
    0 1 2 3 4 5 6 7 8
 0  . . . . . . . . .
 1  . . . . . . . . .
 2  . . . . . . . . .
 3  . . . . . . . . .
 4  . . . . . . . . .
 5  . . . . . . . . .
 6  . . . . . . . . .
 7  . . . . . . . . .
 8  . . . . . . . . .

Mines remaining: 10
Enter command: r 4 4
```

Legend:
- `.` = Unrevealed cell
- `F` = Flagged cell
- `*` = Mine (shown when game ends)
- Numbers = Count of adjacent mines
- Empty space = Cell with no adjacent mines
