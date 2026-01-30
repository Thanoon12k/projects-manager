"""
Google Sheets integration service
Handles creating and syncing data with Google Sheets
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import os
from typing import List, Dict, Any


class GoogleSheetsService:
    """Service to interact with Google Sheets"""
    
    def __init__(self):
        self.credentials_file = settings.GOOGLE_SHEETS_CREDENTIALS_FILE
        self.spreadsheet_name = settings.GOOGLE_SHEETS_SPREADSHEET_NAME
        self.client = None
        self.spreadsheet = None
        
    def _get_client(self):
        """Get authenticated Google Sheets client"""
        if self.client is None:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds_path = os.path.join(settings.BASE_DIR, self.credentials_file)
            if not os.path.exists(creds_path):
                raise FileNotFoundError(
                    f"Google Sheets credentials file not found at {creds_path}. "
                    "Please download your service account JSON key from Google Cloud Console."
                )
            
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
            self.client = gspread.authorize(creds)
        
        return self.client
    
    def _get_or_create_spreadsheet(self):
        """Get existing spreadsheet or create new one"""
        client = self._get_client()
        
        try:
            # Try to open existing spreadsheet
            spreadsheet = client.open(self.spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            # Create new spreadsheet
            spreadsheet = client.create(self.spreadsheet_name)
            # Share with your email if needed
            # spreadsheet.share('your-email@gmail.com', perm_type='user', role='writer')
        
        self.spreadsheet = spreadsheet
        return spreadsheet
    
    def _get_or_create_worksheet(self, worksheet_name: str, headers: List[str] = None):
        """Get existing worksheet or create new one with headers"""
        spreadsheet = self._get_or_create_spreadsheet()
        
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(
                title=worksheet_name,
                rows=1000,
                cols=20
            )
            if headers:
                worksheet.append_row(headers)
        
        return worksheet
    
    def sync_projects(self, projects_data: List[Dict[str, Any]]):
        """Sync projects data to Google Sheets"""
        headers = [
            'ID', 'Name', 'Description', 'Project Type', 'Customer', 'Status',
            'Total Budget', 'Total Revenue', 'Total Cost', 'Profit', 'Loss',
            'Live URL', 'Repository URL', 'Start Date', 'End Date', 'Deadline',
            'Created At', 'Updated At'
        ]
        
        worksheet = self._get_or_create_worksheet('Projects', headers)
        
        # Clear existing data (except headers)
        if worksheet.row_count > 1:
            worksheet.delete_rows(2, worksheet.row_count)
        
        # Add project data
        for project in projects_data:
            row = [
                project.get('id', ''),
                project.get('name', ''),
                project.get('description', ''),
                project.get('project_type', ''),
                project.get('customer', ''),
                project.get('status', ''),
                project.get('total_budget', 0),
                project.get('total_revenue', 0),
                project.get('total_cost', 0),
                project.get('profit', 0),
                project.get('loss', 0),
                project.get('live_url', ''),
                project.get('repository_url', ''),
                project.get('start_date', ''),
                project.get('end_date', ''),
                project.get('deadline', ''),
                project.get('created_at', ''),
                project.get('updated_at', ''),
            ]
            worksheet.append_row(row)
        
        return worksheet.url
    
    def sync_customers(self, customers_data: List[Dict[str, Any]]):
        """Sync customers data to Google Sheets"""
        headers = [
            'ID', 'Name', 'Email', 'WhatsApp Number', 'Phone Number',
            'Company', 'Address', 'Notes', 'Created At', 'Updated At'
        ]
        
        worksheet = self._get_or_create_worksheet('Customers', headers)
        
        # Clear existing data (except headers)
        if worksheet.row_count > 1:
            worksheet.delete_rows(2, worksheet.row_count)
        
        # Add customer data
        for customer in customers_data:
            row = [
                customer.get('id', ''),
                customer.get('name', ''),
                customer.get('email', ''),
                customer.get('whatsapp_number', ''),
                customer.get('phone_number', ''),
                customer.get('company', ''),
                customer.get('address', ''),
                customer.get('notes', ''),
                customer.get('created_at', ''),
                customer.get('updated_at', ''),
            ]
            worksheet.append_row(row)
        
        return worksheet.url
    
    def sync_payments(self, payments_data: List[Dict[str, Any]]):
        """Sync payment parts data to Google Sheets"""
        headers = [
            'ID', 'Project', 'Amount', 'Payment Date', 'Payment Method',
            'Reference Number', 'Notes', 'Created At', 'Updated At'
        ]
        
        worksheet = self._get_or_create_worksheet('Payments', headers)
        
        # Clear existing data (except headers)
        if worksheet.row_count > 1:
            worksheet.delete_rows(2, worksheet.row_count)
        
        # Add payment data
        for payment in payments_data:
            row = [
                payment.get('id', ''),
                payment.get('project', ''),
                payment.get('amount', 0),
                payment.get('payment_date', ''),
                payment.get('payment_method', ''),
                payment.get('reference_number', ''),
                payment.get('notes', ''),
                payment.get('created_at', ''),
                payment.get('updated_at', ''),
            ]
            worksheet.append_row(row)
        
        return worksheet.url
    
    def get_spreadsheet_url(self):
        """Get the URL of the spreadsheet"""
        spreadsheet = self._get_or_create_spreadsheet()
        return spreadsheet.url

