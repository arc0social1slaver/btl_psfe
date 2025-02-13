# Bookstore project

Bookstore is an e-commerce platform allowed users to buy and sell books.
## Tech Stack

- **Frontend + Backend**: Django
- **Database**: MySQL
## Features

- Book listing and search
- Shopping cart functionality
- Order management
- User profiles
- Admin dashboard
## Prerequisites

- Python
- MySQL Server
## Usage

1. **Connecting to the database MySQL**
   - Package `mysqlclient` is required for Django connecting to MySQL server. This package can be installed via `pip3`:
     ```bash
     pip3 install mysqlclient
     ```
   - After that, change the directory to `bookstore` and Django connects to the MySQL server via the command:
     ```bash
     python3 manage.py migrate
     ```
2. **Run the website**
   ```bash
   python3 manage.py runserver
   ```
