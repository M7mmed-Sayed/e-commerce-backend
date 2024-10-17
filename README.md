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
### 5. Create stripe Payment GetWay
- Create Stripe  Account 
- Get your  STRIPE_SECRET_KEY & STRIPE_PUBLISHABLE_KEY for `test_mode`
- Create `.env` file separates your secrets from code and add `.env` to `.gitignore` file
- set `STRIPE_SECRET_KEY= "sk_test_5.................."`
- set `STRIPE_PUBLISHABLE_KEY= "pk_test_5_............"`
- 
 #### 6. migrate database i'm using Mysql you can change as You like:
 -  `py manage.py migrate`
 #### 7. Run the local server:
 - `py manage.py runserver 8000`

# **Features**

   - ## user API 
       - `/account/register/` POST register / create new user
       - `/account/login/` POST login
       - `/account/logout/` POST logout
       - `/account/` GET the current Authorized user data
       - `/account/update/{abc}` PUT update username data if it's Authorized and the current user username is `abc`
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
        - `/cart/orders/` GET action  list of orders
        - `/cart/orders/id` GET action   retrieve an order by id if he is authorized for that, or he is admin
        - `/cart/orders/id` PUT action only owner for the product can edit  by id and edit order statue
   - ## Payment & Check out
        
        - `/payments/stripe/` POST Checkout the order and create url for payment at stripe 
        - Copy the url and past at your web browser 
        - Test cart info `4242 4242 4242 4242` `12/28` cvc `254`
        - If you wanna to test ur webhook log to stripe CLI , use command  `stripe listen --forward-to localhost:8000/payments/webhook/` I'm using port 8000 
        - You can log to stripe dashboard or CLI and see the payments  
    
        



# **Contact Information:**

For any inquiries or collaboration opportunities, you can reach out to me:

- **LinkedIn**: [LinkedIn Profile](https://www.linkedin.com/in/m7mmed-sayed/)
- **Email**: mohamedsayed1167@gmail.com
