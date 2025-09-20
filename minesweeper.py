#!/usr/bin/env python3
"""
Simple terminal-based Minesweeper game implementation.
"""

import random
import sys


class Minesweeper:
    """A simple minesweeper game implementation."""
    
    def __init__(self, width=9, height=9, mines=10):
        """Initialize a new minesweeper game.
        
        Args:
            width: Width of the game board
            height: Height of the game board  
            mines: Number of mines to place
        """
        self.width = width
        self.height = height
        self.num_mines = mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flagged = [[False for _ in range(width)] for _ in range(height)]
        self.game_over = False
        self.won = False
        self._place_mines()
        self._calculate_numbers()
    
    def _place_mines(self):
        """Randomly place mines on the board."""
        mine_positions = set()
        while len(mine_positions) < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            mine_positions.add((x, y))
        
        for x, y in mine_positions:
            self.board[y][x] = -1  # -1 represents a mine
    
    def _calculate_numbers(self):
        """Calculate the number of adjacent mines for each cell."""
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1:  # Not a mine
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            ny, nx = y + dy, x + dx
                            if (0 <= ny < self.height and 0 <= nx < self.width 
                                and self.board[ny][nx] == -1):
                                count += 1
                    self.board[y][x] = count
    
    def reveal_cell(self, x, y):
        """Reveal a cell and handle game logic.
        
        Args:
            x: X coordinate (0-indexed)
            y: Y coordinate (0-indexed)
            
        Returns:
            True if the game should continue, False if game over
        """
        if (x < 0 or x >= self.width or y < 0 or y >= self.height 
            or self.revealed[y][x] or self.flagged[y][x]):
            return True
        
        self.revealed[y][x] = True
        
        # Hit a mine
        if self.board[y][x] == -1:
            self.game_over = True
            return False
        
        # If the cell is empty (0), reveal all adjacent cells
        if self.board[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    self.reveal_cell(x + dx, y + dy)
        
        # Check win condition
        if self._check_win():
            self.won = True
            self.game_over = True
            return False
        
        return True
    
    def toggle_flag(self, x, y):
        """Toggle flag on a cell."""
        if (0 <= x < self.width and 0 <= y < self.height 
            and not self.revealed[y][x]):
            self.flagged[y][x] = not self.flagged[y][x]
    
    def _check_win(self):
        """Check if the player has won."""
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True
    
    def display(self):
        """Display the current state of the board."""
        print("\n   ", end="")
        for x in range(self.width):
            print(f"{x:2}", end="")
        print()
        
        for y in range(self.height):
            print(f"{y:2} ", end="")
            for x in range(self.width):
                if self.flagged[y][x]:
                    print(" F", end="")
                elif not self.revealed[y][x]:
                    print(" .", end="")
                elif self.board[y][x] == -1:
                    print(" *", end="")
                elif self.board[y][x] == 0:
                    print("  ", end="")
                else:
                    print(f" {self.board[y][x]}", end="")
            print()


def main():
    """Main game loop."""
    print("Welcome to Terminal Minesweeper!")
    print("Commands:")
    print("  r x y  - Reveal cell at coordinates (x, y)")
    print("  f x y  - Toggle flag at coordinates (x, y)")
    print("  q      - Quit game")
    print()
    
    # Initialize game with default settings
    game = Minesweeper()
    
    while not game.game_over:
        game.display()
        print(f"\nMines remaining: {game.num_mines - sum(sum(row) for row in game.flagged)}")
        
        try:
            user_input = input("Enter command: ").strip().lower().split()
            
            if not user_input:
                continue
                
            command = user_input[0]
            
            if command == 'q':
                print("Thanks for playing!")
                sys.exit(0)
            elif command == 'r' and len(user_input) == 3:
                x, y = int(user_input[1]), int(user_input[2])
                game.reveal_cell(x, y)
            elif command == 'f' and len(user_input) == 3:
                x, y = int(user_input[1]), int(user_input[2])
                game.toggle_flag(x, y)
            else:
                print("Invalid command. Use 'r x y' to reveal, 'f x y' to flag, or 'q' to quit.")
                
        except (ValueError, IndexError):
            print("Invalid input. Please enter coordinates as numbers.")
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            sys.exit(0)
    
    # Game over
    game.display()
    if game.won:
        print("\nCongratulations! You won!")
    else:
        print("\nGame Over! You hit a mine!")


if __name__ == "__main__":
    main()