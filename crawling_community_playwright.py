# playwright installation help
# https://brunch.co.kr/@jameshjkang/82

#pip install playwright
#playwright install
#playwright codegen

import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.ppomppu.co.kr/")
    page.get_by_role("link", name="정치자유게시판").click()
    page.get_by_role("cell", name="이미지뻔뻔무쌍 철면피 폐족당 국힘 경선주자론 나빠루가 제격이다").click()
    page.goto("https://www.ppomppu.co.kr/zboard/zboard.php?id=issue")
    page.locator("div").filter(has_text="정치자유게시판 입니다. 자유게시판 진보공감게시판 보수공감게시판 유머/감동 정치글을 포함하여 모든 주제를 자유롭게 공유하는 공간입니다.[정치자유게").nth(3).click()
    page.get_by_role("link", name="이래서 기독이야기가 나옴").click()
    page.get_by_role("link", name="2", exact=True).click()
    page.get_by_role("link", name="쥐새끼 판사 하나가 내란범 똥구멍에 박혀있는듯").click()
    page.get_by_role("link", name="10").click()
    page.get_by_role("link", name="[50억] 내란의힘 '우'진우 - 내란대행의 헌번재판관 지명은 당연한 수순").click()
    page.locator("#bottom-table").get_by_role("link").filter(has_text=re.compile(r"^$")).click()
    page.get_by_role("link", name="내란당에서 대선 후보를 낸다고??").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
