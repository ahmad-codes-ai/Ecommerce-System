# E-Commerce Management System

A terminal-based multi-role e-commerce system built with Python.

The system simulates a small online store where three types of users interact: Admin, Customer, and Driver. All data is saved to JSON files so nothing is lost when the program closes.

---

## What the System Does

### Admin
- Logs in with a hardcoded username and password
- Has a starting balance of Rs. 100,000
- Can add new products (checks if balance is enough)
- Can restock existing products (checks if balance is enough)
- Sees all products in inventory
- Sees low stock products
- Sees analytics dashboard (balance, revenue, profit, orders, stock)

### Customer
- Can sign up and log in
- Can browse all available products
- Can add products to cart
- Can remove products from cart
- Can view cart
- Can checkout (creates an order)
- Can view order status (pending, assigned, delivered)

### Driver
- Can sign up and log in
- Sees pending orders in their city
- Can pick an order and mark it as assigned
- Can complete a delivery
- Sees earnings from completed deliveries

---

## Why I Built This

I built this project to put my Python skills to use and create something real before moving on to the next stage of my learning. It is my first big project, with over 1000 lines of main logic, and it helped me practice working with OOP, file handling, and organizing code across multiple files.