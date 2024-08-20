
import numpy as np
def check_duplicated(data,name):
    if "Link" in data.columns:
        num_dup=data.duplicated(subset="ProductId").sum()
    else:
        num_dup=data.duplicated().sum()
    if num_dup >0:
        print(f"Delete duplicated of {name}:",num_dup)
        if "Link" in data.columns:
            data=data.drop_duplicates(subset="ProductId",keep='first',ignore_index=True)
        else:
            data=data.drop_duplicates(ignore_index=True)
    return data

# remove comma  in price and convert to number
def transform_types_of_product(data):
    # remove comma  in price 
    data["Price"]=data["Price"].astype(str).str.replace(",","")
    # set types 
    data["ProductId"]=data["ProductId"].astype(str)
    data["RatingCount"]=data["RatingCount"].astype(int)
    data["StarRating"]=data["StarRating"].astype(float)
    data["Price"]=data["Price"].astype(float)
    data["Link"]=data["Link"].astype(str)
    return data

#Transform product and review
def transform_columns_of_product_review(product,review):
    review["Rating"]=review["Rating"].astype(int)
    product=product.drop(columns=["StarRating","RatingCount"],axis=1)
    product = product.merge(review[["ProductID",'ReviewCount',"RatingCount","StarRating"]], left_on='ProductId',right_on="ProductID", how='left')
    product=product.drop_duplicates(subset="ProductId",ignore_index=True)
    product.drop("ProductID",inplace=True,axis=1)
    product["ReviewCount"] = product["ReviewCount"].replace(['', ' ', None], 0)
    product["RatingCount"] = product["RatingCount"].replace(['', ' ', None], 0)
    product["StarRating"] = product["StarRating"].replace(['', ' ', None,np.nan], 0)
    product["ReviewCount"]=product["ReviewCount"].astype(str).str.replace(",","")
    product["RatingCount"]=product["RatingCount"].astype(str).str.replace(",","")
    review=review.drop(columns=['ReviewCount',"RatingCount","StarRating"],axis=1)
    return product,review

#Transform product information and product
def transform_columns_of_productinf_product(productinf,product):
    productinf = productinf.merge(product[["ProductId","Price"]],on='ProductId', how='right')
    productinf=productinf.drop_duplicates(ignore_index=True)
    product=product.drop("Price",axis=1)
    return productinf,product
def transform_productinf(productinf):
    # replace charater by space
    productinf['Brand'] = productinf['Brand'].str.upper()
    productinf['Brand'] = productinf['Brand'].str.replace(r'[-_&/]', ' ', regex=True)
    # Add "Inches"
    def add_inches(value):
        if 'Inches' not in value:
            return f"{value} Inches"
        return value
    productinf["ScreenSize"]=productinf["ScreenSize"].map(add_inches)

    productinf["HardDiskSize"]=productinf["HardDiskSize"].str.replace("1 GB","1 TB")
    #Replace Blank by Unknow
    productinf["CPUModel"] = productinf["CPUModel"].replace(['', ' ', None], 'Unknow')
    #Split to multi record if Operating System have multi values
    productinf["OperatingSystem"]=productinf["OperatingSystem"].str.split(", ")
    productinf = productinf.explode('OperatingSystem').reset_index(drop=True)
    productinf = productinf.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return productinf
