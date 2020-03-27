import argparse
import glob
import os
import pickle
import numpy as np

from process import Preprocess


def main():
    # parsing argument
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--data-dir', help='Set datafolder path', required=True)
    parser.add_argument('-r', '--rank', help='Horse rank info file path', required=True)
    parser.add_argument('-o', '--output-dir', help='Output folder path', required=True)
    args = parser.parse_args()

    horses_stats = {}
    with open(args.rank, 'rb') as file_handler:
        file_handler.readline()
        for line in file_handler:
            line = line.decode('utf-8').strip().split('\t')
            horses_stats[int(line[0], 10)] = list(map(lambda val: float(val) / 100, line[-3:]))
    
    min_track = 7
    max_track = 20

    x, y, z = [[] for _ in range(max_track)], [[] for _ in range(max_track)], [[] for _ in range(max_track)]
    for filepath in glob.glob(os.path.join(args.data_dir, '*.tsv')):
        x_, y_, z_ = Preprocess(filepath, min_track, max_track, horses_stats).run()
        x = [x[index] + x_[index] for index in range(max_track)]
        y = [y[index] + y_[index] for index in range(max_track)]
        z = [z[index] + z_[index] for index in range(max_track)]

    for index in range(min_track, max_track):
        print(f'Track no: {index:02}; size: {len(y[index])}')
        if len(y[index]) > 0:
            with open(os.path.join(args.output_dir, f'data_{index:02}.pkl'), 'wb') as file_h:
                pickle.dump({'x': x[index], 'y': y[index], 'z': z[index]}, file_h)


if __name__ == "__main__":
    main()
