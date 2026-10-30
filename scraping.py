import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

url = 'https://www.musashino-u.ac.jp'
domain = urlparse(url).netloc

urls_to_visit = [url] 
visited_urls = set()
result_dict = {}

while urls_to_visit:
  current_url = urls_to_visit.pop(0)

  if current_url in visited_urls:
    continue
  visited_urls.add(current_url)

  try:
    
    res = requests.get(current_url, timeout=5)


    if 'text/html' not in res.headers.get('Content-Type', ''):
      continue

    html_soup = BeautifulSoup(res.content, 'html.parser')

    
    soup_title = (
        html_soup.title.text.strip() if html_soup.title else 'タイトルなし'
    )
 
    result_dict[current_url] = soup_title
    print(f'取得: {current_url} -> {soup_title}')

    for a_tag in html_soup.find_all('a', href=True):
      full_url = urljoin(current_url, a_tag['href']).split('#')[0]
      if (
          urlparse(full_url).netloc == domain
          and full_url not in visited_urls
      ):
        urls_to_visit.append(full_url)

    time.sleep(1)

  except Exception as e:
    print(f'エラー: {e}')

with open('musashino_homepages.csv', 'w', encoding='utf-8-sig') as f:
  f.write('URL,Title\n')
  for page_url, page_title in result_dict.items():
    clean_title = (
        page_title.replace(',', '、').replace('\n', ' ').replace('\r', '')
    )
    f.write(f'{page_url},{clean_title}\n')
