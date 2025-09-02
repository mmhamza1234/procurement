#!/usr/bin/env python3
"""
Demo script for AEDCO One Platform
Showcases key features and functionality
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

def print_banner():
    """Print the AEDCO One Platform banner."""
    print("=" * 70)
    print("🚀 AEDCO ONE PLATFORM — NEWSLETTER EDITOR")
    print("=" * 70)
    print("📰 HTML-Only Newsletter Generation for 3 Sectors")
    print("🌍 Africa/Cairo Timezone • 2 Editions per Sector")
    print("🤖 OpenAI GPT-4 Powered • Consistent AEDCO Branding")
    print("=" * 70)

def show_sectors():
    """Display available sectors and their configurations."""
    print("\n📊 AVAILABLE SECTORS")
    print("-" * 40)
    
    try:
        from app import SECTORS
        
        for sector_key, sector_info in SECTORS.items():
            print(f"\n🔸 {sector_info['name']}")
            print(f"   Key: {sector_key}")
            print(f"   Sections: {len(sector_info['sections'])}")
            print(f"   Prompt: {sector_info['prompt_file']}")
            
            # Show first few sections
            for i, section in enumerate(sector_info['sections'][:3]):
                print(f"     {i+1}. {section}")
            if len(sector_info['sections']) > 3:
                print(f"     ... and {len(sector_info['sections']) - 3} more")
                
    except ImportError as e:
        print(f"❌ Could not load sectors: {e}")

def show_editions():
    """Display newsletter editions."""
    print("\n📋 NEWSLETTER EDITIONS")
    print("-" * 40)
    
    try:
        from app import EDITIONS
        
        for i, edition in enumerate(EDITIONS, 1):
            print(f"{i}. {edition} Edition")
            
        print(f"\n📈 Total Output: {len(EDITIONS) * len(SECTORS)} HTML files per run")
        
    except ImportError as e:
        print(f"❌ Could not load editions: {e}")

def show_date_logic():
    """Demonstrate date calculation logic."""
    print("\n📅 DATE CALCULATION LOGIC")
    print("-" * 40)
    
    try:
        from app import AEDCONewsletterGenerator
        
        generator = AEDCONewsletterGenerator()
        now = generator.get_cairo_datetime()
        
        print(f"Current Cairo Time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        # Test mode dates
        test_display, test_cutoff = generator.calculate_dates('test')
        print(f"\n🧪 Test Mode:")
        print(f"   Display Date: {test_display.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Research Cutoff: {test_cutoff.strftime('%Y-%m-%d %H:%M')}")
        
        # Production mode dates
        prod_display, prod_cutoff = generator.calculate_dates('production')
        print(f"\n🏭 Production Mode:")
        print(f"   Display Date: {prod_display.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Research Cutoff: {prod_cutoff.strftime('%Y-%m-%d %H:%M')}")
        
    except ImportError as e:
        print(f"❌ Could not load date logic: {e}")

def show_branding():
    """Display AEDCO branding information."""
    print("\n🎨 AEDCO BRANDING")
    print("-" * 40)
    
    try:
        from app import AEDCO_COLORS
        
        print(f"Primary Color: {AEDCO_COLORS['primary']}")
        print(f"Secondary Color: {AEDCO_COLORS['secondary']}")
        print(f"Gradient: {AEDCO_COLORS['gradient']}")
        
        # Show color preview
        print("\nColor Preview:")
        print("🔵 Primary: #0B3D91 (AEDCO Blue)")
        print("⚫ Secondary: #1F2937 (Dark Gray)")
        print("🌈 Gradient: Blue to Dark Gray")
        
    except ImportError as e:
        print(f"❌ Could not load branding: {e}")

def show_output_structure():
    """Show the output file structure."""
    print("\n📁 OUTPUT STRUCTURE")
    print("-" * 40)
    
    print("Generated files are organized by sector and date:")
    print("runs/")
    print("├── oil_gas/")
    print("│   └── 2024-01-15/")
    print("│       ├── Principals-OilGas-Newsletter-15-Jan-2024-FINAL.html")
    print("│       ├── EgyptianClients-OilGas-Newsletter-15-Jan-2024-FINAL.html")
    print("│       └── oil_gas_20240115_0900_manifest.json")
    print("├── transportation/")
    print("│   └── 2024-01-15/")
    print("│       ├── Principals-Transportation-Newsletter-15-Jan-2024-FINAL.html")
    print("│       ├── EgyptianClients-Transportation-Newsletter-15-Jan-2024-FINAL.html")
    print("│       └── transportation_20240115_0900_manifest.json")
    print("└── electricity/")
    print("    └── 2024-01-15/")
    print("        ├── Principals-Electricity-Newsletter-15-Jan-2024-FINAL.html")
    print("        ├── EgyptianClients-Electricity-Newsletter-15-Jan-2024-FINAL.html")
    print("        └── electricity_20240115_0900_manifest.json")

def show_features():
    """Highlight key platform features."""
    print("\n✨ KEY FEATURES")
    print("-" * 40)
    
    features = [
        "🎯 HTML-Only Output (No EML files)",
        "🌍 Africa/Cairo Timezone Support",
        "🤖 OpenAI GPT-4 Integration",
        "📊 3 Sectors: Oil & Gas, Transportation, Electricity",
        "📰 2 Editions: Principals + Egyptian Clients",
        "🔄 Past Issues Integration & Deduplication",
        "🎨 Consistent AEDCO Branding",
        "📱 Responsive Design & Mobile Support",
        "📁 File Management & ZIP Downloads",
        "🔒 Security & Input Validation"
    ]
    
    for feature in features:
        print(f"  {feature}")

def show_usage():
    """Show how to use the platform."""
    print("\n🚀 GETTING STARTED")
    print("-" * 40)
    
    print("1. Install Dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n2. Set Environment Variables:")
    print("   export OPENAI_API_KEY='your-api-key-here'")
    print("   export SECRET_KEY='your-secret-key-here'")
    
    print("\n3. Run the Platform:")
    print("   python run.py")
    print("   # or")
    print("   python app.py")
    
    print("\n4. Access the Interface:")
    print("   Open http://localhost:5000 in your browser")
    
    print("\n5. Generate Newsletters:")
    print("   - Select a sector (Oil & Gas, Transportation, Electricity)")
    print("   - Choose mode (Test or Production)")
    print("   - Click 'Generate Newsletter'")
    print("   - Preview and download HTML files")

def show_testing():
    """Show how to test the platform."""
    print("\n🧪 TESTING")
    print("-" * 40)
    
    print("Run the test suite to verify functionality:")
    print("   python test_platform.py")
    
    print("\nThis will test:")
    print("  ✅ Module imports")
    print("  ✅ File structure")
    print("  ✅ Configuration")
    print("  ✅ Sector prompts")
    print("  ✅ Date calculations")
    print("  ✅ Prompt sanitization")

def main():
    """Run the demo."""
    print_banner()
    
    show_sectors()
    show_editions()
    show_date_logic()
    show_branding()
    show_output_structure()
    show_features()
    show_usage()
    show_testing()
    
    print("\n" + "=" * 70)
    print("🎉 AEDCO One Platform Demo Complete!")
    print("📚 Check README.md for detailed documentation")
    print("🧪 Run test_platform.py to verify installation")
    print("🚀 Run run.py to start the platform")
    print("=" * 70)

if __name__ == '__main__':
    main()