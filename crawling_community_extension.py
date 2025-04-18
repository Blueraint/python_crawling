# pip install selenium
# pip install ChromeDriverManager
# pip install bs4
# pip install webdriver_manager
# pip install elements_manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from elements_manager import *
from selenium.webdriver.chrome.service import Service


# driver = webdriver.Chrome(ChromeDriverManager().install())
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)




# to click on the element(자유게시판) found
driver.find_element(By.XPATH,get_xpath(driver,'U_wXMHuKaPsrdUH')).click()

# to click on the element(경호처 폭로 : 국힘갔다가 다시 돌아...) found
driver.find_element(By.XPATH,get_xpath(driver,'btvE_I8FtjjX4is')).click()

# to click on the element([단독]"이완규 함상훈 지명했다"더니...) found
driver.find_element(By.XPATH,get_xpath(driver,'qYh06dCIlBsjVPg')).click()

# to click on the element(2) found
driver.find_element(By.XPATH,get_xpath(driver,'37isAT70n8rwiPU')).click()

# to click on the element(어제 야당VIP 시사회 아이유 퇴근길) found
driver.find_element(By.XPATH,get_xpath(driver,'y4pda0gWtUC138s')).click()

# to click on the element(비왔다고 포사격 무지 하네요..) found
driver.find_element(By.XPATH,get_xpath(driver,'hd_PpPNjsQFMiGa')).click()

# to click on the element(3) found
driver.find_element(By.XPATH,get_xpath(driver,'2owgEq45O3DqPbz')).click()

# to click on the element(넷플릭스 탑텐) found
driver.find_element(By.XPATH,get_xpath(driver,'fyY1s2Ew7s_AjFN')).click()

# to click on the element(10) found
driver.find_element(By.XPATH,get_xpath(driver,'GkUwszueJkxkm8Z')).click()

# to click on the element([50억] 종양일보 안혜리 - 윤석열...) found
driver.find_element(By.XPATH,get_xpath(driver,'DR2MYMreQAgTjEC')).click()

# to click on the element(새롭게 떠오르고 있는 지구 생명의 기...) found
driver.find_element(By.XPATH,get_xpath(driver,'QyPyC7BdGRVKRqS')).click()

# to click on the element found
driver.find_element(By.XPATH,get_xpath(driver,'dYTqlVJVqodKAvK')).click()

# to click on the element(반숙 계란  완숙 보다 비싸네요) found
driver.find_element(By.XPATH,get_xpath(driver,'I_qWLstALiua5H8')).click()

# to click on the element(진짜 ㅈ된거 같다는 요즘 취업시장 ㄷ...) found
driver.find_element(By.XPATH,get_xpath(driver,'AWovrlyRrGsnogR')).click()

