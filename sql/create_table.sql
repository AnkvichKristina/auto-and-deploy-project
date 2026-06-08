 CREATE TABLE IF NOT EXISTS sales (
        id serial PRIMARY KEY,
    	doc_id varchar(10) NOT NULL,
    	item varchar(30) NOT NULL,
    	category varchar(30) NOT NULL,
    	amount int4 NOT NULL,
    	price numeric(10, 2) NOT NULL,
    	discount numeric(10, 2) NOT NULL,
        shop_num int4 NOT NULL,
    	cash_num int4 NOT NULL
        )