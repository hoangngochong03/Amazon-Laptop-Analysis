#DayCrawl : 07/08/2024
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver.common.by import By
from product_infor import scroll,Crawl_product
import os
df1=pd.DataFrame(columns=["ProductId","ReviewCount","StarRating","Price","Link"])
df2=pd.DataFrame(columns=["ProductId","Name","Brand","ScreenSize","HardDiskSize","CPUModel","RamMemory","OperatingSystem"])

# create file 
file1 = "../data/products.xlsx"
file2 = "../data/product_inf.xlsx"
if not os.path.exists(file1):
    df1.to_excel(file1, index=False)
    print(f"{file1} created.")
if not os.path.exists(file2):
    df2.to_excel(file2, index=False)
    print(f"{file2} created.")

# Crawl laptop information
url="https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fyour-orders%2Forders%3F_encoding%3DUTF8%26%252AVersion%252A%3D1%26%252Aentries%252A%3D0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_retail_yourorders_us&openid.mode=checkid_setup&language=en_US&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
url_laptop="https://www.amazon.com/hz/mobile/mission?p=5tIbRdXgJoWoF2wixImDmhE1TdQXbWE47QIiMmlwoY7I9wPj0DMC41ubDkhf%2BzeblbIEVsX%2BZJ9ru%2FonpWzsF3zs5n9MLpYavcC3IeB2R5uhUT9ctrX1vxdWrxKfHxm5x0QeollidBd9gNlJBWNXWKLkGi1JQIdQnrz6dfZpkktwfjny5SUBNJS2ZOuFzf1iTk%2BxkHhHN2MET4m6dI5jbVMT97iXGTYStagz4CPyPQCcKkd6XEXNyNR1QHZvT9W%2F7XY%2FazP8rTBkRB4KTFhZbZXr6UEvREYWnNwLjwRK4%2FHoxsGE%2FO46MB9mbpuDGJ%2BOjp4isNvtbgTUUxH776KbdJZ4lR4JgclJTOxLoiwWz27CawrShicEq0wEuXFjb3N28dj0nrWXHEjdL%2FFd28Lngg41JIqzFZnnhdx9F9kaST4PZP98Oo1jag%3D%3D&ref_=nb_sb_ss_di_ci_mcx_mi_ci-mcx-ksf1_0&crid=3C466D3YTK0SA"

# Initialize Chrome
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver=webdriver.Chrome(options=chrome_options)
driver.get(url)
time.sleep(3)
#Login
email=WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.ID,"ap_email"))
)
email.send_keys("account") #replace with account of amazon
email.send_keys(Keys.TAB)
password=WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.ID,"ap_password"))
)
password.send_keys("password") #replace with password of amazon
password.send_keys(Keys.ENTER)
time.sleep(10)
time.sleep(3)
#Remember the original tab
driver.get(url_laptop)
original_window = driver.current_window_handle

# crawl laptop information by each brand
#brand_lst=["HP","Dell","ASUS","MSI","Apple","Lenovo","Acer","LG","Samsung"]
brand_lst=["Alienware","Microsoft","Gateway","Razer"]
driver.execute_script("window.scrollTo(0, 300);")
for b in brand_lst:
    time.sleep(5)
    print(b)
    WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.ID,'chevron-Brand'))
    ).click()
    time.sleep(3)
    #see more 
    WebDriverWait(driver,5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="attribute-modal-Brand"]/div/div[3]/div[3]/div[3]/div/a/span[2]/span[1]'))
    ).click()
    time.sleep(1)
    brand_detail=WebDriverWait(driver,5).until(
        EC.element_to_be_clickable((By.XPATH,f'//div[@data-attribute-value="{b}"]'))
    )
    brand_detail.click()
    time.sleep(2)
    WebDriverWait(driver,5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="attribute-modal-Brand"]/div/div[3]/div[3]/div[4]/button'))
    ).click()
    time.sleep(5)
    scroll(driver)
    products_lst=WebDriverWait(driver,5).until(
    EC.presence_of_all_elements_located((By.XPATH,'//div[@data-wdg-category="Default"]'))
    )
    Crawl_product(driver,products_lst,original_window)
    driver.switch_to.window(original_window)
    driver.execute_script("window.scrollTo(0, 300);")
    time.sleep(1)
    WebDriverWait(driver,5).until(
    EC.element_to_be_clickable((By.ID,'chevron-Brand'))).click()
    brand_detail=WebDriverWait(driver,5).until(
    EC.element_to_be_clickable((By.XPATH,f'//div[@data-attribute-value="{b}"]'))
    )
    brand_detail.click()
driver.quit()