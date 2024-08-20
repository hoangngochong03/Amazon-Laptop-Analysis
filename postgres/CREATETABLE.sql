CREATE TABLE IF NOT EXISTS product (
    productid text PRIMARY KEY,
    link TEXT,
    reviewcount INT,
    ratingcount int,
    starrating DECIMAL(3, 2)
    
);
CREATE TABLE IF NOT EXISTS productdetail (
    id BIGSERIAL PRIMARY KEY,
    productid text ,
    name text,
    brand VARCHAR(100),
    screensize text,
    harddisksize text,
    cpumodel text,
    rammemory text,
    operatingsystem text,
    price DECIMAL(10, 2),
    FOREIGN KEY (productid) REFERENCES product(productid)
);
CREATE TABLE IF NOT EXISTS reviews(
    reviewid BIGSERIAL PRIMARY KEY,
    productid text,
    title text,
    rating int,
    review text,
    score decimal(3,2),
    label text,
    FOREIGN KEY (productid) REFERENCES product(productid)
)
