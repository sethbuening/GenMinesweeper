# Change the input to be only the robot's y position
import torch as t
class NeuralNetwork(t.nn.Module):
    def __init__(self, weights, biases, _neurons):
        with t.no_grad():
            super().__init__()
            t.manual_seed(0)
            t.set_num_threads(10)
            # Define layers
            neurons = _neurons
            self.layers = len(neurons)-1
            self.network = []
            for i in range(self.layers):
                self.network.append(t.nn.Linear(neurons[i], neurons[i+1]))
            self.weightsCount = []
            for i in range(self.layers):
                self.weightsCount.append(neurons[i]*neurons[i+1])

            self.weights = weights
            self.biases = biases

            #Manually set weights and biases for each layer
            for i in range(self.layers):
                self.network[i].weight.data = t.tensor(self.weights[sum(self.weightsCount[:i]):sum(self.weightsCount[:i+1])], dtype=t.float32).view(neurons[i+1], neurons[i])  # [6, 2]
                self.network[i].bias.data = t.tensor(self.biases[sum(neurons[1:i+1]):sum(neurons[1:i+2])], dtype=t.float32)  # [16]

    def forward(self, x):
        with t.no_grad():
            for i in range(self.layers - 1):
                x = t.relu(self.network[i](x)) # used to use tanh() but switched to relu for now
                #print(f"Layer {i+1} output: {str(x)}")
            x = t.softmax(self.network[-1](x), dim=1)
            output = t.flatten(x)
            #print("Final output: " + str(output))
            output = [value.item() for value in output] # converts from tensor to list
            output = output.index(max(output))
            
            return output # Returns 0 to (GRID_X*GRID_Y)-1     The index of the slot to click on for the minesweeper
