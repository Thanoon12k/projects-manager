"""
Setup script for Project Manager
Run this script to set up the project for the first time
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"{'='*50}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("="*50)
    print("Project Manager - Setup Script")
    print("="*50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("\nCreating virtual environment...")
        if not run_command('python -m venv venv', 'Creating virtual environment'):
            print("Failed to create virtual environment")
            sys.exit(1)
    
    # Determine activation command based on OS
    if os.name == 'nt':  # Windows
        activate_cmd = '.\\venv\\Scripts\\activate'
        pip_cmd = '.\\venv\\Scripts\\pip'
        python_cmd = '.\\venv\\Scripts\\python'
    else:  # Linux/Mac
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
        python_cmd = 'venv/bin/python'
    
    # Install dependencies
    print("\nInstalling dependencies...")
    if not run_command(f'{pip_cmd} install -r requirements.txt', 'Installing dependencies'):
        print("Failed to install dependencies")
        sys.exit(1)
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("\n.env file not found. Creating from .env.example...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as f:
                env_content = f.read()
            with open('.env', 'w') as f:
                f.write(env_content)
            print("Created .env file. Please update it with your configuration.")
        else:
            print("Warning: .env.example not found. Please create .env manually.")
    
    # Run migrations
    print("\nRunning migrations...")
    if not run_command(f'{python_cmd} manage.py makemigrations', 'Creating migrations'):
        print("Warning: Failed to create migrations")
    if not run_command(f'{python_cmd} manage.py migrate', 'Applying migrations'):
        print("Failed to run migrations")
        sys.exit(1)
    
    # Check for superuser
    print("\nChecking for superuser...")
    result = subprocess.run(
        f'{python_cmd} manage.py shell -c "from django.contrib.auth.models import User; print(\'Superuser exists\' if User.objects.filter(is_superuser=True).exists() else \'No superuser\')"',
        shell=True,
        capture_output=True,
        text=True
    )
    if 'No superuser' in result.stdout:
        print("\nNo superuser found. You can create one with:")
        print(f"  {python_cmd} manage.py createsuperuser")
    
    # Collect static files
    print("\nCollecting static files...")
    run_command(f'{python_cmd} manage.py collectstatic --noinput', 'Collecting static files')
    
    print("\n" + "="*50)
    print("Setup completed successfully!")
    print("="*50)
    print("\nNext steps:")
    print("1. Update .env file with your configuration")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Set up Google Sheets credentials (if using)")
    print("4. Configure Twilio credentials (if using WhatsApp)")
    print("5. Run the server: python manage.py runserver")
    print("\nFor more information, see the documentation in the document/ folder.")

if __name__ == '__main__':
    main()

