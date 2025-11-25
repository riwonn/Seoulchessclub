# Kakao Pay Integration Setup Guide

This guide will help you set up Kakao Pay payment integration for the Seoul Chess Club application.

## Overview

The application now supports:
- **Meeting Registration Payments**: Users can pay for chess meeting registrations (₩10,000)
- **Membership Subscriptions**: Users can subscribe to monthly (₩30,000) or annual (₩300,000) memberships
- **Payment History**: Track all user payments and transactions
- **Refunds**: Process refunds for cancelled meetings or memberships

## Features Implemented

### 1. Payment Policies
- Updated Terms of Service with Korean e-commerce requirements:
  - Service delivery period (서비스 제공 기간)
  - Cancellation policy (취소 규정)
  - Refund policy (환불 정책)
  - Exchange policy (교환 정책)

### 2. Database Models
- **Payment**: Tracks all payment transactions
- **Membership**: Manages user membership subscriptions

### 3. API Endpoints
- `POST /payment/ready` - Initialize Kakao Pay payment
- `GET /payment/approve` - Handle payment approval callback
- `GET /payment/cancel` - Handle payment cancellation
- `GET /payment/fail` - Handle payment failure
- `POST /payment/refund` - Process refund requests
- `GET /payment/history` - Get user payment history
- `GET /membership/current` - Get current active membership

### 4. User Interface
- **Meetings List Page**: Kakao Pay button for meeting registration
- **Dashboard**: Membership subscription plans with Kakao Pay integration
- **Main Page Footer**: Business registration information

## Setup Instructions

### Step 1: Get Kakao Pay Credentials

1. Go to [Kakao Developers Console](https://developers.kakao.com/)
2. Create or select your application
3. Navigate to "Kakao Pay" section
4. Get your **Admin Key** (DEV_SECRET_KEY)
5. For testing, you can use the test CID: `TC0ONETIME`
6. For production, apply for a real merchant account and get your CID

### Step 2: Update Environment Variables

Update your `.env` file with the following:

```env
# Kakao Pay Configuration
KAKAO_PAY_ADMIN_KEY=your-admin-key-here
KAKAO_PAY_CID=TC0ONETIME  # Use test CID for testing, replace with real CID for production
BASE_DOMAIN=http://localhost:8000  # Update with your production domain
```

**Important**: When deploying to production, update `BASE_DOMAIN` with your actual domain (e.g., `https://yourdomain.com`)

### Step 3: Update Database Schema

Run the database migration to create the new payment tables:

```bash
python migrate_payment_tables.py
```

Or run the application once, and it will auto-create the tables:

```bash
python main.py
```

### Step 4: Test Payment Flow

#### Testing Meeting Registration Payment:
1. Start the application: `uvicorn main:app --reload`
2. Navigate to `/meetings_list`
3. Click "Register" on any meeting
4. Click "Pay with Kakao Pay"
5. Complete the payment on Kakao Pay test page
6. You'll be redirected back to the success page

#### Testing Membership Subscription:
1. Navigate to `/dashboard` (admin page)
2. Scroll to "Membership Plans" section
3. Click "Subscribe with Kakao Pay" on Monthly or Annual plan
4. Complete the payment on Kakao Pay test page
5. Check membership status on dashboard

### Step 5: Production Deployment Checklist

Before going live:

- [ ] Replace `KAKAO_PAY_ADMIN_KEY` with production key
- [ ] Replace `KAKAO_PAY_CID` with real merchant CID
- [ ] Update `BASE_DOMAIN` with production domain
- [ ] Verify Terms of Service are complete and accurate
- [ ] Test payment flow end-to-end
- [ ] Set up payment monitoring and alerts
- [ ] Configure refund policies and procedures
- [ ] Add business address to footer (currently incomplete)
- [ ] Register for 통신판매신고번호 if required

## Payment Flow

### Meeting Registration Payment Flow:
1. User clicks "Register" on meeting
2. Payment modal appears with Kakao Pay button
3. User clicks "Pay with Kakao Pay"
4. Frontend calls `/payment/ready` API
5. Backend creates Payment record and calls Kakao Pay API
6. User is redirected to Kakao Pay
7. User completes payment
8. Kakao Pay redirects to `/payment/approve`
9. Backend verifies payment and updates database
10. User sees success page

### Membership Subscription Flow:
1. User clicks "Subscribe with Kakao Pay" on plan
2. Frontend calls `/payment/ready` API with membership type
3. Backend creates Payment record and calls Kakao Pay API
4. User is redirected to Kakao Pay
5. User completes payment
6. Kakao Pay redirects to `/payment/approve`
7. Backend creates Membership record and links to Payment
8. User sees success page
9. Dashboard shows active membership

## File Structure

### New Files:
- `payment.py` - Kakao Pay API client
- `KAKAO_PAY_SETUP.md` - This setup guide

### Modified Files:
- `database.py` - Added Payment and Membership models
- `schemas.py` - Added payment-related schemas
- `main.py` - Added payment endpoints
- `templates/terms-of-service.html` - Updated payment policies
- `templates/meetings_list.html` - Added Kakao Pay integration
- `templates/dashboard.html` - Added membership plans
- `templates/index.html` - Added business registration info
- `.env` - Added Kakao Pay configuration

## Database Schema

### Payment Table:
- `id`: Primary key
- `user_id`: Foreign key to users
- `payment_type`: 'meeting' or 'membership'
- `meeting_id`: Foreign key to meetings (if meeting payment)
- `membership_id`: Foreign key to memberships (if membership payment)
- `amount`: Payment amount
- `tid`: Kakao Pay transaction ID
- `partner_order_id`: Unique order ID
- `status`: 'ready', 'approved', 'cancelled', 'failed', 'refunded'
- `created_at`, `approved_at`, `cancelled_at`: Timestamps

### Membership Table:
- `id`: Primary key
- `user_id`: Foreign key to users (unique)
- `membership_type`: 'monthly' or 'annual'
- `status`: 'active', 'cancelled', 'expired'
- `start_date`, `end_date`: Membership period
- `auto_renew`: Boolean for auto-renewal
- `price`: Membership price

## Testing

### Test Cards (Kakao Pay Test Environment):
- The test environment uses test CID: `TC0ONETIME`
- No real cards are charged in test mode
- All test payments will be automatically approved

### Manual Testing Checklist:
- [ ] Meeting registration payment
- [ ] Monthly membership subscription
- [ ] Annual membership subscription
- [ ] Payment cancellation
- [ ] Payment approval
- [ ] Payment history display
- [ ] Membership status display
- [ ] Mobile payment flow
- [ ] Desktop payment flow

## Troubleshooting

### Payment initialization fails:
- Check if `KAKAO_PAY_ADMIN_KEY` is set correctly
- Verify BASE_DOMAIN matches your current environment
- Check network connectivity to Kakao Pay API

### Payment approval fails:
- Verify payment record exists in database
- Check if `tid` was saved correctly
- Review Kakao Pay API response in logs

### Refund fails:
- Ensure payment status is 'approved'
- Verify user has permission
- Check if refund amount is valid

## Support

For Kakao Pay API documentation:
- [Kakao Pay API Docs](https://developers.kakao.com/docs/latest/ko/kakaopay/common)

For application-specific issues:
- Contact: seoulchessclub@gmail.com

## Security Notes

- Never commit real API keys to version control
- Use environment variables for sensitive data
- Implement rate limiting on payment endpoints
- Log all payment transactions for audit trail
- Encrypt sensitive payment data
- Follow PCI DSS guidelines for payment processing

## Next Steps

After basic setup:
1. Implement automatic membership renewal
2. Add payment analytics dashboard
3. Set up automated refund processing
4. Implement payment webhooks for real-time updates
5. Add email notifications for payment confirmations
6. Create admin panel for payment management

---

**Last Updated**: November 2025
**Version**: 1.0.0
