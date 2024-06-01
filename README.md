At my real job at Discount Tire, we carry used tires as a cheaper option for customers on a budget. There's just one problem: this inventory is never accounted for and is always misorganized. You'll find a 15 inch tire trailer tire next to a big ol' mud terrain and it gets frustrating.
This web app aims to reduce those confusions by providing a system that can store available inventory as well as key details on used tires, such as size, age, brand, and if it's already been checked for leaks.
The main function would be to search for a specific size and show that size as well as the next two sizes above and below that. For this to prove functional, all returned searches should have matching wheel sizes, a -1/+1 range in width, and a -2/+2 range in aspect ratio. Ex: User searches for a 245/40/R18 and the search returns a 235/45/R18.
For more complicated searches, such as when a fancy car needs a higher speed rating, you can also set filters for that as well as the load rating for trucks/heavy-load vehicles.

Setup via a basic Flask app and basic HTTP Basic Authentication. 
So far, there are 2 paths:
	"GET /inventory" returns the current inventory as a JSON array.
	"POST /inventory" adds a new item to the inventory.
"auth_required" handles authentication.
Uses Firebase for hosting.
