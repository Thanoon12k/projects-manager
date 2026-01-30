# API Documentation

## Authentication

All API endpoints require authentication. The API uses Django's session authentication by default.

### Authentication Methods
1. **Session Authentication**: Login via `/admin/` or web interface
2. **Token Authentication**: (Can be configured) Use token in Authorization header

## Base URL
```
http://localhost:8000/api/
```

## Projects API

### List Projects
```http
GET /api/projects/
```

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Project Name",
      "project_type_name": "Web Development",
      "customer_name": "Customer Name",
      "status": "in_progress",
      "total_budget": "10000.00",
      "total_revenue": "8000.00",
      "total_cost": "6000.00",
      "profit": "2000.00",
      "loss": "0.00",
      "total_paid": "5000.00",
      "live_url": "https://example.com",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Get Project Details
```http
GET /api/projects/{id}/
```

**Response:**
```json
{
  "id": 1,
  "name": "Project Name",
  "description": "Project description",
  "project_type": 1,
  "project_type_name": "Web Development",
  "customer": 1,
  "customer_name": "Customer Name",
  "customer_email": "customer@example.com",
  "customer_whatsapp": "+1234567890",
  "status": "in_progress",
  "total_budget": "10000.00",
  "total_revenue": "8000.00",
  "total_cost": "6000.00",
  "profit": "2000.00",
  "loss": "0.00",
  "total_paid": "5000.00",
  "live_url": "https://example.com",
  "repository_url": "https://github.com/example",
  "start_date": "2024-01-01",
  "end_date": null,
  "deadline": "2024-12-31",
  "notes": "Additional notes",
  "images": [],
  "files": [],
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z",
  "is_active": true
}
```

### Create Project
```http
POST /api/projects/
Content-Type: application/json

{
  "name": "New Project",
  "description": "Project description",
  "project_type": 1,
  "customer": 1,
  "status": "planning",
  "total_budget": "10000.00",
  "total_revenue": "0.00",
  "total_cost": "0.00",
  "live_url": "https://example.com"
}
```

### Update Project
```http
PUT /api/projects/{id}/
PATCH /api/projects/{id}/
```

### Delete Project
```http
DELETE /api/projects/{id}/
```

### Calculate Profit/Loss
```http
POST /api/projects/{id}/calculate_profit_loss/
```

**Response:**
```json
{
  "profit": "2000.00",
  "loss": "0.00",
  "message": "Profit and loss calculated successfully"
}
```

### Sync to Google Sheets
```http
POST /api/projects/{id}/sync_to_sheets/
```

**Response:**
```json
{
  "success": true,
  "message": "Project synced to Google Sheets successfully",
  "sheet_url": "https://docs.google.com/spreadsheets/..."
}
```

### Send WhatsApp Update
```http
POST /api/projects/{id}/send_whatsapp_update/
Content-Type: application/json

{
  "message": "Your project has been updated!"
}
```

## Customers API

### List Customers
```http
GET /api/customers/
```

### Get Customer Details
```http
GET /api/customers/{id}/
```

### Create Customer
```http
POST /api/customers/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "whatsapp_number": "+1234567890",
  "phone_number": "+1234567890",
  "company": "Company Name",
  "address": "123 Main St"
}
```

### Send WhatsApp Message
```http
POST /api/customers/{id}/send_whatsapp/
Content-Type: application/json

{
  "message": "Hello from Project Manager!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "WhatsApp message sent successfully",
  "details": {
    "message_sid": "SM...",
    "status": "queued",
    "to": "whatsapp:+1234567890"
  }
}
```

## Payments API

### List Payments
```http
GET /api/payments/
GET /api/payments/?project={project_id}
```

### Create Payment
```http
POST /api/payments/
Content-Type: application/json

{
  "project": 1,
  "amount": "2000.00",
  "payment_date": "2024-01-15",
  "payment_method": "bank_transfer",
  "reference_number": "TXN123456",
  "notes": "First payment"
}
```

### Get Payment Details
```http
GET /api/payments/{id}/
```

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Error message"
}
```

