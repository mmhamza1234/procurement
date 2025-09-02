#!/usr/bin/env python3
"""
Test script for AEDCO One Platform
Verifies core functionality without requiring OpenAI API
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import app
        print("✅ Main app module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import main app: {e}")
        return False
    
    try:
        import config
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import config: {e}")
        return False
    
    try:
        from datetime import datetime, timedelta
        import pytz
        print("✅ Date/time modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import date/time modules: {e}")
        return False
    
    return True

def test_file_structure():
    """Test that all required files and directories exist."""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'run.py'
    ]
    
    required_dirs = [
        'templates',
        'static',
        'static/js',
        'prompts',
        'assets',
        'past_issues',
        'runs'
    ]
    
    required_prompts = [
        'prompts/OilGas.txt',
        'prompts/Transportation.txt',
        'prompts/Electricity.txt'
    ]
    
    all_good = True
    
    # Check required files
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_good = False
    
    # Check required directories
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - Missing")
            all_good = False
    
    # Check prompt files
    for prompt_path in required_prompts:
        if Path(prompt_path).exists():
            print(f"✅ {prompt_path}")
        else:
            print(f"❌ {prompt_path} - Missing")
            all_good = False
    
    return all_good

def test_configuration():
    """Test configuration loading."""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import current_config, get_config
        
        # Test config loading
        config = get_config()
        print(f"✅ Configuration loaded: {config.__class__.__name__}")
        
        # Test brand colors
        if hasattr(config, 'BRAND_COLORS'):
            print(f"✅ Brand colors configured: {config.BRAND_COLORS['primary']}")
        else:
            print("❌ Brand colors not configured")
            return False
        
        # Test timezone
        if hasattr(config, 'DEFAULT_TIMEZONE'):
            print(f"✅ Default timezone: {config.DEFAULT_TIMEZONE}")
        else:
            print("❌ Default timezone not configured")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_sector_prompts():
    """Test that sector prompts can be loaded and parsed."""
    print("\n📝 Testing sector prompts...")
    
    try:
        from app import SECTORS
        
        for sector_key, sector_info in SECTORS.items():
            prompt_file = Path(sector_info['prompt_file'])
            
            if prompt_file.exists():
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) > 1000:  # Basic size check
                        print(f"✅ {sector_key}: {sector_info['name']} - {len(content)} chars")
                    else:
                        print(f"⚠️ {sector_key}: Content seems too short ({len(content)} chars)")
            else:
                print(f"❌ {sector_key}: Prompt file not found")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Sector prompts test failed: {e}")
        return False

def test_date_calculations():
    """Test date calculation logic."""
    print("\n📅 Testing date calculations...")
    
    try:
        from app import AEDCONewsletterGenerator
        
        generator = AEDCONewsletterGenerator()
        
        # Test Cairo timezone
        cairo_time = generator.get_cairo_datetime()
        print(f"✅ Cairo time: {cairo_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        # Test production mode dates
        prod_display, prod_cutoff = generator.calculate_dates('production')
        print(f"✅ Production display: {prod_display.strftime('%Y-%m-%d %H:%M')}")
        print(f"✅ Production cutoff: {prod_cutoff.strftime('%Y-%m-%d %H:%M')}")
        
        # Test test mode dates
        test_display, test_cutoff = generator.calculate_dates('test')
        print(f"✅ Test display: {test_display.strftime('%Y-%m-%d %H:%M')}")
        print(f"✅ Test cutoff: {test_cutoff.strftime('%Y-%m-%d %H:%M')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Date calculations test failed: {e}")
        return False

def test_prompt_sanitization():
    """Test EML removal from prompts."""
    print("\n🧹 Testing prompt sanitization...")
    
    try:
        from app import AEDCONewsletterGenerator
        
        generator = AEDCONewsletterGenerator()
        
        # Test with a sample prompt containing EML content
        test_prompt = """
        This is a test prompt.
        
        ***
        EML-Specific Requirements:
        - Multipart/related MIME structure
        - Logo attachment with Content-ID: <aedco-logo>
        - Base64 placeholder for logo content
        
        ***
        HTML Structure:
        <!DOCTYPE html>
        <html>
        <body>Content</body>
        </html>
        """
        
        sanitized = generator._remove_eml_sections(test_prompt)
        
        # Check that EML content was removed
        if 'EML-Specific' not in sanitized and 'Content-ID' not in sanitized:
            print("✅ EML content successfully removed")
            return True
        else:
            print("❌ EML content not properly removed")
            return False
            
    except Exception as e:
        print(f"❌ Prompt sanitization test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 AEDCO One Platform - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_file_structure,
        test_configuration,
        test_sector_prompts,
        test_date_calculations,
        test_prompt_sanitization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test {test.__name__} failed")
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AEDCO One Platform is ready to run.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)