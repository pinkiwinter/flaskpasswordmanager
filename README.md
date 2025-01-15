# Flask-Based Password Manager API

This project is a secure and scalable password management API built with Flask. It allows users to manage their credentials for various services through encrypted storage and retrieval, ensuring data privacy and integrity. The application includes robust user authentication, encryption mechanisms, and testing capabilities.

# Key Features

-   **User Registration and Authentication**
    
    -   Users can register with a master password and email.
    -   JWT-based authentication for secure access to endpoints.
-   **Password Management**
    
    -   Secure storage and retrieval of account credentials (e.g., usernames, emails, passwords).
    -   Encrypted data storage using the cryptography library (AES encryption).
-   **Encryption Utilities**
    
    -   Data encryption and decryption based on user-specific master passwords.
-   **Validation and Security**
    
    -   Validation of incoming data using Marshmallow schemas.
    -   Password policies enforce minimum security standards (e.g., length, special characters).
-   **Testing**
  
    -   Comprehensive testing suite using pytest for consistent API validation.

# Project Structure
```
├── app/
│   ├── routes/           		# API endpoints for authentication and password management
│   │   ├── auth.py       		# Handles user registration and login
│   │   ├── passwords.py  		# Manages account storage and retrieval
│   ├── utils/            		# Helper utilities for encryption and other operations
│   │   ├── encryption.py 		# Provides data encryption and decryption
│   ├── __init__.py       		# Application initialization
│   ├── config.py         		# Configuration settings (e.g., database, JWT)
│   ├── models.py         		# ORM models for users and account data
│   ├── schemas.py        		# Marshmallow schemas for validating request data
├── migrations/           		# Database migrations using Flask-Migrate
├── tests/                		# Unit tests with pytest
│   ├── conftest.py       		# Test setup and fixtures
│   ├── t/
│   │   ├── test_auth.py  		# Tests for authentication endpoints
│   │   ├── test_passwords.py   # Tests for password management endpoints
├── pytest.ini            		# Pytest configuration
├── run.py                		# Application entry point
├── .env                  		# Environment variables (e.g., secrets, database URL)
├── requirements.txt      		# Python dependencies
```

# Technologies

-   **Backend**: Flask, Flask-JWT-Extended, Flask-Migrate, SQLAlchemy.
-   **Database**: PostgreSQL.
-   **Validation**: Marshmallow.
-   **Encryption**: Cryptography.
-   **Testing**: Pytest.

# Running the Project

-   Install dependencies: `pip install -r requirements.txt`.
-   Configure environment variables in a `.env` file (e.g., database URL, secret keys).
-   Run database migrations: `flask db upgrade`.
-   Start the application: `flask run`.

