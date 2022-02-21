import json
import numpy as np

# Pytorch
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nlp_inicial import tokenizacao, stem, bagOfWords, st
from model import Neural

with open('intents.json', 'r') as f:
	intents = json.load(f)

all_words = []
tags = []
xy = []

for intent in intents['intents']:
	tag = intent['tag']
	tags.append(tag)
	for pattern in intent['patterns']:
		w = tokenizacao(pattern)
		all_words.extend(w)
		xy.append((w, tag))

ignore_words = ['?', '!', '.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))


x_train = []
y_train = []
for(pattern_setence, tag) in xy:
	bag =bagOfWords(pattern_setence, all_words)
	x_train.append(bag)

	label = tags.index(tag)
	y_train.append(label) # CrossEntropyLoss

x_train = np.array(x_train)
y_train = np.array(y_train)

#Hyperparametrs
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(all_words)
learning_rate = 0.001
number_epochs = 1000

#Create to automatically iterate over and get a better training
class ChatDataset(Dataset):
	def __init__(self):
		self.n_samples = len(x_train)
		self.x_data = x_train
		self.y_data = y_train

	#dataset[idx]
	def __getitem__(self, index):
		return self.x_data[index], self.y_data[index]

	def __len__(self):
		return self.n_samples


dataset = ChatDataset()
train_loader = DataLoader(dataset = dataset, 
                          batch_size = batch_size, 
                          shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = Neural(input_size, hidden_size, output_size).to(device)

#perdas e otimizacao
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(number_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{number_epochs}], Loss: {loss.item():.4f}')


print(f'final loss: {loss.item():.4f}')

data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
        }

FILE = "data.pth"
torch.save(data, FILE)

print(f'FILE SAVED TO: {FILE}')