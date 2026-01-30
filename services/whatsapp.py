"""
WhatsApp integration service using Twilio
Handles sending WhatsApp messages to customers
"""
from twilio.rest import Client
from django.conf import settings
from typing import Optional


class WhatsAppService:
    """Service to send WhatsApp messages via Twilio"""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER
        self.client = None
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
    
    def is_configured(self) -> bool:
        """Check if WhatsApp service is properly configured"""
        return bool(self.account_sid and self.auth_token and self.client)
    
    def format_phone_number(self, phone_number: str) -> str:
        """Format phone number for WhatsApp (E.164 format)"""
        # Remove all non-digit characters except +
        cleaned = ''.join(c for c in phone_number if c.isdigit() or c == '+')
        
        # If doesn't start with +, add it
        if not cleaned.startswith('+'):
            cleaned = '+' + cleaned
        
        # Ensure it's in whatsapp: format for Twilio
        if cleaned.startswith('whatsapp:'):
            return cleaned
        return f"whatsapp:{cleaned}"
    
    def send_message(self, to_number: str, message: str) -> Optional[dict]:
        """
        Send WhatsApp message to a customer
        
        Args:
            to_number: Recipient's WhatsApp number (with country code)
            message: Message content to send
            
        Returns:
            dict with message details or None if failed
        """
        if not self.is_configured():
            raise ValueError(
                "WhatsApp service is not configured. "
                "Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_WHATSAPP_NUMBER in your .env file."
            )
        
        try:
            formatted_to = self.format_phone_number(to_number)
            
            message_obj = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=formatted_to
            )
            
            return {
                'success': True,
                'message_sid': message_obj.sid,
                'status': message_obj.status,
                'to': formatted_to,
                'from': self.whatsapp_number,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'to': to_number,
            }
    
    def send_project_update(self, customer_number: str, project_name: str, update_message: str) -> Optional[dict]:
        """Send project update message to customer"""
        message = f"📋 Project Update: {project_name}\n\n{update_message}"
        return self.send_message(customer_number, message)
    
    def send_payment_reminder(self, customer_number: str, project_name: str, amount: float, due_date: str = None) -> Optional[dict]:
        """Send payment reminder to customer"""
        message = f"💰 Payment Reminder\n\nProject: {project_name}\nAmount: ${amount:,.2f}"
        if due_date:
            message += f"\nDue Date: {due_date}"
        return self.send_message(customer_number, message)

