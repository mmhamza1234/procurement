# Hamada Tool - Oil & Gas Procurement Solution

## Overview

Hamada Tool is an automated tender-reading and supplier-quoting productivity application designed specifically for the oil & gas procurement industry. Built for Arab Engineering & Distribution Company, this Streamlit-based tool streamlines the procurement process by automating document parsing, supplier management, email generation, and deadline tracking for bulk materials including piping, valves, flanges, fittings, bolts, gaskets, and finned tubes.

## Features

### 🔧 Core Functionality
- **Document Processing**: Multi-format document ingestion (PDF, Word, Excel, text) with intelligent information extraction
- **Supplier Management**: CRUD operations for supplier database with filtering and search capabilities
- **Email Generation**: Professional email draft creation with customizable templates
- **Deadline Management**: Automatic deadline calculation with configurable buffer periods
- **Order Tracking**: Comprehensive order tracking and follow-up management
- **Data Collection**: Secure data collection for service improvement and AI training

### 📊 Data Collection & Analytics
- **User Activity Tracking**: Logs all user interactions for service improvement
- **Usage Analytics**: Dashboard with detailed usage statistics
- **Performance Metrics**: Tool performance monitoring and optimization
- **Training Data**: Anonymized data collection for AI model improvement

### 🔒 Privacy & Security
- **Terms & Conditions**: Comprehensive terms with data collection consent
- **Secure Storage**: All data stored securely in Supabase cloud database
- **Data Encryption**: Data encrypted in transit and at rest
- **User Consent**: Explicit consent required for data collection

## Setup Instructions

### 1. Prerequisites
- Python 3.11 or higher
- Supabase account and project
- Required API keys (see Environment Variables section)

### 2. Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd procurment-tool
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or using uv
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with the following variables:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

### 3. Database Setup

1. **Create Supabase project**:
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Note your project URL and anon key

2. **Run database setup script**:
   - Open your Supabase project dashboard
   - Go to SQL Editor
   - Run the contents of `setup_database.sql`

### 4. Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Environment Variables

The following environment variables are required:

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Your Supabase project URL | Yes |
| `SUPABASE_ANON_KEY` | Your Supabase anonymous key | Yes |

Optional variables for additional features:
| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | No |
| `ELEVENLABS_API_KEY` | ElevenLabs text-to-speech API key | No |
| `GEMINI_API_KEY` | Google Gemini API key | No |
| `OPENAI_API_KEY` | OpenAI API key | No |

## Usage

### First Time Setup
1. **Accept Terms & Conditions**: Users must accept the comprehensive terms and conditions before using the tool
2. **Data Collection Consent**: Explicit consent is required for data collection for service improvement

### Document Processing
1. Upload tender documents (PDF, Word, Excel, text)
2. Or paste text directly into the text area
3. Select processing options (deadlines, materials, specifications)
4. Review extracted information

### Supplier Management
1. View current supplier database
2. Add new suppliers with detailed information
3. Filter suppliers by country, material category, or search terms
4. Edit existing supplier information

### Email Generation
1. Enter project details (auto-populated from processed documents)
2. Select material categories and exclude origins if needed
3. Add requirements and specifications
4. Generate professional email drafts for all matching suppliers

### Deadline Management
1. Input client deadline manually or parse from text
2. Automatic calculation of supplier deadlines
3. View days remaining and status

### Order Tracking
1. Track all processed orders
2. Update order status and add notes
3. Manage follow-ups with suppliers
4. View order statistics

### Dashboard
1. View comprehensive usage statistics
2. Monitor system status
3. Track supplier database metrics
4. View activity breakdown and trends

## Data Collection

### What We Collect
- **Document Processing Data**: Extracted deadlines, materials, specifications
- **User Interactions**: Searches, email generations, deadline calculations
- **Usage Analytics**: Feature usage patterns and performance metrics
- **Session Information**: Tool usage patterns and preferences

### How We Use Your Data
- **Service Improvement**: Enhance tool functionality and user experience
- **AI Training**: Improve AI model accuracy and capabilities
- **Performance Optimization**: Identify and resolve technical issues
- **Feature Development**: Develop new features based on usage patterns

### Data Security
- **Encryption**: All data encrypted in transit and at rest
- **Access Control**: Restricted access to authorized personnel only
- **Secure Storage**: Cloud-based storage with enterprise-grade security
- **Data Retention**: Configurable retention policies with user control

## API Integration

The tool is designed to integrate with various APIs for enhanced functionality:

### Current Integrations
- **Supabase**: Database and authentication
- **Streamlit**: Web application framework

### Potential Future Integrations
- **Email Services**: SMTP, SendGrid, Mailgun for automated email sending
- **OCR Services**: Google Vision, Azure Computer Vision for document processing
- **AI Services**: OpenAI, Anthropic, Google for enhanced document analysis
- **Payment Processing**: Stripe, PayPal for premium features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is proprietary software developed for Arab Engineering & Distribution Company.

## Support

For support and questions:
- Email: support@hamadatool.com
- Phone: +20100 0266 344
- Documentation: [Link to documentation]

## Changelog

### Version 1.0 (Current)
- Initial release with core functionality
- Document processing and supplier management
- Email generation and deadline tracking
- Data collection and analytics
- Terms and conditions with consent management

### Planned Features
- Advanced AI-powered document analysis
- Automated email sending
- Mobile application
- Advanced analytics and reporting
- Integration with ERP systems