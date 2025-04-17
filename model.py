import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    
    def save(self, filename='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(model_folder_path)
        filename = os.path.join(model_folder_path, filename)
        torch.save(self.state_dict(), filename)
    
    def load(self, filename='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(model_folder_path)
        filename = os.path.join(model_folder_path, filename)
        self.load_state_dict(torch.load(filename))
        self.eval()
    
class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        
    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # Q value from the current state
        pred = self.model(state)

        target = pred.clone()
        
        for i in range(len(done)):
            Q_new = reward[i]
            if not done[i]:
                Q_new = reward[i] + self.gamma * torch.max(self.model(next_state[i]))
            
            target[i][torch.argmax(action[i]).item()] = Q_new

        # Train the model
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()