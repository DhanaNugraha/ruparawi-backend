# Sustainable Community Market Platform API

## Overview

A RESTful API for connecting local communities with sustainable products. This platform enables eco-conscious consumers to discover and purchase from vendors offering environmentally friendly goods while supporting local economies.

## Key Features

### 1. User Management
- JWT Authentication (Register/Login)
- Role-based access (Buyer/Vendor/Admin)
- Profile management 

### 2. Product Catalog
- CRUD operations for sustainable products
- Advanced filtering by:
  - Price range
  - Product categories
  - Tags (eco-friendly, handmade)
- Product ratings and reviews 

### 3. Order System
- Shopping cart functionality (Upcoming)
- Checkout process with multiple payment options (Upcoming)
- Order tracking and history (Upcoming)
- Sustainable packaging preferences (Upcoming)

### 4. Community Features
- Vendor verification system (Upcoming)
- Sustainability impact dashboard (Upcoming)
- Product discussion forums (Upcoming)

## Installation and Setup

### Prerequisites
- uv installed

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/your-repo/bank-app-api.git
   cd Revou-Module-7-Assignment
   ```

2. Install all dependencies:
   ```
   uv sync
   ```
   Kill and restart terminal to run the terminal using the virtual environment.

3. Run the application:
   ```
   uv run task fr
   ```

4. The API will be available at `http://127.0.0.1:3002`.
   
5. Run the tests:
   ```
   uv run pytest -v -s --cov=.
   ```

## API Usage Documentation

The full documentation of each endpoints, along with their request requirements and expected  response are shown in [API Documentation](https://6uvtx8to8t.apidog.io/)

### Base URL
This API is deployed using **Koyeb**  with the following base url for the API request.
`mad-adriane-dhanapersonal-9be85724.koyeb.app/`

## Database Schema Documentation
<img src="https://github.com/DhanaNugraha/Revou-Individual-test/blob/main/assets/Sustainable%20Community%20Market.png">


## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---
## License

---

## Contact
For questions or support, please contact [dhananugraha1511@gmail.com](mailto:dhananugraha1511@gmail.com).


