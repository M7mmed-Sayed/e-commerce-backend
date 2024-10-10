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
       - `localhost/account/register/` register / create new user
       - `localhost/account/login/` login
       - `localhost/account/logout/` logout
       - `localhost/account/` get the current Autherized user data
       - `localhost/account/update/{abc}` update username data if it's Autherized and the curent user username is `abc`
       


# **Contact Information:**

For any inquiries or collaboration opportunities, you can reach out to me:

- **LinkedIn**: [LinkedIn Profile](https://www.linkedin.com/in/m7mmed-sayed/)
- **Email**: mohamedsayed1167@gmail.com
