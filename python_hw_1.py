# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
# %%
## https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page=1&divpage=100

# %%
## def : 단일 link site 를 이동하는 함수(반복기능) define
def get_board_response(url, pagenum) :
    # pagenum 은 1 보다 커야 합니다
    if pagenum < 1 :
        print("페이지 번호는 1보다 크거나 같아야 합니다")
        # 빈 값을 반환한다
        return

    ## urlparse 라는 library를 이용하면 더 쉽게 문장을 만들 수 있습니다
    ## 특정  page로 가는 url String 을 만듭니다
    request_url = url + '&page = ' + str(pagenum)
    print(f"요청 게시판 URL 주소 : {request_url}")

    # 요청 응답
    response = requests.get(url)

    # 응닶값(response) 확인
    # 200 : 정상, 403 : 권한 없음 등, 404 : 페이지 없음(주소 잘못됨), 500 : 서버 쪽 에러로 페이지 못가져옴
    print(f"요청 응답값 : {response.status_code}")

    # 응답값을 반환합니다
    return response

def get_board_list(pagenum) :
    site_html = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"

    html = get_board_response(site_html,pagenum)


    # %%
    bs = BeautifulSoup(html.text, "html.parser")

    # %%
    # 전체 html 중 게시판에 해당하는 부분을 개발자 도구로 확인 후 TABLE의 각 line 부분을 가져옵니다
    data = bs.find('tr', attrs={'class':'baseList bbs_new1'})

    # %%
    # 위에서 가져온 1줄의 데이터 중 number 를 가져옵니다
    board_number=data.find('td', attrs={'class','baseList-numb'}).text

    # %%
    # 위에서 가져온 1줄의 데이터 중 세부 게시물의 주소를 를 가져옵니다
    article_url=data.find('a', attrs={'class','baseList-title'})['href']

    # %%
    # 위에서 가져온 1줄의 데이터 중 세부 게시물의 제목을 가져옵니다
    title=data.find('a', attrs={'class','baseList-title'}).text

    # %%
    list = []

    # %%
    # 이를 응용해서 테이블의 모든 줄(tr)을 find_all 로 가져와서 for 문으로 loop 를 돌면서 위의 텍스트 등 추출 작업을 진행합니다 
    for tr in bs.find_all('tr', attrs={'class':'baseList bbs_new1'}) :
        # 게시물 번호, url, 제목 추출
        board_number=tr.find('td', attrs={'class','baseList-numb'}).text
        article_url=tr.find('a', attrs={'class','baseList-title'})['href']
        title=tr.find('a', attrs={'class','baseList-title'}).text

        # 각 데이터를 dictionary 에 넣어줍니다
        data_dict= {'번호' : board_number, '링크' : article_url, '제목' : title}
        
        list.append(data_dict)

    return list

start_pagenum=input("Start Page Number : ")
end_pagenum=input("End Page Number : ")

result_list = []

for i in range(int(start_pagenum), int(end_pagenum)+1) :
    result_list.extend(get_board_list(i))


# %%
# 모든 리스트 취합 이후에 dataFrame 으로 변환(after N page recursive)
df = pd.DataFrame(result_list)

# %%
# 사이트 추출
df['사이트']=df['제목'].str.extract(r'\[([^\]]+)\]')


# 파일로 추출, 경로 지정
export_path = "./data/"
export_name="mydata.txt"

# 없으면 디렉토리 생성
try:
    if not os.path.exists(export_path):
        os.makedirs(export_path)
except OSError:
    print("Error: Failed to create the directory.")

# csv 로 파일 export
df.to_csv(export_path+export_name, index=False, sep='|')

# %%
