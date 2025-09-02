#!/usr/bin/env python3
"""
Simple Demo for AEDCO One Platform
Works without external dependencies to showcase the platform structure
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print the AEDCO One Platform banner."""
    print("=" * 70)
    print("🚀 AEDCO ONE PLATFORM — NEWSLETTER EDITOR")
    print("=" * 70)
    print("📰 HTML-Only Newsletter Generation for 3 Sectors")
    print("🌍 Africa/Cairo Timezone • 2 Editions per Sector")
    print("🤖 OpenAI GPT-4 Powered • Consistent AEDCO Branding")
    print("=" * 70)

def show_project_structure():
    """Display the project structure."""
    print("\n📁 PROJECT STRUCTURE")
    print("-" * 40)
    
    project_dir = Path(__file__).parent
    
    # Show main files
    main_files = [
        'app.py',
        'config.py', 
        'requirements.txt',
        'README.md',
        'run.py',
        'test_platform.py',
        'demo.py'
    ]
    
    print("Main Files:")
    for file_name in main_files:
        file_path = project_dir / file_name
        if file_path.exists():
            print(f"  ✅ {file_name}")
        else:
            print(f"  ❌ {file_name} - Missing")
    
    # Show directories
    directories = [
        'templates',
        'static',
        'static/js',
        'prompts',
        'assets',
        'past_issues',
        'runs'
    ]
    
    print("\nDirectories:")
    for dir_name in directories:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ - Missing")
    
    # Show prompt files
    print("\nSector Prompts:")
    prompt_files = [
        'prompts/OilGas.txt',
        'prompts/Transportation.txt',
        'prompts/Electricity.txt'
    ]
    
    for prompt_file in prompt_files:
        prompt_path = project_dir / prompt_file
        if prompt_path.exists():
            # Get file size
            size = prompt_path.stat().st_size
            print(f"  ✅ {prompt_file} ({size:,} bytes)")
        else:
            print(f"  ❌ {prompt_file} - Missing")

def show_sector_configuration():
    """Show the sector configuration from the app.py file."""
    print("\n📊 SECTOR CONFIGURATION")
    print("-" * 40)
    
    try:
        # Read the sectors configuration from app.py
        app_file = Path(__file__).parent / 'app.py'
        if app_file.exists():
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract sector information
            sectors = {
                'oil_gas': 'Oil & Gas',
                'transportation': 'Transportation', 
                'electricity': 'Electricity'
            }
            
            for sector_key, sector_name in sectors.items():
                print(f"\n🔸 {sector_name}")
                print(f"   Key: {sector_key}")
                
                # Count sections by looking for patterns in the file
                section_count = content.count(f"'{sector_key}':")
                print(f"   Configuration: Found in app.py")
                
        else:
            print("❌ app.py not found")
            
    except Exception as e:
        print(f"❌ Error reading sector configuration: {e}")

def show_prompt_samples():
    """Show samples from the sector prompts."""
    print("\n📝 PROMPT SAMPLES")
    print("-" * 40)
    
    project_dir = Path(__file__).parent
    
    for prompt_file in ['OilGas.txt', 'Transportation.txt', 'Electricity.txt']:
        prompt_path = project_dir / 'prompts' / prompt_file
        if prompt_path.exists():
            print(f"\n📄 {prompt_file}:")
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Show first few lines
            lines = content.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"   {line}")
            
            if len(content.split('\n')) > 5:
                print(f"   ... ({len(content.split('\n')) - 5} more lines)")
        else:
            print(f"❌ {prompt_file} not found")

def show_requirements():
    """Show the Python requirements."""
    print("\n📦 PYTHON REQUIREMENTS")
    print("-" * 40)
    
    requirements_file = Path(__file__).parent / 'requirements.txt'
    if requirements_file.exists():
        with open(requirements_file, 'r', encoding='utf-8') as f:
            requirements = f.read()
        
        print("Required packages:")
        for line in requirements.split('\n'):
            if line.strip() and not line.startswith('#'):
                print(f"  📦 {line}")
    else:
        print("❌ requirements.txt not found")

def show_usage_instructions():
    """Show usage instructions."""
    print("\n🚀 USAGE INSTRUCTIONS")
    print("-" * 40)
    
    instructions = [
        "1. Install Python 3.8+ and pip",
        "2. Install dependencies: pip install -r requirements.txt",
        "3. Set OpenAI API key: export OPENAI_API_KEY='your-key'",
        "4. Run the platform: python run.py",
        "5. Open browser to: http://localhost:5000",
        "6. Select sector and generate newsletters"
    ]
    
    for instruction in instructions:
        print(f"  {instruction}")

def show_features():
    """Show platform features."""
    print("\n✨ PLATFORM FEATURES")
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

def show_output_examples():
    """Show example output file names."""
    print("\n📄 OUTPUT EXAMPLES")
    print("-" * 40)
    
    sectors = ['OilGas', 'Transportation', 'Electricity']
    editions = ['Principals', 'EgyptianClients']
    date = '15-Jan-2024'
    
    print("Generated HTML files:")
    for sector in sectors:
        for edition in editions:
            filename = f"{edition}-{sector}-Newsletter-{date}-FINAL.html"
            print(f"  📄 {filename}")
    
    print(f"\n📊 Total: {len(sectors) * len(editions)} HTML files per run")

def main():
    """Run the simple demo."""
    print_banner()
    
    show_project_structure()
    show_sector_configuration()
    show_prompt_samples()
    show_requirements()
    show_features()
    show_output_examples()
    show_usage_instructions()
    
    print("\n" + "=" * 70)
    print("🎉 AEDCO One Platform Simple Demo Complete!")
    print("📚 Check README.md for detailed documentation")
    print("🚀 Install dependencies and run run.py to start")
    print("=" * 70)

if __name__ == '__main__':
    main()