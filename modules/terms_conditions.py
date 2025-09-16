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
    page_title="Hamada Tool - Oil & Gas Procurement",
    page_icon="🛠️",
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
        'terms_conditions': TermsConditions()
    }

def main():
    """Main application function."""
    
    # Initialize modules
    modules = initialize_modules()
    
    # Check terms acceptance first
    if not modules['terms_conditions'].check_terms_acceptance():
        st.title("🛠️ Welcome to Hamada Tool")
        st.markdown("### Oil & Gas Procurement Automation Platform")
        st.markdown("---")
        
        # Show terms and conditions
        accepted = modules['terms_conditions'].show_terms_and_conditions()
        
        if accepted:
            # Log terms acceptance
            acceptance_data = modules['terms_conditions'].get_acceptance_data()
            modules['data_collector'].log_terms_acceptance('user_' + str(datetime.now().timestamp()), acceptance_data)
        
        return
    
    # Main application header
    st.title("🛠️ Hamada Tool")
    st.markdown("### Automated Oil & Gas Procurement Solution")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Module",
        [
            "📄 Document Processing",
            "🏢 Supplier Management", 
            "📧 Email Generation",
            "⏰ Deadline Management",
            "📊 Order Tracking",
            "📈 Dashboard"
        ]
    )
    
    # Log page navigation
    modules['data_collector'].log_user_activity('page_navigation', {'page': page})
    
    # Route to appropriate page
    if page == "📄 Document Processing":
        document_processing_page(modules)
    elif page == "🏢 Supplier Management":
        supplier_management_page(modules)
    elif page == "📧 Email Generation":
        email_generation_page(modules)
    elif page == "⏰ Deadline Management":
        deadline_management_page(modules)
    elif page == "📊 Order Tracking":
        order_tracking_page(modules)
    elif page == "📈 Dashboard":
        dashboard_page(modules)

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

def supplier_management_page(modules):
    """Enhanced supplier management page."""
    st.header("🏢 Supplier Management")
    
    # Load suppliers
    suppliers_df = modules['supplier_manager'].load_suppliers()
    
    # Display current statistics
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
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 View Suppliers", "➕ Add Supplier", "📊 Analytics"])
    
    with tab1:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            countries = ['All'] + sorted(suppliers_df['Country'].dropna().unique().tolist())
            filter_country = st.selectbox("Filter by Country", countries)
        
        with col2:
            materials = ['All', 'piping', 'valves', 'flanges', 'fittings', 'bolts', 'gaskets', 'finned tubes']
            filter_material = st.selectbox("Filter by Material", materials)
        
        with col3:
            search_query = st.text_input("Search suppliers")
        
        # Apply filters
        display_df = suppliers_df.copy()
        
        if filter_country != 'All':
            display_df = modules['supplier_manager'].get_suppliers_by_country(display_df, filter_country)
        
        if filter_material != 'All':
            display_df = modules['supplier_manager'].get_suppliers_by_material(display_df, filter_material)
        
        if search_query:
            display_df = modules['supplier_manager'].search_suppliers(display_df, search_query)
        
        # Display filtered results
        st.write(f"Showing {len(display_df)} suppliers")
        
        if not display_df.empty:
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No suppliers match the current filters.")
    
    with tab2:
        # Add new supplier form
        st.subheader("Add New Supplier")
        
        with st.form("new_supplier_form"):
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
            
            submit_new = st.form_submit_button("Add Supplier", type="primary")
            
            if submit_new:
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
                        modules['data_collector'].log_user_activity('supplier_added', supplier_data)
                        st.rerun()
                    else:
                        st.error("Failed to add supplier. Company may already exist.")
                else:
                    st.error("Please fill in all required fields (marked with *).")
    
    with tab3:
        # Analytics and insights
        st.subheader("Supplier Database Analytics")
        
        if not suppliers_df.empty:
            # Country distribution
            country_counts = suppliers_df['Country'].value_counts()
            st.bar_chart(country_counts.head(10))
            
            # Material category distribution
            st.subheader("Material Categories Distribution")
            material_data = []
            for material in ['piping', 'valves', 'flanges', 'fittings', 'bolts', 'gaskets', 'finned tubes']:
                count = len(modules['supplier_manager'].get_suppliers_by_material(suppliers_df, material))
                material_data.append({'Material': material, 'Count': count})
            
            material_df = pd.DataFrame(material_data)
            st.bar_chart(material_df.set_index('Material'))

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