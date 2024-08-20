import pandas as pd
from transform_func import check_duplicated,transform_types_of_product,transform_columns_of_product_review,transform_columns_of_productinf_product,transform_productinf
product=pd.read_excel("../data/products.xlsx")
review=pd.read_excel("../data/review.xlsx")
productinf=pd.read_excel("../data/product_inf.xlsx")

#Check duplicated
product=check_duplicated(product,"Product")
review=check_duplicated(review,"Review")
productinf=check_duplicated(productinf,"Product Information")

#Transform type of product
product=transform_types_of_product(product)

#Transform product and review
product,review=transform_columns_of_product_review(product,review)

#Transform product information and product
productinf,product=transform_columns_of_productinf_product(productinf,product)
productinf=transform_productinf(productinf)
#Save file to data
try:
    #product.to_csv("../data/products.csv",index=False)
    productinf.to_csv("../data/productinf.csv",index=False)
    #review.to_csv("../data/reviews.csv",index=False)
    print("Save sucessfully!")
except Exception as e:
    print(f"Error: {e}")