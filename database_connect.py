import pandas as pd
import psycopg2
from sqlalchemy import create_engine

user = 'postgres'
password = '12345'
host = 'localhost'
port = '5432'
database = 'gyk1'

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

def cutomer_segmentation():
    query ="""
select c.customer_id, 
count(o.order_id) as total_orders, 
sum(od.quantity * od.unit_price) as total_spent,
avg(od.quantity * od.unit_price)as avg_order_value
from customers c inner join orders o
on c.customer_id = o.customer_id
inner join order_details od
on o.order_id = od.order_id
group by c.customer_id
having count(o.order_id)>0
"""
    df = pd.read_sql_query(query, engine) 
    return df

def product_segmentation():
    query ="""
select p.product_id, avg(od.unit_price) as avg_unit_price , count(*) as sales_frequency,
avg(od.quantity) as avg_quantity,
count(distinct o.customer_id) as unique_customer_count
from products as p inner join order_details as od
on p.product_id = od.product_id
inner join orders as o
on od.order_id = o.order_id
group by p.product_id
order by p.product_id
"""
    df = pd.read_sql_query(query, engine) 
    return df

def supplier_segmentation():
    query ="""
select s.supplier_id,
count(distinct p.product_id) as num_of_products_supplied,
sum(od.quantity * od.unit_price) as total_spent,
avg(od.quantity * od.unit_price) as avg_spent,
count(distinct o.customer_id) as num_of_customer
from suppliers as s inner join products as p
on s.supplier_id = p.supplier_id 
inner join order_details as od on od.product_id =p.product_id
inner join orders as o on od.order_id = o.order_id
group by s.supplier_id
order by s.supplier_id

"""
    df = pd.read_sql_query(query, engine) 
    return df

def country_segmentation():
    query ="""
select c.country, count(distinct od.order_id) as total_order_count,
avg(od.quantity * od.unit_price) avg_spent,
sum(od.quantity) / count(distinct od.order_id) AS avg_items_per_order
from customers as c
inner join orders as o on o.customer_id = c.customer_id
inner join order_details as od on od.order_id = o.order_id
group by c.country
order by c.country
"""
    df = pd.read_sql_query(query, engine) 
    return df


if __name__ ==  '__main__':

    data_frames = [cutomer_segmentation(),product_segmentation(),
                   supplier_segmentation(),country_segmentation()]

    for df in data_frames:
        print(df)
