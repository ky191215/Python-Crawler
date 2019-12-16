from crawler import Crawler
from args import get_args

if __name__ == '__main__':
    args = get_args()
    print(args.start_date, args.end_date)
    crawler = Crawler()
    results = crawler.crawl(args.start_date, args.end_date)
    print(results)
    
    # TODO: write result to file according to spec
    with open(args.output + '.csv', 'w') as fp:
        #result[0] -> post date, [1] -> title, [2] -> content (url for now)
        for result in results:
            # Need modification for output specification afterwards
            fp.write(result[0]+'\n' + result[1] + '\n' + result[2] + '\n\n')


# Noun specification   
''' 
An article is a result
A result contains: post date, title, content
'''