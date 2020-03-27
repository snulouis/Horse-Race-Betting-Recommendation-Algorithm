import pickle

import pandas as pd

from data_parser import Parser


def parse_win(value):
    return (0.001 if value == '----' or value == '' else float(value))

class Preprocess:
    def __init__(self, filepath: str, track_size: int, max_track_size: int, horses_stats, encoding: str='utf-8'):
        datas = pd.read_csv(filepath, encoding=encoding, sep='\t', converters={'단승': parse_win, '연승': parse_win})
        self.datas = filter(lambda data: len(data[1].index) >= track_size, datas[datas['순위'].notnull()].groupby([datas['날짜'], datas['경기번호']]))
        self.track_size = track_size
        self.horses_stats = horses_stats
        self.max_track_size = max_track_size
    
    def run(self):
        result_x = [[] for _ in range(self.max_track_size)]
        result_y = [[] for _ in range(self.max_track_size)]
        result_z = [[] for _ in range(self.max_track_size)]
        for data in self.datas:
            data = data[1].values.tolist()
            parser = Parser(data)
            x_ = parser.parse_x(self.horses_stats)
            y_ = parser.parse_y()
            z_ = parser.parse_z()
            if len(x_.shape) == 2 and x_.shape[1] == 9:
                result_x[len(data)].append(x_)
                result_y[len(data)].append(y_)
                result_z[len(data)].append(z_)
        return result_x, result_y, result_z
