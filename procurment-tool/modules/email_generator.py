import pandas as pd
from datetime import datetime, date
from typing import Dict, List, Any

class EmailGenerator:
    """
    Generates professional email drafts for supplier quotations.
    Includes custom footer and origin filtering notes.
    """
    
    def __init__(self):
        self.default_footer = """
Regards,
Hamada Tool
Procurement Manager
Arab Engineering & Distribution Company
Building B2 Mivida Business Park 90 St. 5th Settlement • Cairo, Egypt
+20100 0266 344 | +202 2322 8800
hamada@aedco.com.eg
www.aedco.com"""
    
    def generate_emails(self, suppliers_df: pd.DataFrame, project_details: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate email drafts for all suppliers in the DataFrame.
        
        Args:
            suppliers_df: DataFrame containing filtered suppliers
            project_details: Dictionary containing project information
            
        Returns:
            List of dictionaries containing email data
        """
        emails = []
        
        for _, supplier in suppliers_df.iterrows():
            email_data = self._generate_single_email(supplier, project_details)
            emails.append(email_data)
        
        return emails
    
    def _generate_single_email(self, supplier: pd.Series, project_details: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate a single email draft for a supplier.
        
        Args:
            supplier: Series containing supplier information
            project_details: Dictionary containing project information
            
        Returns:
            Dictionary containing email data
        """
        # Extract project details
        project_name = project_details.get('project_name', '')
        tender_reference = project_details.get('tender_reference', '')
        quote_deadline = project_details.get('quote_deadline', '')
        requirements = project_details.get('requirements', '')
        additional_notes = project_details.get('additional_notes', '')
        exclude_origins = project_details.get('exclude_origins', [])
        include_note = project_details.get('include_note', False)
        
        # Format deadline
        if isinstance(quote_deadline, date):
            deadline_str = quote_deadline.strftime('%B %d, %Y')
        else:
            deadline_str = str(quote_deadline)
        
        # Generate subject line
        subject = f"Request for Quotation - {project_name}"
        if tender_reference:
            subject += f" (Ref: {tender_reference})"
        
        # Generate email body
        email_body = self._create_email_body(
            supplier=supplier,
            project_name=project_name,
            tender_reference=tender_reference,
            deadline_str=deadline_str,
            requirements=requirements,
            additional_notes=additional_notes,
            exclude_origins=exclude_origins,
            include_note=include_note
        )
        
        return {
            'company_name': str(supplier.get('Company_Name', '') or ''),
            'contact_person': str(supplier.get('Contact_Person', '') or ''),
            'email': str(supplier.get('Email', '') or ''),
            'country': str(supplier.get('Country', '') or ''),
            'materials': str(supplier.get('Material_Categories', '') or ''),
            'subject': subject,
            'email_body': email_body
        }
    
    def _create_email_body(self, supplier: pd.Series, project_name: str, 
                          tender_reference: str, deadline_str: str, requirements: str,
                          additional_notes: str, exclude_origins: List[str], 
                          include_note: bool) -> str:
        """
        Create the email body content.
        
        Args:
            supplier: Supplier information
            project_name: Name of the project
            tender_reference: Tender reference number
            deadline_str: Formatted deadline string
            requirements: Project requirements
            additional_notes: Additional notes
            exclude_origins: List of excluded origins
            include_note: Whether to include origin exclusion note
            
        Returns:
            Formatted email body
        """
        # Email greeting
        contact_person_raw = supplier.get('Contact_Person', '')
        contact_person = str(contact_person_raw).strip() if contact_person_raw and str(contact_person_raw) != 'nan' else ''
        company_name = str(supplier.get('Company_Name', '') or '')
        
        if contact_person:
            greeting = f"Dear {contact_person},"
        else:
            greeting = f"Dear Sir/Madam,"
        
        # Build email body
        body_parts = [greeting, ""]
        
        # Introduction
        body_parts.extend([
            "I hope this email finds you well.",
            "",
            f"We are pleased to invite {company_name} to submit a quotation for the following project:",
            ""
        ])
        
        # Project details
        body_parts.append(f"**Project:** {project_name}")
        if tender_reference:
            body_parts.append(f"**Reference:** {tender_reference}")
        body_parts.extend([
            f"**Quote Deadline:** {deadline_str}",
            "",
            "**Requirements and Specifications:**"
        ])
        
        # Add requirements
        if requirements:
            # Split requirements into lines and format
            req_lines = requirements.split('\n')
            for line in req_lines:
                if line.strip():
                    body_parts.append(f"• {line.strip()}")
        
        body_parts.append("")
        
        # Additional notes
        if additional_notes:
            body_parts.extend([
                "**Additional Information:**",
                additional_notes,
                ""
            ])
        
        # Origin exclusion note
        if include_note and exclude_origins:
            origins_text = ", ".join(exclude_origins)
            body_parts.extend([
                f"**Please note:** For this project, we are specifically seeking suppliers from origins other than {origins_text}.",
                ""
            ])
        
        # Standard requirements
        body_parts.extend([
            "**Please include in your quotation:**",
            "• Detailed technical specifications",
            "• Unit prices and total costs",
            "• Delivery schedule and lead times",
            "• Payment terms",
            "• Validity period of the quotation",
            "• Compliance certificates and quality documentation",
            "• Country of origin for all materials",
            "",
            "We look forward to receiving your competitive quotation by the specified deadline. Should you have any questions or require clarification, please do not hesitate to contact us.",
            "",
            "Thank you for your time and consideration.",
            ""
        ])
        
        # Add footer
        body_parts.append(self.default_footer)
        
        return "\n".join(body_parts)
    
    def generate_bulk_email_summary(self, emails: List[Dict[str, str]], 
                                   project_details: Dict[str, Any]) -> str:
        """
        Generate a summary for bulk email generation.
        
        Args:
            emails: List of generated emails
            project_details: Project information
            
        Returns:
            Summary text
        """
        project_name = project_details.get('project_name', 'Unknown Project')
        deadline = project_details.get('quote_deadline', 'Not specified')
        exclude_origins = project_details.get('exclude_origins', [])
        
        # Count by country
        country_counts = {}
        for email in emails:
            country = email['country']
            country_counts[country] = country_counts.get(country, 0) + 1
        
        summary_parts = [
            f"**Email Generation Summary for {project_name}**",
            "",
            f"• Total emails generated: {len(emails)}",
            f"• Quote deadline: {deadline}",
            f"• Countries covered: {len(country_counts)}",
            ""
        ]
        
        if exclude_origins:
            summary_parts.extend([
                f"• Excluded origins: {', '.join(exclude_origins)}",
                ""
            ])
        
        summary_parts.append("**Distribution by Country:**")
        for country, count in sorted(country_counts.items()):
            summary_parts.append(f"  - {country}: {count} suppliers")
        
        return "\n".join(summary_parts)
    
    def export_emails_to_csv(self, emails: List[Dict[str, str]]) -> str:
        """
        Export emails to CSV format for external use.
        
        Args:
            emails: List of email data
            
        Returns:
            CSV string
        """
        df = pd.DataFrame(emails)
        return df.to_csv(index=False)
    
    def validate_email_addresses(self, suppliers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate email addresses in supplier DataFrame.
        
        Args:
            suppliers_df: DataFrame containing supplier data
            
        Returns:
            DataFrame with validation results
        """
        import re
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        validation_results = []
        
        for _, supplier in suppliers_df.iterrows():
            email_raw = supplier.get('Email', '')
            email = str(email_raw).strip() if email_raw and str(email_raw) != 'nan' else ''
            is_valid = bool(re.match(email_pattern, email)) if email else False
            
            validation_results.append({
                'Company_Name': supplier.get('Company_Name', ''),
                'Email': email,
                'Is_Valid': is_valid,
                'Issue': 'Valid' if is_valid else ('Missing' if not email else 'Invalid format')
            })
        
        return pd.DataFrame(validation_results)
    
    def create_follow_up_email(self, original_email_data: Dict[str, str], 
                              days_since_sent: int = 7) -> str:
        """
        Create a follow-up email for non-responding suppliers.
        
        Args:
            original_email_data: Original email data
            days_since_sent: Number of days since original email
            
        Returns:
            Follow-up email body
        """
        company_name = str(original_email_data.get('company_name', '') or '')
        contact_person = str(original_email_data.get('contact_person', '') or '')
        
        if contact_person and contact_person != 'nan':
            greeting = f"Dear {contact_person},"
        else:
            greeting = "Dear Sir/Madam,"
        
        body_parts = [
            greeting,
            "",
            f"I hope this email finds you well.",
            "",
            f"We sent a request for quotation to {company_name} {days_since_sent} days ago and have not yet received a response.",
            "",
            "We understand that you may be busy, but we would greatly appreciate your quotation for our project. The information is valuable to our procurement process.",
            "",
            "If you need additional time or have any questions regarding the requirements, please let us know. We are happy to extend the deadline or provide clarification as needed.",
            "",
            "If you are unable to provide a quotation for this project, please let us know so we can update our records accordingly.",
            "",
            "Thank you for your time and consideration. We look forward to hearing from you soon.",
            "",
            self.default_footer
        ]
        
        return "\n".join(body_parts)
