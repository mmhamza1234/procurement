import os
import json
from datetime import datetime
from typing import Optional, Dict, Any
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

class GoogleDriveClient:
    """
    Google Drive client for file storage and management.
    Handles OAuth authentication and file operations.
    """
    
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID', '121616453789-874oa7d9rimqmk0bhbni8nviko7d0cgb.apps.googleusercontent.com')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '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')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8501')
        self.parent_folder_name = os.getenv('GOOGLE_DRIVE_PARENT_FOLDER_NAME', 'Procurement Tool Egypt')
        
        self.scopes = ['https://www.googleapis.com/auth/drive.file']
        self.service = None
        self.parent_folder_id = None
        
        # Initialize authentication
        self._initialize_auth()
    
    def _initialize_auth(self):
        """Initialize Google Drive authentication."""
        try:
            # Check if we have stored credentials
            if 'google_credentials' in st.session_state:
                creds_data = st.session_state.google_credentials
                credentials = Credentials.from_authorized_user_info(creds_data, self.scopes)
                
                if credentials.valid:
                    self.service = build('drive', 'v3', credentials=credentials)
                    self._ensure_parent_folder()
                    return
            
            # Need to authenticate
            self._show_auth_ui()
            
        except Exception as e:
            st.error(f"Failed to initialize Google Drive: {str(e)}")
    
    def _show_auth_ui(self):
        """Show authentication UI."""
        st.warning("Google Drive authentication required.")
        
        if st.button("🔐 Authenticate with Google Drive"):
            auth_url = self._get_auth_url()
            st.markdown(f"[Click here to authenticate with Google Drive]({auth_url})")
            
            # Input for authorization code
            auth_code = st.text_input("Enter the authorization code:")
            
            if auth_code and st.button("Complete Authentication"):
                self._complete_auth(auth_code)
    
    def _get_auth_url(self) -> str:
        """Get Google OAuth authorization URL."""
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes
        )
        flow.redirect_uri = self.redirect_uri
        
        auth_url, _ = flow.authorization_url(prompt='consent')
        return auth_url
    
    def _complete_auth(self, auth_code: str):
        """Complete OAuth authentication."""
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            # Exchange authorization code for credentials
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
            
            # Store credentials
            st.session_state.google_credentials = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            
            self.service = build('drive', 'v3', credentials=credentials)
            self._ensure_parent_folder()
            
            st.success("✅ Google Drive authentication successful!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
    
    def _ensure_parent_folder(self):
        """Ensure parent folder exists."""
        if not self.service:
            return
        
        try:
            # Search for existing folder
            results = self.service.files().list(
                q=f"name='{self.parent_folder_name}' and mimeType='application/vnd.google-apps.folder'",
                fields="files(id, name)"
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                self.parent_folder_id = folders[0]['id']
            else:
                # Create parent folder
                folder_metadata = {
                    'name': self.parent_folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                
                self.parent_folder_id = folder.get('id')
            
            st.session_state.parent_folder_id = self.parent_folder_id
            
        except Exception as e:
            st.error(f"Failed to create/find parent folder: {str(e)}")
    
    def upload_file(self, filename: str, file_content: bytes, subfolder: str = None) -> Optional[str]:
        """
        Upload file to Google Drive.
        
        Args:
            filename: Name of the file
            file_content: File content as bytes
            subfolder: Optional subfolder name
            
        Returns:
            File ID if successful, None otherwise
        """
        if not self.service or not self.parent_folder_id:
            st.warning("Google Drive not authenticated or parent folder not found.")
            return None
        
        try:
            # Determine parent folder
            parent_id = self.parent_folder_id
            
            if subfolder:
                parent_id = self._ensure_subfolder(subfolder)
            
            # Prepare file metadata
            file_metadata = {
                'name': filename,
                'parents': [parent_id]
            }
            
            # Determine MIME type
            mime_type = self._get_mime_type(filename)
            
            # Create media upload
            media = MediaIoBaseUpload(
                BytesIO(file_content),
                mimetype=mime_type,
                resumable=True
            )
            
            # Upload file
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            file_id = file.get('id')
            web_link = file.get('webViewLink')
            
            st.success(f"✅ File uploaded: [{filename}]({web_link})")
            
            return file_id
            
        except Exception as e:
            st.error(f"Failed to upload file {filename}: {str(e)}")
            return None
    
    def _ensure_subfolder(self, subfolder_name: str) -> str:
        """Ensure subfolder exists and return its ID."""
        try:
            # Search for existing subfolder
            results = self.service.files().list(
                q=f"name='{subfolder_name}' and mimeType='application/vnd.google-apps.folder' and '{self.parent_folder_id}' in parents",
                fields="files(id, name)"
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                return folders[0]['id']
            else:
                # Create subfolder
                folder_metadata = {
                    'name': subfolder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [self.parent_folder_id]
                }
                
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                
                return folder.get('id')
                
        except Exception as e:
            st.error(f"Failed to create subfolder {subfolder_name}: {str(e)}")
            return self.parent_folder_id
    
    def _get_mime_type(self, filename: str) -> str:
        """Get MIME type based on file extension."""
        extension = filename.lower().split('.')[-1]
        
        mime_types = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'doc': 'application/msword',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'xls': 'application/vnd.ms-excel',
            'csv': 'text/csv',
            'txt': 'text/plain',
            'json': 'application/json'
        }
        
        return mime_types.get(extension, 'application/octet-stream')
    
    def list_files(self, subfolder: str = None) -> list:
        """List files in Drive folder."""
        if not self.service:
            return []
        
        try:
            parent_id = self.parent_folder_id
            if subfolder:
                parent_id = self._ensure_subfolder(subfolder)
            
            results = self.service.files().list(
                q=f"'{parent_id}' in parents",
                fields="files(id, name, createdTime, webViewLink)"
            ).execute()
            
            return results.get('files', [])
            
        except Exception as e:
            st.error(f"Failed to list files: {str(e)}")
            return []
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Download file content."""
        if not self.service:
            return None
        
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_content = request.execute()
            return file_content
            
        except Exception as e:
            st.error(f"Failed to download file: {str(e)}")
            return None
    
    def is_authenticated(self) -> bool:
        """Check if Google Drive is authenticated."""
        return self.service is not None and self.parent_folder_id is not None