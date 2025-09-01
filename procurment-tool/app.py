import streamlit as st
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
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
    page_icon="⚙️",
    layout="wide"
)

# Initialize session state
if 'supplier_manager' not in st.session_state:
    st.session_state.supplier_manager = SupplierManager()
if 'document_parser' not in st.session_state:
    st.session_state.document_parser = DocumentParser()
if 'email_generator' not in st.session_state:
    st.session_state.email_generator = EmailGenerator()
if 'deadline_calculator' not in st.session_state:
    st.session_state.deadline_calculator = DeadlineCalculator()

if 'order_tracker' not in st.session_state:
    st.session_state.order_tracker = OrderTracker()
if 'data_collector' not in st.session_state:
    st.session_state.data_collector = DataCollector()
if 'terms_conditions' not in st.session_state:
    st.session_state.terms_conditions = TermsConditions()

# Check terms and conditions acceptance
if not st.session_state.terms_conditions.check_terms_acceptance():
    st.session_state.terms_conditions.show_terms_and_conditions()
    st.stop()

# Main title and description
st.title("⚙️ Hamada Tool")
st.subheader("Automated Tender-Reading & Supplier-Quoting Productivity Tool")
st.markdown("**Arab Engineering & Distribution Company** - Oil & Gas Procurement Solutions")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Module",
    ["📄 Document Processing", "🏢 Supplier Management", "📧 Email Generation", "⏰ Deadline Management", "📋 Order Tracking", "📊 Dashboard"]
)

# Sidebar additional options
st.sidebar.markdown("---")
st.sidebar.markdown("### Additional Options")

if st.sidebar.button("📄 View Terms & Conditions"):
    st.session_state.terms_conditions.show_terms_and_conditions()

if st.sidebar.button("🔒 Privacy Policy"):
    st.session_state.terms_conditions.show_privacy_policy()

# Show data collection status
st.sidebar.markdown("---")
st.sidebar.markdown("### Data Collection Status")
if st.session_state.terms_conditions.check_terms_acceptance():
    st.sidebar.success("✅ Terms Accepted")
    st.sidebar.success("✅ Data Collection Enabled")
else:
    st.sidebar.error("❌ Terms Not Accepted")

# Material categories
MATERIAL_CATEGORIES = ["piping", "valves", "flanges", "fittings", "bolts", "gaskets", "finned tubes"]

if page == "📄 Document Processing":
    st.header("Document Processing")
    st.markdown("Upload tender documents for automated parsing and information extraction.")
    
    # File upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Upload Tender Documents",
            type=['pdf', 'docx', 'xlsx', 'xls', 'txt'],
            accept_multiple_files=True,
            help="Supported formats: PDF (native & scanned), Word documents, Excel files, and text files"
        )
        
        # Text input option
        st.markdown("**Or paste text directly:**")
        pasted_text = st.text_area(
            "Paste tender text here",
            height=200,
            placeholder="Copy and paste tender requirements here..."
        )
    
    with col2:
        st.markdown("**Processing Options:**")
        extract_deadlines = st.checkbox("Extract deadlines automatically", value=True)
        extract_materials = st.checkbox("Identify material categories", value=True)
        extract_specifications = st.checkbox("Parse technical specifications", value=True)
    
    # Process documents
    if st.button("Process Documents", type="primary"):
        if uploaded_files or pasted_text.strip():
            with st.spinner("Processing documents..."):
                try:
                    results = []
                    
                    # Process uploaded files
                    if uploaded_files:
                        for file in uploaded_files:
                            result = st.session_state.document_parser.parse_file(file)
                            result['source'] = f"File: {file.name}"
                            results.append(result)
                    
                    # Process pasted text
                    if pasted_text.strip():
                        result = st.session_state.document_parser.parse_text(pasted_text)
                        result['source'] = "Pasted Text"
                        results.append(result)
                    
                    # Display results
                    st.success(f"Successfully processed {len(results)} document(s)")
                    
                    # Store processed data in session state for use in other modules
                    st.session_state.processed_documents = results
                    
                    # Log document processing activity
                    for result in results:
                        file_info = {
                            'source': result.get('source', 'unknown'),
                            'file_size': len(result.get('text', '')),
                            'extraction_date': datetime.now().isoformat()
                        }
                        st.session_state.data_collector.log_document_processing(file_info, result)
                    
                    for i, result in enumerate(results):
                        with st.expander(f"📄 {result['source']}", expanded=True):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Extracted Text:**")
                                st.text_area(
                                    "Content",
                                    value=result.get('text', 'No text extracted')[:500] + "..." if len(result.get('text', '')) > 500 else result.get('text', 'No text extracted'),
                                    height=150,
                                    key=f"text_{i}",
                                    disabled=True
                                )
                                
                                if extract_deadlines and result.get('deadline'):
                                    st.markdown("**📅 Detected Deadline:**")
                                    st.info(f"Client Deadline: {result['deadline']}")
                                    
                                    # Calculate supplier deadline
                                    supplier_deadline = st.session_state.deadline_calculator.calculate_supplier_deadline(result['deadline'])
                                    if supplier_deadline:
                                        st.warning(f"Supplier Quote Due: {supplier_deadline}")
                                        # Store deadline in session state
                                        st.session_state.supplier_deadline = supplier_deadline
                                        st.session_state.client_deadline = result['deadline']
                            
                            with col2:
                                if extract_materials and result.get('materials'):
                                    st.markdown("**🔧 Detected Materials:**")
                                    materials_text = ", ".join(result['materials'])
                                    st.info(f"Materials: {materials_text}")
                                    # Store materials in session state
                                    st.session_state.detected_materials = result['materials']
                                
                                if extract_specifications and result.get('specifications'):
                                    st.markdown("**📋 Technical Specifications:**")
                                    for spec in result['specifications']:
                                        st.write(f"• {spec}")
                                    # Store specifications in session state
                                    st.session_state.detected_specifications = result['specifications']
                                
                                # Store project info in session state
                                if result.get('project_name'):
                                    st.session_state.detected_project_name = result['project_name']
                                    st.markdown("**📋 Project Name:**")
                                    st.info(f"Project: {result['project_name']}")
                                    
                                if result.get('tender_reference'):
                                    st.session_state.detected_tender_reference = result['tender_reference']
                                    st.markdown("**📄 Tender Reference:**")
                                    st.info(f"Reference: {result['tender_reference']}")
                    
                    # Next steps section
                    st.markdown("---")
                    st.markdown("### 🚀 Next Steps")
                    
                    st.info("📧 Go to **Email Generation** tab to create supplier quotation requests based on the processed tender")
                    st.info("🏢 Go to **Supplier Management** tab to filter suppliers by detected materials")
                    
                    if result.get('materials'):
                        st.success(f"✅ Ready to find suppliers for: {', '.join(result['materials'])}")
                    if result.get('deadline'):
                        st.success(f"✅ Supplier deadline calculated: {st.session_state.get('supplier_deadline', 'N/A')}")
                
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")
        else:
            st.warning("Please upload documents or paste text to process.")

elif page == "🏢 Supplier Management":
    st.header("Supplier Management")
    st.markdown("Manage your supplier database with CRUD operations.")
    
    # Load current suppliers
    suppliers_df = st.session_state.supplier_manager.load_suppliers()
    
    # Tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View Suppliers", "➕ Add Supplier", "✏️ Edit Supplier", "📊 Statistics"])
    
    with tab1:
        st.subheader("Current Supplier Database")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            # Handle NaN values in Country column
            unique_countries = suppliers_df['Country'].dropna().unique().tolist()
            country_filter = st.selectbox(
                "Filter by Country",
                ["All"] + sorted([str(country) for country in unique_countries])
            )
        with col2:
            category_filter = st.selectbox(
                "Filter by Material Category",
                ["All"] + MATERIAL_CATEGORIES
            )
        with col3:
            search_term = st.text_input("Search Company Name")
        
        # Apply filters
        filtered_df = suppliers_df.copy()
        if country_filter != "All":
            filtered_df = filtered_df[filtered_df['Country'] == country_filter]
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['Material_Categories'].str.contains(category_filter, case=False, na=False)]
        if search_term:
            filtered_df = filtered_df[filtered_df['Company_Name'].str.contains(search_term, case=False, na=False)]
        
        # Log supplier search activity
        search_criteria = {
            'country_filter': country_filter,
            'category_filter': category_filter,
            'search_term': search_term,
            'total_suppliers': len(suppliers_df)
        }
        st.session_state.data_collector.log_supplier_search(search_criteria, len(filtered_df))
        
        st.markdown(f"**Showing {len(filtered_df)} of {len(suppliers_df)} suppliers**")
        
        # Display suppliers table
        if not filtered_df.empty:
            st.dataframe(
                filtered_df[['Company_Name', 'Country', 'Contact_Person', 'Email', 'Material_Categories', 'Established_Year']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No suppliers found matching the current filters.")
    
    with tab2:
        st.subheader("Add New Supplier")
        
        with st.form("add_supplier"):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("Company Name*", placeholder="Enter company name")
                contact_person = st.text_input("Contact Person", placeholder="Enter contact person name")
                email = st.text_input("Email*", placeholder="Enter email address")
                phone = st.text_input("Phone", placeholder="Enter phone number")
                
            with col2:
                address = st.text_area("Address", placeholder="Enter full address")
                country = st.text_input("Country*", placeholder="Enter country")
                specialization = st.text_area("Specialization", placeholder="Enter specialization details")
                established_year = st.number_input("Established Year", min_value=1800, max_value=2025, value=2020)
            
            material_categories = st.multiselect(
                "Material Categories*",
                MATERIAL_CATEGORIES,
                help="Select all applicable material categories"
            )
            
            submitted = st.form_submit_button("Add Supplier", type="primary")
            
            if submitted:
                if company_name and email and country and material_categories:
                    try:
                        success = st.session_state.supplier_manager.add_supplier({
                            'Company_Name': company_name,
                            'Contact_Person': contact_person,
                            'Email': email,
                            'Phone': phone,
                            'Address': address,
                            'Country': country,
                            'Specialization': specialization,
                            'Established_Year': established_year,
                            'Material_Categories': ', '.join(material_categories)
                        })
                        
                        if success:
                            st.success("✅ Supplier added successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to add supplier. Company may already exist.")
                    except Exception as e:
                        st.error(f"❌ Error adding supplier: {str(e)}")
                else:
                    st.error("❌ Please fill in all required fields (marked with *)")
    
    with tab3:
        st.subheader("Edit Existing Supplier")
        
        if not suppliers_df.empty:
            # Select supplier to edit
            supplier_to_edit = st.selectbox(
                "Select Supplier to Edit",
                suppliers_df['Company_Name'].tolist(),
                format_func=lambda x: f"{x} ({suppliers_df[suppliers_df['Company_Name']==x]['Country'].iloc[0]})"
            )
            
            if supplier_to_edit:
                supplier_data = suppliers_df[suppliers_df['Company_Name'] == supplier_to_edit].iloc[0]
                
                with st.form("edit_supplier"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_company_name = st.text_input("Company Name*", value=supplier_data['Company_Name'])
                        new_contact_person = st.text_input("Contact Person", value=supplier_data.get('Contact_Person', ''))
                        new_email = st.text_input("Email*", value=supplier_data['Email'])
                        new_phone = st.text_input("Phone", value=supplier_data.get('Phone', ''))
                        
                    with col2:
                        new_address = st.text_area("Address", value=supplier_data.get('Address', ''))
                        new_country = st.text_input("Country*", value=supplier_data['Country'])
                        new_specialization = st.text_area("Specialization", value=supplier_data.get('Specialization', ''))
                        new_established_year = st.number_input(
                            "Established Year", 
                            min_value=1800, 
                            max_value=2025, 
                            value=int(supplier_data.get('Established_Year', 2020)) if pd.notna(supplier_data.get('Established_Year')) else 2020
                        )
                    
                    current_categories = supplier_data.get('Material_Categories', '').split(', ') if supplier_data.get('Material_Categories') else []
                    new_material_categories = st.multiselect(
                        "Material Categories*",
                        MATERIAL_CATEGORIES,
                        default=[cat for cat in current_categories if cat in MATERIAL_CATEGORIES]
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_submitted = st.form_submit_button("Update Supplier", type="primary")
                    with col2:
                        delete_submitted = st.form_submit_button("Delete Supplier", type="secondary")
                    
                    if update_submitted:
                        if new_company_name and new_email and new_country and new_material_categories:
                            try:
                                success = st.session_state.supplier_manager.update_supplier(
                                    supplier_to_edit,
                                    {
                                        'Company_Name': new_company_name,
                                        'Contact_Person': new_contact_person,
                                        'Email': new_email,
                                        'Phone': new_phone,
                                        'Address': new_address,
                                        'Country': new_country,
                                        'Specialization': new_specialization,
                                        'Established_Year': new_established_year,
                                        'Material_Categories': ', '.join(new_material_categories)
                                    }
                                )
                                
                                if success:
                                    st.success("✅ Supplier updated successfully!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update supplier.")
                            except Exception as e:
                                st.error(f"❌ Error updating supplier: {str(e)}")
                        else:
                            st.error("❌ Please fill in all required fields (marked with *)")
                    
                    if delete_submitted:
                        try:
                            success = st.session_state.supplier_manager.delete_supplier(supplier_to_edit)
                            if success:
                                st.success("✅ Supplier deleted successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete supplier.")
                        except Exception as e:
                            st.error(f"❌ Error deleting supplier: {str(e)}")
        else:
            st.info("No suppliers available for editing.")
    
    with tab4:
        st.subheader("Supplier Database Statistics")
        
        if not suppliers_df.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Suppliers", len(suppliers_df))
            with col2:
                st.metric("Countries", suppliers_df['Country'].nunique())
            with col3:
                chinese_count = len(suppliers_df[suppliers_df['Country'] == 'China'])
                st.metric("Chinese Suppliers", chinese_count)
            with col4:
                emirati_count = len(suppliers_df[suppliers_df['Country'] == 'UAE'])
                st.metric("Emirati Suppliers", emirati_count)
            
            # Regional distribution
            st.markdown("**Regional Distribution:**")
            country_counts = suppliers_df['Country'].value_counts().head(10)
            st.bar_chart(country_counts)
            
            # Material category distribution
            st.markdown("**Material Category Coverage:**")
            category_stats = {}
            for category in MATERIAL_CATEGORIES:
                count = suppliers_df['Material_Categories'].str.contains(category, case=False, na=False).sum()
                category_stats[category] = count
            
            category_df = pd.DataFrame(list(category_stats.items()), columns=['Category', 'Supplier Count'])
            st.bar_chart(category_df.set_index('Category'))

elif page == "📧 Email Generation":
    st.header("Email Generation")
    st.markdown("Generate professional email drafts for supplier quotations.")
    
    # Quick navigation helper
    if not st.session_state.get('detected_materials') and not st.session_state.get('detected_specifications'):
        st.info("💡 **Quick Start:** Process tender documents first in the **Document Processing** section to auto-populate project details!")
    
    # Load suppliers
    suppliers_df = st.session_state.supplier_manager.load_suppliers()
    
    if suppliers_df.empty:
        st.warning("No suppliers available. Please add suppliers first in the Supplier Management section.")
    else:
        # Auto-populate from processed documents
        processed_materials = st.session_state.get('detected_materials', [])
        processed_specs = st.session_state.get('detected_specifications', [])
        auto_deadline = st.session_state.get('supplier_deadline', datetime.now().date())
        
        if processed_materials:
            st.info(f"📄 Auto-detected materials from processed documents: {', '.join(processed_materials)}")
        if processed_specs:
            st.info(f"📋 {len(processed_specs)} specifications extracted from documents")
        
        # Email generation form
        with st.form("email_generation"):
            st.subheader("Quote Request Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Auto-populate with extracted data if available
                default_project_name = st.session_state.get('detected_project_name', '')
                default_tender_ref = st.session_state.get('detected_tender_reference', '')
                
                project_name = st.text_input("Project Name*", value=default_project_name, placeholder="Enter project name")
                tender_reference = st.text_input("Tender Reference", value=default_tender_ref, placeholder="Enter tender reference number")
                quote_deadline = st.date_input("Quote Deadline*", value=auto_deadline)
                
            with col2:
                selected_categories = st.multiselect(
                    "Material Categories*",
                    MATERIAL_CATEGORIES,
                    default=processed_materials if processed_materials else [],
                    help="Select material categories for this quotation"
                )
                
                # Origin filter
                unique_countries = suppliers_df['Country'].dropna().unique().tolist()
                exclude_origins = st.multiselect(
                    "Exclude Origins (Optional)",
                    sorted([str(country) for country in unique_countries]),
                    help="Select countries to exclude from supplier list"
                )
                
                include_note = st.checkbox(
                    "Include origin exclusion note in emails",
                    value=True,
                    help="Add a note about excluded origins in the email body"
                )
            
            # Requirements text - auto-populate with processed specs
            default_requirements = "\n".join(processed_specs) if processed_specs else ""
            requirements = st.text_area(
                "Requirements/Specifications*",
                value=default_requirements,
                height=200,
                placeholder="Enter detailed requirements and specifications for the quotation..."
            )
            
            # Additional notes
            additional_notes = st.text_area(
                "Additional Notes (Optional)",
                height=100,
                placeholder="Any additional information or special instructions..."
            )
            
            generate_emails = st.form_submit_button("Generate Email Drafts", type="primary")
            
            if generate_emails:
                if project_name and selected_categories and requirements and quote_deadline:
                    with st.spinner("Generating email drafts..."):
                        try:
                            # Filter suppliers
                            filtered_suppliers = st.session_state.supplier_manager.filter_suppliers(
                                suppliers_df, 
                                selected_categories, 
                                exclude_origins
                            )
                            
                            if filtered_suppliers.empty:
                                st.error("No suppliers found matching the selected criteria.")
                            else:
                                # Store exclude origins and selected categories for summary
                                st.session_state.last_exclude_origins = exclude_origins
                                st.session_state.last_selected_categories = selected_categories
                                
                                # Generate emails for all filtered suppliers
                                emails = st.session_state.email_generator.generate_emails(
                                    filtered_suppliers,
                                    {
                                        'project_name': project_name,
                                        'tender_reference': tender_reference,
                                        'quote_deadline': quote_deadline,
                                        'requirements': requirements,
                                        'additional_notes': additional_notes,
                                        'exclude_origins': exclude_origins,
                                        'include_note': include_note
                                    }
                                )
                                
                                st.success(f"✅ Generated {len(emails)} email drafts from {len(filtered_suppliers)} suppliers!")
                                
                                # Store emails in session state for persistence
                                st.session_state.generated_emails = emails
                                
                                # Log email generation activity
                                email_data = {
                                    'project_name': project_name,
                                    'tender_reference': tender_reference,
                                    'quote_deadline': quote_deadline.strftime('%Y-%m-%d'),
                                    'materials': selected_categories,
                                    'exclude_origins': exclude_origins,
                                    'requirements_length': len(requirements)
                                }
                                st.session_state.data_collector.log_email_generation(email_data, len(filtered_suppliers))
                                
                                # Track the processed order
                                supplier_categories = st.session_state.order_tracker.categorize_suppliers(emails)
                                order_id = st.session_state.order_tracker.add_processed_order({
                                    'project_name': project_name,
                                    'tender_reference': tender_reference,
                                    'materials': selected_categories,
                                    'total_suppliers': len(filtered_suppliers),
                                    'emails_sent': len(emails),
                                    'supplier_categories': supplier_categories,
                                    'follow_up_date': (quote_deadline + pd.Timedelta(days=1)).strftime('%Y-%m-%d'),
                                    'notes': f"Generated for materials: {', '.join(selected_categories)}"
                                })
                                
                                st.info(f"📋 Order tracked with ID: {order_id}")
                        
                        except Exception as e:
                            st.error(f"❌ Error generating emails: {str(e)}")
                else:
                    st.error("❌ Please fill in all required fields (marked with *)")
        
        # Display generated emails outside the form
        if st.session_state.get('generated_emails'):
            st.markdown("---")
            st.subheader("Generated Email Drafts")
            emails = st.session_state.generated_emails
            
            # Get material categories for proper categorization
            selected_categories = st.session_state.get('last_selected_categories', [])
            
            # Categorize emails by country and their specific materials
            email_categories = {}
            for email in emails:
                country = email.get('country', 'Unknown')
                if country not in email_categories:
                    email_categories[country] = {'emails': [], 'materials': set()}
                email_categories[country]['emails'].append(email)
                
                # Find this supplier's actual material specializations
                company_name = email.get('company_name', '')
                supplier_row = suppliers_df[suppliers_df['Company_Name'] == company_name]
                if not supplier_row.empty:
                    supplier_materials = supplier_row.iloc[0].get('Material_Categories', '')
                    if supplier_materials:
                        # Extract materials that match selected categories
                        for category in selected_categories:
                            if category.lower() in supplier_materials.lower():
                                email_categories[country]['materials'].add(category)
            
            # Display categories with specific materials
            st.markdown("**📂 Email Categories by Supplier Origin & Materials:**")
            for country, data in email_categories.items():
                country_emails = data['emails']
                materials_in_country = data['materials']
                
                # Format country name 
                if country.lower() == 'china':
                    country_display = "Chinese"
                elif country.lower() == 'uae':
                    country_display = "Emirati"
                else:
                    country_display = country
                
                material_text = ', '.join(sorted(materials_in_country)) if materials_in_country else 'All Selected Materials'
                st.info(f"**{country_display}** ({len(country_emails)} suppliers): {material_text}")
            
            st.markdown("---")
            
            # Display emails
            for i, email_data in enumerate(emails):
                with st.expander(f"📧 Email {i+1}: {email_data['company_name']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("**Email Draft:**")
                        st.text_area(
                            "Email Content",
                            value=email_data['email_body'],
                            height=400,
                            key=f"email_{i}",
                            help="Copy this content to your email client"
                        )
                    
                    with col2:
                        st.markdown("**Recipient Details:**")
                        st.write(f"**Company:** {email_data['company_name']}")
                        st.write(f"**Contact:** {email_data['contact_person']}")
                        st.write(f"**Email:** {email_data['email']}")
                        st.write(f"**Country:** {email_data['country']}")
                        
                        # Show supplier's specific materials
                        supplier_materials = email_data.get('materials', '')
                        if supplier_materials:
                            # Find matching materials from selected categories
                            matching_materials = []
                            for category in selected_categories:
                                if category.lower() in supplier_materials.lower():
                                    matching_materials.append(category)
                            
                            if matching_materials:
                                st.write(f"**Specializes in:** {', '.join(matching_materials)}")
                            else:
                                st.write(f"**Materials:** {supplier_materials}")
                        
                        # Copy button (now outside form)
                        if st.button(f"📋 Copy Email {i+1}", key=f"copy_{i}"):
                            st.code(email_data['email_body'], language=None)
            
            # Summary
            st.markdown("---")
            st.markdown("**📊 Generation Summary:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Emails", len(emails))
            with col2:
                unique_countries = len(set([email['country'] for email in emails]))
                st.metric("Countries Covered", unique_countries)
            with col3:
                exclude_origins_count = len(st.session_state.get('last_exclude_origins', []))
                st.metric("Origins Excluded", exclude_origins_count)

elif page == "⏰ Deadline Management":
    st.header("Deadline Management")
    st.markdown("Calculate and manage procurement deadlines.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Deadline Calculator")
        
        # Input options
        deadline_input_method = st.radio(
            "How do you want to input the deadline?",
            ["Manual Date Selection", "Parse from Text"]
        )
        
        if deadline_input_method == "Manual Date Selection":
            client_deadline = st.date_input(
                "Client Deadline",
                value=datetime.now().date(),
                help="Select the client's deadline date"
            )
            
            if st.button("Calculate Supplier Deadline"):
                supplier_deadline = st.session_state.deadline_calculator.calculate_supplier_deadline(client_deadline)
                if supplier_deadline:
                    st.success(f"📅 **Client Deadline:** {client_deadline}")
                    st.warning(f"⏰ **Supplier Quote Due:** {supplier_deadline}")
                    
                    # Calculate days remaining
                    days_remaining = (client_deadline - datetime.now().date()).days
                    supplier_days_remaining = (supplier_deadline - datetime.now().date()).days
                    
                    if days_remaining >= 0:
                        st.info(f"📊 **Days until client deadline:** {days_remaining}")
                        st.info(f"📊 **Days until supplier deadline:** {supplier_days_remaining}")
                    else:
                        st.error("⚠️ Client deadline has already passed!")
                    
                    # Log deadline calculation activity
                    st.session_state.data_collector.log_deadline_calculation(
                        client_deadline.strftime('%Y-%m-%d'),
                        supplier_deadline.strftime('%Y-%m-%d'),
                        2  # Default buffer days
                    )
        
        else:  # Parse from text
            deadline_text = st.text_area(
                "Enter text containing deadline information",
                height=150,
                placeholder="Paste text that contains deadline information (e.g., 'Proposals must be submitted by December 15, 2024')"
            )
            
            if st.button("Parse and Calculate"):
                if deadline_text.strip():
                    extracted_deadline = st.session_state.deadline_calculator.extract_deadline_from_text(deadline_text)
                    
                    if extracted_deadline:
                        supplier_deadline = st.session_state.deadline_calculator.calculate_supplier_deadline(extracted_deadline)
                        
                        st.success(f"📅 **Extracted Client Deadline:** {extracted_deadline}")
                        if supplier_deadline:
                            st.warning(f"⏰ **Calculated Supplier Deadline:** {supplier_deadline}")
                            
                            # Calculate days remaining
                            days_remaining = (extracted_deadline - datetime.now().date()).days
                            supplier_days_remaining = (supplier_deadline - datetime.now().date()).days
                            
                            if days_remaining >= 0:
                                st.info(f"📊 **Days until client deadline:** {days_remaining}")
                                st.info(f"📊 **Days until supplier deadline:** {supplier_days_remaining}")
                            else:
                                st.error("⚠️ Client deadline has already passed!")
                    else:
                        st.error("❌ Could not extract deadline from the provided text. Please try manual date selection.")
                else:
                    st.warning("Please enter text containing deadline information.")
    
    with col2:
        st.subheader("Deadline Rules & Guidelines")
        
        st.markdown("""
        **📋 Deadline Calculation Rules:**
        
        • **Supplier Quote Deadline** = Client Deadline - 2 days
        • This provides sufficient time for internal review and submission preparation
        • Weekends are considered in the calculation
        
        **📅 Supported Date Formats:**
        
        • Full dates: "December 15, 2024", "15/12/2024", "2024-12-15"
        • Relative dates: "next Friday", "in 2 weeks"
        • Text patterns: "due by", "deadline", "submit before", "no later than"
        
        **⚠️ Important Notes:**
        
        • Always verify extracted deadlines manually
        • Consider holidays and business days
        • Factor in time zones for international suppliers
        • Add buffer time for document preparation
        """)
        
        # Recent deadline calculations (if any stored in session)
        if 'recent_deadlines' not in st.session_state:
            st.session_state.recent_deadlines = []
        
        if st.session_state.recent_deadlines:
            st.markdown("**📈 Recent Calculations:**")
            for i, calc in enumerate(st.session_state.recent_deadlines[-5:]):  # Show last 5
                st.write(f"• Client: {calc['client']} → Supplier: {calc['supplier']}")

elif page == "📋 Order Tracking":
    st.header("Order Tracking & Follow-up")
    st.markdown("Track processed orders and manage follow-ups with suppliers.")
    
    # Load orders
    orders_df = st.session_state.order_tracker.get_orders()
    
    if orders_df.empty:
        st.info("No orders processed yet. Generate emails first to start tracking orders.")
    else:
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 All Orders", "⏰ Pending Follow-ups", "📊 Order Statistics"])
        
        with tab1:
            st.subheader("All Processed Orders")
            
            # Display orders table
            display_df = orders_df.copy()
            display_df['Date_Processed'] = pd.to_datetime(display_df['Date_Processed']).dt.strftime('%Y-%m-%d %H:%M')
            
            st.dataframe(
                display_df[['Order_ID', 'Project_Name', 'Tender_Reference', 'Date_Processed', 
                           'Materials', 'Total_Suppliers', 'Emails_Sent', 'Status']],
                use_container_width=True,
                hide_index=True
            )
            
            # Order details expander
            if len(display_df) > 0:
                selected_order = st.selectbox("Select Order for Details", display_df['Order_ID'].tolist())
                if selected_order:
                    order_details = orders_df[orders_df['Order_ID'] == selected_order].iloc[0]
                    
                    with st.expander(f"📄 Order Details: {selected_order}", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Project:** {order_details['Project_Name']}")
                            st.write(f"**Reference:** {order_details['Tender_Reference']}")
                            st.write(f"**Materials:** {order_details['Materials']}")
                            st.write(f"**Status:** {order_details['Status']}")
                        
                        with col2:
                            st.write(f"**Total Suppliers:** {order_details['Total_Suppliers']}")
                            st.write(f"**Emails Sent:** {order_details['Emails_Sent']}")
                            st.write(f"**Follow-up Date:** {order_details['Follow_Up_Date']}")
                            st.write(f"**Supplier Categories:** {order_details['Supplier_Categories']}")
                        
                        # Update status form
                        with st.form(f"update_status_{selected_order}"):
                            new_status = st.selectbox(
                                "Update Status",
                                ["Pending Response", "Quotes Received", "Under Review", "Follow Up Required", "Completed", "Cancelled"],
                                index=["Pending Response", "Quotes Received", "Under Review", "Follow Up Required", "Completed", "Cancelled"].index(order_details['Status']) if order_details['Status'] in ["Pending Response", "Quotes Received", "Under Review", "Follow Up Required", "Completed", "Cancelled"] else 0
                            )
                            
                            notes = st.text_area("Add Notes", value=order_details.get('Notes', ''))
                            
                            if st.form_submit_button("Update Order"):
                                success = st.session_state.order_tracker.update_order_status(selected_order, new_status, notes)
                                if success:
                                    st.success("✅ Order updated successfully!")
                                    
                                    # Log order tracking activity
                                    order_data = {
                                        'order_id': selected_order,
                                        'project_name': order_details['Project_Name'],
                                        'old_status': order_details['Status'],
                                        'new_status': new_status,
                                        'materials': order_details['Materials'],
                                        'total_suppliers': order_details['Total_Suppliers']
                                    }
                                    st.session_state.data_collector.log_order_tracking(order_data)
                                    
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update order.")
        
        with tab2:
            st.subheader("Pending Follow-ups")
            
            pending_orders = st.session_state.order_tracker.get_pending_orders()
            
            if pending_orders.empty:
                st.info("No pending follow-ups.")
            else:
                st.markdown(f"**{len(pending_orders)} orders require follow-up:**")
                
                for _, order in pending_orders.iterrows():
                    with st.expander(f"⏰ {order['Order_ID']} - {order['Project_Name']}", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Project:** {order['Project_Name']}")
                            st.write(f"**Materials:** {order['Materials']}")
                            st.write(f"**Status:** {order['Status']}")
                        
                        with col2:
                            st.write(f"**Emails Sent:** {order['Emails_Sent']}")
                            st.write(f"**Follow-up Date:** {order['Follow_Up_Date']}")
                            
                            days_since = (datetime.now() - pd.to_datetime(order['Date_Processed'])).days
                            st.write(f"**Days Since Sent:** {days_since}")
                        
                        if st.button(f"Mark as Followed Up", key=f"followup_{order['Order_ID']}"):
                            success = st.session_state.order_tracker.update_order_status(order['Order_ID'], "Follow Up Completed")
                            if success:
                                st.success("✅ Marked as followed up!")
                                st.rerun()
        
        with tab3:
            st.subheader("Order Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Orders", len(orders_df))
            with col2:
                pending_count = len(orders_df[orders_df['Status'] == 'Pending Response'])
                st.metric("Pending Response", pending_count)
            with col3:
                total_suppliers = orders_df['Total_Suppliers'].sum()
                st.metric("Total Suppliers Contacted", total_suppliers)
            with col4:
                total_emails = orders_df['Emails_Sent'].sum()
                st.metric("Total Emails Generated", total_emails)
            
            # Status distribution
            st.markdown("**Order Status Distribution:**")
            status_counts = orders_df['Status'].value_counts()
            st.bar_chart(status_counts)
            
            # Materials frequency
            st.markdown("**Most Requested Materials:**")
            all_materials = []
            for materials in orders_df['Materials'].dropna():
                all_materials.extend([m.strip() for m in materials.split(',')])
            
            if all_materials:
                material_counts = pd.Series(all_materials).value_counts().head(10)
                st.bar_chart(material_counts)

elif page == "📊 Dashboard":
    st.header("Dashboard Overview")
    st.markdown("Summary of your procurement tool status and key metrics.")
    
    # Load data
    suppliers_df = st.session_state.supplier_manager.load_suppliers()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Suppliers",
            len(suppliers_df),
            help="Total number of suppliers in the database"
        )
    
    with col2:
        if not suppliers_df.empty:
            countries_count = suppliers_df['Country'].nunique()
        else:
            countries_count = 0
        st.metric(
            "Countries Covered",
            countries_count,
            help="Number of countries represented in supplier database"
        )
    
    with col3:
        if not suppliers_df.empty:
            chinese_suppliers = len(suppliers_df[suppliers_df['Country'] == 'China'])
        else:
            chinese_suppliers = 0
        st.metric(
            "Chinese Suppliers",
            chinese_suppliers,
            help="Number of suppliers from China"
        )
    
    with col4:
        if not suppliers_df.empty:
            recent_suppliers = len(suppliers_df[suppliers_df['Established_Year'] >= 2020])
        else:
            recent_suppliers = 0
        st.metric(
            "Recent Suppliers",
            recent_suppliers,
            help="Suppliers established since 2020"
        )
    
    # Charts and visualizations
    if not suppliers_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌍 Top 10 Countries by Supplier Count**")
            country_counts = suppliers_df['Country'].value_counts().head(10)
            st.bar_chart(country_counts)
        
        with col2:
            st.markdown("**🔧 Material Category Coverage**")
            category_stats = {}
            for category in MATERIAL_CATEGORIES:
                count = suppliers_df['Material_Categories'].str.contains(category, case=False, na=False).sum()
                category_stats[category] = count
            
            category_df = pd.DataFrame(list(category_stats.items()), columns=['Category', 'Count'])
            st.bar_chart(category_df.set_index('Category'))
        
        # Regional requirements compliance
        st.markdown("**📋 Regional Requirements Compliance**")
        
        compliance_data = []
        regions = {
            'Chinese': ('China', 10),
            'Emirati': ('UAE', 10),
            'European': (['Germany', 'France', 'Austria', 'Denmark', 'Finland'], 10)
        }
        
        for region_name, (countries, required) in regions.items():
            if isinstance(countries, list):
                count = len(suppliers_df[suppliers_df['Country'].isin(countries)])
            else:
                count = len(suppliers_df[suppliers_df['Country'] == countries])
            
            compliance_data.append({
                'Region': region_name,
                'Current': count,
                'Required': required,
                'Status': '✅ Met' if count >= required else f'❌ Need {required - count} more'
            })
        
        compliance_df = pd.DataFrame(compliance_data)
        st.dataframe(compliance_df, use_container_width=True, hide_index=True)
        
        # Usage statistics
        st.markdown("**📈 Usage Statistics**")
        
        # Get usage statistics from data collector
        usage_stats = st.session_state.data_collector.get_usage_statistics()
        
        if usage_stats:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Activities",
                    usage_stats.get('total_activities', 0),
                    help="Total user interactions logged"
                )
            
            with col2:
                doc_processed = usage_stats.get('activity_breakdown', {}).get('document_processed', 0)
                st.metric(
                    "Documents Processed",
                    doc_processed,
                    help="Number of documents processed"
                )
            
            with col3:
                emails_generated = usage_stats.get('activity_breakdown', {}).get('email_generated', 0)
                st.metric(
                    "Emails Generated",
                    emails_generated,
                    help="Number of email drafts created"
                )
            
            with col4:
                supplier_searches = usage_stats.get('activity_breakdown', {}).get('supplier_searched', 0)
                st.metric(
                    "Supplier Searches",
                    supplier_searches,
                    help="Number of supplier searches performed"
                )
            
            # Activity breakdown chart
            if usage_stats.get('activity_breakdown'):
                st.markdown("**📊 Activity Breakdown**")
                activity_df = pd.DataFrame(list(usage_stats['activity_breakdown'].items()), 
                                         columns=['Activity', 'Count'])
                st.bar_chart(activity_df.set_index('Activity'))
        else:
            st.info("📊 Usage statistics will appear here as you use the tool.")
        
        # System status
        st.markdown("**🔧 System Status**")
        status_cols = st.columns(3)
        
        with status_cols[0]:
            st.success("✅ Document Parser: Ready")
        with status_cols[1]:
            st.success("✅ Email Generator: Ready")
        with status_cols[2]:
            st.success("✅ Supplier Database: Loaded")
    
    else:
        st.warning("⚠️ No supplier data available. Please load suppliers in the Supplier Management section.")
        if st.button("Load Sample Suppliers", type="primary"):
            # This would trigger loading of the CSV file
            st.info("Please use the Supplier Management section to load suppliers.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p><strong>Hamada Tool</strong> v1.0 | Arab Engineering & Distribution Company</p>
        <p>Oil & Gas Procurement Solutions | Built with ❤️ using Streamlit</p>
        <p><small>Data collection enabled for service improvement and AI training</small></p>
    </div>
    """,
    unsafe_allow_html=True
)
