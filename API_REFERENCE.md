# BankSight API Reference

## REST API Endpoints

### Authentication

All API requests should include:
```
Authorization: Bearer <token>
Content-Type: application/json
```

### Base URL
```
http://localhost:8000/api
```

## Endpoints

### Transactions

#### Get All Transactions
```http
GET /transactions
```

**Query Parameters:**
- `skip` (int): Skip n records (default: 0)
- `limit` (int): Limit results (default: 100)
- `customer_id` (int): Filter by customer
- `start_date` (string): ISO format date
- `end_date` (string): ISO format date

**Response:**
```json
{
  "data": [
    {
      "transaction_id": "TXN_00000001",
      "customer_id": 1,
      "amount": 150.00,
      "merchant_name": "Walmart",
      "status": "COMPLETED",
      "fraud_score": 0.15,
      "is_flagged": false,
      "transaction_date": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1000,
  "skip": 0,
  "limit": 100
}
```

#### Get Transaction by ID
```http
GET /transactions/{transaction_id}
```

**Response:** Single transaction object

#### Create Transaction
```http
POST /transactions
```

**Request Body:**
```json
{
  "customer_id": 1,
  "amount": 150.00,
  "merchant_name": "Walmart",
  "merchant_category": "RETAIL",
  "transaction_type": "DEBIT"
}
```

### Customers

#### Get All Customers
```http
GET /customers
```

**Query Parameters:**
- `skip` (int): Skip n records
- `limit` (int): Limit results
- `risk_level` (string): Filter by risk level (LOW, MEDIUM, HIGH)

**Response:**
```json
{
  "data": [
    {
      "customer_id": "CUST_00001",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "risk_score": 0.35,
      "risk_classification": "LOW",
      "kyc_verified": true
    }
  ],
  "total": 5000
}
```

#### Get Customer by ID
```http
GET /customers/{customer_id}
```

#### Get Customer Transactions
```http
GET /customers/{customer_id}/transactions
```

#### Get Customer Profile
```http
GET /customers/{customer_id}/profile
```

**Response:**
```json
{
  "customer_id": "CUST_00001",
  "avg_transaction_amount": 125.50,
  "transaction_frequency": 2.5,
  "preferred_merchants": ["Walmart", "Target"],
  "preferred_categories": ["RETAIL"],
  "typical_hours": [9, 10, 14, 18]
}
```

### Fraud Detection

#### Flag Transaction as Fraud
```http
POST /fraud/flag
```

**Request Body:**
```json
{
  "transaction_id": "TXN_00000001",
  "reason": "Unusual amount"
}
```

#### Get Fraud Alerts
```http
GET /fraud/alerts
```

**Query Parameters:**
- `status` (string): OPEN, INVESTIGATING, CLOSED
- `severity` (string): LOW, MEDIUM, HIGH, CRITICAL

**Response:**
```json
{
  "data": [
    {
      "alert_id": "ALERT_0001",
      "customer_id": 1,
      "transaction_ids": ["TXN_00000001", "TXN_00000002"],
      "alert_type": "FRAUD",
      "severity": "HIGH",
      "status": "OPEN",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Resolve Fraud Alert
```http
PUT /fraud/alerts/{alert_id}
```

**Request Body:**
```json
{
  "status": "CLOSED",
  "resolution_status": "FRAUD_CONFIRMED",
  "notes": "Investigation completed"
}
```

### Analytics

#### Get Transaction Summary
```http
GET /analytics/transactions/summary
```

**Response:**
```json
{
  "total_transactions": 10000,
  "total_volume": 1500000.00,
  "avg_transaction": 150.00,
  "flagged_transactions": 150,
  "fraud_rate": 1.5,
  "peak_hour": 12
}
```

#### Get Daily Metrics
```http
GET /analytics/transactions/daily
```

**Query Parameters:**
- `days` (int): Number of days to analyze (default: 30)

**Response:**
```json
{
  "data": [
    {
      "date": "2024-01-15",
      "total_amount": 45000.00,
      "transaction_count": 300,
      "avg_amount": 150.00
    }
  ]
}
```

#### Get Merchant Analytics
```http
GET /analytics/merchants
```

**Query Parameters:**
- `top_n` (int): Top n merchants (default: 20)

**Response:**
```json
{
  "top_merchants": {
    "Walmart": {
      "total_volume": 500000.00,
      "transaction_count": 5000,
      "avg_amount": 100.00
    }
  },
  "total_unique_merchants": 1000
}
```

### Risk Scoring

#### Calculate Customer Risk Score
```http
POST /risk/score
```

**Request Body:**
```json
{
  "customer_id": 1
}
```

**Response:**
```json
{
  "customer_id": 1,
  "overall_score": 0.45,
  "risk_level": "MEDIUM",
  "components": {
    "behavioral_risk": 0.4,
    "geographic_risk": 0.5,
    "temporal_risk": 0.45
  }
}
```

#### Identify High-Risk Customers
```http
GET /risk/customers/high-risk
```

**Query Parameters:**
- `threshold` (float): Risk score threshold (default: 0.7)
- `limit` (int): Number of results (default: 20)

## Error Responses

### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "success": false,
  "error": "INVALID_REQUEST",
  "message": "Transaction ID not found",
  "status_code": 404
}
```

### Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid request |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

## Rate Limiting

- **Requests per minute**: 60
- **Requests per hour**: 3,600
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Examples

### Using cURL

```bash
# Get transactions
curl -X GET "http://localhost:8000/api/transactions?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create transaction
curl -X POST "http://localhost:8000/api/transactions" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "amount": 150.00,
    "merchant_name": "Walmart"
  }'

# Flag fraud
curl -X POST "http://localhost:8000/api/fraud/flag" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "transaction_id": "TXN_00000001",
    "reason": "Suspicious activity"
  }'
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000/api"
HEADERS = {"Authorization": "Bearer YOUR_TOKEN"}

# Get transactions
response = requests.get(
    f"{BASE_URL}/transactions",
    headers=HEADERS,
    params={"limit": 10}
)
transactions = response.json()

# Create transaction
payload = {
    "customer_id": 1,
    "amount": 150.00,
    "merchant_name": "Walmart"
}
response = requests.post(
    f"{BASE_URL}/transactions",
    headers=HEADERS,
    json=payload
)
```

### Using JavaScript

```javascript
const BASE_URL = "http://localhost:8000/api";
const token = "YOUR_TOKEN";

// Get transactions
fetch(`${BASE_URL}/transactions?limit=10`, {
  headers: {
    "Authorization": `Bearer ${token}`
  }
})
.then(res => res.json())
.then(data => console.log(data));

// Create transaction
fetch(`${BASE_URL}/transactions`, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    customer_id: 1,
    amount: 150.00,
    merchant_name: "Walmart"
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

## Webhooks

### Transaction Fraud Detected
```
POST /webhooks/fraud-detected
```

**Payload:**
```json
{
  "event": "fraud_detected",
  "transaction_id": "TXN_00000001",
  "fraud_score": 0.85,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Customer Risk Score Changed
```
POST /webhooks/risk-changed
```

**Payload:**
```json
{
  "event": "risk_score_changed",
  "customer_id": 1,
  "old_score": 0.4,
  "new_score": 0.65,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## API Status

Check API health:
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "database": "connected",
  "cache": "connected"
}
```

---

**API Version**: 1.0.0
**Last Updated**: 2024
