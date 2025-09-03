import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import streamlit as st
from supabase import create_client, Client

class DataCollector:
    """
    Comprehensive data collection system for Hamada Tool.
    Collects user interactions, document processing data, and usage analytics
    for service improvement and AI training purposes.
    """
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            st.error("Supabase configuration missing. Please check your .env file.")
            self.connected = False
            return
        
        try:
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
            self.connected = True
            
            # Generate session ID if not exists
            if 'session_id' not in st.session_state:
                st.session_state.session_id = str(uuid.uuid4())
                
        except Exception as e:
            st.error(f"Failed to connect to Supabase: {str(e)}")
            self.connected = False
    
    def log_user_activity(self, activity_type: str, data: Dict[str, Any], user_id: Optional[str] = None):
        """
        Log comprehensive user activity to the database.
        
        Args:
            activity_type: Type of activity (e.g., 'document_processed', 'email_generated')
            data: Dictionary containing activity data
            user_id: Optional user identifier
        """
        if not self.connected:
            return
        
        try:
            # Enhance data with additional context
            enhanced_data = {
                **data,
                'timestamp': datetime.utcnow().isoformat(),
                'tool_version': 'hamada_tool_v1.0',
                'page_url': st.get_option('browser.serverAddress') if hasattr(st, 'get_option') else 'unknown'
            }
            
            activity_record = {
                'activity_type': activity_type,
                'data': enhanced_data,
                'user_id': user_id or f"user_{st.session_state.get('session_id', 'unknown')}",
                'session_id': st.session_state.get('session_id'),
                'timestamp': datetime.utcnow().isoformat(),
                'tool_version': 'hamada_tool_v1.0'
            }
            
            result = self.supabase.table('user_activities').insert(activity_record).execute()
            return result
            
        except Exception as e:
            # Silently fail to avoid disrupting user experience
            print(f"Failed to log activity: {str(e)}")
    
    def log_document_processing(self, file_info: Dict[str, Any], processing_results: Dict[str, Any]):
        """
        Log document processing activities with full details.
        """
        # Log to user_activities
        activity_data = {
            'file_info': file_info,
            'processing_results': {
                'materials_found': processing_results.get('materials', []),
                'deadline_extracted': str(processing_results.get('deadline')) if processing_results.get('deadline') else None,
                'specifications_count': len(processing_results.get('specifications', [])),
                'project_name': processing_results.get('project_name', ''),
                'tender_reference': processing_results.get('tender_reference', ''),
                'text_length': len(processing_results.get('text', ''))
            }
        }
        
        self.log_user_activity('document_processed', activity_data)
        
        # Store in processed_documents table
        if self.connected:
            try:
                document_record = {
                    'document_name': file_info.get('filename', 'unknown'),
                    'document_type': file_info.get('type', 'unknown'),
                    'document_size': file_info.get('size', 0),
                    'extracted_text': processing_results.get('text', '')[:10000],  # Limit text size
                    'extracted_materials': processing_results.get('materials', []),
                    'extracted_deadline': processing_results.get('deadline'),
                    'extracted_specifications': processing_results.get('specifications', []),
                    'project_name': processing_results.get('project_name', ''),
                    'tender_reference': processing_results.get('tender_reference', ''),
                    'user_id': f"user_{st.session_state.get('session_id', 'unknown')}",
                    'session_id': st.session_state.get('session_id')
                }
                
                self.supabase.table('processed_documents').insert(document_record).execute()
                
            except Exception as e:
                print(f"Failed to store document data: {str(e)}")
    
    def log_email_generation(self, email_data: Dict[str, Any], supplier_count: int):
        """
        Log email generation activities with detailed metrics.
        """
        activity_data = {
            'project_details': email_data,
            'supplier_count': supplier_count,
            'materials': email_data.get('materials', []),
            'exclude_origins': email_data.get('exclude_origins', []),
            'deadline': str(email_data.get('quote_deadline', '')),
            'generation_timestamp': datetime.utcnow().isoformat()
        }
        
        self.log_user_activity('email_generated', activity_data)
    
    def log_supplier_search(self, search_criteria: Dict[str, Any], results_count: int):
        """
        Log supplier search activities for analytics.
        """
        search_data = {
            'search_criteria': search_criteria,
            'results_count': results_count,
            'search_timestamp': datetime.utcnow().isoformat()
        }
        
        self.log_user_activity('supplier_searched', search_data)
    
    def log_deadline_calculation(self, client_deadline: str, supplier_deadline: str, buffer_days: int):
        """
        Log deadline calculation activities.
        """
        deadline_data = {
            'client_deadline': client_deadline,
            'supplier_deadline': supplier_deadline,
            'buffer_days': buffer_days,
            'calculation_timestamp': datetime.utcnow().isoformat()
        }
        
        self.log_user_activity('deadline_calculated', deadline_data)
    
    def log_order_tracking(self, order_data: Dict[str, Any]):
        """
        Log order tracking activities and store in database.
        """
        activity_data = {
            'order_data': order_data,
            'tracking_timestamp': datetime.utcnow().isoformat()
        }
        
        self.log_user_activity('order_tracked', activity_data)
        
        # Store in order_tracking table
        if self.connected:
            try:
                order_record = {
                    'order_id': order_data.get('order_id', f"ORD-{datetime.now().strftime('%Y%m%d-%H%M%S')}"),
                    'project_name': order_data.get('project_name', ''),
                    'tender_reference': order_data.get('tender_reference', ''),
                    'materials': order_data.get('materials', []),
                    'total_suppliers': order_data.get('total_suppliers', 0),
                    'emails_sent': order_data.get('emails_sent', 0),
                    'supplier_categories': order_data.get('supplier_categories', ''),
                    'status': order_data.get('status', 'Pending Response'),
                    'follow_up_date': order_data.get('follow_up_date'),
                    'notes': order_data.get('notes', ''),
                    'user_id': f"user_{st.session_state.get('session_id', 'unknown')}"
                }
                
                self.supabase.table('order_tracking').insert(order_record).execute()
                
            except Exception as e:
                print(f"Failed to store order data: {str(e)}")
    
    def log_terms_acceptance(self, user_id: str, acceptance_data: Dict[str, Any]):
        """
        Log terms and conditions acceptance with full audit trail.
        """
        # Log to user_activities
        self.log_user_activity('terms_accepted', acceptance_data, user_id)
        
        # Store in terms_acceptance table
        if self.connected:
            try:
                terms_record = {
                    'user_id': user_id,
                    'session_id': st.session_state.get('session_id'),
                    'terms_version': acceptance_data.get('version', '1.0'),
                    'data_collection_consent': acceptance_data.get('data_collection_consent', True),
                    'acceptance_method': 'web_form'
                }
                
                self.supabase.table('terms_acceptance').insert(terms_record).execute()
                
            except Exception as e:
                print(f"Failed to store terms acceptance: {str(e)}")
    
    def store_generated_emails(self, emails: list, project_details: Dict[str, Any], order_id: str):
        """
        Store all generated emails in the database for future reference.
        """
        if not self.connected:
            return
        
        try:
            email_records = []
            
            for email in emails:
                record = {
                    'project_name': project_details.get('project_name', ''),
                    'tender_reference': project_details.get('tender_reference', ''),
                    'supplier_company': email.get('company_name', ''),
                    'supplier_email': email.get('email', ''),
                    'supplier_country': email.get('country', ''),
                    'email_subject': email.get('subject', ''),
                    'email_body': email.get('email_body', ''),
                    'material_categories': project_details.get('materials', []),
                    'user_id': f"user_{st.session_state.get('session_id', 'unknown')}",
                    'session_id': st.session_state.get('session_id'),
                    'order_id': order_id
                }
                email_records.append(record)
            
            # Batch insert
            self.supabase.table('generated_emails').insert(email_records).execute()
            
        except Exception as e:
            print(f"Failed to store emails: {str(e)}")
    
    def store_supplier_data(self, suppliers_df):
        """
        Sync supplier data from CSV to database for backup and analytics.
        """
        if not self.connected:
            return
        
        try:
            # Clear existing data and insert fresh data
            self.supabase.table('supplier_data').delete().neq('id', 0).execute()
            
            supplier_records = []
            for _, supplier in suppliers_df.iterrows():
                record = {
                    'company_name': str(supplier.get('Company_Name', '')),
                    'contact_person': str(supplier.get('Contact_Person', '')),
                    'email': str(supplier.get('Email', '')),
                    'phone': str(supplier.get('Phone', '')),
                    'address': str(supplier.get('Address', '')),
                    'country': str(supplier.get('Country', '')),
                    'specialization': str(supplier.get('Specialization', '')),
                    'established_year': int(supplier.get('Established_Year', 0)) if pd.notna(supplier.get('Established_Year')) else None,
                    'material_categories': str(supplier.get('Material_Categories', '')),
                    'created_by': 'hamada_tool_sync'
                }
                supplier_records.append(record)
            
            # Batch insert
            if supplier_records:
                self.supabase.table('supplier_data').insert(supplier_records).execute()
                
        except Exception as e:
            print(f"Failed to sync supplier data: {str(e)}")
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive usage statistics for the dashboard.
        """
        if not self.connected:
            return {}
        
        try:
            # Get activity summary
            activities = self.supabase.table('user_activities').select('*').execute()
            
            # Count by activity type
            activity_counts = {}
            unique_users = set()
            unique_sessions = set()
            
            for activity in activities.data:
                activity_type = activity.get('activity_type', 'unknown')
                activity_counts[activity_type] = activity_counts.get(activity_type, 0) + 1
                
                if activity.get('user_id'):
                    unique_users.add(activity['user_id'])
                if activity.get('session_id'):
                    unique_sessions.add(activity['session_id'])
            
            # Get recent activity
            recent_activities = self.supabase.table('user_activities')\
                .select('*')\
                .order('timestamp', desc=True)\
                .limit(10)\
                .execute()
            
            return {
                'total_activities': len(activities.data),
                'activity_breakdown': activity_counts,
                'unique_users': len(unique_users),
                'unique_sessions': len(unique_sessions),
                'recent_activities': recent_activities.data,
                'last_activity': activities.data[-1]['timestamp'] if activities.data else None
            }
            
        except Exception as e:
            print(f"Failed to get usage statistics: {str(e)}")
            return {}
    
    def get_analytics_data(self, days_back: int = 30) -> Dict[str, Any]:
        """
        Get detailed analytics data for the specified time period.
        """
        if not self.connected:
            return {}
        
        try:
            # Get activity trends
            trends_result = self.supabase.rpc('get_usage_trends', {'days_back': days_back}).execute()
            
            # Get activity summary
            summary_result = self.supabase.rpc('get_activity_summary', {'days_back': days_back}).execute()
            
            return {
                'trends': trends_result.data,
                'summary': summary_result.data,
                'period_days': days_back
            }
            
        except Exception as e:
            print(f"Failed to get analytics data: {str(e)}")
            return {}
    
    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Export all data for a specific user (GDPR compliance).
        """
        if not self.connected:
            return {}
        
        try:
            # Get user activities
            activities = self.supabase.table('user_activities')\
                .select('*')\
                .eq('user_id', user_id)\
                .execute()
            
            # Get terms acceptance
            terms = self.supabase.table('terms_acceptance')\
                .select('*')\
                .eq('user_id', user_id)\
                .execute()
            
            # Get processed documents
            documents = self.supabase.table('processed_documents')\
                .select('*')\
                .eq('user_id', user_id)\
                .execute()
            
            # Get generated emails
            emails = self.supabase.table('generated_emails')\
                .select('*')\
                .eq('user_id', user_id)\
                .execute()
            
            return {
                'user_id': user_id,
                'export_timestamp': datetime.utcnow().isoformat(),
                'activities': activities.data,
                'terms_acceptance': terms.data,
                'processed_documents': documents.data,
                'generated_emails': emails.data
            }
            
        except Exception as e:
            print(f"Failed to export user data: {str(e)}")
            return {}
    
    def delete_user_data(self, user_id: str) -> bool:
        """
        Delete all data for a specific user (GDPR compliance).
        """
        if not self.connected:
            return False
        
        try:
            # Delete from all tables
            tables = ['user_activities', 'terms_acceptance', 'processed_documents', 'generated_emails', 'order_tracking']
            
            for table in tables:
                self.supabase.table(table).delete().eq('user_id', user_id).execute()
            
            return True
            
        except Exception as e:
            print(f"Failed to delete user data: {str(e)}")
            return False
    
    def log_system_event(self, event_type: str, event_data: Dict[str, Any]):
        """
        Log system-level events for monitoring and debugging.
        """
        system_data = {
            **event_data,
            'system_timestamp': datetime.utcnow().isoformat(),
            'tool_version': 'hamada_tool_v1.0'
        }
        
        self.log_user_activity(f'system_{event_type}', system_data, 'system')
    
    def get_data_collection_summary(self) -> Dict[str, Any]:
        """
        Get summary of all collected data for transparency.
        """
        if not self.connected:
            return {}
        
        try:
            # Count records in each table
            tables_info = {}
            
            tables = [
                'user_activities', 'terms_acceptance', 'supplier_data',
                'processed_documents', 'generated_emails', 'order_tracking'
            ]
            
            for table in tables:
                result = self.supabase.table(table).select('id', count='exact').execute()
                tables_info[table] = result.count
            
            return {
                'collection_summary': tables_info,
                'last_updated': datetime.utcnow().isoformat(),
                'data_retention_policy': '2 years for analytics, indefinite for AI training (anonymized)',
                'privacy_contact': 'privacy@hamadatool.com'
            }
            
        except Exception as e:
            print(f"Failed to get data collection summary: {str(e)}")
            return {}