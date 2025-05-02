import requests
from bs4 import BeautifulSoup

###################################################################
# AI 관련 기사 중 제목, 언론사, 링크주소를 크롤링하는 함수
def crawl_titles_presses_links():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'referer': 'https://www.naver.com/',
        'accept-language': 'ko-KR,ko;q=0.9',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    url = 'https://search.naver.com/search.naver?where=news&sm=tab_opt&query=금융'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    print("응답코드:", response.status_code)
    # print("HTML 일부:", soup.prettify()[:500])  # 디버깅용

    titles = []
    presses = []
    links = []
    seen = set()
    
    for item in soup.select('div.sds-comps-full-layout'):
      try:
          # 제목
          title_tag = item.select_one('span.sds-comps-text-type-headline1')
          if not title_tag:
              continue
          title = title_tag.text.strip()

          # 링크
          link_tag = item.select_one('span.sds-comps-profile-info-subtext a[href*="n.news.naver.com"]')
          link = link_tag['href'].strip() if link_tag else "링크 없음"

          # 언론사
          press_tag = item.select_one('a[href*="media.naver.com/press"] > span')
          press = press_tag.text.strip() if press_tag else "언론사 없음"

          # 중복 제거
          if title not in seen:
              seen.add(title)
              titles.append(title)
              links.append(link)
              presses.append(press)

      except Exception as e:
          print("에러:", e)

    print(f"[크롤링된 뉴스 수]: {len(titles)}")
    print(f"[크롤링된 링크 수]: {len(links),links}")
    print(f"[크롤링된 언론사 수]: {len(presses)}")
    print(f"[크롤링된 언론사 목록]: {presses}")

    return titles, presses, links

###################################################################

# 링크에 들어가 기사를 추출하는 함수
def extract_news(link):
  
  headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
  url = link
  response = requests.get(headers=headers, url=url)
  soup = BeautifulSoup(response.text, 'html.parser')
  news = soup.select_one('#dic_area').text
  date = soup.select_one('._ARTICLE_DATE_TIME').attrs['data-date-time']
  print(f"[크롤링 중] 뉴스 링크: {link}")
  response = requests.get(headers=headers, url=link)
  print(f"[응답 코드] {response.status_code}")
  print("[HTML 일부 미리보기]")
  print(response.text[:1000])  # HTML 일부 확인

  return news, date
#################################

#테스트용
#################################
def crawl_news():
  # requests 모듈을 통해서 요청보내고, html 문서받기
  headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
  url = f'https://n.news.naver.com/mnews/article/001/0014400079?sid=101' ## 예시
  response = requests.get(headers=headers, url=url)

  # 파싱하기
  soup = BeautifulSoup(response.text, 'html.parser')

  # 원하는 정보 선택하기
  paragraphs = soup.select_one('._ARTICLE_DATE_TIME').attrs['data-date-time']
  
  news = []
  for paragraph in paragraphs:
    news.append(paragraph.strip())
  news = ' '.join(news)
  return paragraphs
