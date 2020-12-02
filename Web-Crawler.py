#!/usr/bin/env python
# coding: utf-8

import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.request import urlretrieve


def download(articles):
    for article in articles:
        print('=' * 10 + 'Now Downloading' + '=' * 10)
        print(article.text)
        
        # Create a folder of the article
        if not os.path.isdir(os.path.join('download', article.text)):
            os.mkdir(os.path.join('download', article.text))

        # Go to the article page
        res = requests.get('https://www.ptt.cc' + article['href'], cookies={'over18': '1'})

        # Get url of each image
        images = reg_imgur_file.findall(res.text)
        set_images = set(images)

        # Download image
        for img in set_images:
            print(img)
            ID = re.search(r'https?://[^\s]*/([^/]*.(?:png|jpg|gif))', img).group(1)
            try:
                urlretrieve(img, os.path.join('download', article.text,ID))
            except Exception as e:
                print(e)
    print('=' * 10 + 'Successed' + '=' * 10)

    
def crawler(page_to_crawl=3, min_comment=50):
    # Create download folder if not exist
    if not os.path.isdir('download'):
        os.mkdir('download')
    
    url = 'https://www.ptt.cc/bbs/Beauty/index.html'
    articles = []
    
    for i in range(page_to_crawl):
        res = requests.get(url, cookies={'over18': '1'})
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Collect articles which comments are more than min_comment
        articles_p = soup.select('div.r-ent')
        for a in articles_p:
            # Extract number of net comments from a.span, if none then 'NA'
            comment_num = 'NA' if a.span == None else a.span.text
            if comment_num.isnumeric() and int(comment_num)>=min_comment:
                if '[公告]' not in a.a.text:
                    articles.append(a.a)
        
        # Update url to next page
        nxt = soup.select('div.btn-group-paging a')
        url = 'https://www.ptt.cc' + nxt[1]['href']
    
    
    print(f'Total {len(articles)} articles')
    for article in articles:
        print(article.text)
    
    # Start dowloading photos from articles in the list
    download(articles)


if __name__ == '__main__':        
    # Set regex of photo url
    reg_imgur_file = re.compile(r'https?://[^\s]*/[^/]*.(?:png|jpg|gif)')

    #Start Crawling
    crawler()






