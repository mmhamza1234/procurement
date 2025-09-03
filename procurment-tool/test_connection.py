#!/usr/bin/env python3
"""
Test script for Hamada Tool database connection
Run this script to verify your Supabase setup is working correctly
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

def test_supabase_connection():
    """Test the Supabase connection and basic operations"""
    
    # Load environment variables
    load_dotenv()
    
    # Get Supabase credentials
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
        return False
    
    try:
        # Create Supabase client
        print("🔗 Connecting to Supabase...")
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Test connection by inserting a test record
        print("📝 Testing database operations...")
        
        test_data = {
            'activity_type': 'connection_test',
            'data': {
                'test_message': 'Database connection successful',
                'timestamp': datetime.utcnow().isoformat(),
                'tool_version': 'hamada_tool_v1.0'
            },
            'user_id': 'test_user',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Insert test record
        result = supabase.table('user_activities').insert(test_data).execute()
        
        if result.data:
            print("✅ Successfully inserted test record")
            
            # Query the test record
            query_result = supabase.table('user_activities').select('*').eq('activity_type', 'connection_test').execute()
            
            if query_result.data:
                print(f"✅ Successfully queried {len(query_result.data)} test records")
                
                # Clean up test records
                supabase.table('user_activities').delete().eq('activity_type', 'connection_test').execute()
                print("🧹 Cleaned up test records")
                
                return True
            else:
                print("❌ Failed to query test records")
                return False
        else:
            print("❌ Failed to insert test record")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your SUPABASE_URL and SUPABASE_ANON_KEY in .env file")
        print("2. Make sure you've run the setup_database.sql script in Supabase")
        print("3. Verify your Supabase project is active")
        print("4. Check your internet connection")
        return False

def test_environment_variables():
    """Test that all required environment variables are set"""
    
    print("🔍 Checking environment variables...")
    
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    optional_vars = [
        'ANTHROPIC_API_KEY', 'ELEVENLABS_API_KEY', 'GEMINI_API_KEY', 
        'OPENAI_API_KEY', 'GOOGLE_OAUTH_CLIENT_ID', 'GOOGLE_OAUTH_CLIENT_SECRET',
        'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER'
    ]
    
    # Check required variables
    missing_required = []
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        return False
    else:
        print("✅ All required environment variables are set")
    
    # Check optional variables
    set_optional = []
    for var in optional_vars:
        if os.getenv(var):
            set_optional.append(var)
    
    if set_optional:
        print(f"✅ Optional variables set: {', '.join(set_optional)}")
    else:
        print("ℹ️  No optional variables set (this is fine)")
    
    return True

def main():
    """Main test function"""
    
    print("🧪 Hamada Tool - Database Connection Test")
    print("=" * 50)
    
    # Test environment variables
    env_ok = test_environment_variables()
    
    if not env_ok:
        print("\n❌ Environment variables test failed")
        return
    
    print("\n" + "=" * 50)
    
    # Test database connection
    db_ok = test_supabase_connection()
    
    print("\n" + "=" * 50)
    
    if db_ok:
        print("🎉 All tests passed! Your Hamada Tool setup is ready.")
        print("\n🚀 You can now run the application with:")
        print("   streamlit run app.py")
    else:
        print("❌ Database connection test failed")
        print("\n🔧 Please fix the issues above before running the application")

if __name__ == "__main__":
    main()