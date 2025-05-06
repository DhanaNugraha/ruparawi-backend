# Sustainable Community Market Platform API

## Overview

A RESTful API for connecting local communities with sustainable products. This platform enables eco-conscious consumers to discover and purchase from vendors offering environmentally friendly goods while supporting local economies.

## Key Features

The Sustainable Community Market Platform API offers the following key features:

### User Management
- Secure user authentication and authorization using JWT.
- Role-based access control for different user types (Buyer, Vendor, Admin).
- User profile management and address book.

### Product Catalog
- Comprehensive CRUD operations for managing sustainable products.
- Advanced product filtering and search capabilities.
- Product ratings and reviews to facilitate informed purchasing decisions.

### Order Management
- Streamlined order placement and tracking.
- Secure payment processing (Upcoming).
- Order history and status updates.

### Community Features
- Vendor verification system to ensure product sustainability and ethical sourcing (Upcoming).
- Sustainability impact dashboard to track the environmental impact of purchases (Upcoming).
## Project Structure

The project has the following directory structure:

- `.git/`: Git repository directory.
- `.vscode/`: VS Code configuration directory.
- `assets/`: Contains static assets such as images.
- `auth/`: Contains authentication-related modules.
- `config/`: Contains configuration files for different environments.
- `instance/`: Contains the database instance.
- `migrations/`: Contains database migration scripts.
- `models/`: Contains data models for the application.
- `repo/`: Contains data access layer for interacting with the database.
- `router/`: Contains API endpoint definitions.
- `scheduled/`: Contains scheduled tasks.
- `schemas/`: Contains data validation and serialization schemas.
- `shared/`: Contains shared modules.
- `tests/`: Contains unit and integration tests.
- `views/`: Contains view functions for handling API requests.
- `app.py`: Main application entry point.
- `conftest.py`: Pytest configuration file.
- `Dockerfile`: Dockerfile for containerizing the application.
- `LICENSE`: License file.
- `pyproject.toml`: Poetry project file.
- `README.md`: Project documentation.
- `requirements.txt`: List of project dependencies.

## Models

The project uses the following data models:

- `User`: Represents a user of the platform. Includes `UserRole`, `UserAddress`, `UserPaymentMethod`, `VendorProfile`, `AdminUser`, and `AdminLog`.
- `Product`: Represents a sustainable product. Includes `ProductCategory`, `ProductTag`, and `ProductImage`.
- `Order`: Represents an order placed by a user. Includes `OrderItem` and `OrderStatusHistory`.
- `Testimonial`: Represents a user testimonial (`VendorTestimonial`).
- `Article`: Represents an article.
- `ProductReview`: Represents a product review.

## Schemas

The project uses the following schemas for data validation and serialization:

- `UserSchema`: Schema for validating user data. Includes `UserRegisterRequest`, `UserLoginRequest`, `UserRoleResponse`, `UserProfileResponse`, `UserAddressCreate`, `UserAddressUpdate`, `UserAddressResponse`, `UserPaymentMethodBase`, `UserPaymentMethodResponse`, and `UserPaymentMethodUnsecuredResponse`.
- `ProductSchema`: Schema for validating product data. Includes `ProductCreateRequest`, `ProductCreatedResponse`, `ProductListFilters`, `ProductListResponse`, `ProductDetailResponse`, `ProductUpdateRequest`, `ProductDeleteResponse`, and `VendorProductsResponse`.
- `OrderSchema`: Schema for validating order data. Includes `ProductBase`, `OrderCreate`, `OrderStatusHistoryResponse`, `OrderResponse`, and `OrderStatusUpdate`.
- `TestimonialSchema`: Schema for validating testimonial data.
- `ArticleSchema`: Schema for validating article data. Includes `ArticleCreate`.
- `AuthSchema`: Schema for validating authentication data.
- `AdminSchema`: Schema for validating admin data. Includes `VendorApprovalRequest` and `AdminLogsResponse`.
- `VendorSchema`: Schema for validating vendor data. Includes `VendorCreateRequest`, `VendorProfileResponse`, and `VendorUpdateRequest`.

## Routes

The project exposes the following API endpoints:

- `/auth`: Authentication endpoints (register, login).
- `/users`: User management endpoints.
- `/products`: Product management endpoints.
- `/orders`: Order management endpoints.
- `/testimonials`: Testimonial management endpoints.
- `/articles`: Article management endpoints.
- `/admin`: Admin endpoints.
- `/vendor`: Vendor endpoints.

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


test push
