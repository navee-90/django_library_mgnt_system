# Project Overview

The Library Management System is a web-based application built using Django and Python. It allows users to browse books, borrow them, manage carts and wishlists, and place orders. The system also includes user authentication and a responsive interface.

# Features
# General

User registration, login, and logout.

Browse and search books.

View detailed book information.

Responsive UI for desktop and mobile.

# Borrowing

Borrow books with availability check.

Track borrowed books.

# Cart & Wishlist

Add books to cart for ordering.

Add/remove books to/from wishlist.

Quick access to cart and wishlist from book details.

# Orders

Place orders for books in the cart.

Reduce available copies automatically after ordering.

# Admin

Manage books, categories, and authors via Django admin.

# Technologies Used

Python 3.x

Django 5.x

MySQL (or SQLite for local development)

HTML, CSS, Bootstrap 4/5

JavaScript (optional for UI enhancements)
# Run code
1.cd library-mgnt
# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
# Install dependencies

pip install -r requirements.txt
# Configure Database

Update settings.py with your MySQL database credentials or use SQLite.
# Apply migrations
python manage.py makemigrations
python manage.py migrate
# Create superuser
python manage.py createsuperuser
# Run the development server
python manage.py runserver
