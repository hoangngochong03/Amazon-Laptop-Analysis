from sqlalchemy import create_engine,text
import pandas as pd


# Connect to PostgreSQL
user = 'postgres'
password = 'password'
host = 'localhost'
port = 'xxxx'
database = 'db'

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

conn=engine.connect()
product_table="product"
productdetail_table="productdetail"
review_table="reviews"

#read file 
products=pd.read_csv("../data/products.csv")
productinf=pd.read_csv("../data/productinf.csv")
review=pd.read_csv("../data/Reviews_sentiment.csv")

products.columns = products.columns.str.lower()
productinf.columns = productinf.columns.str.lower()
review.columns = review.columns.str.lower()
products=products[['productid', 'link', 'reviewcount', 'ratingcount', 'starrating']]
productinf=productinf[['productid', 'name', 'brand', 'screensize', 'harddisksize', 'cpumodel',
       'rammemory', 'operatingsystem', 'price']]
review=review[['productid', 'title', 'rating', 'review', 'score', 'label']]

# insert to table
products.to_sql(product_table,engine,"public",if_exists="append",index=False)
productinf.to_sql('productdetail',engine,"public",if_exists="append",index=False)
review.to_sql('reviews',engine,"public",if_exists="append",index=False)


