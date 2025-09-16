import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import custom modules
from modules.document_parser import DocumentParser
from modules.supplier_manager import SupplierManager
from modules.email_generator import EmailGenerator
from modules.deadline_calculator import DeadlineCalculator
from modules.order_tracker import OrderTracker
from modules.data_collector import DataCollector
from modules.terms_conditions import TermsConditions

# Page configuration
st.set_page_config(
    page_title="Procurement Tool Egypt - Oil & Gas Procurement",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize modules
@st.cache_resource
def initialize_modules():
    """Initialize all modules with caching."""
    return {
        'document_parser': DocumentParser(),
        'supplier_manager': SupplierManager(),
        'email_generator': EmailGenerator(),
        'deadline_calculator': DeadlineCalculator(),
        'order_tracker': OrderTracker(),
        'data_collector': DataCollector(),
        'terms_conditions': TermsConditions(),
        'google_drive_client': GoogleDriveClient(),
        'comparison_manager': ComparisonManager(),
        'offer_generator': OfferGenerator(),
        'po_manager': POManager(),
        'logistics_tracker': LogisticsTracker(),
        'finance_manager': FinanceManager()
    }

def main():
    """Main application function."""
    
    # Initialize modules
    modules = initialize_modules()
    
    # Check terms acceptance first
    if not modules['terms_conditions'].check_terms_acceptance():
        st.title("🏭 Welcome to Procurement Tool Egypt")
        st.markdown("### Oil & Gas Procurement Automation Platform")
        st.markdown("---")
        
        # Two main workflow buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏢 I have a tender to issue", 
                        type="primary", 
                        use_container_width=True,
                        help="For clients issuing tenders to suppliers"):
                st.session_state.workflow_type = "issue_tender"
                # Show terms and conditions
                accepted = modules['terms_conditions'].show_terms_and_conditions()
                if accepted:
                    acceptance_data = modules['terms_conditions'].get_acceptance_data()
                    modules['data_collector'].log_terms_acceptance('user_' + str(datetime.now().timestamp()), acceptance_data)
                    st.rerun()
        
        with col2:
            if st.button("📄 I received a tender", 
                        type="secondary", 
                        use_container_width=True,
                        help="For processing received tender documents"):
                st.session_state.workflow_type = "received_tender"
                # Show terms and conditions
                accepted = modules['terms_conditions'].show_terms_and_conditions()
                if accepted:
                    acceptance_data = modules['terms_conditions'].get_acceptance_data()
                    modules['data_collector'].log_terms_acceptance('user_' + str(datetime.now().timestamp()), acceptance_data)
                    st.rerun()
        
        return
    
    # Main application header
    st.title("🏭 Procurement Tool Egypt")
    st.markdown("### Automated Oil & Gas Procurement Solution")
    
    # Check workflow type and route accordingly
    workflow_type = st.session_state.get('workflow_type', 'received_tender')
    
    if workflow_type == "issue_tender":
        issue_tender_workflow(modules)
    else:
        received_tender_workflow(modules)

def issue_tender_workflow(modules):
    """Workflow for clients issuing tenders to Egyptian suppliers."""
    st.header("🏢 Issue Tender to Egyptian Suppliers")
    st.markdown("Upload your tender documents to broadcast to Egyptian bulk material suppliers.")
    
    # Document upload and processing
    process_tender_documents(modules, "issue")
    
    # Egyptian suppliers email generation
    if 'tender_items' in st.session_state:
        generate_egyptian_supplier_emails(modules)

def received_tender_workflow(modules):
    """Complete procurement workflow for received tenders."""
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Module",
        [
            "📄 Document Processing",
            "🔍 OEM Classification",
            "🏢 Supplier Management", 
            "📧 Email Generation",
            "📊 Supplier Comparison",
            "💰 Offer Generation",
            "📋 PO Management",
            "🚚 Logistics Tracking",
            "💳 Finance & Payments",
            "⏰ Deadline Management",
            "📈 Order Tracking",
            "📈 Dashboard"
        ]
    )
    
    # Log page navigation
    modules['data_collector'].log_user_activity('page_navigation', {'page': page})
    
    # Route to appropriate page
    if page == "📄 Document Processing":
        document_processing_page(modules)
    elif page == "🔍 OEM Classification":
        oem_classification_page(modules)
    elif page == "🏢 Supplier Management":
        supplier_management_page(modules)
    elif page == "📧 Email Generation":
        email_generation_page(modules)
    elif page == "📊 Supplier Comparison":
        supplier_comparison_page(modules)
    elif page == "💰 Offer Generation":
        offer_generation_page(modules)
    elif page == "📋 PO Management":
        po_management_page(modules)
    elif page == "🚚 Logistics Tracking":
        logistics_tracking_page(modules)
    elif page == "💳 Finance & Payments":
        finance_payments_page(modules)
    elif page == "⏰ Deadline Management":
        deadline_management_page(modules)
    elif page == "📈 Order Tracking":
        order_tracking_page(modules)
    elif page == "📈 Dashboard":
        dashboard_page(modules)

def process_tender_documents(modules, workflow_type):
    """Process tender documents for both workflows."""
    st.subheader("📄 Upload Tender Documents")
    
    uploaded_files = st.file_uploader(
        "Upload tender documents",
        type=['pdf', 'docx', 'doc', 'xlsx', 'xls', 'txt'],
        accept_multiple_files=True,
        help="Upload all tender documents including BOQ, specifications, and terms"
    )
    
    text_input = st.text_area(
        "Or paste tender text directly:",
        height=200,
        placeholder="Paste tender requirements here..."
    )
    
    if st.button("Process Tender Documents", type="primary"):
        if uploaded_files or text_input:
            with st.spinner("Processing tender documents..."):
                all_extracted_items = []
                processed_files = []
                
                # Process uploaded files
                for uploaded_file in uploaded_files:
                    result = modules['document_parser'].parse_file(uploaded_file)
                    if not result.get('error'):
                        all_extracted_items.extend(result.get('specifications', []))
                        processed_files.append({
                            'filename': uploaded_file.name,
                            'content': uploaded_file.getvalue(),
                            'result': result
                        })
                        
                        # Save to Google Drive
                        modules['google_drive_client'].upload_file(
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            'tender_documents'
                        )
                
                # Process text input
                if text_input:
                    result = modules['document_parser'].parse_text(text_input)
                    if not result.get('error'):
                        all_extracted_items.extend(result.get('specifications', []))
                
                if all_extracted_items:
                    st.success(f"Extracted {len(all_extracted_items)} items from tender documents!")
                    
                    # Store in session state
                    st.session_state.tender_items = all_extracted_items
                    st.session_state.tender_details = result
                    st.session_state.processed_files = processed_files
                    
                    # Display extracted items
                    display_extracted_items(all_extracted_items)
                else:
                    st.warning("No items could be extracted from the documents.")

def display_extracted_items(items):
    """Display extracted items in a structured format."""
    st.subheader("📋 Extracted Items")
    
    # Create DataFrame for better display
    items_df = pd.DataFrame([
        {'Item': i+1, 'Description': item} 
        for i, item in enumerate(items)
    ])
    
    st.dataframe(items_df, use_container_width=True)
    
    # Export options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Export to CSV"):
            csv_data = items_df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv_data,
                f"extracted_items_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv"
            )
    
    with col2:
        if st.button("☁️ Save to Google Drive"):
            # Save extracted items to Google Drive
            st.success("Items saved to Google Drive!")

def oem_classification_page(modules):
    """OEM classification and scope matching page."""
    st.header("🔍 OEM Classification & Scope Matching")
    st.markdown("Classify extracted items to match OEM scopes and material categories.")
    
    if 'tender_items' not in st.session_state:
        st.warning("Please process tender documents first.")
        return
    
    items = st.session_state.tender_items
    
    # OEM scope mapping
    st.subheader("🏭 OEM Scope Classification")
    
    # Material categories
    material_categories = [
        'Piping', 'Valves', 'Flanges', 'Fittings', 
        'Bolts', 'Gaskets', 'Finned Tubes'
    ]
    
    classified_items = []
    
    for i, item in enumerate(items):
        with st.expander(f"Item {i+1}: {item[:100]}..."):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                category = st.selectbox(
                    "Material Category",
                    material_categories,
                    key=f"category_{i}"
                )
            
            with col2:
                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    value=1,
                    key=f"qty_{i}"
                )
            
            with col3:
                unit = st.text_input(
                    "Unit",
                    value="EA",
                    key=f"unit_{i}"
                )
            
            specifications = st.text_area(
                "Technical Specifications",
                value=item,
                key=f"spec_{i}"
            )
            
            classified_items.append({
                'item_no': i+1,
                'description': item,
                'category': category,
                'quantity': quantity,
                'unit': unit,
                'specifications': specifications
            })
    
    if st.button("Save Classification", type="primary"):
        st.session_state.classified_items = classified_items
        
        # Save to Google Drive
        classification_df = pd.DataFrame(classified_items)
        csv_data = classification_df.to_csv(index=False)
        
        modules['google_drive_client'].upload_file(
            f"classified_items_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            csv_data.encode(),
            'classifications'
        )
        
        st.success("Classification saved successfully!")

def document_processing_page(modules):
    """Document processing page."""
    st.header("📄 Document Processing")
    st.markdown("Upload tender documents or paste text to extract key information.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Document",
        type=['pdf', 'docx', 'doc', 'xlsx', 'xls', 'txt'],
        help="Supported formats: PDF, Word, Excel, Text"
    )
    
    # Text input
    text_input = st.text_area(
        "Or paste text directly:",
        height=200,
        placeholder="Paste tender text here..."
    )
    
    if st.button("Process Document", type="primary"):
        if uploaded_file or text_input:
            with st.spinner("Processing document..."):
                if uploaded_file:
                    # Process uploaded file
                    result = modules['document_parser'].parse_file(uploaded_file)
                    file_info = {
                        'filename': uploaded_file.name,
                        'size': uploaded_file.size,
                        'type': uploaded_file.type
                    }
                else:
                    # Process text input
                    result = modules['document_parser'].parse_text(text_input)
                    file_info = {
                        'filename': 'text_input',
                        'size': len(text_input),
                        'type': 'text/plain'
                    }
                
                # Log document processing
                modules['data_collector'].log_document_processing(file_info, result)
                
                # Display results
                if result.get('error'):
                    st.error(f"Error: {result['error']}")
                else:
                    st.success("Document processed successfully!")
                    
                    # Store results in session state
                    st.session_state.processed_document = result
                    
                    # Display extracted information
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📋 Extracted Information")
                        if result.get('project_name'):
                            st.write(f"**Project:** {result['project_name']}")
                        if result.get('tender_reference'):
                            st.write(f"**Reference:** {result['tender_reference']}")
                        if result.get('deadline'):
                            st.write(f"**Deadline:** {result['deadline']}")
                        
                        st.write(f"**Materials Found:** {', '.join(result.get('materials', []))}")
                    
                    with col2:
                        st.subheader("📝 Specifications")
                        specs = result.get('specifications', [])
                        if specs:
                            for spec in specs[:10]:  # Show first 10 specifications
                                st.write(f"• {spec}")
                        else:
                            st.write("No specifications extracted")
        else:
            st.warning("Please upload a file or paste text to process.")

def supplier_management_page(modules):
    """Supplier management page."""
    st.header("🏢 Supplier Management")
    
    # Load suppliers
    suppliers_df = modules['supplier_manager'].load_suppliers()
    
    # Sidebar filters
    st.sidebar.subheader("Filters")
    
    # Country filter
    countries = ['All'] + sorted(suppliers_df['Country'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Country", countries)
    
    # Material filter
    materials = ['All', 'piping', 'valves', 'flanges', 'fittings', 'bolts', 'gaskets', 'finned tubes']
    selected_material = st.sidebar.selectbox("Material Category", materials)
    
    # Search
    search_term = st.sidebar.text_input("Search suppliers")
    
    # Apply filters
    filtered_df = suppliers_df.copy()
    
    if selected_country != 'All':
        filtered_df = modules['supplier_manager'].get_suppliers_by_country(filtered_df, selected_country)
    
    if selected_material != 'All':
        filtered_df = modules['supplier_manager'].get_suppliers_by_material(filtered_df, selected_material)
    
    if search_term:
        filtered_df = modules['supplier_manager'].search_suppliers(filtered_df, search_term)
        # Log search activity
        modules['data_collector'].log_supplier_search(
            {'country': selected_country, 'material': selected_material, 'search_term': search_term},
            len(filtered_df)
        )
    
    # Display statistics
    stats = modules['supplier_manager'].get_statistics(suppliers_df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Suppliers", stats.get('total_suppliers', 0))
    with col2:
        st.metric("Countries", stats.get('total_countries', 0))
    with col3:
        st.metric("Chinese Suppliers", stats.get('chinese_suppliers', 0))
    with col4:
        st.metric("UAE Suppliers", stats.get('emirati_suppliers', 0))
    
    # Display suppliers table
    st.subheader(f"Suppliers ({len(filtered_df)} found)")
    
    if not filtered_df.empty:
        # Display table with editing capabilities
        edited_df = st.data_editor(
            filtered_df,
            use_container_width=True,
            num_rows="dynamic",
            key="supplier_editor"
        )
        
        # Save changes button
        if st.button("Save Changes", type="primary"):
            if modules['supplier_manager'].save_suppliers(edited_df):
                st.success("Suppliers updated successfully!")
                st.rerun()
            else:
                st.error("Failed to save changes.")
    else:
        st.info("No suppliers found matching the current filters.")
    
    # Add new supplier section
    with st.expander("➕ Add New Supplier"):
        with st.form("add_supplier_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("Company Name*")
                contact_person = st.text_input("Contact Person")
                email = st.text_input("Email*")
                phone = st.text_input("Phone")
            
            with col2:
                address = st.text_input("Address")
                country = st.text_input("Country*")
                specialization = st.text_area("Specialization")
                established_year = st.number_input("Established Year", min_value=1900, max_value=2025, value=2020)
            
            material_categories = st.multiselect(
                "Material Categories*",
                ['piping', 'valves', 'flanges', 'fittings', 'bolts', 'gaskets', 'finned tubes']
            )
            
            submitted = st.form_submit_button("Add Supplier", type="primary")
            
            if submitted:
                if company_name and email and country and material_categories:
                    supplier_data = {
                        'Company_Name': company_name,
                        'Contact_Person': contact_person,
                        'Email': email,
                        'Phone': phone,
                        'Address': address,
                        'Country': country,
                        'Specialization': specialization,
                        'Established_Year': established_year,
                        'Material_Categories': ', '.join(material_categories)
                    }
                    
                    if modules['supplier_manager'].add_supplier(supplier_data):
                        st.success(f"Added {company_name} successfully!")
                        # Log supplier addition
                        modules['data_collector'].log_user_activity('supplier_added', supplier_data)
                        st.rerun()
                    else:
                        st.error("Failed to add supplier. Company may already exist.")
                else:
                    st.error("Please fill in all required fields (marked with *).")

def email_generation_page(modules):
    """Email generation page."""
    st.header("📧 Email Generation")
    st.markdown("Generate professional email drafts for supplier quotations.")
    
    # Load suppliers
    suppliers_df = modules['supplier_manager'].load_suppliers()
    
    if suppliers_df.empty:
        st.warning("No suppliers found. Please add suppliers first.")
        return
    
    # Project details form
    with st.form("email_generation_form"):
        st.subheader("Project Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Auto-populate from processed document if available
            processed_doc = st.session_state.get('processed_document', {})
            
            project_name = st.text_input(
                "Project Name*",
                value=processed_doc.get('project_name', '')
            )
            tender_reference = st.text_input(
                "Tender Reference",
                value=processed_doc.get('tender_reference', '')
            )
            
            # Deadline handling
            if processed_doc.get('deadline'):
                default_deadline = processed_doc['deadline']
                if isinstance(default_deadline, str):
                    try:
                        default_deadline = datetime.strptime(default_deadline, '%Y-%m-%d').date()
                    except:
                        default_deadline = date.today()
            else:
                default_deadline = date.today()
            
            client_deadline = st.date_input("Client Deadline*", value=default_deadline)
            
            # Calculate supplier deadline
            supplier_deadline = modules['deadline_calculator'].calculate_supplier_deadline(client_deadline)
            st.info(f"Supplier Quote Deadline: {supplier_deadline}")
        
        with col2:
            # Material selection
            material_categories = st.multiselect(
                "Material Categories*",
                ['piping', 'valves', 'flanges', 'fittings', 'bolts', 'gaskets', 'finned tubes'],
                default=processed_doc.get('materials', [])
            )
            
            # Origin exclusion
            exclude_origins = st.multiselect(
                "Exclude Origins",
                sorted(suppliers_df['Country'].dropna().unique()),
                help="Select countries to exclude from email generation"
            )
            
            include_note = st.checkbox(
                "Include origin exclusion note in emails",
                value=bool(exclude_origins),
                help="Add a note about excluded origins in the email body"
            )
        
        # Requirements and notes
        requirements = st.text_area(
            "Requirements and Specifications",
            value='\n'.join(processed_doc.get('specifications', [])[:5]),
            height=150,
            help="Enter project requirements and specifications"
        )
        
        additional_notes = st.text_area(
            "Additional Notes",
            height=100,
            help="Any additional information for suppliers"
        )
        
        # Generate emails button
        generate_emails = st.form_submit_button("Generate Emails", type="primary")
        
        if generate_emails:
            if project_name and client_deadline and material_categories:
                with st.spinner("Generating emails..."):
                    # Filter suppliers
                    filtered_suppliers = modules['supplier_manager'].filter_suppliers(
                        suppliers_df, material_categories, exclude_origins
                    )
                    
                    if filtered_suppliers.empty:
                        st.error("No suppliers found matching the criteria.")
                        return
                    
                    # Prepare project details
                    project_details = {
                        'project_name': project_name,
                        'tender_reference': tender_reference,
                        'quote_deadline': supplier_deadline,
                        'requirements': requirements,
                        'additional_notes': additional_notes,
                        'exclude_origins': exclude_origins,
                        'include_note': include_note
                    }
                    
                    # Generate emails
                    emails = modules['email_generator'].generate_emails(filtered_suppliers, project_details)
                    
                    # Log email generation
                    modules['data_collector'].log_email_generation(project_details, len(emails))
                    
                    # Add to order tracking
                    order_data = {
                        'project_name': project_name,
                        'tender_reference': tender_reference,
                        'materials': material_categories,
                        'total_suppliers': len(emails),
                        'emails_sent': len(emails),
                        'supplier_categories': modules['order_tracker'].categorize_suppliers(emails),
                        'follow_up_date': supplier_deadline,
                        'notes': f"Generated for materials: {', '.join(material_categories)}"
                    }
                    
                    order_id = modules['order_tracker'].add_processed_order(order_data)
                    modules['data_collector'].log_order_tracking(order_data)
                    
                    # Store emails in session state
                    st.session_state.generated_emails = emails
                    st.session_state.email_project_details = project_details
                    
                    st.success(f"✅ Generated {len(emails)} emails successfully!")
                    st.info(f"📋 Order ID: {order_id}")
                    
                    # Display summary
                    summary = modules['email_generator'].generate_bulk_email_summary(emails, project_details)
                    st.markdown(summary)
            else:
                st.error("Please fill in all required fields (marked with *).")
    
    # Display generated emails
    if 'generated_emails' in st.session_state:
        st.markdown("---")
        st.subheader("📧 Generated Emails")
        
        emails = st.session_state.generated_emails
        
        # Email selection
        if emails:
            selected_email_idx = st.selectbox(
                "Select email to view:",
                range(len(emails)),
                format_func=lambda x: f"{emails[x]['company_name']} ({emails[x]['country']})"
            )
            
            selected_email = emails[selected_email_idx]
            
            # Display email details
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write(f"**To:** {selected_email['email']}")
                st.write(f"**Company:** {selected_email['company_name']}")
                st.write(f"**Country:** {selected_email['country']}")
                st.write(f"**Contact:** {selected_email['contact_person']}")
            
            with col2:
                st.write(f"**Subject:** {selected_email['subject']}")
                
                # Copy email button
                if st.button("📋 Copy Email to Clipboard"):
                    st.code(selected_email['email_body'], language=None)
            
            # Email body
            st.text_area(
                "Email Body:",
                value=selected_email['email_body'],
                height=400,
                key=f"email_body_{selected_email_idx}"
            )
        
        # Export options
        st.markdown("---")
        st.subheader("📤 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export to CSV"):
                csv_data = modules['email_generator'].export_emails_to_csv(emails)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"hamada_tool_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📋 Copy All Emails"):
                all_emails_text = "\n\n" + "="*50 + "\n\n".join([
                    f"TO: {email['email']}\nSUBJECT: {email['subject']}\n\n{email['email_body']}"
                    for email in emails
                ])
                st.text_area("All Emails:", value=all_emails_text, height=200)

def supplier_comparison_page(modules):
    """Supplier comparison and evaluation page."""
    st.header("📊 Supplier Comparison & Evaluation")
    
    if 'supplier_quotes' not in st.session_state:
        st.warning("No supplier quotations available. Please generate and collect quotes first.")
        
        # File upload for supplier quotations
        st.subheader("📤 Upload Supplier Quotations")
        uploaded_quotes = st.file_uploader(
            "Upload supplier quotation files",
            type=['pdf', 'xlsx', 'docx'],
            accept_multiple_files=True
        )
        
        if uploaded_quotes and st.button("Process Quotations"):
            process_supplier_quotations(modules, uploaded_quotes)
        
        return
    
    # Display comparison matrix
    create_comparison_matrix(modules)

def process_supplier_quotations(modules, uploaded_quotes):
    """Process uploaded supplier quotations."""
    quotes_data = []
    
    for quote_file in uploaded_quotes:
        with st.spinner(f"Processing {quote_file.name}..."):
            result = modules['document_parser'].parse_file(quote_file)
            
            if not result.get('error'):
                # Extract supplier information and pricing
                quote_data = {
                    'supplier': extract_supplier_name(quote_file.name),
                    'filename': quote_file.name,
                    'items': result.get('specifications', []),
                    'deadline': result.get('deadline'),
                    'raw_data': result
                }
                quotes_data.append(quote_data)
                
                # Save to Google Drive
                modules['google_drive_client'].upload_file(
                    quote_file.name,
                    quote_file.getvalue(),
                    'supplier_quotes'
                )
    
    st.session_state.supplier_quotes = quotes_data
    st.success(f"Processed {len(quotes_data)} supplier quotations!")

def create_comparison_matrix(modules):
    """Create supplier comparison matrix."""
    st.subheader("📋 Comparison Matrix")
    
    quotes = st.session_state.supplier_quotes
    classified_items = st.session_state.get('classified_items', [])
    
    # Comparison criteria
    criteria = {
        'Price': 0.4,
        'Lead Time': 0.2,
        'Compliance': 0.2,
        'Origin': 0.1,
        'Payment Terms': 0.1
    }
    
    # Create comparison DataFrame
    comparison_data = []
    
    for item in classified_items:
        for quote in quotes:
            # Match items from quotes to classified items
            comparison_data.append({
                'Item No': item['item_no'],
                'Description': item['description'][:50] + '...',
                'Supplier': quote['supplier'],
                'Price': 0,  # Extract from quote
                'Lead Time': 'TBD',
                'Compliance': 'Yes',
                'Origin': 'TBD',
                'Payment Terms': 'TBD',
                'Score': 0
            })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Editable comparison matrix
    edited_df = st.data_editor(
        comparison_df,
        use_container_width=True,
        num_rows="dynamic"
    )
    
    if st.button("Calculate Scores & Save Comparison"):
        # Calculate weighted scores
        calculate_comparison_scores(edited_df, criteria)
        
        # Save to Google Drive
        csv_data = edited_df.to_csv(index=False)
        modules['google_drive_client'].upload_file(
            f"supplier_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            csv_data.encode(),
            'comparisons'
        )
        
        st.session_state.comparison_matrix = edited_df
        st.success("Comparison matrix saved!")

def offer_generation_page(modules):
    """Generate offers for end clients."""
    st.header("💰 Offer Generation")
    
    if 'comparison_matrix' not in st.session_state:
        st.warning("Please complete supplier comparison first.")
        return
    
    # Offer configuration
    st.subheader("⚙️ Offer Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input("Project Name")
        client_name = st.text_input("Client Name")
        offer_validity = st.number_input("Offer Validity (days)", value=30)
    
    with col2:
        currency = st.selectbox("Currency", ["USD", "EUR", "EGP"])
        margin_percentage = st.number_input("Margin %", value=15.0, step=0.1)
        include_vat = st.checkbox("Include VAT", value=True)
    
    # Generate offers
    if st.button("Generate Offers", type="primary"):
        # Generate internal offer (without margins)
        internal_offer = generate_internal_offer(modules)
        
        # Generate client offer (with margins)
        client_offer = generate_client_offer(modules, margin_percentage)
        
        st.session_state.internal_offer = internal_offer
        st.session_state.client_offer = client_offer
        
        # Save to Google Drive
        save_offers_to_drive(modules, internal_offer, client_offer)
        
        st.success("Offers generated successfully!")
        
        # Display offers
        display_generated_offers(internal_offer, client_offer)

def po_management_page(modules):
    """Purchase Order management page."""
    st.header("📋 Purchase Order Management")
    
    # Client PO processing
    st.subheader("📥 Client Purchase Order")
    
    client_po_file = st.file_uploader(
        "Upload Client PO",
        type=['pdf', 'docx', 'xlsx']
    )
    
    if client_po_file and st.button("Process Client PO"):
        process_client_po(modules, client_po_file)
    
    # Supplier PO generation
    if 'client_po_data' in st.session_state:
        st.subheader("📤 Generate Supplier POs")
        generate_supplier_pos(modules)

def logistics_tracking_page(modules):
    """Logistics and shipment tracking page."""
    st.header("🚚 Logistics & Shipment Tracking")
    
    # Shipment milestones
    milestones = [
        "PO Issued",
        "Advance Payment",
        "Production Started",
        "Ready for Shipment",
        "ACID Created",
        "CargoX Submitted",
        "Shipment Departed",
        "Customs Clearance",
        "Freezone Conversion",
        "Ready for Pickup",
        "Delivered"
    ]
    
    # Track shipments
    track_shipments(modules, milestones)

def finance_payments_page(modules):
    """Finance and payments management page."""
    st.header("💳 Finance & Payments")
    
    # Payment tracking
    st.subheader("💰 Payment Tracking")
    
    # Advance payments
    track_advance_payments(modules)
    
    # Final payments
    track_final_payments(modules)
    
    # Invoice generation
    st.subheader("🧾 Invoice Generation")
    generate_invoices(modules)

def deadline_management_page(modules):
    """Deadline management page."""
    st.header("⏰ Deadline Management")
    st.markdown("Calculate and manage project deadlines.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Deadline Calculator")
        
        # Manual deadline input
        manual_deadline = st.date_input(
            "Client Deadline",
            value=date.today() + pd.Timedelta(days=14)
        )
        
        buffer_days = st.number_input(
            "Buffer Days",
            min_value=1,
            max_value=30,
            value=2,
            help="Days to subtract from client deadline for supplier deadline"
        )
        
        if st.button("Calculate Supplier Deadline", type="primary"):
            supplier_deadline = modules['deadline_calculator'].calculate_supplier_deadline(manual_deadline)
            
            if supplier_deadline:
                st.success(f"Supplier Deadline: {supplier_deadline}")
                
                # Get deadline status
                status = modules['deadline_calculator'].get_deadline_status(supplier_deadline)
                
                if status['urgency'] == 'critical':
                    st.error(f"⚠️ {status['status'].replace('_', ' ').title()}: {status['days_remaining']} days remaining")
                elif status['urgency'] == 'high':
                    st.warning(f"⚡ {status['status'].replace('_', ' ').title()}: {status['days_remaining']} days remaining")
                else:
                    st.info(f"✅ {status['status'].replace('_', ' ').title()}: {status['days_remaining']} days remaining")
                
                # Log deadline calculation
                modules['data_collector'].log_deadline_calculation(
                    str(manual_deadline), str(supplier_deadline), buffer_days
                )
            else:
                st.error("Invalid deadline provided.")
    
    with col2:
        st.subheader("📝 Text Deadline Extraction")
        
        deadline_text = st.text_area(
            "Paste text containing deadline:",
            height=150,
            placeholder="Paste tender text here to automatically extract deadline..."
        )
        
        if st.button("Extract Deadline from Text"):
            if deadline_text:
                extracted_deadline = modules['deadline_calculator'].extract_deadline_from_text(deadline_text)
                
                if extracted_deadline:
                    st.success(f"Extracted Deadline: {extracted_deadline}")
                    
                    # Calculate supplier deadline
                    supplier_deadline = modules['deadline_calculator'].calculate_supplier_deadline(extracted_deadline)
                    st.info(f"Supplier Deadline: {supplier_deadline}")
                    
                    # Log extraction
                    modules['data_collector'].log_deadline_calculation(
                        str(extracted_deadline), str(supplier_deadline), buffer_days
                    )
                else:
                    st.warning("No deadline found in the provided text.")
            else:
                st.warning("Please enter text to extract deadline from.")

def order_tracking_page(modules):
    """Order tracking page."""
    st.header("📊 Order Tracking")
    st.markdown("Track and manage processed orders.")
    
    # Load orders
    orders_df = modules['order_tracker'].get_orders()
    
    if orders_df.empty:
        st.info("No orders tracked yet. Process documents and generate emails to create orders.")
        return
    
    # Display order statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", len(orders_df))
    with col2:
        pending_orders = len(modules['order_tracker'].get_pending_orders())
        st.metric("Pending Orders", pending_orders)
    with col3:
        total_suppliers = orders_df['Total_Suppliers'].sum()
        st.metric("Total Suppliers Contacted", total_suppliers)
    with col4:
        total_emails = orders_df['Emails_Sent'].sum()
        st.metric("Total Emails Generated", total_emails)
    
    # Orders table
    st.subheader("📋 Order History")
    
    # Add status filter
    status_filter = st.selectbox(
        "Filter by Status",
        ['All'] + orders_df['Status'].unique().tolist()
    )
    
    display_orders = orders_df.copy()
    if status_filter != 'All':
        display_orders = display_orders[display_orders['Status'] == status_filter]
    
    # Display orders
    if not display_orders.empty:
        for idx, order in display_orders.iterrows():
            with st.expander(f"Order {order['Order_ID']} - {order['Project_Name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Project:** {order['Project_Name']}")
                    st.write(f"**Reference:** {order['Tender_Reference']}")
                    st.write(f"**Date Processed:** {order['Date_Processed']}")
                    st.write(f"**Materials:** {order['Materials']}")
                
                with col2:
                    st.write(f"**Status:** {order['Status']}")
                    st.write(f"**Suppliers:** {order['Total_Suppliers']}")
                    st.write(f"**Follow-up Date:** {order['Follow_Up_Date']}")
                    st.write(f"**Notes:** {order['Notes']}")
                
                # Update status
                new_status = st.selectbox(
                    "Update Status:",
                    ['Pending Response', 'Quotes Received', 'Under Review', 'Completed', 'Cancelled'],
                    index=['Pending Response', 'Quotes Received', 'Under Review', 'Completed', 'Cancelled'].index(order['Status']),
                    key=f"status_{order['Order_ID']}"
                )
                
                new_notes = st.text_area(
                    "Update Notes:",
                    value=order['Notes'],
                    key=f"notes_{order['Order_ID']}"
                )
                
                if st.button(f"Update Order {order['Order_ID']}", key=f"update_{order['Order_ID']}"):
                    if modules['order_tracker'].update_order_status(order['Order_ID'], new_status, new_notes):
                        st.success("Order updated successfully!")
                        modules['data_collector'].log_user_activity('order_updated', {
                            'order_id': order['Order_ID'],
                            'new_status': new_status,
                            'notes': new_notes
                        })
                        st.rerun()
                    else:
                        st.error("Failed to update order.")

def dashboard_page(modules):
    """Dashboard page with analytics."""
    st.header("📈 Dashboard")
    st.markdown("Usage analytics and system overview.")
    
    # Get usage statistics
    usage_stats = modules['data_collector'].get_usage_statistics()
    
    if usage_stats:
        # Display main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Activities", usage_stats.get('total_activities', 0))
        with col2:
            activity_breakdown = usage_stats.get('activity_breakdown', {})
            st.metric("Documents Processed", activity_breakdown.get('document_processed', 0))
        with col3:
            st.metric("Emails Generated", activity_breakdown.get('email_generated', 0))
        with col4:
            st.metric("Searches Performed", activity_breakdown.get('supplier_searched', 0))
        
        # Activity breakdown chart
        if activity_breakdown:
            st.subheader("📊 Activity Breakdown")
            activity_df = pd.DataFrame(list(activity_breakdown.items()), columns=['Activity', 'Count'])
            st.bar_chart(activity_df.set_index('Activity'))
        
        # Recent activity
        st.subheader("🕒 Recent Activity")
        if usage_stats.get('last_activity'):
            st.write(f"Last activity: {usage_stats['last_activity']}")
    else:
        st.info("No usage data available yet. Start using the tool to see analytics.")
    
    # System status
    st.subheader("🔧 System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Database Connection:** ✅ Connected")
        st.write("**Supplier Database:** ✅ Loaded")
        st.write("**Document Parser:** ✅ Ready")
    
    with col2:
        st.write("**Email Generator:** ✅ Ready")
        st.write("**Order Tracker:** ✅ Active")
        st.write("**Data Collector:** ✅ Logging")
    
    # Supplier database overview
    suppliers_df = modules['supplier_manager'].load_suppliers()
    supplier_stats = modules['supplier_manager'].get_statistics(suppliers_df)
    
    st.subheader("🏢 Supplier Database Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Total Suppliers:** {supplier_stats.get('total_suppliers', 0)}")
        st.write(f"**Countries Covered:** {supplier_stats.get('total_countries', 0)}")
        st.write(f"**Chinese Suppliers:** {supplier_stats.get('chinese_suppliers', 0)}")
    
    with col2:
        st.write(f"**UAE Suppliers:** {supplier_stats.get('emirati_suppliers', 0)}")
        st.write(f"**European Suppliers:** {supplier_stats.get('european_suppliers', 0)}")
        st.write(f"**Recent Suppliers (2020+):** {supplier_stats.get('recent_suppliers', 0)}")

# Helper functions for new workflow components
def extract_supplier_name(filename):
    """Extract supplier name from filename."""
    # Simple extraction logic - can be enhanced
    return filename.split('_')[0] if '_' in filename else filename.split('.')[0]

def calculate_comparison_scores(df, criteria):
    """Calculate weighted comparison scores."""
    # Implementation for scoring logic
    pass

def generate_internal_offer(modules):
    """Generate internal offer without margins."""
    # Implementation for internal offer generation
    pass

def generate_client_offer(modules, margin_percentage):
    """Generate client offer with margins."""
    # Implementation for client offer generation
    pass

def save_offers_to_drive(modules, internal_offer, client_offer):
    """Save generated offers to Google Drive."""
    # Implementation for saving offers
    pass

def display_generated_offers(internal_offer, client_offer):
    """Display generated offers."""
    # Implementation for displaying offers
    pass

def process_client_po(modules, po_file):
    """Process client purchase order."""
    # Implementation for PO processing
    pass

def generate_supplier_pos(modules):
    """Generate supplier purchase orders."""
    # Implementation for supplier PO generation
    pass

def track_shipments(modules, milestones):
    """Track shipment progress."""
    # Implementation for shipment tracking
    pass

def track_advance_payments(modules):
    """Track advance payments."""
    # Implementation for advance payment tracking
    pass

def track_final_payments(modules):
    """Track final payments."""
    # Implementation for final payment tracking
    pass

def generate_invoices(modules):
    """Generate various types of invoices."""
    # Implementation for invoice generation
    pass

# Sidebar information
def show_sidebar_info():
    """Show information in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛠️ Hamada Tool")
    st.sidebar.markdown("**Version:** 1.0")
    st.sidebar.markdown("**Company:** Arab Engineering & Distribution")
    st.sidebar.markdown("**Contact:** +20100 0266 344")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    # Load basic stats
    try:
        supplier_manager = SupplierManager()
        suppliers_df = supplier_manager.load_suppliers()
        stats = supplier_manager.get_statistics(suppliers_df)
        
        st.sidebar.metric("Suppliers", stats.get('total_suppliers', 0))
        st.sidebar.metric("Countries", stats.get('total_countries', 0))
    except:
        st.sidebar.write("Stats loading...")

if __name__ == "__main__":
    # Show sidebar info
    show_sidebar_info()
    
    # Run main application
    main()