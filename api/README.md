
# Pocket Bank API

Pocket Bank is a comprehensive banking application built with Django Rest Framework (DRF). It offers a secure and scalable platform for personal and business banking needs, including account management, transaction tracking, loan and investment management, and financial reporting.

## Project Structure

```
Pocket_Bank/
    api/
        core/
        accounts/
        pocket_bank/
            __init__.py
            settings.py
            urls.py
            wsgi.py
        requirements.txt
        manage.py
```

## Features

- **Account Management:** Real-time balance updates and account details.
- **Transaction Tracking:** View and manage transaction history.
- **Loan and Investment Management:** Track loans and investments.
- **Financial Reports:** Generate balance sheets and other financial reports.
- **Secure Authentication:** Manage users and ensure secure login.

## Technologies Used

- **Django Rest Framework (DRF)**
- **SQLite** (for development)
- **PostgreSQL** (for production)
- **Python 3.x**

## Setup and Installation

### Prerequisites

- Python 3.x installed
- pip (Python package manager)

### Clone the Repository

```bash
git clone < https://github.com/lemyjay/Pocket_Bank.git >
cd Pocket_Bank/api
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the `api` directory and add the following:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@localhost:5432/yourdbname
```

### Run Migrations

```bash
python manage.py migrate
```

### Start the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

### Authentication

- **POST /api/auth/login/**: Log in a user.
- **POST /api/auth/register/**: Register a new user.
- **POST /api/auth/logout/**: Log out a user.

### Accounts

- **GET /api/accounts/**: List all accounts.
- **GET /api/accounts/{id}/**: Retrieve account details.
- **POST /api/accounts/**: Create a new account.
- **PUT /api/accounts/{id}/**: Update account details.
- **DELETE /api/accounts/{id}/**: Delete an account.

### Transactions

- **GET /api/transactions/**: List all transactions.
- **GET /api/transactions/{id}/**: Retrieve transaction details.
- **POST /api/transactions/**: Create a new transaction.
- **PUT /api/transactions/{id}/**: Update transaction details.
- **DELETE /api/transactions/{id}/**: Delete a transaction.

### Loans

- **GET /api/loans/**: List all loans.
- **GET /api/loans/{id}/**: Retrieve loan details.
- **POST /api/loans/**: Apply for a new loan.
- **PUT /api/loans/{id}/**: Update loan details.
- **DELETE /api/loans/{id}/**: Delete a loan.

### Investments

- **GET /api/investments/**: List all investments.
- **GET /api/investments/{id}/**: Retrieve investment details.
- **POST /api/investments/**: Make a new investment.
- **PUT /api/investments/{id}/**: Update investment details.
- **DELETE /api/investments/{id}/**: Delete an investment.

## Contributing

We welcome contributions to the Pocket Bank API. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Open a pull request to the main repository.



## Contact

For any questions or issues, please reach out to [lemyjay17@gmail.com].
