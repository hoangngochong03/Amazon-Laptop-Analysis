-- Number of product by brand
select brand,count(id) as num_of_product from productdetail
group by brand
order by count(id) desc;

-- Number of Review by brand 
select brand,COUNT(DISTINCT r.reviewid) as num_of_review from productdetail p join reviews r
	on p.productid = r.productid
group by brand
order by count(reviewid) desc;

-- top 10 product with the highest number of review
select p.productid,d.name,p.reviewcount 
from 
	product p join productdetail d on p.productid=d.productid
order by p.reviewcount desc
limit 10;

--  Total, Average rating by brand
select brand, Avg(starrating) as avgrating, count(starrating) as totalrating from
product join productdetail on product.productid=productdetail.productid
group by brand
order by brand;

-- Avg price by brand
select brand, round(avg(price),0) as avgprice from productdetail 
group by brand
order by avg(price) desc;

-- Top 10 product with the highest price
select name,price from productdetail 
order by price  desc
limit 10

-- count number of product by price range
SELECT 
    CASE
        WHEN p.price < 500 THEN 'Under 500'
        WHEN p.price BETWEEN 500 AND 1000 THEN '500 - 1000'
        WHEN p.price BETWEEN 1000 AND 1500 THEN '1000 - 1500'
		WHEN p.price BETWEEN 1500 AND 2000 THEN '1500 - 2000'
		ELSE 'Over 2000'
    END AS price_range,
    COUNT(p.productid) AS num_of_products
FROM productdetail p
GROUP BY price_range
ORDER BY COUNT(p.productid) desc;

-- Allocation of rating review
select  
	CASE
		WHEN r.rating <=2 then '1 - 2 star'
		WHEN r.rating >2 and r.rating<=3 then '3 star '
		WHEN r.rating >=3 then '4 - 5 star'
	END as rating_range,
count(rating) as numofrating
from reviews r
group by rating_range
order by count(rating)

-- Allocation of Review Label
select label,count(reviewid) as quantity from reviews
group by label
order by label

