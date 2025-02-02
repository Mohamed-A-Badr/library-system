# Library Management System

## Overview
This is a Django-based Library Management System that provides comprehensive functionality for managing books, authors, accounts, and favorites.

## Project Structure
- `accounts/`: User account management and authentication
- `authors/`: Author management and information
- `books/`: Book catalog and management
- `favorites/`: User favorite books functionality
- `core/`: Core project configurations and utilities

## Prerequisites
- Python 3.8+
- Django
- Scikit-learn
- Pandas
- Other dependencies listed in `requirements.txt`

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Mohamed-A-Badr/library-system.git
cd library-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## Features
- User account management
- Book catalog
- Author information
- Favorites system
- Comprehensive database models

## Technologies Used
- Django
- SQLite
- Scikit-learn
- Pandas
- Python
