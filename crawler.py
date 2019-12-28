import requests
import time
from datetime import datetime
from lxml import etree

class Crawler(object):
    def __init__(self,
                 base_url='https://www.csie.ntu.edu.tw/news/',
                 rel_url='news.php?class=101'):
        self.base_url = base_url
        self.rel_url = rel_url

    def crawl(self, start_date, end_date, date_thres=datetime(2012, 1, 1)):
        # DONE
        if end_date < date_thres:
            end_date = date_thres
        results = list()
        page_num = 0

        time.sleep(0.1)
        
        # DONE: crawl the page
        while True:
            results_buffer, end_crawl = self.crawl_page(start_date, end_date, page=f'&no={page_num}')
            page_num += 10
            results += results_buffer
            if end_crawl:
                break
        
        return results

    def crawl_page(self, start_date, end_date, page=''):
        """Parse ten rows of the given page

        Parameters:
            start_date (datetime): the start date (included)
            end_date (datetime): the end date (included)
            page (str): the relative url specified page num

        Returns:
            content (list): a list of date, title, and content
            last_date (datetime): the smallest date in the page
        """

        # DONE: get the html content
        res = requests.get(
            self.base_url + self.rel_url + page,
            headers={'Accept-Language':
                     'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        ).content.decode()

        # DONE: get post dates, titles and urls from the response
        root = etree.HTML(res)
        post_dates = root.xpath('/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]/text()')
        titles = root.xpath('/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]/a/text()')
        rel_urls = root.xpath('/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]/a/@href')

        # Each element of results contains a list of the post date, the title and the content
        # ex:[['date1', 'title1', 'content1'], ['date2', 'title2', 'content2'], ['date3', 'title3', 'content3']]
        results = list()
        end_crawl = False
        
        for rel_url, date, title in zip(rel_urls, post_dates, titles):
            # Check the post date exceeds the end date or not
            temp_date = datetime.strptime(date, '%Y-%m-%d')
            if temp_date > start_date:
                continue
            if end_date <= temp_date :
                result = list()
                result.append(date)
                result.append(title)

                url = self.base_url + rel_url
                content = self.crawl_content(url) 
                result.append(content)

                results.append(result)
            else:
                end_crawl = True
                break
        
        return results, end_crawl
    
    def crawl_content(self, url):
        """Crawl the content of given url

        For example, if the url is
        https://www.csie.ntu.edu.tw/news/news.php?Sn=15216
        then you are to crawl contents of
        ``Title : 我與DeepMind的A.I.研究之路, My A.I. Journey with DeepMind Date : 2019-12-27 2:20pm-3:30pm Location : R103, CSIE Speaker : 黃士傑博士, DeepMind Hosted by : Prof. Shou-De Lin Abstract: 我將與同學們分享，我博士班研究到加入DeepMind所參與的projects (AlphaGo, AlphaStar與AlphaZero)，以及從我個人與DeepMind的視角對未來AI發展的展望。 Biography: 黃士傑, Aja Huang 台灣人，國立臺灣師範大學資訊工程研究所博士，現為DeepMind Staff Research Scientist。``
        """
        res = requests.get(url).content.decode()
        root = etree.HTML(res)

        # DONE: find all the text in <div class="editor content"> and add them to the content
        content_list = root.xpath('/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[2]//text()')
        content = ' '.join(content_list) #transform the format of content from list to string
        content = content.replace('\xa0',' ')
        return content
    