-- trigger insert product table
CREATE OR REPLACE FUNCTION product_duplicate_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Kiểm tra nếu sản phẩm đã tồn tại (giả sử tên sản phẩm là duy nhất)
    IF EXISTS (SELECT 1 FROM product WHERE productid = NEW.productid) THEN
        -- Nếu sản phẩm đã tồn tại, bỏ qua việc chèn
        RETURN NULL;
    ELSE
        -- Nếu sản phẩm chưa tồn tại, thực hiện chèn như bình thường
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_duplicate_insert
BEFORE INSERT ON product
FOR EACH ROW
EXECUTE FUNCTION product_duplicate_insert();

-- trigger insert productdetail table
CREATE OR REPLACE FUNCTION check_productdetail_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Kiểm tra nếu productid có tồn tại trong bảng product
    IF NOT EXISTS (SELECT 1 FROM product WHERE productid = NEW.productid) THEN
        -- Nếu productid không tồn tại, thông báo lỗi và hủy bỏ việc chèn
        RAISE EXCEPTION 'Productid % does not exist in product table', NEW.productid;
    END IF;
    -- Nếu productid tồn tại, cho phép chèn
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER productdetail_insert
BEFORE INSERT ON productdetail
FOR EACH ROW
EXECUTE FUNCTION check_productdetail_insert();




