from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pandas as pd
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os
from review_infor import crawl_review,scroll

#take product information
df_product=pd.read_excel("../data/products.xlsx")
reviewed=pd.read_excel("../data/review.xlsx")
id_unique=reviewed["ProductID"].unique()
id_norv=pd.read_excel("../data/ProductNOReview.xlsx")["ProductId"]
#initialize and login
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver=webdriver.Chrome(options=chrome_options)

url="https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fyour-orders%2Forders%3F_encoding%3DUTF8%26%252AVersion%252A%3D1%26%252Aentries%252A%3D0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_retail_yourorders_us&openid.mode=checkid_setup&language=en_US&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
driver.get(url)

email=WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.ID,"ap_email"))
)
email.send_keys("account")  #replace with account of amazon
email.send_keys(Keys.TAB)
password=WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.ID,"ap_password")) 
)
password.send_keys("password")  #replace with password of amazon
password.send_keys(Keys.ENTER)
time.sleep(2)
# Crawl  Reviews 
for product_id in df_product["ProductId"]:
    if product_id in id_unique or product_id in id_norv:
        continue
    elif int(df_product.loc[df_product['ProductId'] ==product_id, 'ReviewCount'].values[0])==0:
        continue
    print(product_id)
    reviews=[]
    link_ref = df_product.loc[df_product['ProductId'] == product_id, 'Link'].values[0]
    driver.get(link_ref)
    time.sleep(2)
    scroll(driver)
    try:
        driver.get(WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//a[@data-hook='see-all-reviews-link-foot']"))
        ).get_attribute("href"))
    except:
        norv=pd.DataFrame([product_id],columns=["ProductId"])
        if os.path.exists("../data/ProductNOReview.xlsx"):
            tmp=pd.read_excel("../data/ProductNOReview.xlsx")
            tmp=pd.concat([tmp,norv],ignore_index=True)
            tmp.to_excel("../data/ProductNOReview.xlsx",index=False)
        continue
    reviews.extend(crawl_review(product_id,driver))
    #save Reviews to file xlsx
    data=pd.DataFrame(reviews,columns=["ProductID","Title", "Rating", "Review","ReviewCount","RatingCount","StarRating"])
    data.drop_duplicates(inplace=True)
    if os.path.exists("../data/review.xlsx"):
        tmp=pd.read_excel("../data/review.xlsx")
        tmp=pd.concat([tmp,data],ignore_index=True)
        tmp.to_excel("../data/review.xlsx",index=False)
    else:
        data.to_excel("../data/review.xlsx",index=False)