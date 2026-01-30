# Setup Guide

## Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
python setup.py
```

The script will:
- Create virtual environment (if needed)
- Install all dependencies
- Create .env file from .env.example
- Run database migrations
- Collect static files

### Option 2: Manual Setup

Follow these steps manually:

#### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your settings
# Windows: notepad .env
# Linux/Mac: nano .env
```

#### 4. Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

#### 5. Create Superuser

```bash
python manage.py createsuperuser
```

#### 6. Collect Static Files

```bash
python manage.py collectstatic
```

#### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Configuration Details

### Required Configuration

1. **SECRET_KEY**: Generate a secure secret key
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **DEBUG**: Set to `True` for development, `False` for production

3. **ALLOWED_HOSTS**: Comma-separated list of allowed domains

### Optional Configuration

#### Google Sheets Integration

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API and Google Drive API
4. Create a Service Account
5. Download JSON credentials
6. Save as `credentials.json` in project root
7. Update `.env`:
   ```env
   GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
   GOOGLE_SHEETS_SPREADSHEET_NAME=ProjectManager
   ```

#### WhatsApp Integration (Twilio)

1. Sign up at [Twilio](https://www.twilio.com/)
2. Get Account SID and Auth Token
3. Set up WhatsApp Sandbox (for testing) or Business API
4. Update `.env`:
   ```env
   TWILIO_ACCOUNT_SID=your-account-sid
   TWILIO_AUTH_TOKEN=your-auth-token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```

## First Steps After Setup

1. **Login to Admin Panel**
   - Go to `http://localhost:8000/admin/`
   - Login with superuser credentials

2. **Create Project Types**
   - Go to Projects > Project Types
   - Add project categories (e.g., Web Development, Mobile App, etc.)

3. **Add Customers**
   - Go to Customers
   - Add your first customer with contact information

4. **Create a Project**
   - Go to Projects
   - Create your first project
   - Link it to a customer
   - Set budget and other details

5. **Test Features**
   - Test Google Sheets sync
   - Test WhatsApp messaging (if configured)
   - Explore the dashboard

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **Database Errors**
   - Run `python manage.py migrate`
   - Check database settings in `.env`

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` in settings

4. **Google Sheets Errors**
   - Verify `credentials.json` exists
   - Check file permissions
   - Verify API is enabled in Google Cloud Console

5. **WhatsApp Errors**
   - Verify Twilio credentials in `.env`
   - Check phone number format (must include country code)
   - Ensure WhatsApp is set up in Twilio console

## Development Tips

1. **Use Django Admin**: Great for quick data entry and testing
2. **Check Logs**: Look at console output for errors
3. **Test API**: Use `/api/` endpoints for API testing
4. **Use Browser DevTools**: Check for JavaScript errors
5. **Read Documentation**: See `document/` folder for detailed docs

## Next Steps

- Read the [Full Documentation](README.md)
- Check [API Documentation](API.md)
- Review [Deployment Guide](DEPLOYMENT.md)
- Explore the codebase structure

