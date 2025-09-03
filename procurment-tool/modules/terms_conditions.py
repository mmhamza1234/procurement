import streamlit as st
from datetime import datetime
from typing import Dict, Any

class TermsConditions:
    """
    Handles terms and conditions acceptance with data collection consent.
    """
    
    def __init__(self):
        self.terms_version = "1.0"
        self.last_updated = "2024-12-19"
    
    def show_terms_and_conditions(self) -> bool:
        """
        Display terms and conditions and return acceptance status.
        
        Returns:
            True if user accepts, False otherwise
        """
        st.markdown("""
        # Terms and Conditions
        
        ## Welcome to Hamada Tool
        
        By using this application, you agree to the following terms and conditions:
        
        ### 1. Service Description
        Hamada Tool is an automated tender-reading and supplier-quoting productivity application designed specifically for the oil & gas procurement industry. The tool provides document processing, supplier management, email generation, and deadline tracking services.
        
        ### 2. Data Collection and Usage
        
        **IMPORTANT: Data Collection Consent**
        
        We collect and store certain information to improve our services and provide better training for our AI systems:
        
        - **Document Processing Data**: Information extracted from uploaded documents including deadlines, materials, and specifications
        - **User Interactions**: Your interactions with the tool including searches, email generations, and deadline calculations
        - **Usage Analytics**: How you use different features of the tool to improve user experience
        - **Performance Metrics**: Tool performance data to identify and fix issues
        
        **Purpose of Data Collection:**
        - Improve AI training and accuracy
        - Enhance tool functionality and user experience
        - Identify and resolve technical issues
        - Provide better customer support
        - Develop new features based on usage patterns
        
        **Data Storage:**
        - All data is stored securely in our cloud database (Supabase)
        - Data is encrypted in transit and at rest
        - Access is restricted to authorized personnel only
        
        **Data Retention:**
        - Data is retained for as long as necessary to provide services
        - You may request data deletion at any time
        - Anonymized data may be retained for research purposes
        
        ### 3. User Responsibilities
        
        - You are responsible for the accuracy of information you provide
        - You must not upload confidential or sensitive documents without proper authorization
        - You agree to use the tool for legitimate business purposes only
        - You must not attempt to reverse engineer or compromise the tool's security
        
        ### 4. Service Availability
        
        - We strive to maintain 99.9% uptime but cannot guarantee uninterrupted service
        - We may perform maintenance that temporarily affects availability
        - We reserve the right to modify or discontinue features with notice
        
        ### 5. Limitation of Liability
        
        - The tool is provided "as is" without warranties
        - We are not liable for any damages arising from tool use
        - We are not responsible for decisions made based on tool outputs
        
        ### 6. Privacy and Security
        
        - We implement industry-standard security measures
        - Your data is protected according to our privacy policy
        - We do not sell or share your personal information with third parties
        
        ### 7. Changes to Terms
        
        - We may update these terms with notice
        - Continued use constitutes acceptance of updated terms
        - Material changes will be communicated via email or in-app notification
        
        ### 8. Contact Information
        
        For questions about these terms or data collection practices:
        - Email: support@hamadatool.com
        - Phone: +20100 0266 344
        
        ---
        
        **By accepting these terms, you acknowledge that:**
        1. You have read and understood these terms and conditions
        2. You consent to data collection for service improvement and AI training
        3. You agree to use the tool responsibly and in accordance with these terms
        4. You understand that your data will be stored securely and used for legitimate purposes
        """)
        
        # Create columns for acceptance buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            accept_button = st.button("✅ Accept Terms & Conditions", type="primary", use_container_width=True)
        
        with col2:
            decline_button = st.button("❌ Decline", use_container_width=True)
        
        with col3:
            if st.button("📄 Download Terms (PDF)", use_container_width=True):
                self._download_terms_pdf()
        
        # Show additional consent checkbox
        st.markdown("---")
        st.markdown("### Additional Data Collection Consent")
        
        data_consent = st.checkbox(
            "I specifically consent to data collection for AI training and service improvement purposes. "
            "I understand that my usage data will be analyzed to enhance the tool's capabilities and provide better service.",
            value=False,
            help="This consent is required to use the tool. Your data will be used responsibly and securely."
        )
        
        if accept_button and data_consent:
            # Store acceptance in session state
            st.session_state.terms_accepted = True
            st.session_state.terms_acceptance_data = {
                'version': self.terms_version,
                'timestamp': datetime.utcnow().isoformat(),
                'data_collection_consent': True
            }
            st.success("✅ Terms and conditions accepted! You can now use Hamada Tool.")
            st.rerun()
            return True
        
        elif decline_button:
            st.error("❌ You must accept the terms and conditions to use Hamada Tool.")
            st.stop()
            return False
        
        elif accept_button and not data_consent:
            st.error("❌ You must consent to data collection to use Hamada Tool.")
            return False
        
        return False
    
    def check_terms_acceptance(self) -> bool:
        """
        Check if user has accepted terms and conditions.
        
        Returns:
            True if accepted, False otherwise
        """
        return st.session_state.get('terms_accepted', False)
    
    def get_acceptance_data(self) -> Dict[str, Any]:
        """
        Get the terms acceptance data.
        
        Returns:
            Dictionary containing acceptance data
        """
        return st.session_state.get('terms_acceptance_data', {})
    
    def _download_terms_pdf(self):
        """
        Generate and download terms and conditions as PDF.
        """
        # This would typically generate a PDF file
        # For now, we'll just show a message
        st.info("PDF download functionality will be implemented in a future update.")
    
    def show_privacy_policy(self):
        """
        Display the privacy policy.
        """
        st.markdown("""
        # Privacy Policy
        
        ## Data Collection and Usage
        
        ### What We Collect
        - Document content and extracted information
        - User interactions and feature usage
        - Performance and error data
        - Session information and preferences
        
        ### How We Use Your Data
        - Improve AI training and accuracy
        - Enhance tool functionality
        - Provide customer support
        - Develop new features
        
        ### Data Security
        - Encryption in transit and at rest
        - Secure cloud storage (Supabase)
        - Access controls and monitoring
        - Regular security audits
        
        ### Your Rights
        - Access your data
        - Request data deletion
        - Opt-out of data collection
        - Export your data
        
        ### Contact Us
        For privacy concerns: privacy@hamadatool.com
        """)