# Auction Site

This is a simple auction platform built using Django and Django Rest Framework (DRF) with JWT authentication. It allows users to create auctions, place bids, and view their bids and selling items.

## Features

- User authentication via JWT
- Auction creation and bidding system
- View active auctions and place bids
- User profile and selling items
- Error handling and validation for auction end times

## Requirements

- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+
- Simple JWT 5.0+

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/auction-site.git
   cd auction-site
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser to access the Django admin:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. You can now access the API at `http://127.0.0.1:8000/` and the Django admin at `http://127.0.0.1:8000/admin/`.

## API Endpoints

- **POST /api/token/**: Obtain JWT token (Username and Password required).
- **GET /api/user-profile/**: Get the profile details of the currently authenticated user.
- **GET /api/user-bids/**: Get the list of bids placed by the authenticated user.
- **GET /api/user-selling-items/**: Get the list of items being sold by the authenticated user.

## Testing
You can test the endpoints using Postman, cURL, or any API client. 

Make sure to include the `Authorization: Bearer <your_token>` header for authenticated routes.
