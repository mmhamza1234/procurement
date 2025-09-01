"""
Order Tracker Module for Hamada Tool
Manages processed orders and follow-up tracking
"""

import pandas as pd
import os
from datetime import datetime, date
from typing import Dict, List, Optional

class OrderTracker:
    def __init__(self, data_file: str = 'data/processed_orders.csv'):
        """Initialize OrderTracker with data file path."""
        self.data_file = data_file
        self.orders_df = self._load_orders()
    
    def _load_orders(self) -> pd.DataFrame:
        """Load processed orders from CSV file."""
        try:
            if os.path.exists(self.data_file):
                return pd.read_csv(self.data_file)
            else:
                # Create empty DataFrame with required columns
                return pd.DataFrame(columns=[
                    'Order_ID', 'Project_Name', 'Tender_Reference', 'Date_Processed',
                    'Materials', 'Total_Suppliers', 'Emails_Sent', 'Supplier_Categories',
                    'Status', 'Follow_Up_Date', 'Notes'
                ])
        except Exception as e:
            print(f"Error loading orders: {e}")
            return pd.DataFrame(columns=[
                'Order_ID', 'Project_Name', 'Tender_Reference', 'Date_Processed',
                'Materials', 'Total_Suppliers', 'Emails_Sent', 'Supplier_Categories',
                'Status', 'Follow_Up_Date', 'Notes'
            ])
    
    def _save_orders(self) -> bool:
        """Save orders to CSV file."""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            self.orders_df.to_csv(self.data_file, index=False)
            return True
        except Exception as e:
            print(f"Error saving orders: {e}")
            return False
    
    def add_processed_order(self, order_data: Dict) -> str:
        """Add a new processed order and return order ID."""
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        new_order = {
            'Order_ID': order_id,
            'Project_Name': order_data.get('project_name', ''),
            'Tender_Reference': order_data.get('tender_reference', ''),
            'Date_Processed': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Materials': ', '.join(order_data.get('materials', [])),
            'Total_Suppliers': order_data.get('total_suppliers', 0),
            'Emails_Sent': order_data.get('emails_sent', 0),
            'Supplier_Categories': order_data.get('supplier_categories', ''),
            'Status': 'Pending Response',
            'Follow_Up_Date': order_data.get('follow_up_date', ''),
            'Notes': order_data.get('notes', '')
        }
        
        # Add to DataFrame
        new_row = pd.DataFrame([new_order])
        self.orders_df = pd.concat([self.orders_df, new_row], ignore_index=True)
        
        # Save to file
        self._save_orders()
        
        return order_id
    
    def get_orders(self) -> pd.DataFrame:
        """Get all processed orders."""
        return self.orders_df.copy()
    
    def update_order_status(self, order_id: str, status: str, notes: str = '') -> bool:
        """Update order status and notes."""
        try:
            mask = self.orders_df['Order_ID'] == order_id
            if mask.any():
                self.orders_df.loc[mask, 'Status'] = status
                if notes:
                    self.orders_df.loc[mask, 'Notes'] = notes
                return self._save_orders()
            return False
        except Exception as e:
            print(f"Error updating order: {e}")
            return False
    
    def get_pending_orders(self) -> pd.DataFrame:
        """Get orders that need follow-up."""
        return self.orders_df[
            self.orders_df['Status'].isin(['Pending Response', 'Follow Up Required'])
        ].copy()
    
    def categorize_suppliers(self, emails: List[Dict]) -> str:
        """Categorize suppliers by country and materials."""
        categories = {}
        
        for email in emails:
            country = email.get('country', 'Unknown')
            materials = email.get('materials', '')
            
            if country not in categories:
                categories[country] = {'count': 0, 'materials': set()}
            categories[country]['count'] += 1
            
            # Extract material keywords from supplier's specializations
            if materials:
                material_keywords = ['piping', 'pipes', 'valves', 'flanges', 'fittings', 'bolts', 'gaskets', 'finned tubes']
                for keyword in material_keywords:
                    if keyword.lower() in materials.lower():
                        categories[country]['materials'].add(keyword)
        
        # Create detailed category strings
        category_strings = []
        for country, data in categories.items():
            count = data['count']
            materials = list(data['materials'])
            
            if country.lower() == 'china':
                country_name = "Chinese"
            elif country.lower() == 'uae':
                country_name = "Emirati"
            else:
                country_name = country
                
            if materials:
                material_text = ', '.join(sorted(materials))
                category_strings.append(f"{country_name}: {count} suppliers ({material_text})")
            else:
                category_strings.append(f"{country_name}: {count} suppliers")
        
        return '; '.join(category_strings)