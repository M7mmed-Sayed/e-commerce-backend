# E-commerce-backend
Django backend for Online Marketplace Backend (E-commerce System)  project

This project is built using Django REST Framework to provide the backend API for E-Commerce project.

Goal: Build a backend system for an online marketplace that supports users, products, orders, payments, and reviews.

# setup
#### 1.  create a new directory
#### 2.  change to this directory
#### 3.  clone  this Repo to the current directory
- `git clone https://github.com/M7mmed-Sayed/e-commerce-backend.git `

#### 4. set up a virtual environment and activate it at Windows open ``` terminal ``` and write the following commands:
1. `python -m pip install virtualenv`
2. `python -m virtualenv venv`
3. `venv\scripts\activate`
4. `pip3 install -r requirements.txt`  to install required packages 

 #### 5. migrate database i'm using Mysql you can change as You like:
 -  `py manage.py migrate`
 #### 6. Run the local server:
 - `py manage.py runserver 8000`

# **Features**

   - ## user API 
       - `/account/register/` POST register / create new user
       - `/account/login/` POST login
       - `/account/logout/` POST logout
       - `/account/` GET the current Autherized user data
       - `/account/update/{abc}` PUT update username data if it's Autherized and the curent user username is `abc`
   - ## categories API 
       - `/products/category/` Post action only admins or employee can create  category
       - `/products/category/` GET action any one can retrieve list categories
       - `/products/category/id` GET action any one can retrieve  category by id
       - `/products/category/id` PUT Action only admins or employee can Edit category by id
       - `/products/category/id` DELETE Action only admins or employee can Destroy category by id
   - ## Products API 
        - `/products/` Post action only sellers can Add Product
        - `/products/` GET action any one can retrieve list products
        - `/products/id` GET action any one can retrieve a product by id
        - `/products/id` PUT action only owner for the product can edit  by id
        - `/products/id` DELETE action only owner for the product can edit  by id
   - ## Cart Item API 
        - `/cart/item/product_id` POST add product_id to the cart
        - `/cart/item/product_id` Get Cart-item by product_id from the cart
        - `/cart/item/` Get Cart-items by  from the cart
        - `/cart/item/product_id` PUT edit the quantity for the current-item `product` 
        - `/cart/item/product_id` DELETE the cart-item  by product_id
   - ## Order API 
        - `/cart/checkout/` POST take the items form the cart and create an order
        - `/cart/orders/` GET action  list of orders
        - `/cart/orders/id` GET action   retrieve a order by id if he is autherized for that  or he is admin
        - `/cart/orders/id` PUT action only owner for the product can edit  by id and edit order statue
        



# **Contact Information:**

For any inquiries or collaboration opportunities, you can reach out to me:

- **LinkedIn**: [LinkedIn Profile](https://www.linkedin.com/in/m7mmed-sayed/)
- **Email**: mohamedsayed1167@gmail.com
