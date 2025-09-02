#!/usr/bin/env python3
"""
Startup script for AEDCO One Platform
Handles environment setup and application launch
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set default environment if not specified
if 'FLASK_ENV' not in os.environ:
    os.environ['FLASK_ENV'] = 'development'

# Import and run the application
from app import app

if __name__ == '__main__':
    print("🚀 Starting AEDCO One Platform...")
    print(f"📍 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"🌍 Timezone: Africa/Cairo")
    print(f"🔑 OpenAI API: {'Configured' if os.environ.get('OPENAI_API_KEY') else 'Not configured'}")
    print(f"🌐 Server: http://localhost:5000")
    print("=" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=os.environ.get('FLASK_ENV') == 'development'
        )
    except KeyboardInterrupt:
        print("\n👋 AEDCO One Platform stopped by user")
    except Exception as e:
        print(f"❌ Error starting AEDCO One Platform: {e}")
        sys.exit(1)