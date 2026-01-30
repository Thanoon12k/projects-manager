# Project Manager

A comprehensive Django-based project management system with Google Sheets integration and WhatsApp messaging capabilities.

## Features

- 📊 **Project Management**: Track projects with budgets, revenues, costs, and profit/loss calculations
- 👥 **Customer Management**: Manage customer information with WhatsApp and email integration
- 💰 **Payment Tracking**: Track partial payments for projects
- 📈 **Interactive Dashboard**: Modern dashboard with statistics and analytics
- 📱 **REST API**: Full REST API for mobile app integration
- 📄 **Google Sheets Sync**: Automatic synchronization with Google Sheets
- 💬 **WhatsApp Integration**: Send messages to customers via WhatsApp
- 🎨 **Modern UI**: Beautiful interface built with Tailwind CSS
- 🔒 **Security**: Production-ready security configurations

## Quick Start

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd projects_manager_new
```

2. **Create virtual environment**
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

4. **Configure environment**
```bash
# Create .env file with your settings
# See .env.example for reference
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

7. **Run server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Configuration

### Required Environment Variables

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Google Sheets Setup

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Sheets API and Google Drive API
3. Create a Service Account and download JSON credentials
4. Place credentials file as `credentials.json` in project root

### WhatsApp Setup (Twilio)

1. Sign up for [Twilio](https://www.twilio.com/)
2. Get Account SID and Auth Token
3. Set up WhatsApp Sandbox or Business API
4. Add credentials to `.env` file

## Project Structure

```
project_manager/
├── project_manager/     # Main project settings
├── projects/            # Projects app
├── customers/           # Customers app
├── payments/            # Payments app
├── dashboard/           # Dashboard app
├── services/            # Service classes (Google Sheets, WhatsApp)
├── templates/           # HTML templates
├── static/              # Static files
├── tests/               # Test files
└── document/            # Documentation
```

## API Documentation

The application provides a RESTful API for all resources. See `document/API.md` for complete API documentation.

Base API URL: `http://localhost:8000/api/`

## Testing

Run tests with:
```bash
python manage.py test
```

## Documentation

Complete documentation is available in the `document/` folder:
- `README.md` - Full project documentation
- `API.md` - API endpoint documentation

## Security

- CSRF protection enabled
- XSS protection
- SQL injection prevention (Django ORM)
- Secure password hashing
- Session security
- HTTPS enforcement in production

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please refer to the documentation or create an issue in the repository.

