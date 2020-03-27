import glob
import time
from multiprocessing import Pool
from os import path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter


def getHorseWinsHelper(horseCode: str, category: int):
    BASE_URL = 'https://race.kra.co.kr/racehorse/profileHorseItem.do'
    s = requests.Session()
    s.mount('https://', HTTPAdapter(max_retries=5))
    res = s.get(BASE_URL, params={'Act': '04', 'hrNo': horseCode, 'meet': category}).content
    soup = BeautifulSoup(res, 'html.parser')
    table = soup.find('div', class_='tableType1')

    tds = table.find_all('tr')[4].find_all('td')
    total = tds[0].text

    if not total:
        return False
    total, val = total[:-1].split('(')
    if category == 2:
        total = total[:-2]
    val = val.split('/')

    assert len(val) == 5
    win0 = tds[1].text.split(':')[1].strip()[:-1]
    win1 = tds[2].text.split(':')[1].strip()[:-1]
    win2 = tds[3].text.split(':')[1].strip()[:-1]
    return [horseCode, total, *val, win0, win1, win2]

def getHorseWins(horseCode: str):
    for category in [1, 2, 3]:
        res = getHorseWinsHelper(horseCode, category)
        if res:
            return res
    print('Error to parse at {}'.format(horseCode))
    return [horseCode, *['-' for _ in range(8)]]

if __name__ == '__main__':
    DIRECTORY = 'crawler\\data'
    paths = glob.glob(path.join(DIRECTORY, '*.tsv'))

    pds = [pd.read_csv(path, usecols =['말id'], encoding='utf-8', sep='\t', converters={'말id': str}) for path in paths]
    pds = pd.concat(pds)
    pds = pds['말id'].unique().tolist()

    headers = ['말id', '전체 경기', '통계1', '통계2', '통계3', '통계4', '통계5', '승률', '복승률', '연승률']
    pool_size = 4

    file_handler = open('horses_win.tsv', 'w')
    file_handler.write(('\t'.join(headers) + '\n').encode('utf-8'))

    batch_size = 64
    with Pool(pool_size) as pool:
        batch_num = (len(pds) + batch_size - 1) // batch_size
        for idx in range(batch_num + 1):
            print('{:5} / {:5}'.format(idx, batch_num))
            items = pds[idx * batch_size: (idx + 1) * batch_size]
            write_datas = pool.imap(getHorseWins, items)
            for write_data in write_datas:
                file_handler.write(('\t'.join(write_data) + '\n').encode('utf-8'))
            file_handler.flush()
            time.sleep(1.0)
