from crawler import Crawler
from args import get_args

if __name__ == '__main__':
    args = get_args()
    crawler = Crawler()
    results = crawler.crawl(args.start_date, args.end_date)
    
    # DONE: write result to file according to spec
    with open(args.output + '.csv', 'w') as fp:
        for date, title, content in results:
            title = title.replace('\n',' ').replace('\r','')
            title = title.replace('\"','\"\"')
            content = content.replace('\n',' ').replace('\r','')
            content = content.replace('\"','\"\"')
            out_str = f'{str(date)},"{title}","{content}"\n'
            fp.write(out_str);


# Noun specification   
''' 
An article is a result
A result contains: post date, title, content
'''