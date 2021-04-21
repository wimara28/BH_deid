import pandas as pd
from selenium import webdriver 

url = "https://koreanname.me/" 
driverPath = "{DRIVER PATH}/chromedriver.exe" # Chrome Driver path 
driver = webdriver.Chrome(driverPath) # Open Chrome 
driver.get(url)


last_height = driver.execute_script("return document.body.scrollHeight")
while True: 
    # Scroll 4 times 
    for i in range(4): 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Click 더보기
    driver.find_element_by_xpath('/html/body/div/section/section/main/div/div/div[2]/button').click() 
    
    # End
    new_height = driver.execute_script("return document.body.scrollHeight") 
    if new_height == last_height: 
        break 
    last_height = new_height



names_m = driver.find_element_by_xpath('//*[@id="__next"]/section/section/main/div/div/div[2]/div[5]/div[1]/div/div/div/div/div/div/table/tbody')
names_f = driver.find_element_by_xpath('/html/body/div/section/section/main/div/div/div[2]/div[5]/div[2]/div/div/div/div/div/div/table/tbody')

names_m = names_m.text.split('\n') #['민준 1 3245', '민서 2 44', ...]
names_f = names_f.text.split('\n')

for i in range(len(names_m)):
    names_m[i] = names_m[i].split(' ') #[['민준', '1', '3245'], ['민서', '2', '44'], ...]
for i in range(len(names_f)):
    names_f[i] = names_f[i].split(' ')


m_df = pd.DataFrame(names_m)
f_df = pd.DataFrame(names_f)

m_df.to_csv('names_m.csv', encoding='utf-8-sig', index=False)
f_df.to_csv('names_f.csv', encoding='utf-8-sig', index=False)