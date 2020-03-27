import torch
import torch.nn as nn

class WinningSetModule(nn.Module):
    def __init__(self, features_num, min_lane, max_lane):
        super(WinningSetModule, self).__init__()
        self.min_lane = min_lane
        self.max_lane = max_lane
        hidden_dim = 16
        self.fc1 = nn.ModuleList([nn.Linear(features_num * size, hidden_dim) for size in range(min_lane, max_lane + 1)])
        self.fc2 = nn.ModuleList([nn.Linear(hidden_dim, size) for size in range(min_lane, max_lane + 1)])
    
    def forward(self, x):
        lane = len(x[0])
        assert self.min_lane <= lane <= self.max_lane
        model_index = lane - self.min_lane
        out = self.fc1[model_index](x.view(len(x), -1))
        out = self.fc2[model_index](out)
        return out

def send_next_layer(candidate_model, x):
    batch_size = len(x)
    if len(x[0]) == 7:
        return x, torch.stack(tuple([torch.Tensor(list(range(7))) for _ in range(batch_size)]))
    output = candidate_model(x)
    result = [None for _ in range(batch_size)]
    recommand_lanes = torch.sort(torch.topk(output, 7, sorted=False)[1])[0]
    for index in range(batch_size):
        result[index] = x[index, recommand_lanes[index]]
    return torch.stack(tuple(result)), recommand_lanes