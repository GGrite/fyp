from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd

def crawling():
    url_list = driver.find_elements(By.CLASS_NAME, 'casename')

    for url in url_list:
        url.click()
        window_after = driver.window_handles[-1] # last opened
        driver.switch_to.window(window_after) 
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'main-sentence')))  # cn-case-title
        
        # crawling
        title = driver.find_element("xpath", '//*[@id="cn-case"]/div[1]/div[1]/div[1]/h1').get_attribute("innerHTML")
        title = title.strip()

        if "모욕" not in title:
            return
        # elif "대법원" in title:
        #     case_type = "대법원"
        # elif "지방법원" in title:
        #     case_type = "지방법원"
        # elif "헌법재판소" in title:
        #     case_type = '헌법재판소'
        # else:
        #     case_type = '기타'
        case_type = "지방법원"

        penalty =  driver.find_element("xpath", '//*[@class="title"][contains(text(),"주")]/following-sibling::p').get_attribute("innerHTML")
        penalty = penalty.strip()

        reason=""
        for r in driver.find_elements("xpath","//div[@class='reason']//p"):
            reason += r.get_attribute("textContent") + '\n'  # innerHTML, innerText
        reason = reason.strip()

        full_text = ""
        for i in driver.find_elements(By.CLASS_NAME,"main-sentence"):
            full_text += i.get_attribute("textContent") + '\n'
        full_text = full_text.strip()

        data_frame.append([title, case_type, penalty,reason,full_text])

        # next url
        driver.close()
        driver.switch_to.window(window_before)


if __name__ == '__main__':
    driver = webdriver.Chrome('./chromedriver')
    wait = WebDriverWait(driver, 10)

    driver.get("https://casenote.kr/search/?q=%EB%AA%A8%EC%9A%95")
    # https://casenote.kr/search/?q=%EB%AA%A8%EC%9A%95+%EB%B2%94%EC%A3%84%EC%82%AC%EC%8B%A4&sort=0&period=0&court=2&page=1
    window_before = driver.window_handles[-1] 

    data_frame = []
    crawling()

    while True:        
        try:
            next_page = driver.find_element(By.CLASS_NAME,'btn-next') # .isEmpty()
            next_page.click()

            window_before = driver.window_handles[-1] 
            driver.switch_to.window(window_before) 
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'searched-item')))
            
            crawling()
        except:
            break
    
    # dataframe
    column_names = ['사건번호','법원 종류','주문','이유','판결문']  
    df = pd.DataFrame(data_frame, columns=column_names)
    filename = "case_data.csv"
    df.to_csv(filename, index=False,encoding="utf-8-sig")


def after_crawling():
    df1 = pd.read_csv('case.csv')
    df2 = pd.read_csv('case_2.csv')
    df1.drop(columns=df1.columns[0], axis=1, inplace=True)
    df2.drop(columns=df2.columns[0], axis=1, inplace=True)
    df_final = pd.concat([df1,df2], ignore_index=True)
    df_final = df_final.drop_duplicates(keep = 'first')

    print(df_final.reason.str.split(pat='"', expand=True) ) # .str[4])  # split by " "