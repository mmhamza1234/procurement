# Procurement Tool Egypt - Runbook

## Quick Start Guide

### Prerequisites
- Python 3.11 or higher
- Supabase account and project
- Google Drive API credentials

### Local Development Setup

1. **Clone and Install**
   ```bash
   git clone <repository-url>
   cd procurement-tool
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

3. **Database Setup**
   - Create Supabase project
   - Run `setup_database.sql` in Supabase SQL Editor
   - Update `.env` with Supabase credentials

4. **Google Drive Setup**
   - Enable Google Drive API in Google Cloud Console
   - Create OAuth 2.0 credentials
   - Add redirect URI: `http://localhost:8501`
   - Update `.env` with Google credentials

5. **Run Application**
   ```bash
   streamlit run app.py
   ```

### Google Drive OAuth Setup

1. **Google Cloud Console Setup**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing
   - Enable Google Drive API
   - Create OAuth 2.0 Client ID credentials
   - Add authorized redirect URI: `http://localhost:8501`

2. **Required Scopes**
   - `https://www.googleapis.com/auth/drive.file`

3. **Environment Variables**
   ```env
   GOOGLE_CLIENT_ID=your_client_id_here
   GOOGLE_CLIENT_SECRET=your_client_secret_here
   GOOGLE_REDIRECT_URI=http://localhost:8501
   GOOGLE_DRIVE_PARENT_FOLDER_NAME=Procurement Tool Egypt
   ```

### Application Workflows

#### "I received a tender" Workflow
1. **Document Processing**
   - Upload tender documents (PDF, Word, Excel, text)
   - OCR and intelligent extraction
   - Auto-save to Google Drive

2. **OEM Classification**
   - Review extracted items
   - Classify by material category
   - Set quantities and specifications

3. **Supplier Management**
   - Filter suppliers by category and origin
   - Generate targeted email drafts
   - Track supplier responses

4. **Comparison & Evaluation**
   - Upload supplier quotations
   - Create weighted comparison matrix
   - Select winning suppliers

5. **Offer Generation**
   - Generate internal offer (no margins)
   - Generate client offer (with margins)
   - Export in multiple formats

6. **PO Management**
   - Process client PO
   - Generate supplier POs
   - Track delivery status

7. **Logistics & Finance**
   - Track shipment milestones
   - Manage payments and invoices
   - Handle delivery and closeout

#### "I have a tender to issue" Workflow
1. **Document Upload**
   - Upload tender documents
   - Extract all requirements

2. **Egyptian Supplier Broadcast**
   - Generate emails for all Egyptian suppliers
   - Include all extracted items
   - Track responses

### File Storage Structure

Google Drive folder structure:
```
Procurement Tool Egypt/
├── tender_documents/
├── classifications/
├── supplier_quotes/
├── comparisons/
├── offers/
├── purchase_orders/
├── logistics/
├── finance/
└── invoices/
```

### Troubleshooting

#### Google Drive Authentication Issues
- Verify client ID and secret in `.env`
- Check redirect URI matches exactly
- Ensure Google Drive API is enabled
- Clear browser cache and retry

#### Database Connection Issues
- Verify Supabase URL and key
- Check network connectivity
- Ensure database schema is up to date

#### File Upload Issues
- Check file size limits
- Verify file format support
- Ensure Google Drive has sufficient space

### Security Considerations

1. **Environment Variables**
   - Never commit `.env` file
   - Use secure credential storage in production
   - Rotate API keys regularly

2. **Data Privacy**
   - All uploads stored in user's Google Drive
   - Data encrypted in transit and at rest
   - User consent required for data processing

3. **Access Control**
   - OAuth-based authentication
   - Minimal required scopes
   - User-controlled data access

### Performance Optimization

1. **Large File Handling**
   - Streaming uploads for large files
   - Progress indicators for user feedback
   - Retry logic for failed uploads

2. **Database Queries**
   - Indexed columns for fast searches
   - Pagination for large datasets
   - Caching for frequently accessed data

### Monitoring and Logging

1. **Application Logs**
   - Structured logging format
   - Error tracking and alerting
   - Performance metrics

2. **User Analytics**
   - Usage patterns and trends
   - Feature adoption metrics
   - Error rates and resolution

### Deployment Options

#### Local Development
- Use `streamlit run app.py`
- Suitable for testing and development

#### Cloud Deployment
- Streamlit Cloud
- Heroku
- Google Cloud Run
- AWS ECS

### Support and Maintenance

1. **Regular Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Update API integrations

2. **Backup Strategy**
   - Database backups via Supabase
   - Google Drive provides file redundancy
   - Export critical data regularly

3. **User Support**
   - In-app help documentation
   - Error message guidance
   - Contact information for issues