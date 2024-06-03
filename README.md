# Used Inventory Web App
## Why It's Needed
In the tire industry, particularly at Discount Tire, used tires are a popular choice for customers on a budget. However, managing the inventory of these used tires can be a challenge. The inventory is often misorganized, making it difficult to find specific tires.

This web app aims to solve these problems by providing a system that can store and manage the inventory of used tires. It keeps track of key details for each tire, such as size, age, brand, and whether it’s been checked for leaks.

## Features

- **User Authentication**: The application includes a basic authentication system. Users must enter a valid username and password to access the inventory.

- **Add Tires**: Users can add new tires to the inventory. Each tire is defined by its measurement type, section width, aspect ratio, rim size, and load rating.

- **Remove Tires**: Users can remove tires from the inventory.

- **Search Tires**: Users can search the inventory for tires of a specific size.

- **View Inventory**: Users can view all tires in the inventory.

## Setup and Installation

1. Clone the repository to your local machine.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Set up your `.env` file with your `APP_USERNAME`, `PASSWORD`, and `SECRET_KEY`.
4. Run the application with `python app.py`.

## Future Improvements

- Implement a more secure authentication system.
- Improve the user interface with CSS.
- Add an 4-digit SKU to each added tire so you can easily ID tires irl
- Add a date added trait to each tire and an age calculator next to it
- TODO: limit tables in /remove and /show_inventory to their respective items per page count
- Add a mini to-do list for tires that need sku's AND tires that will be removed/sold. 
- ^ Can be printed ^

## License

MIT
