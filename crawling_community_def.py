#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse, parse_qs, parse_qsl, urlencode, urlunparse

# TODO : define expt-try case
def get_bs(driver : webdriver.Chrome) :
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    
    return bs

## def : 단일 link site 를 이동하는 함수(반복기능) define
def move_url(driver, main_url, sub_url="") :
    tot_url=main_url+sub_url
    print("Move url link : " + tot_url)
    driver.get(tot_url)
    driver.implicitly_wait(3)

    return tot_url

# board page 변경
def get_board_url_page(url : str, pagenum : int) :
    url_parse=urlparse(url)
    qs = dict(parse_qsl(url_parse.query))
    # parse_qsl의 결과를 dictionary로 캐스팅
    qs['page'] = str(pagenum)
    # 수정 작업
    url_parse = url_parse._replace(query=urlencode(qs))
    # dictionary로 되어 있는 query string을 urlencode에 넘겨 문자열화하고 replace
    new_url = urlunparse(url_parse)

    return new_url


# 특정 페이지의 bs4 Object 를 가지고 특정 DOM요소를 잡아 링크를 검색하는 기능 define
def get_bs_href(driver, attr : dict) :
    bs= get_bs(driver)
    # query string 포함된 href 추출
    href=bs.find_all("a",attrs=attr)[0]['href']
    print("href inner link in BeautifulSoup parser : "+ href)

    return href


# href link 안의 게시물 번호를 추출
def get_board_no(href) :
    # href 에서 querystring 추출
    parser=urlparse(href)
    print("urlParser : " + parser)

    # parse_qs : str 형태의 url parser.query 를 dict 형태로 반환
    # parse_qsl : tuple 형태로 변환
    url_board_no_str = parse_qs(parser.query)['no'][0]

    return url_board_no_str


# 게시물 bs4 로 crawling
def get_board_container_info(driver) :
    bs = get_bs(driver)
    
    data = bs.find("div","container")
    
    return data


# 게시물 bs4 로 특정 attr의 DOM 요소 crawling
def get_board_info(driver, element : str, attr : dict) :
    bs= get_bs(driver)
    data = bs.find(element, attr)
    
    return data

# 게시물 bs4 로 특정 attr의 DOM 요소 crawling
def get_all_board_info(driver, element : str, attr : dict) :
    bs= get_bs(driver)
    data = bs.find_all(element, attr)
    
    return data

# href 추출 후 게시물로 이동하여 article 및 url link 추출 기능 (define)
# parameters : (dataframe, article no)
def get_article_info(driver, url, href) :
    # https://ppomppu.co.kr/zboard/{href} 방식으로 view.php 를 따로 보여주는 방식임
    # href 추출하여 sub menu url 을 생성하고 이동
    # 위와 비슷한 로직을 이용하므로 func 을 만들어 리팩토링한다
    move_url(driver, url, href)

    if '404' in driver.title :
        driver.back()
        move_url(driver, site_url, href)

    # function 정의하여 반복을 피한다(var html 과 동일)
    data = get_board_container_info(driver)

    # article
    try : 
        board_article=data.find_all("table")[2]
        board_article_text=board_article.text
    except :
        board_article_text=""

    # board main link url
    try :
        board_main_link_url=board_article.find("div", attrs={'class':'scrap_bx_txt'}).text
    except :
        board_main_link_url=""
    
    result = {"url":board_main_link_url, "article" : board_article_text}    
    print(result)

    return result


# 특정 page (driver 에 의해 접근된) 에 대해 한 html 내의 게시물을 가져오는 함수 정의
# Parameter : 게시물 dataframe, bs4.tag
def get_board_data(dataFrame, bs) :
    df = dataFrame.copy()

    # Class : baseList-title 로 가올 경우 공지, 알림 등을 모두 가져오는 문제 발생
    bs_href_list = bs.find_all("a",attrs={'class':'baseList-title'})
    for data in bs_href_list :
        try :
            # query string 포함된 href 추출
            data_href=data['href']
            print(data_href)

            # href 에서 querystring 추출
            parser=urlparse(data_href)

            # parse_qs : str 형태의 url parser.query 를 dict 형태로 반환
            # parse_qsl : tuple 형태로 변환
            url_board_no = parse_qs(parser.query)['no'][0]

            # 게시물 List 안의 href 로 이동하여 세부 url link 및 acticle text 가져오기
            zboard_url = "https://ppomppu.co.kr/zboard/"
            zboard_result = get_article_info(driver, zboard_url, data_href)

            # df_board(sub_board) DataFrame 에 새로운 column 으로 link url 및 article 추가

            df.loc[df_board[0]==url_board_no,'link_url']=zboard_result['url']
            df.loc[df_board[0]==url_board_no,'article']=zboard_result['article']

            # df col 에 url_link 및 article 추가 완료

        except :
            # error 발생한 경우 다음 a tag object 읽어서 추출
            continue

    print(df.shape)

    return df


# Get Board article data from Start Page number to End Page number
def get_tot_board_data(dataFrame, startPage : int, endPage : int) :
    df_result = pd.DataFrame([])
    
    if startPage < endPage :
        Exception("시작 페이지는 끝 페이지보다 작거나 같아야 합니다.")

    for i in range(startPage, endPage + 1) :
        page_url = get_board_url_page(submenu_url, i)

        df_page_result=get_board_data(dataFrame, tbl_data)
        # Result dataframe 과 새로 page 에서 추출한 dataframe 을 합친다
        df_result=pd.concat([df_page_result, df_result], axis=0)

    return df_result


# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver = webdriver.Chrome(ChromeDriverManager().install())
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)



# move ppomppu site
site_url = "https://ppomppu.co.kr"
move_url(driver, site_url,)

# find 1st class(main) menu in community index site
# html = driver.page_source
# bs = BeautifulSoup(html, "html.parser")
# menu_data = bs.find_all("a",attrs={'class':'menu'})
menu_data = get_all_board_info(driver, "a", {'class':'menu'})
print(menu_data[0])

# href 추출하여 sub menu url 을 생성하고 이동
submenu_url = move_url(driver, site_url, menu_data[0]['href']) 


# 단위 sub-main 메뉴 내에서 게시물 리스트 -> 게시물 추출하는 기능 (define)
tbl_data = get_board_container_info(driver)
# pip install lxml
df = pd.read_html(str(tbl_data.find("table",attrs={'id':'revolution_main_table'})))

# 알림, 공지 등 string data는 to_numeric 에 의해 NaN 값으로 변경
# 변경 이후 결측치 제거하고 순수하게 올라온 게시물 글만 DataFrame화
df_board = df[0][(df[0][0].apply(pd.to_numeric, errors='coerce').isnull() == False)]

# df_board 에 게시글의 link_url 및 article 을 추가하기 위해 빈값(Null, NaN)의 컬럼 추가
df_board['link_url']=np.nan
df_board['article']=np.nan
print(df_board.head())



df_result = get_tot_board_data(df_board, 1,2)
print(df_result)
print(df_result.shape)

# Rename column
df_result.rename(columns={0: '번호1', 1 : '번호2', 2: '제목', 3 : '글쓴이', 4 : '글쓴이2', 5 : '등록시간', 6:'수정시간', 7:'추천-비추천1', 8:'추천-비추천2', 9:'조회1', 10:'조회2'}, inplace=True)

# export csv file
df_result.to_csv('crawling.csv', index=False, sep='|')

