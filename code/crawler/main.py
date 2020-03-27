import argparse

from crawler import Crawler


def get_year_data(year, pool_size=10):
    crawler = Crawler(year + '0101', year + '1231', 'data/' + year + '.tsv', encoding='utf-8', pool_size=pool_size)
    crawler.run()


def main():
    # parsing argument
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start-year', type=int, help='Set start year', required=True)
    parser.add_argument('-e', '--end-year', type=int, help='Set end year', required=True)
    parser.add_argument('-p', '--pool-size', type=int, help='Set thread pool size', default=4)
    args = parser.parse_args()

    for year in range(args.start_year, args.end_year + 1):
        get_year_data(str(year), args.pool_size)


if __name__ == '__main__':
    main()
