import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv

base_url = 'https://www.notion.so'
help_url = 'https://www.notion.so/help/reference'

header = {'user-agent': UserAgent().edge}
help_page = requests.get(help_url, header).text

bs = BeautifulSoup(help_page, 'html.parser')
div_html = bs.find('div', {
    'class': 'oldGrid_gridContainer__FOosa oldGrid_gridColumns12__u39a_ oldGrid_gridRowGapXsS__vnNNU oldGrid_gridRowGapXlS__zoeuK'})
div_list = div_html.find_all('div')
title_dict = {}
for div in div_list:
    title = div.find('section').find('h2').find('a').text
    title_url = base_url + div.find('section').find('h2').find('a')['href']
    title_dict[f'{title}'] = title_url
content_dict = {}
for title, url in title_dict.items():
    content_dict[title] = {}
    page = requests.get(url, header).text
    content_bs = BeautifulSoup(page, 'html.parser')
    section = content_bs.find('section', {'class': 'helpCenterContentSpacing_contentSpacing__7jwfD'})
    div_list = section.find_all('div', {'class': 'spacing_marginS__EV58C'})
    for div in div_list:
        article_title = div.find('article').find('a')['title']
        article_url = base_url + div.find('article').find('a')['href']
        content_dict[title][article_title] = article_url

for category, article_dict in content_dict.items():
    content_list = [['标题', '内容']]
    for article_title, article_url in article_dict.items():
        article_page = requests.get(article_url, header).text
        article_bs = BeautifulSoup(article_page, 'html.parser')
        article_content = article_bs.find('article', {'class': 'helpArticle_helpArticle__devPW'}).text
        content_list.append([article_title, article_content])
    with open(f'{category}.csv', 'w', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(content_list)
    print(f'{category}爬取完成')
    content_list = []

