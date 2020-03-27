import math
import random
import numpy as np


class Parser:
    def __init__(self, datas: list):
        self.datas = datas
        self.place_mapping = {}
        self.rand = list(range(0, len(self.datas)))
        places = ['남', '뉴', '러', '모', '미', '브', '아일', '영', '우크', '인', '일', '중', '캐', '프', '한', '헨', '호']
        for (index, value) in enumerate(places):
            self.place_mapping[value] = index / len(places)
        # random.shuffle(self.rand)
        self.datas.sort(key=lambda val: val[3])
        try:
            self._win1 = sum([math.log10(item[15]) if item[15] != 0 else 0 for item in datas])
        except Exception:
            print([item[15] for item in datas])
        try:
            self._win2 = sum([math.log10(item[16]) if item[16] != 0 else 0 for item in datas])
        except Exception:
            print([])

        assert (self._win1 != 0 and self._win2 != 0)

    def __get_rank(self, index: int):
        return int(self.datas[index][2])
    
    def __get_birth_place(self, index: int):
        assert (self.datas[index][5] in self.place_mapping)
        return self.place_mapping[self.datas[index][5]]
    
    def __get_gender(self, index: int):
        mapping = {'암': 0, '거': 0.5, '수': 1}
        assert (self.datas[index][6] in mapping)
        return mapping[self.datas[index][6]]
    
    def __get_age(self, index: int):
        assert self.datas[index][7][-1] == '세'
        return int(self.datas[index][7][:-1]) / 8
    
    def __get_weight(self, index: int):
        return (int(self.datas[index][14].split('(')[0]) - 300) / 200
    
    def __get_win1(self, index: int):
        value = self.datas[index][15]
        return math.log10(value) / self._win1
    
    def __get_win2(self, index: int):
        value = self.datas[index][16]
        return math.log10(value) / self._win2
    
    def __get_stats(self, index: int, horses_stats):
        horseCode = self.datas[index][18]
        return horses_stats[horseCode]
    
    def __get_input(self, index: int, horses_stats):
        return np.asarray([self.__get_birth_place(index), self.__get_gender(index),
            self.__get_age(index), self.__get_weight(index), self.__get_win1(index),
            self.__get_win2(index), *self.__get_stats(index, horses_stats)], dtype=np.float32)
    
    def __get_output(self, index: int):
        return self.__get_rank(index)
    
    def parse_x(self, horses_wins):
        return np.asarray([self.__get_input(idx, horses_wins) for idx in self.rand])
    
    def parse_y(self):
        return np.asarray([self.__get_output(idx) for idx in self.rand], dtype=np.int32)
    
    def parse_z(self):
        return np.asarray([[self.datas[index][15], self.datas[index][16]] for index in self.rand])
