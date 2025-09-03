import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
import streamlit as st
from supabase import create_client, Client

class DataCollector:
    """
    Collects and stores user interaction data for training and service improvement.
    Uses Supabase as the backend database.
    """
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://supabase.com/dashboard/project/aocttoqwlpiqvikealbi')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFvY3R0b3F3bHBpcXZpa2VhbGJpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5NDI0NzgsImV4cCI6MjA1OTUxODQ3OH0.2hrd5_9jNPxzQ3XtskUAVD4SQ7SAE6zZqFTRgN7J93E')
        
        try:
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
            self.connected = True
        except Exception as e:
            st.error(f"Failed to connect to Supabase: {str(e)}")
            self.connected = False
    
    def log_user_activity(self, activity_type: str, data: Dict[str, Any], user_id: Optional[str] = None):
        """
        Log user activity to the database.
        
        Args:
            activity_type: Type of activity (e.g., 'document_processed', 'email_generated', 'supplier_searched')
            data: Dictionary containing activity data
            user_id: Optional user identifier
        """
        if not self.connected:
            return
        
        try:
            activity_data = {
                'activity_type': activity_type,
                'data': json.dumps(data),
                'user_id': user_id or 'anonymous',
                'timestamp': datetime.utcnow().isoformat(),
                'tool_version': 'hamada_tool_v1.0'
            }
            
            result = self.supabase.table('user_activities').insert(activity_data).execute()
            return result
        except Exception as e:
            st.error(f"Failed to log activity: {str(e)}")
    
    def log_document_processing(self, file_info: Dict[str, Any], processing_results: Dict[str, Any]):
        """
        Log document processing activities.
        
        Args:
            file_info: Information about the processed file
            processing_results: Results from document processing
        """
        data = {
            'file_info': file_info,
            'processing_results': processing_results,
            'extracted_deadlines': processing_results.get('deadlines', []),
            'extracted_materials': processing_results.get('materials', []),
            'extracted_specifications': processing_results.get('specifications', [])
        }
        
        self.log_user_activity('document_processed', data)
    
    def log_email_generation(self, email_data: Dict[str, Any], supplier_count: int):
        """
        Log email generation activities.
        
        Args:
            email_data: Email generation data
            supplier_count: Number of suppliers contacted
        """
        data = {
            'email_data': email_data,
            'supplier_count': supplier_count,
            'project_name': email_data.get('project_name', ''),
            'tender_reference': email_data.get('tender_reference', '')
        }
        
        self.log_user_activity('email_generated', data)
    
    def log_supplier_search(self, search_criteria: Dict[str, Any], results_count: int):
        """
        Log supplier search activities.
        
        Args:
            search_criteria: Search criteria used
            results_count: Number of results returned
        """
        data = {
            'search_criteria': search_criteria,
            'results_count': results_count,
            'materials_searched': search_criteria.get('materials', [])
        }
        
        self.log_user_activity('supplier_searched', data)
    
    def log_deadline_calculation(self, client_deadline: str, supplier_deadline: str, buffer_days: int):
        """
        Log deadline calculation activities.
        
        Args:
            client_deadline: Client deadline
            supplier_deadline: Calculated supplier deadline
            buffer_days: Buffer days used
        """
        data = {
            'client_deadline': client_deadline,
            'supplier_deadline': supplier_deadline,
            'buffer_days': buffer_days
        }
        
        self.log_user_activity('deadline_calculated', data)
    
    def log_order_tracking(self, order_data: Dict[str, Any]):
        """
        Log order tracking activities.
        
        Args:
            order_data: Order tracking data
        """
        data = {
            'order_data': order_data,
            'order_status': order_data.get('status', ''),
            'order_value': order_data.get('value', 0)
        }
        
        self.log_user_activity('order_tracked', data)
    
    def log_terms_acceptance(self, user_id: str, acceptance_data: Dict[str, Any]):
        """
        Log terms and conditions acceptance.
        
        Args:
            user_id: User identifier
            acceptance_data: Acceptance data including timestamp and version
        """
        data = {
            'terms_version': acceptance_data.get('version', '1.0'),
            'acceptance_timestamp': acceptance_data.get('timestamp', datetime.utcnow().isoformat()),
            'data_collection_consent': acceptance_data.get('data_collection_consent', True)
        }
        
        self.log_user_activity('terms_accepted', data, user_id)
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """
        Get usage statistics for the dashboard.
        
        Returns:
            Dictionary containing usage statistics
        """
        if not self.connected:
            return {}
        
        try:
            # Get total activities
            activities = self.supabase.table('user_activities').select('*').execute()
            
            # Count by activity type
            activity_counts = {}
            for activity in activities.data:
                activity_type = activity.get('activity_type', 'unknown')
                activity_counts[activity_type] = activity_counts.get(activity_type, 0) + 1
            
            return {
                'total_activities': len(activities.data),
                'activity_breakdown': activity_counts,
                'last_activity': activities.data[-1]['timestamp'] if activities.data else None
            }
        except Exception as e:
            st.error(f"Failed to get usage statistics: {str(e)}")
            return {}