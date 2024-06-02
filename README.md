# My Inventory App
## Why This App is Needed
In the tire industry, particularly at Discount Tire, used tires are a popular choice for customers on a budget. However, managing the inventory of these used tires can be a challenge. The inventory is often misorganized, making it difficult to find specific tires.

This web app aims to solve these problems by providing a system that can store and manage the inventory of used tires. It keeps track of key details for each tire, such as size, age, brand, and whether it’s been checked for leaks.

## Main Functionality
The main function of this app is to allow users to search for a specific tire size and view tires in that size as well as the next two sizes above and below. To ensure the search results are relevant, all returned tires have matching wheel sizes, a width within a -1/+1 range, and an aspect ratio within a -2/+2 range. For example, if a user searches for a 245/40/R18 tire, the search might return a 235/45/R18 tire.

For context, tread widths always end with a 5 (e.g., 245, 205, 295), and aspect ratios are divisible by 5 (e.g., 30, 45, 60).

## Advanced Search Features
For more complicated searches, such as when a high-performance car needs a tire with a higher speed rating, users can set filters for that as well as the load rating for trucks and other heavy-load vehicles.

By providing these features, this web app aims to make managing used tire inventories easier and more efficient, ultimately leading to better customer service and satisfaction.

## Current Progress

So far, the following paths have been implemented:

- `GET /inventory`: Returns the current inventory as a JSON array.
- `POST /inventory`: Adds a new item to the inventory.

The `auth_required` function handles authentication, ensuring that only authorized users can access the inventory data.

The app is hosted on Firebase, making it accessible from anywhere with an internet connection.

## Features

- View inventory of used tires
- Filter tires by brand, age, tread depth, and leak check status
- Basic authentication for secure access

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies:

```
pip install flask
npm install -g firebase-tools
