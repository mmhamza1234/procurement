import pandas as pd
import streamlit as st
import os
from typing import Dict, List, Optional

class SupplierManager:
    """
    Manages the supplier database with CRUD operations.
    Handles CSV file operations and supplier filtering.
    """
    
    def __init__(self, csv_file_path: str = "data/oil_gas_suppliers_consolidated.csv"):
        self.csv_file_path = csv_file_path
        self.ensure_data_directory()
        self.load_initial_data()
    
    def ensure_data_directory(self):
        """Ensure the data directory exists."""
        data_dir = os.path.dirname(self.csv_file_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def load_initial_data(self):
        """Load initial supplier data if CSV doesn't exist."""
        if not os.path.exists(self.csv_file_path):
            # Create initial CSV with column headers
            initial_df = pd.DataFrame(columns=[
                'Company_Name', 'Contact_Person', 'Email', 'Phone', 'Address',
                'Country', 'Specialization', 'Established_Year', 'Material_Categories'
            ])
            initial_df.to_csv(self.csv_file_path, index=False)
    
    def load_suppliers(self) -> pd.DataFrame:
        """
        Load suppliers from CSV file.
        
        Returns:
            DataFrame containing supplier data
        """
        try:
            if os.path.exists(self.csv_file_path):
                df = pd.read_csv(self.csv_file_path)
                # Ensure all required columns exist
                required_columns = [
                    'Company_Name', 'Contact_Person', 'Email', 'Phone', 'Address',
                    'Country', 'Specialization', 'Established_Year', 'Material_Categories'
                ]
                
                for col in required_columns:
                    if col not in df.columns:
                        df[col] = ''
                
                return df
            else:
                # Return empty DataFrame with proper columns
                return pd.DataFrame(columns=[
                    'Company_Name', 'Contact_Person', 'Email', 'Phone', 'Address',
                    'Country', 'Specialization', 'Established_Year', 'Material_Categories'
                ])
        
        except Exception as e:
            st.error(f"Error loading suppliers: {str(e)}")
            return pd.DataFrame(columns=[
                'Company_Name', 'Contact_Person', 'Email', 'Phone', 'Address',
                'Country', 'Specialization', 'Established_Year', 'Material_Categories'
            ])
    
    def save_suppliers(self, df: pd.DataFrame) -> bool:
        """
        Save suppliers DataFrame to CSV file.
        
        Args:
            df: DataFrame containing supplier data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df.to_csv(self.csv_file_path, index=False)
            return True
        except Exception as e:
            st.error(f"Error saving suppliers: {str(e)}")
            return False
    
    def add_supplier(self, supplier_data: Dict) -> bool:
        """
        Add a new supplier to the database.
        
        Args:
            supplier_data: Dictionary containing supplier information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df = self.load_suppliers()
            
            # Check if company already exists
            if not df.empty and supplier_data['Company_Name'] in df['Company_Name'].values:
                return False
            
            # Add new supplier
            new_row = pd.DataFrame([supplier_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            return self.save_suppliers(df)
        
        except Exception as e:
            st.error(f"Error adding supplier: {str(e)}")
            return False
    
    def update_supplier(self, company_name: str, updated_data: Dict) -> bool:
        """
        Update an existing supplier.
        
        Args:
            company_name: Name of the company to update
            updated_data: Dictionary containing updated information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df = self.load_suppliers()
            
            if df.empty or company_name not in df['Company_Name'].values:
                return False
            
            # Update the supplier
            mask = df['Company_Name'] == company_name
            for key, value in updated_data.items():
                df.loc[mask, key] = value
            
            return self.save_suppliers(df)
        
        except Exception as e:
            st.error(f"Error updating supplier: {str(e)}")
            return False
    
    def delete_supplier(self, company_name: str) -> bool:
        """
        Delete a supplier from the database.
        
        Args:
            company_name: Name of the company to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df = self.load_suppliers()
            
            if df.empty or company_name not in df['Company_Name'].values:
                return False
            
            # Remove the supplier
            df = df[df['Company_Name'] != company_name]
            
            return self.save_suppliers(df)
        
        except Exception as e:
            st.error(f"Error deleting supplier: {str(e)}")
            return False
    
    def filter_suppliers(self, df: pd.DataFrame, material_categories: List[str], 
                        exclude_origins: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Filter suppliers based on material categories and origin exclusions.
        
        Args:
            df: DataFrame containing supplier data
            material_categories: List of material categories to include
            exclude_origins: List of countries to exclude
            
        Returns:
            Filtered DataFrame
        """
        try:
            if df.empty:
                return df
            
            filtered_df = df.copy()
            
            # Filter by material categories
            if material_categories:
                category_mask = pd.Series([False] * len(filtered_df))
                
                for category in material_categories:
                    category_mask |= filtered_df['Material_Categories'].str.contains(
                        category, case=False, na=False
                    )
                
                filtered_df = filtered_df[category_mask]
            
            # Exclude specified origins
            if exclude_origins:
                for origin in exclude_origins:
                    filtered_df = filtered_df[filtered_df['Country'] != origin]
            
            return filtered_df
        
        except Exception as e:
            st.error(f"Error filtering suppliers: {str(e)}")
            return pd.DataFrame()
    
    def get_suppliers_by_country(self, df: pd.DataFrame, country: str) -> pd.DataFrame:
        """
        Get suppliers from a specific country.
        
        Args:
            df: DataFrame containing supplier data
            country: Country name
            
        Returns:
            Filtered DataFrame
        """
        try:
            if df.empty:
                return df
            
            return df[df['Country'] == country]
        
        except Exception as e:
            st.error(f"Error filtering by country: {str(e)}")
            return pd.DataFrame()
    
    def get_suppliers_by_material(self, df: pd.DataFrame, material: str) -> pd.DataFrame:
        """
        Get suppliers for a specific material category.
        
        Args:
            df: DataFrame containing supplier data
            material: Material category
            
        Returns:
            Filtered DataFrame
        """
        try:
            if df.empty:
                return df
            
            return df[df['Material_Categories'].str.contains(material, case=False, na=False)]
        
        except Exception as e:
            st.error(f"Error filtering by material: {str(e)}")
            return pd.DataFrame()
    
    def search_suppliers(self, df: pd.DataFrame, search_term: str) -> pd.DataFrame:
        """
        Search suppliers by company name or specialization.
        
        Args:
            df: DataFrame containing supplier data
            search_term: Search term
            
        Returns:
            Filtered DataFrame
        """
        try:
            if df.empty or not search_term.strip():
                return df
            
            search_mask = (
                df['Company_Name'].str.contains(search_term, case=False, na=False) |
                df['Specialization'].str.contains(search_term, case=False, na=False)
            )
            
            return df[search_mask]
        
        except Exception as e:
            st.error(f"Error searching suppliers: {str(e)}")
            return pd.DataFrame()
    
    def get_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Get statistics about the supplier database.
        
        Args:
            df: DataFrame containing supplier data
            
        Returns:
            Dictionary containing statistics
        """
        try:
            if df.empty:
                return {
                    'total_suppliers': 0,
                    'total_countries': 0,
                    'chinese_suppliers': 0,
                    'emirati_suppliers': 0,
                    'european_suppliers': 0,
                    'recent_suppliers': 0
                }
            
            # Define European countries commonly found in oil & gas
            european_countries = [
                'Germany', 'France', 'Austria', 'Denmark', 'Finland', 
                'Italy', 'Netherlands', 'Norway', 'United Kingdom', 'Belgium'
            ]
            
            stats = {
                'total_suppliers': len(df),
                'total_countries': df['Country'].nunique(),
                'chinese_suppliers': len(df[df['Country'] == 'China']),
                'emirati_suppliers': len(df[df['Country'] == 'UAE']),
                'european_suppliers': len(df[df['Country'].isin(european_countries)]),
                'recent_suppliers': len(df[pd.to_numeric(df['Established_Year'], errors='coerce') >= 2020])
            }
            
            return stats
        
        except Exception as e:
            st.error(f"Error calculating statistics: {str(e)}")
            return {}
    
    def export_filtered_suppliers(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Export filtered suppliers to CSV format.
        
        Args:
            df: DataFrame containing supplier data
            filename: Optional filename for export
            
        Returns:
            CSV string
        """
        try:
            if filename:
                df.to_csv(filename, index=False)
                return f"Exported to {filename}"
            else:
                return df.to_csv(index=False)
        
        except Exception as e:
            return f"Error exporting suppliers: {str(e)}"
