# Project Manager - Complete Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Project Structure](#project-structure)
7. [Models](#models)
8. [API Documentation](#api-documentation)
9. [Google Sheets Integration](#google-sheets-integration)
10. [WhatsApp Integration](#whatsapp-integration)
11. [Deployment](#deployment)
12. [Testing](#testing)
13. [Security](#security)

## Project Overview

Project Manager is a comprehensive Django-based web application for managing projects, customers, payments, and business operations. It provides a modern dashboard interface, RESTful API for mobile app integration, Google Sheets synchronization, and WhatsApp messaging capabilities.

## Features

### Core Features
- **Project Management**: Create, update, and track projects with detailed information
- **Customer Management**: Manage customer information with contact details
- **Payment Tracking**: Track partial payments for projects
- **Financial Analytics**: Calculate profit/loss, revenue, and costs
- **File Management**: Upload and manage project files and images
- **Modern Dashboard**: Interactive dashboard with statistics and charts
- **Google Sheets Sync**: Automatic synchronization with Google Sheets
- **WhatsApp Integration**: Send messages to customers via WhatsApp

### Technical Features
- RESTful API for mobile app integration
- Responsive UI with Tailwind CSS
- Media file handling
- Comprehensive test suite
- Production-ready configuration
- Security best practices

## Technology Stack

- **Backend**: Django 6.0.1
- **API**: Django REST Framework 3.16.1
- **Frontend**: Tailwind CSS (via CDN)
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Google Sheets**: gspread 6.2.1
- **WhatsApp**: Twilio 9.10.0
- **Image Processing**: Pillow 12.1.0

## Installation

### Prerequisites
- Python 3.12+
- pip
- Virtual environment (recommended)

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd projects_manager_new
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy .env.example to .env and fill in your values
cp .env.example .env
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic
```

8. **Run development server**
```bash
python manage.py runserver
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_SPREADSHEET_NAME=ProjectManager

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Sheets API and Google Drive API
4. Create a Service Account
5. Download the JSON credentials file
6. Place it in the project root as `credentials.json`

### Twilio WhatsApp Setup

1. Sign up for [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Set up WhatsApp Sandbox or Business API
4. Add credentials to `.env` file

## Project Structure

```
project_manager/
├── project_manager/          # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── projects/                # Projects app
│   ├── models.py            # Project models
│   ├── views.py             # View functions
│   ├── api_views.py         # API views
│   ├── serializers.py       # API serializers
│   ├── forms.py             # Forms
│   └── urls.py              # App URLs
├── customers/                # Customers app
├── payments/                 # Payments app
├── dashboard/                # Dashboard app
├── services/                 # Service classes
│   ├── google_sheets.py     # Google Sheets service
│   └── whatsapp.py          # WhatsApp service
├── templates/                # HTML templates
├── static/                   # Static files
├── media/                    # Media files (user uploads)
├── tests/                    # Test files
├── document/                 # Documentation
├── manage.py
├── requirements.txt
└── .gitignore
```

## Models

### Project Model
- **Fields**: name, description, project_type, customer, status, financial fields, dates, URLs
- **Relationships**: ForeignKey to Customer and ProjectType
- **Methods**: calculate_profit_loss(), total_paid property

### Customer Model
- **Fields**: name, email, whatsapp_number, phone_number, company, address
- **Methods**: get_whatsapp_link()

### PaymentPart Model
- **Fields**: project, amount, payment_date, payment_method, reference_number
- **Relationships**: ForeignKey to Project

## API Documentation

### Base URL
```
/api/
```

### Endpoints

#### Projects
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create new project
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project
- `POST /api/projects/{id}/calculate_profit_loss/` - Calculate profit/loss
- `POST /api/projects/{id}/sync_to_sheets/` - Sync to Google Sheets
- `POST /api/projects/{id}/send_whatsapp_update/` - Send WhatsApp update

#### Customers
- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create new customer
- `GET /api/customers/{id}/` - Get customer details
- `POST /api/customers/{id}/send_whatsapp/` - Send WhatsApp message
- `POST /api/customers/{id}/sync_to_sheets/` - Sync to Google Sheets

#### Payments
- `GET /api/payments/` - List all payments
- `POST /api/payments/` - Create new payment
- `GET /api/payments/?project={id}` - Filter by project

### Authentication

All API endpoints require authentication. Use session authentication or configure token authentication.

## Google Sheets Integration

The application automatically syncs data to Google Sheets when:
- A project is created or updated
- A customer is created or updated
- A payment is created or updated

Sheets are created automatically if they don't exist. Three worksheets are created:
- **Projects**: All project data
- **Customers**: All customer data
- **Payments**: All payment data

## WhatsApp Integration

### Sending Messages

1. **Via Web Interface**: Navigate to customer detail page and click "Send WhatsApp"
2. **Via API**: POST to `/api/customers/{id}/send_whatsapp/` with message in body

### Message Types
- General messages
- Project updates
- Payment reminders

## Deployment

### Production Settings

1. Set `DEBUG=False` in `.env`
2. Set `ALLOWED_HOSTS` to your domain
3. Configure proper database (PostgreSQL recommended)
4. Set up static file serving (WhiteNoise or CDN)
5. Configure SSL/HTTPS
6. Set up proper logging

### Recommended Hosting
- Heroku
- DigitalOcean
- AWS
- Railway

## Testing

Run tests with:
```bash
python manage.py test
```

Test files are located in the `tests/` directory:
- `test_projects.py` - Project model and view tests
- `test_customers.py` - Customer model and view tests
- `test_payments.py` - Payment model and view tests

## Security

### Implemented Security Measures
- CSRF protection
- XSS protection
- SQL injection prevention (Django ORM)
- Secure password hashing
- Session security
- HTTPS enforcement in production
- Environment variable for secrets

### Best Practices
- Never commit `.env` file
- Use strong SECRET_KEY
- Keep dependencies updated
- Regular security audits
- Use HTTPS in production
- Implement rate limiting for API

## Support

For issues or questions, please refer to the project repository or contact the development team.

