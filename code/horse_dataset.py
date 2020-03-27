from torch.utils.data import Dataset, DataLoader
import pickle

class HorseDataset(Dataset):
    def __init__(self, filepath: str):
        with open(filepath, 'rb') as f_handler:
            data = pickle.load(f_handler)
            self.x_data = data['x']
            self.y_data = data['y']
            self.z_data = data['z']
        self.len = len(self.y_data)
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index], self.z_data[index]
    
    def __len__(self):
        return self.len

if __name__ == '__main__':
    dataset = HorseDataset('./preprocess/data/data_07.pkl')

    _loader = DataLoader(dataset, batch_size=64)

    for i, (x, y, z) in enumerate(_loader):
        print(x.shape)
        print(y.shape)
        print(z.shape)
