import random, Network, torch, time
class Minesweeper:
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    def __init__(self, width=9, height=9, mines=10):
        self.lost = False
        self.won = False
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
            self.lost = True
        else:
            self.revealed[y*self.width + x] = self.board[y*self.width + x]
        # Win check
        self.won = True
        for i in range(self.height):
            for j in range(self.width):
                if(self.revealed[i*self.width + j] == -1 and self.board[i*self.width + j] != 9):
                    self.won = False
                    break
            if(not self.won):
                break
def run (WIDTH, HEIGHT, BOMBS, weights, biases, neurons, test):
    # Run the minesweeper game 5 times, averaging the scores together
    average_score = 0
    network = Network.NeuralNetwork(weights, biases, neurons)
    for _ in range(2):
        minesweeper = Minesweeper(WIDTH, HEIGHT, BOMBS)
        minesweeper.place_mines()
        minesweeper.calc_nums()

        index = minesweeper.board.index(0)
        minesweeper.reveal(index%WIDTH, int(index/HEIGHT))

        while (not (minesweeper.lost or minesweeper.won)):
            input = torch.tensor(minesweeper.revealed, dtype=torch.float32)
            output = network.forward(input, minesweeper)

            x = output % minesweeper.width
            y = int(output / minesweeper.width)

            minesweeper.reveal(x, y)

            if(test):
                time.sleep(1)
        # Calculate the score
        score = 0
        for i in range(minesweeper.height):
            for j in range(minesweeper.width):
                if(minesweeper.revealed[i*WIDTH + j] != -1):
                    score += 1
        average_score += score
    return average_score/2