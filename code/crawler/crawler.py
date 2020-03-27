import re
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

from logger import print_debug, print_error


class Crawler:
    """
    Crawling horse racing informations from Korea Horse Association website.
    """
    def __init__(self, from_date, end_date, file_name, encoding='utf-8', pool_size=5):
        self.from_date = from_date
        self.end_date = end_date
        self.encoding = encoding
        self.file_handler = open(file_name, 'wb')
        self.pool_size = pool_size
    
    @staticmethod
    def get_index(s):
        return re.findall(r"'(\d+)'", s.a.get('href'))[0] if s.a is not None else ''

    def __get_rc_datas(self):
        print_debug('Get racing date & raceno (%s - %s)', self.from_date, self.end_date)
        def get_rc_data_helper(index):
            res = requests.post('http://race.kra.co.kr/raceScore/ScoretableScoreList.do', {
                'nextFlag':'true',
                'fromDate': self.from_date,
                'toDate': self.end_date,
                'pageIndex':index
            }, timeout=5).content.decode('euc-kr')
            soup = BeautifulSoup(res, 'html.parser')
            table = soup.find('div', class_='tableType2').table
            items = table.find_all('tr')[1:]
            
            result = []
            for item in items:
                data = item.find_all('td')[1:]
                if len(data) == 0:
                    return None
                result += [(data[0].text.strip().split('\n')[0].replace('/', ''), rc_no.text.split(' ')[0].strip()) for rc_no in data[1].find_all('a')]
            return result
        result = []
        index = 1
        while True:
            item = get_rc_data_helper(index)
            if item is None:
                return result
            result += item
            index += 1

    @staticmethod
    def get_rc_result_helper(info):
        date, RcNo = info
        if RcNo == '1':
            print_debug('Trying %s', date)
        res = requests.post('http://race.kra.co.kr/raceScore/ScoretableDetailList.do', {
            'meet':'1',
            'realRcDate':date,
            'realRcNo':RcNo
        }).content.decode('euc-kr')

        soup = BeautifulSoup(res, 'html.parser')
        table = soup.find_all('div', class_='tableType2')
        if len(table) < 2:
            print_error('Failed to get table (%s, %s)', *info)
            return None
        table1 = table[0].table
        table2 = table[1].table
        tmp = {}
        for horse1 in table1.find_all('tr')[1:]:
            datas = horse1.find_all('td')
            item = [date, RcNo]
            item += list(map(lambda x: x.text.strip(), datas))
            item += [Crawler.get_index(datas[2]), Crawler.get_index(datas[8]),
                     Crawler.get_index(datas[9]), Crawler.get_index(datas[10])]
            tmp[int(datas[1].text)] = item
        
        for horse2 in table2.find_all('tr')[1:]:
            datas = horse2.find_all('td')
            item = list(map(lambda x: x.text.strip(), datas[3:]))
            tmp[int(datas[1].text)] += item
        
        return sorted(list(tmp.values()), key=lambda x: int(x[0][0]))
    
    def __write_file(self, data):
        if data is None:
            return
        write_data = '\n'.join(['\t'.join(item) for item in data])+'\n'
        self.file_handler.write(write_data.encode(self.encoding))
        self.file_handler.flush()
    
    def __write_header(self):
        header = [
            '날짜', '경기번호', '순위', '마번', '마명', '산지', '성별', '연령', '중량',
            '레이팅', '기수명', '조교사명', '마주명', '도착차', '마체중', '단승', '연승', '장구현황',
            '말id', '기수id', '조교사id', '마주id', 'S-1F', '1코너', '2코너', '3코너', '4코너', 'G-3F', 'G-1F', '경주기록'
        ]
        self.file_handler.write(('\t'.join(header) + '\n').encode(self.encoding))
    
    def run(self):
        self.__write_header()
        rc_datas = self.__get_rc_datas()
        print_debug('Get racing result [ %3d ]', len(rc_datas))
        with Pool(self.pool_size) as pool:
            write_datas = pool.imap(Crawler.get_rc_result_helper, rc_datas)
            for write_data in write_datas:
                self.__write_file(write_data)
        self.file_handler.close()
