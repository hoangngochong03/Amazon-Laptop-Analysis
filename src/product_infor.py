from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
def scroll(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    start=0
    for _ in range(10):
        driver.execute_script(f"window.scrollTo({start}, {start+total_height/5});")
        start+=total_height/5
        time.sleep(1)
def products(inf):
    try:
        product_id=inf.get_attribute("data-asin")
    except:
        return []
    try:
        review_count=inf.get_attribute("data-review-count")
    except:
        review_count=-1
    try:
        star_rating=inf.get_attribute("data-review-star-count")
    except:
        star_rating=-1
    try:
        price=inf.find_element(By.XPATH,'.//span[@class="a-price"]').text.replace('\n', '.')[1:]
        link=inf.find_element(By.XPATH,f'//a[@data-asin="{product_id}"]').get_attribute("href")
        return [product_id,review_count,star_rating,price,link]
    except:
        return []
    
    
def product_detail(driver,id):
    detail_list=["Brand","Screen Size","Hard Disk Size","CPU Model","Ram Memory Installed Size","Operating System"]
    lst=[id]
    lst.append(driver.find_element(By.XPATH,'//*[@id="productTitle"]').text)
    table_details=driver.find_element(By.XPATH,'//table[contains(@class,"a-normal") and contains(@class,"a-spacing-micro")]')
    tr_tag=table_details.find_elements(By.XPATH,'//tr[contains(@class,"a-spacing-small")]')
    detail_col={}
    for each_tr in tr_tag:
        detail_col[each_tr.find_element(By.XPATH, './/td[contains(@class, "a-span3")]').text.strip()]=each_tr
    for dt in detail_list:
        if dt in detail_col.keys():
            detail_name=detail_col[dt].find_element(By.XPATH, './/td[contains(@class, "a-span9")]')
            lst.append(detail_name.text)
        else:
            lst.append("Unknow")
    return lst
def Crawl_product(driver,products_lst,original_window):
    product_list=[]
    product_inf_list=[]
    product_file=pd.read_excel("../data/products.xlsx")
    product_inf_file=pd.read_excel("../data/product_inf.xlsx")
    for inf in products_lst:
        product=products(inf)
        if not product:
            continue
        link=product[-1]
        id=product[0]
        driver.execute_script("window.open(arguments[0]);",link)
        new_tab_handle = driver.window_handles[1] 
        driver.switch_to.window(new_tab_handle)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,500);")
        try:
            WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.ID,"poToggleButton"))
            ).find_element(By.XPATH,".//span[contains(@class,a-expander-prompt)]").click()
        except:
            continue
        product_list.append(product)
        product_inf=product_detail(driver,id)
        product_inf_list.append(product_inf)
        time.sleep(1)
        driver.close()
        driver.switch_to.window(original_window)
        time.sleep(1)
    df_product=pd.DataFrame(product_list,columns=["ProductId","ReviewCount","StarRating","Price","Link"])
    df_product_inf=pd.DataFrame(product_inf_list,columns=["ProductId","Name","Brand","ScreenSize","HardDiskSize","CPUModel","RamMemory","OperatingSystem"])
    product_file=pd.concat([product_file,df_product],ignore_index=True)
    product_inf_file=pd.concat([product_inf_file,df_product_inf],ignore_index=True)
    product_inf_file.to_excel("../data/product_inf.xlsx",index=False)
    product_file.to_excel("../data/products.xlsx",index=False)