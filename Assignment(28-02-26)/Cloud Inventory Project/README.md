# Cloud Inventory Project

A containerized backend system managing Users, Products, Orders, Inventory, and Activity Logs. Built with Flask, dual-database (MySQL & MongoDB), Docker, and a modern Tailwind CSS frontend.

## Project Structure
- `src/`: Flask Application Code (Models, Routes, DB connections)
- `db/`: SQL Initialization Scripts
- `frontend/`: HTML, CSS (Tailwind CDN), JavaScript files
- `docker/`: Dockerfiles and related container config
- `tests/`: Pytest integration tests

## Setup locally

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up `.env` based on the `.env.template` (already provided as `.env`).
4. (To be done) Spin up Docker containers for DBs `docker-compose up -d`.



## how to see data
Now your system is running, let’s see the data inside MySQL and MongoDB in the simplest way.

You have 2 databases:

🐬 MySQL → for Users, Products, Orders, Inventory

🍃 MongoDB → for Logs / Activity Logs

I’ll show you both methods:

🐬 PART 1 — View MySQL Data (Easiest Way)

Your MySQL container name:

inventory_mysql
✅ Method 1: View MySQL from Terminal (fastest)

Run this in VS Code terminal:

docker exec -it inventory_mysql mysql -uadmin -padminpassword

Now you are inside MySQL.

Step 1: Select database
USE inventory_db;
Step 2: Show tables
SHOW TABLES;

You should see:

Users

Products

Orders

Inventory

Order_Items

Step 3: View data from each table
See Users
SELECT id, username, email FROM Users;
See Products
SELECT * FROM Products;
See Orders
SELECT * FROM Orders;
See Order Items
SELECT * FROM Order_Items;
Exit MySQL
exit
🖥️ Optional: Use MySQL Workbench (GUI)

Connection details:

Field	Value
Host	localhost
Port	3307
Username	admin
Password	adminpassword
Database	inventory_db

Because Docker maps:

3307 → 3306 (inside container)



## MONGO DB
🍃 PART 2 — View MongoDB Data

Your Mongo container name:

inventory_mongo
✅ Method 1: View Mongo from Terminal

Run:

docker exec -it inventory_mongo mongosh
Step 1: Show databases
show dbs
Step 2: Select your database
use cloud_inventory_logs
Step 3: Show collections
show collections

You may see:

logs

users

activity_logs

Step 4: View documents
db.logs.find().pretty()

OR

db.activity_logs.find().pretty()
Exit Mongo
exit