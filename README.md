@@ .. @@
-# Hamada Tool - Oil & Gas Procurement Solution
+# Procurement Tool Egypt - Oil & Gas Procurement Solution
 
 ## Overview
 
-Hamada Tool is an automated tender-reading and supplier-quoting productivity application designed specifically for the oil & gas procurement industry. Built for Arab Engineering & Distribution Company, this Streamlit-based tool streamlines the procurement process by automating document parsing, supplier management, email generation, and deadline tracking for bulk materials including piping, valves, flanges, fittings, bolts, gaskets, and finned tubes.
+Procurement Tool Egypt is a comprehensive procurement management system designed specifically for the oil & gas industry. This Streamlit-based tool provides end-to-end workflow automation from tender receipt to delivery and invoicing, handling bulk materials including piping, valves, flanges, fittings, bolts, gaskets, and finned tubes.
 
 ## Features
 
 ### 🔧 Core Functionality
 - **Document Processing**: Multi-format document ingestion (PDF, Word, Excel, text) with intelligent information extraction
+- **OEM Classification**: Automatic classification of items to match OEM scopes and material categories
 - **Supplier Management**: CRUD operations for supplier database with filtering and search capabilities
 - **Email Generation**: Professional email draft creation with customizable templates
+- **Supplier Comparison**: Advanced comparison matrix with weighted scoring
+- **Offer Generation**: Automated offer generation with and without margins
+- **PO Management**: Complete purchase order lifecycle management
+- **Logistics Tracking**: Shipment tracking from production to delivery
+- **Finance Integration**: Payment tracking and invoice generation
 - **Deadline Management**: Automatic deadline calculation with configurable buffer periods
-- **Order Tracking**: Comprehensive order tracking and follow-up management
+- **Google Drive Integration**: Automatic file storage and organization
 - **Data Collection**: Secure data collection for service improvement and AI training
 
+### 🏢 Dual Workflow Support
+- **"I received a tender"**: Complete procurement workflow for processing received tenders
+- **"I have a tender to issue"**: Streamlined workflow for issuing tenders to Egyptian suppliers
+
 ### 📊 Data Collection & Analytics
 - **User Activity Tracking**: Logs all user interactions for service improvement
 - **Usage Analytics**: Dashboard with detailed usage statistics
@@ -35,6 +42,7 @@ Hamada Tool is an automated tender-reading and supplier-quoting productivity app
 ### 1. Prerequisites
 - Python 3.11 or higher
 - Supabase account and project
+- Google Drive API credentials
 - Required API keys (see Environment Variables section)
 
 ### 2. Installation
@@ -42,7 +50,7 @@ Hamada Tool is an automated tender-reading and supplier-quoting productivity app
 1. **Clone the repository**:
    ```bash
    git clone <repository-url>
-   cd procurment-tool
+   cd procurement-tool
    ```
 
 2. **Install dependencies**:
@@ -56,6 +64,10 @@ Hamada Tool is an automated tender-reading and supplier-quoting productivity app
    ```env
    SUPABASE_URL=your_supabase_url
    SUPABASE_ANON_KEY=your_supabase_anon_key
+   GOOGLE_CLIENT_ID=your_google_client_id
+   GOOGLE_CLIENT_SECRET=your_google_client_secret
+   GOOGLE_REDIRECT_URI=http://localhost:8501
+   GOOGLE_DRIVE_PARENT_FOLDER_NAME=Procurement Tool Egypt
    ```
 
 ### 3. Database Setup
@@ -82,6 +94,8 @@ The following environment variables are required:
 |----------|-------------|----------|
 | SUPABASE_URL | Your Supabase project URL | Yes |
 | SUPABASE_ANON_KEY | Your Supabase anonymous key | Yes |
+| GOOGLE_CLIENT_ID | Google OAuth client ID | Yes |
+| GOOGLE_CLIENT_SECRET | Google OAuth client secret | Yes |
 
 Optional variables for additional features:
 | Variable | Description | Required |
@@ -95,8 +109,10 @@ Optional variables for additional features:
 
 ### First Time Setup
 1. **Accept Terms & Conditions**: Users must accept the comprehensive terms and conditions before using the tool
-2. **Data Collection Consent**: Explicit consent is required for data collection for service improvement
+2. **Choose Workflow**: Select between "I received a tender" or "I have a tender to issue"
+3. **Google Drive Authentication**: Authenticate with Google Drive for file storage
 
+### Complete Procurement Workflow ("I received a tender")
 ### Document Processing
 1. Upload tender documents (PDF, Word, Excel, text)
 2. Or paste text directly into the text area
@@ -104,6 +120,11 @@ Optional variables for additional features:
 4. Review extracted information
 
+### OEM Classification
+1. Review extracted items
+2. Classify items by material category
+3. Set quantities and specifications
+
 ### Supplier Management
 1. View current supplier database
 2. Add new suppliers with detailed information
@@ -116,6 +137,21 @@ Optional variables for additional features:
 3. Add requirements and specifications
 4. Generate professional email drafts for all matching suppliers
 
+### Supplier Comparison
+1. Upload supplier quotations
+2. Create comparison matrix
+3. Apply weighted scoring
+4. Select winning suppliers
+
+### Offer Generation
+1. Configure offer parameters
+2. Generate internal offer (without margins)
+3. Generate client offer (with margins)
+4. Export offers in multiple formats
+
+### PO Management
+1. Process client purchase orders
+2. Generate supplier purchase orders
 3. Track PO status and deliveries
 
 ### Deadline Management
@@ -123,11 +159,21 @@ Optional variables for additional features:
 2. Automatic calculation of supplier deadlines
 3. View days remaining and status
 
-### Order Tracking
-1. Track all processed orders
-2. Update order status and add notes
-3. Manage follow-ups with suppliers
-4. View order statistics
+### Logistics Tracking
+1. Track shipment milestones
+2. Monitor ACID and CargoX status
+3. Manage customs and freezone processes
+4. Coordinate delivery and pickup
+
+### Finance & Payments
+1. Track advance payments
+2. Monitor final payments
+3. Generate invoices and credit notes
+4. Manage SWIFT confirmations
+
+### Egyptian Supplier Workflow ("I have a tender to issue")
+1. Upload tender documents
+2. Generate emails for all Egyptian suppliers
+3. Track responses and follow-ups
 
 ### Dashboard
 1. View comprehensive usage statistics
@@ -138,7 +184,7 @@ Optional variables for additional features:
 ## Data Collection
 
 ### What We Collect
-- **Document Processing Data**: Extracted deadlines, materials, specifications
+- **Document Processing Data**: Extracted deadlines, materials, specifications, classifications
 - **User Interactions**: Searches, email generations, deadline calculations
 - **Usage Analytics**: Feature usage patterns and performance metrics
 - **Session Information**: Tool usage patterns and preferences
@@ -158,6 +204,7 @@ Optional variables for additional features:
 
 ### Current Integrations
 - **Supabase**: Database and authentication
+- **Google Drive**: File storage and organization
 - **Streamlit**: Web application framework
 
 ### Potential Future Integrations
@@ -175,13 +222,7 @@ Optional variables for additional features:
 
 ## License
 
-This project is proprietary software developed for Arab Engineering & Distribution Company.
-
-## Support
-
-For support and questions:
-- Email: support@hamadatool.com
-- Phone: +20100 0266 344
-- Documentation: [Link to documentation]
+This project is open-source software for the oil & gas procurement industry.
 
 ## Changelog
 
@@ -189,8 +230,14 @@ For support and questions:
 - Initial release with core functionality
 - Document processing and supplier management
 - Email generation and deadline tracking
+- OEM classification and supplier comparison
+- Offer generation and PO management
+- Logistics tracking and finance integration
+- Google Drive integration
 - Data collection and analytics
 - Terms and conditions with consent management
+- Dual workflow support
+- Complete procurement lifecycle automation
 
 ### Planned Features
 - Advanced AI-powered document analysis
@@ -198,4 +245,5 @@ For support and questions:
 - Mobile application
 - Advanced analytics and reporting
 - Integration with ERP systems
+- Multi-language support
+- Advanced workflow customization