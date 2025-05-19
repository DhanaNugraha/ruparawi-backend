# 🌱 [Rupa Rawi](https://ruparawi-frontend.vercel.app/) API 🌍

A RESTful API for connecting local communities with sustainable products. This platform enables eco-conscious consumers to discover and purchase from vendors offering environmentally friendly goods while supporting local economies. 

## 🚀 Key Features

### 👥 User Management
- Secure JWT authentication & authorization
- Role-based access control (Buyer/Vendor/Admin)
- User profiles & address book

### 🛍️ Product Catalog
- Full CRUD operations for sustainable products
- Advanced filtering & search
- Product ratings & reviews

### 📦 Order Management
- Streamlined order placement & tracking
- Order history & status updates

### 🤝 Community Features
- Product review
- Community Articles

## 🏗️ Project Structure
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


## 🗃️ Data Models

| Model | Description |
|-------|-------------|
| `User` | Platform users with roles |
| `Product` | Sustainable products |
| `Order` | Customer purchases |
| `Testimonial` | Vendor feedback |
| `Article` | Community articles |
| `ProductReview` | Product ratings |

## 🔌 API Endpoints

| Route | Description |
|-------|-------------|
| `/auth` | Authentication |
| `/users` | User management |
| `/products` | Product operations |
| `/orders` | Order processing |
| `/testimonials` | Feedback system |
| `/articles` | Community content |
| `/admin` | Admin functions |
| `/vendor` | Vendor portal |

## 🛠️ Installation

### Setup Steps
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

# 📚 API Documentation

Full endpoint documentation available at:
[API Documentation](https://6uvtx8to8t.apidog.io/)

Deployed on Koyeb, base URL:
`mad-adriane-dhanapersonal-9be85724.koyeb.app/`

# 🗄️ Database Schema
<img src="https://github.com/DhanaNugraha/ruparawi-backend/blob/main/assets/Rupa%20Rawi%202.png">

# 🤝 Contributing

We welcome contributions!
🙌 Please submit PRs or open issues.

# 📜 License

MIT License
Copyright (c) 2025 Dhana Nugraha
