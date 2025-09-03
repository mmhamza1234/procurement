import streamlit as st
from datetime import datetime
from typing import Dict, Any

class TermsConditions:
    """
    Comprehensive terms and conditions handler with data collection consent.
    Ensures users understand and consent to data collection for AI training and service improvement.
    """
    
    def __init__(self):
        self.terms_version = "1.0"
        self.last_updated = "2025-01-08"
    
    def show_terms_and_conditions(self) -> bool:
        """
        Display comprehensive terms and conditions with data collection consent.
        
        Returns:
            True if user accepts, False otherwise
        """
        st.markdown("""
        # 📋 Terms and Conditions - Hamada Tool
        
        **Version:** 1.0 | **Last Updated:** January 8, 2025
        
        ## Welcome to Hamada Tool
        
        By using this application, you agree to the following terms and conditions. Please read carefully.
        
        ---
        
        ## 1. 🛠️ Service Description
        
        **Hamada Tool** is an automated tender-reading and supplier-quoting productivity application designed specifically for the oil & gas procurement industry. The tool provides:
        
        - Document processing and information extraction
        - Supplier database management
        - Professional email generation for quotations
        - Deadline calculation and management
        - Order tracking and follow-up management
        
        ---
        
        ## 2. 📊 Data Collection and Usage
        
        ### **IMPORTANT: Comprehensive Data Collection Notice**
        
        **We collect and store extensive information to improve our services and train our AI systems. By using this tool, you consent to the collection of:**
        
        #### **Document Processing Data:**
        - ✅ Full text content of uploaded documents
        - ✅ Extracted deadlines, materials, and specifications
        - ✅ Project names and tender references
        - ✅ File metadata (name, size, type, upload timestamp)
        
        #### **User Interaction Data:**
        - ✅ All searches performed (materials, countries, suppliers)
        - ✅ Email generation activities and parameters
        - ✅ Deadline calculations and modifications
        - ✅ Supplier database modifications (additions, edits, deletions)
        - ✅ Page navigation and feature usage patterns
        - ✅ Session duration and interaction frequency
        
        #### **System Analytics:**
        - ✅ Performance metrics and error logs
        - ✅ Feature usage statistics
        - ✅ User workflow patterns
        - ✅ Tool effectiveness measurements
        
        #### **Technical Data:**
        - ✅ IP addresses and browser information
        - ✅ Session identifiers and timestamps
        - ✅ Device and operating system information
        
        ### **Purpose of Data Collection:**
        
        #### **🤖 AI Training and Improvement:**
        - Train machine learning models for better document parsing
        - Improve deadline detection algorithms
        - Enhance material categorization accuracy
        - Develop predictive analytics for procurement workflows
        
        #### **🔧 Service Enhancement:**
        - Identify and fix technical issues
        - Optimize user interface and experience
        - Develop new features based on usage patterns
        - Improve system performance and reliability
        
        #### **📈 Business Intelligence:**
        - Analyze procurement industry trends
        - Understand supplier market dynamics
        - Improve tool effectiveness metrics
        - Generate insights for product development
        
        ### **Data Storage and Security:**
        
        #### **🔒 Secure Storage:**
        - All data stored in enterprise-grade cloud database (Supabase)
        - Data encrypted in transit and at rest using industry standards
        - Access restricted to authorized personnel only
        - Regular security audits and monitoring
        
        #### **🌍 Data Location:**
        - Primary storage: Secure cloud infrastructure
        - Backup storage: Geographically distributed for redundancy
        - Data processing: May occur in multiple regions for optimization
        
        #### **⏰ Data Retention:**
        - **Active Data:** Retained while you use the service
        - **Analytics Data:** Retained for 2 years for service improvement
        - **AI Training Data:** Anonymized data retained indefinitely for model training
        - **Audit Logs:** Retained for 7 years for compliance purposes
        
        ---
        
        ## 3. 👤 User Responsibilities
        
        **You agree to:**
        - ✅ Provide accurate information when using the tool
        - ✅ Use the tool for legitimate business purposes only
        - ✅ Respect intellectual property rights
        - ✅ Not upload confidential documents without proper authorization
        - ✅ Not attempt to reverse engineer or compromise the tool's security
        - ✅ Comply with all applicable laws and regulations
        
        **You must not:**
        - ❌ Share your access credentials with unauthorized persons
        - ❌ Use the tool for illegal or unethical purposes
        - ❌ Attempt to extract or scrape data from the system
        - ❌ Upload malicious files or content
        - ❌ Interfere with the tool's operation or security
        
        ---
        
        ## 4. 🔧 Service Availability and Support
        
        ### **Service Level:**
        - We strive to maintain 99.9% uptime
        - Scheduled maintenance will be announced in advance
        - Emergency maintenance may occur without notice
        
        ### **Support:**
        - Email support: support@hamadatool.com
        - Phone support: +20100 0266 344
        - Business hours: Sunday-Thursday, 9 AM - 6 PM (Cairo time)
        
        ### **Updates and Changes:**
        - We may update features and functionality
        - Major changes will be communicated via email or in-app notifications
        - Continued use constitutes acceptance of updates
        
        ---
        
        ## 5. ⚖️ Limitation of Liability
        
        ### **Service Disclaimer:**
        - The tool is provided "as is" without warranties of any kind
        - We do not guarantee accuracy of extracted information
        - Users are responsible for verifying all tool outputs
        - We are not liable for business decisions made based on tool outputs
        
        ### **Liability Limits:**
        - Our liability is limited to the amount paid for the service
        - We are not liable for indirect, consequential, or punitive damages
        - We are not responsible for data loss due to user error
        
        ---
        
        ## 6. 🔐 Privacy and Data Protection
        
        ### **Privacy Commitment:**
        - We implement industry-standard security measures
        - Your data is protected according to international privacy standards
        - We do not sell personal information to third parties
        - We may share anonymized data for research purposes
        
        ### **Your Rights:**
        - **Access:** Request a copy of your data
        - **Correction:** Request correction of inaccurate data
        - **Deletion:** Request deletion of your data (subject to legal requirements)
        - **Portability:** Request export of your data in machine-readable format
        - **Objection:** Object to certain types of data processing
        
        ### **Data Sharing:**
        - We may share data with service providers (hosting, analytics)
        - We may share anonymized data for academic research
        - We will comply with legal requests for data disclosure
        - We will notify users of data breaches as required by law
        
        ---
        
        ## 7. 🔄 Changes to Terms
        
        - We may update these terms with 30 days notice
        - Material changes will be highlighted and require re-acceptance
        - Continued use after changes constitutes acceptance
        - Previous versions will be archived and available upon request
        
        ---
        
        ## 8. 📞 Contact Information
        
        **For questions about these terms or data collection:**
        
        **Hamada Tool Support Team**
        - 📧 Email: support@hamadatool.com
        - 📱 Phone: +20100 0266 344
        - 🏢 Address: Arab Engineering & Distribution Company, Building B2 Mivida Business Park, 90 St. 5th Settlement, Cairo, Egypt
        
        **Data Protection Officer:**
        - 📧 Email: privacy@hamadatool.com
        - 📱 Phone: +202 2322 8800
        
        ---
        
        ## 9. ✅ Consent and Acceptance
        
        **By accepting these terms, you explicitly acknowledge and consent to:**
        
        1. **Full Data Collection:** You understand that we collect comprehensive data about your usage
        2. **AI Training:** Your data will be used to train and improve AI systems
        3. **Service Improvement:** Your usage patterns will be analyzed for service enhancement
        4. **Data Storage:** Your data will be stored securely in our cloud infrastructure
        5. **International Transfer:** Your data may be processed in different countries
        6. **Retention Periods:** Different types of data have different retention periods
        7. **Business Use:** We may use anonymized data for business intelligence
        
        ### **Special Consent for AI Training:**
        
        You specifically consent to the use of your data for:
        - Training machine learning models
        - Improving natural language processing algorithms
        - Developing predictive analytics capabilities
        - Creating industry benchmarks and insights
        
        ---
        
        **🔒 Your privacy and data security are our top priorities. We are committed to using your data responsibly and transparently.**
        """)
        
        # Consent checkboxes
        st.markdown("---")
        st.markdown("## ✅ Required Consents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            terms_consent = st.checkbox(
                "**I have read and accept the Terms and Conditions**",
                value=False,
                help="Required to use Hamada Tool"
            )
            
            data_consent = st.checkbox(
                "**I consent to comprehensive data collection for service improvement**",
                value=False,
                help="We collect usage data to improve the tool and provide better service"
            )
        
        with col2:
            ai_training_consent = st.checkbox(
                "**I consent to data usage for AI training and model improvement**",
                value=False,
                help="Your data helps us train better AI models for document processing and analysis"
            )
            
            analytics_consent = st.checkbox(
                "**I consent to usage analytics and business intelligence collection**",
                value=False,
                help="We analyze usage patterns to develop new features and improve user experience"
            )
        
        # Additional consent information
        st.markdown("### 📋 What This Means:")
        st.markdown("""
        - **Your document content** will be analyzed and stored for AI training
        - **Your usage patterns** will be tracked for service improvement
        - **Your supplier interactions** will be logged for analytics
        - **Your email generations** will be stored for quality improvement
        - **All data is anonymized** for research and training purposes
        - **You can request data deletion** at any time by contacting support
        """)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            accept_button = st.button(
                "✅ Accept All Terms & Start Using Hamada Tool",
                type="primary",
                use_container_width=True,
                disabled=not (terms_consent and data_consent and ai_training_consent and analytics_consent)
            )
        
        with col2:
            decline_button = st.button(
                "❌ Decline Terms",
                use_container_width=True
            )
        
        with col3:
            download_button = st.button(
                "📄 Download Terms (PDF)",
                use_container_width=True
            )
        
        # Handle button clicks
        if accept_button:
            if terms_consent and data_consent and ai_training_consent and analytics_consent:
                # Store acceptance in session state
                st.session_state.terms_accepted = True
                st.session_state.terms_acceptance_data = {
                    'version': self.terms_version,
                    'timestamp': datetime.utcnow().isoformat(),
                    'data_collection_consent': True,
                    'ai_training_consent': True,
                    'analytics_consent': True,
                    'acceptance_method': 'comprehensive_web_form'
                }
                
                st.success("✅ Terms and conditions accepted! Welcome to Hamada Tool!")
                st.balloons()
                st.rerun()
                return True
            else:
                st.error("❌ Please accept all required consents to use Hamada Tool.")
        
        elif decline_button:
            st.error("❌ You must accept the terms and conditions to use Hamada Tool.")
            st.markdown("### Alternative Options:")
            st.markdown("- Contact our sales team for enterprise licensing: sales@hamadatool.com")
            st.markdown("- Request a demo without data collection: demo@hamadatool.com")
            st.stop()
        
        elif download_button:
            self._generate_terms_pdf()
        
        return False
    
    def check_terms_acceptance(self) -> bool:
        """
        Check if user has accepted terms and conditions.
        """
        return st.session_state.get('terms_accepted', False)
    
    def get_acceptance_data(self) -> Dict[str, Any]:
        """
        Get the terms acceptance data.
        """
        return st.session_state.get('terms_acceptance_data', {})
    
    def _generate_terms_pdf(self):
        """
        Generate and offer download of terms and conditions as PDF.
        """
        st.info("📄 PDF generation feature will be implemented in the next update. For now, you can copy the terms from this page.")
        
        # Provide text version for copying
        with st.expander("📋 Copy Terms Text"):
            terms_text = """
HAMADA TOOL - TERMS AND CONDITIONS

Version 1.0 | Last Updated: January 8, 2025

[Full terms text would be included here for copying]

For the complete terms and conditions, please refer to the web version above.

Contact: support@hamadatool.com | +20100 0266 344
Arab Engineering & Distribution Company
Building B2 Mivida Business Park, 90 St. 5th Settlement, Cairo, Egypt
            """
            st.text_area("Terms Text:", value=terms_text, height=200)
    
    def show_privacy_dashboard(self):
        """
        Show user privacy dashboard with data management options.
        """
        st.markdown("""
        # 🔐 Privacy Dashboard
        
        ## Your Data Rights
        
        As a user of Hamada Tool, you have the following rights regarding your data:
        
        ### 📋 Data Access
        - View all data we have collected about you
        - Download your data in machine-readable format
        - Understand how your data is being used
        
        ### ✏️ Data Correction
        - Request correction of inaccurate information
        - Update your preferences and settings
        - Modify consent preferences
        
        ### 🗑️ Data Deletion
        - Request complete deletion of your data
        - Selective deletion of specific data types
        - Right to be forgotten (subject to legal requirements)
        
        ### 📤 Data Portability
        - Export your data in standard formats
        - Transfer data to other services
        - Receive data summaries and reports
        
        ## Contact for Privacy Requests
        
        **Data Protection Officer:**
        - Email: privacy@hamadatool.com
        - Phone: +202 2322 8800
        - Response time: 30 days maximum
        
        ## Data Collection Summary
        
        We collect data to:
        1. **Improve AI Models** - Better document parsing and analysis
        2. **Enhance User Experience** - More intuitive interface and workflows
        3. **Develop New Features** - Based on actual usage patterns
        4. **Ensure Quality** - Monitor and improve service reliability
        5. **Provide Support** - Help users when they encounter issues
        
        Your data helps us build better tools for the entire oil & gas procurement industry.
        """)
    
    def log_terms_view(self, data_collector):
        """
        Log when user views terms and conditions.
        """
        if data_collector and data_collector.connected:
            data_collector.log_user_activity('terms_viewed', {
                'terms_version': self.terms_version,
                'view_timestamp': datetime.utcnow().isoformat()
            })
    
    def validate_consent_requirements(self) -> Dict[str, bool]:
        """
        Validate that all required consents are provided.
        """
        acceptance_data = self.get_acceptance_data()
        
        return {
            'terms_accepted': acceptance_data.get('data_collection_consent', False),
            'data_collection': acceptance_data.get('data_collection_consent', False),
            'ai_training': acceptance_data.get('ai_training_consent', False),
            'analytics': acceptance_data.get('analytics_consent', False),
            'all_required': all([
                acceptance_data.get('data_collection_consent', False),
                acceptance_data.get('ai_training_consent', False),
                acceptance_data.get('analytics_consent', False)
            ])
        }