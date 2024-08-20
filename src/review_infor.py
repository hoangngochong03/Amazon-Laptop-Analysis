
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
def scroll(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    start=0
    for _ in range(4):
        driver.execute_script(f"window.scrollTo({start}, {start+total_height/5});")
        start+=total_height/5
        time.sleep(1)
def crawl_review(product_id,driver):
    review_data = []
    star_rating=driver.find_element(By.XPATH,'//span[@data-hook="rating-out-of-text"]').text.strip().split(" ")[0]
    review_rating_count=driver.find_element(By.XPATH,'//div[@data-hook="cr-filter-info-review-rating-count"]').text.strip()
    review_count=review_rating_count.split(" ")[3]
    rating_count=review_rating_count.split(" ")[0]
    
    for j in range(2):
        WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.ID,  'a-autoid-3-announce'))).click()
        WebDriverWait(driver,2).until(
            EC.element_to_be_clickable((By.ID,f"sort-order-dropdown_{j}"))
        ).click()
        time.sleep(3)
        for k in range(1,6):

            WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID,  'a-autoid-5-announce'))).click()
            try:
                WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.ID,  f'star-count-dropdown_{k}'))
                        ).click()
            except:
                print(j,k)
            time.sleep(1)
            # check num of review <100 => continue
            num_rv=driver.find_element(By.XPATH,'//div[@data-hook="cr-filter-info-review-rating-count"]').text.strip().split(" ")[3]
            if "," in num_rv:
                num_rv = num_rv.replace(",", "")
            if j==1 and int(num_rv)<100:
                time.sleep(2)
                continue
            for i in range(10):
                # Translate review to English by Amazon
                try:
                    time.sleep(2)
                    translate = driver.find_elements(By.XPATH, '//a[@data-hook="cr-translate-these-reviews-link"] | //input[@data-hook="cr-translate-these-reviews-link"]')
                    translate[0].click()
                    time.sleep(2)
                except:
                    pass
                #Start crawl review
                try:
                    time.sleep(1)
                    driver.execute_script("window.scrollTo(0, 2500);")
                    time.sleep(1)
                    reviews = WebDriverWait(driver, 2).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-hook='review']")))
                    for review in reviews:
                        try:
                            try:
                                title = WebDriverWait(review, 1).until(
                            EC.presence_of_element_located((By.XPATH, ".//a[@data-hook='review-title']"))).text.strip()
                            except:
                                title = WebDriverWait(review, 1).until(
                            EC.presence_of_element_located((By.XPATH, ".//span[@data-hook='review-title']"))).text.strip()
                            try:
                                rating = WebDriverWait(review, 1).until(
                            EC.presence_of_element_located((By.XPATH, ".//i[@data-hook='review-star-rating']/span"))).get_attribute("innerHTML").strip().split(" ")[0]
                            except:
                                rating = WebDriverWait(review, 1).until(
                            EC.presence_of_element_located((By.XPATH, ".//i[@data-hook='cmps-review-star-rating']/span"))).get_attribute("innerHTML").strip().split(" ")[0]
                            body = WebDriverWait(review, 1).until(
                        EC.presence_of_element_located((By.XPATH, ".//span[@data-hook='review-body']/span"))).text.strip()
                            review_data.append([product_id,title, rating, body,review_count,rating_count,star_rating])
                            
                        except Exception as e:
                            continue
                    # click to the next page
                    try:
                        next=WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#cm_cr-pagination_bar > ul > li.a-disabled.a-last")))
                        break
                    except:
                        WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.a-last"))).click()
                except Exception as e:
                    break
    return review_data
