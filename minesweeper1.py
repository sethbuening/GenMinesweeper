import random
class Minesweeper:
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    def __init__(self, width=9, height=9, mines=10):
        self.lost = False
        self.width = width
        self.height = height
        self.board = []
        self.revealed = []
        self.num_mines = mines
        for i in range(self.height):
            for j in range(self.width):
                self.board.append(0)
                self.revealed.append(-1)

    def place_mines(self):
        for i in range(self.num_mines):
            mine_location = random.randint(0, self.width * self.height - 1)
            while self.board[mine_location] == 9:
                mine_location = random.randint(0, self.width * self.height - 1)
            self.board[mine_location] = 9


    def calc_nums(self):
        for i in range(self.height):
            for j in range(self.width):
                if(self.board[i*self.width + j] != 9):
                    continue
                for x, y in self.directions:
                    loc = [j, i]
                    loc[0] += x
                    loc[1] += y
                    if loc[0] >= self.width or loc[1] >= self.height:  #if out of bounds below or rightwards
                        continue
                    if(loc[0] < 0 or loc[1] < 0):  #if out of bounds above or leftwards
                        continue
                    if(self.board[loc[1]*self.width + loc[0]] != 9):
                        self.board[loc[1]*self.width + loc[0]]+=1

    def reveal(self, x, y):
        if self.board[y*self.width + x] == 0:
            zeroes = []
            self.revealed[y*self.width + x] = 0
            zeroes.append(y * self.width + x)

            while(len(zeroes) > 0):
                current_tile = zeroes.pop()
                j = current_tile % self.width
                i = int(current_tile / self.width)
                for x, y in self.directions:
                    loc = [j, i]
                    loc[0] += x
                    loc[1] += y
                    if loc[0] >= self.width or loc[1] >= self.height:  #if out of bounds below or rightwards
                        continue
                    if(loc[0] < 0 or loc[1] < 0):  #if out of bounds above or leftwards
                        continue
                    if(self.board[loc[1] * self.width + loc[0]] == 0):
                        if(self.revealed[loc[1] * self.width + loc[0]] == -1):
                            zeroes.append(loc[1] * self.width + loc[0])
                    if(self.board[loc[1] * self.width + loc[0]] != 9):
                        self.revealed[loc[1] * self.width + loc[0]] = self.board[loc[1] * self.width + loc[0]]
        elif self.board[y*self.width + x] == 9:
            print("You lose")
            self.lost = True
        else:
            self.revealed[y*self.width + x] = self.board[y*self.width + x]
minesweeper = Minesweeper()
minesweeper.place_mines()
minesweeper.calc_nums()


while(not minesweeper.lost):
    print(len(minesweeper.revealed))
    for i in range(9):
        for j in range(9):
            if(minesweeper.revealed[i * minesweeper.width + j] == -1):
                print("*", end=" ")
            else:
                print(minesweeper.revealed[i * minesweeper.width + j], end=" ")
        print("")
    guess = input("Reveal a tile (x,y): ")
    guess = guess.split(',')
    minesweeper.reveal(int(guess[0]), int(guess[1]))
