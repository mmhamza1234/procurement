#!/usr/bin/env python3
"""
AEDCO One Platform — Newsletter Editor (HTML-Only, 6 Outputs)
Master application for generating sector-specific newsletters with HTML-only output.
"""

import os
import json
import base64
import zipfile
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pytz
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import openai

# Configuration
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'aedco-dev-secret-key-2024')

# OpenAI Configuration
openai.api_key = os.environ.get('OPENAI_API_KEY', 'your-openai-api-key-here')

# AEDCO Brand Colors
AEDCO_COLORS = {
    'primary': '#0B3D91',
    'secondary': '#1F2937',
    'gradient': 'linear-gradient(135deg, #0B3D91 0%, #1F2937 100%)'
}

# Sectors Configuration
SECTORS = {
    'oil_gas': {
        'name': 'Oil & Gas',
        'prompt_file': 'prompts/OilGas.txt',
        'sections': [
            'Market Snapshot',
            'Upstream – Exploration & Production (Egypt)',
            'Midstream – Pipelines, Gas & LNG (Egypt)',
            'Downstream – Refining & Petrochemicals (Egypt)',
            'Fertilizers (Egypt)',
            'Upstream Chemicals (Egypt)',
            'Projects (Egypt)'
        ]
    },
    'transportation': {
        'name': 'Transportation',
        'prompt_file': 'prompts/Transportation.txt',
        'sections': [
            'Market Snapshot',
            'Urban Rail & Metro (Egypt)',
            'National Rail (Egypt)',
            'Roads & Bridges (Egypt)',
            'Ports, Logistics & Suez Canal (Egypt)',
            'Public Transport & BRT (Egypt)',
            'Projects & Tenders (Egypt)'
        ]
    },
    'electricity': {
        'name': 'Electricity',
        'prompt_file': 'prompts/Electricity.txt',
        'sections': [
            'Market Snapshot',
            'Policy & Tariffs (Egypt)',
            'Generation — Thermal & IPP (Egypt)',
            'Renewables — Solar/Wind/Hydro (Egypt)',
            'Transmission & Grid Services (Egypt)',
            'Distribution & Smart Metering (Egypt)',
            'Projects & Tenders (Egypt)'
        ]
    }
}

# Editions
EDITIONS = ['Principals', 'Egyptian Clients']

# Color rotation for news cards
NEWS_CARD_COLORS = [
    {'border': '#0B3D91', 'background': '#eff6ff'},
    {'border': '#10b981', 'background': '#f0fdf4'},
    {'border': '#f59e0b', 'background': '#fef7f0'},
    {'border': '#ef4444', 'background': '#fef2f2'},
    {'border': '#8b5cf6', 'background': '#f5f3ff'},
    {'border': '#06b6d4', 'background': '#f0f9ff'},
    {'border': '#eab308', 'background': '#fefce8'},
    {'border': '#3b82f6', 'background': '#eff6ff'}
]

class AEDCONewsletterGenerator:
    """Core newsletter generation engine for AEDCO One Platform."""
    
    def __init__(self):
        self.cairo_tz = pytz.timezone('Africa/Cairo')
        self.base_path = Path(__file__).parent
        
    def get_cairo_datetime(self) -> datetime:
        """Get current datetime in Africa/Cairo timezone."""
        return datetime.now(self.cairo_tz)
    
    def calculate_dates(self, mode: str) -> Tuple[datetime, datetime]:
        """
        Calculate display date and research cutoff based on mode.
        
        Args:
            mode: 'production' or 'test'
            
        Returns:
            Tuple of (display_date, cutoff_date)
        """
        now = self.get_cairo_datetime()
        
        if mode == 'production':
            # Production: Next/current Monday at 09:00, cutoff at 08:00
            days_ahead = 7 - now.weekday()  # Days until Monday
            if days_ahead == 7:  # Today is Monday
                days_ahead = 0
            monday = now + timedelta(days=days_ahead)
            cutoff = monday.replace(hour=8, minute=0, second=0, microsecond=0)
            display_date = monday.replace(hour=9, minute=0, second=0, microsecond=0)
        else:
            # Test: Next 09:00 (same day or next day)
            today_9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
            if now < today_9am:
                display_date = today_9am
            else:
                display_date = today_9am + timedelta(days=1)
            cutoff = display_date - timedelta(hours=1)
        
        return display_date, cutoff
    
    def load_sector_prompt(self, sector: str) -> str:
        """Load and sanitize sector prompt, enforcing HTML-only output."""
        prompt_file = self.base_path / SECTORS[sector]['prompt_file']
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            original_prompt = f.read()
        
        # Enforce HTML-only output by prepending overrides
        html_override = """OUTPUT_MODE=HTML_ONLY
IGNORE_EML=true
RENDER_ONLY: HTML web preview per edition

IMPORTANT: Generate HTML files only. Ignore any EML/email directives in the original prompt.
"""
        
        # Strip EML-related sections
        sanitized_prompt = self._remove_eml_sections(original_prompt)
        
        return html_override + sanitized_prompt
    
    def _remove_eml_sections(self, prompt: str) -> str:
        """Remove EML-related sections from the prompt."""
        import re
        
        # Patterns to remove EML-related content
        eml_patterns = [
            r'(?i)(^|\n)\*+\s*EML[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)(^|\n)EML[-\s]Specific[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)multipart/related[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)MIME[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)Content-Type[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)Content-ID[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)Content-Disposition[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)Content-Transfer-Encoding[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)Message-ID[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)Subject[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)Date[\s\S]*?(?=\n\*{3,}|$)',
            r'(?i)boundary[\s\S]*?(?=\n\*{3,}|$)'
        ]
        
        sanitized = prompt
        for pattern in eml_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.MULTILINE | re.DOTALL)
        
        return sanitized
    
    def load_past_issues(self, sector: str) -> str:
        """Load past issues for deduplication."""
        past_issues_dir = self.base_path / 'past_issues' / sector
        if not past_issues_dir.exists():
            return ""
        
        past_issues = []
        for date_dir in sorted(past_issues_dir.iterdir(), reverse=True)[:5]:  # Last 5 dates
            if date_dir.is_dir():
                for edition_file in date_dir.glob('*.txt'):
                    with open(edition_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        past_issues.append(f"--- {edition_file.stem} ({date_dir.name}) ---\n{content}\n")
        
        if past_issues:
            return "\n--- PAST_ISSUES_START ---\n" + "\n".join(past_issues)
        return ""
    
    def generate_newsletter(self, sector: str, mode: str = 'test') -> Dict:
        """
        Generate newsletter for a sector using OpenAI API.
        
        Args:
            sector: Sector key (oil_gas, transportation, electricity)
            mode: Generation mode ('production' or 'test')
            
        Returns:
            Dictionary with generation results and metadata
        """
        try:
            # Calculate dates
            display_date, cutoff = self.calculate_dates(mode)
            
            # Load and prepare prompt
            base_prompt = self.load_sector_prompt(sector)
            past_issues = self.load_past_issues(sector)
            
            # Assemble final prompt
            final_prompt = f"""{base_prompt}

GENERATION CONTEXT:
- Sector: {SECTORS[sector]['name']}
- Mode: {mode.title()}
- Display Date: {display_date.strftime('%d %b %Y')} 09:00 Africa/Cairo
- Research Cutoff: {cutoff.strftime('%d %b %Y %H:%M')} Africa/Cairo
- Timezone: Africa/Cairo
- Brand: AEDCO (Arab Engineering & Distribution Company)
- Logo: /assets/aedco-logo-blue.png

{past_issues}

IMPORTANT: Generate HTML files only. Output exactly 2 HTML files:
1. Principals Edition HTML (web preview, no logo)
2. Egyptian Clients Edition HTML (web preview, no logo)

No EML files. No email formatting. Pure HTML newsletters only.
"""
            
            # Generate content using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are AEDCO's newsletter researcher & formatter. Follow instructions strictly. Facts only. Inline links only. Output HTML only. Generate exactly 2 HTML files as specified."
                    },
                    {
                        "role": "user",
                        "content": final_prompt
                    }
                ],
                temperature=0.2,
                max_tokens=8000
            )
            
            # Parse response and extract HTML content
            content = response.choices[0].message.content
            
            # Extract HTML files from response
            html_files = self._extract_html_files(content, sector, display_date)
            
            # Save files and create manifest
            run_id = f"{sector}_{display_date.strftime('%Y%m%d_%H%M')}"
            run_dir = self.base_path / 'runs' / sector / display_date.strftime('%Y-%m-%d')
            run_dir.mkdir(parents=True, exist_ok=True)
            
            # Save HTML files
            saved_files = []
            for edition, html_content in html_files.items():
                filename = f"{edition}-{SECTORS[sector]['name'].replace(' ', '')}-Newsletter-{display_date.strftime('%d-%b-%Y')}-FINAL.html"
                file_path = run_dir / filename
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                saved_files.append({
                    'edition': edition,
                    'filename': filename,
                    'path': str(file_path),
                    'size': len(html_content)
                })
            
            # Create manifest
            manifest = {
                'run_id': run_id,
                'sector': sector,
                'sector_name': SECTORS[sector]['name'],
                'mode': mode,
                'display_date': display_date.isoformat(),
                'cutoff_date': cutoff.isoformat(),
                'timezone': 'Africa/Cairo',
                'files_generated': len(saved_files),
                'files': saved_files,
                'tokens_used': response.usage.total_tokens,
                'cost_estimate': self._estimate_cost(response.usage),
                'generated_at': datetime.now().isoformat()
            }
            
            # Save manifest
            manifest_path = run_dir / f"{run_id}_manifest.json"
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True,
                'manifest': manifest,
                'run_dir': str(run_dir),
                'message': f"Successfully generated {len(saved_files)} HTML newsletters for {SECTORS[sector]['name']}"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to generate newsletter: {str(e)}"
            }
    
    def _extract_html_files(self, content: str, sector: str, display_date: datetime) -> Dict[str, str]:
        """Extract HTML files from OpenAI response."""
        html_files = {}
        
        # Look for HTML content blocks
        import re
        
        # Pattern to find HTML content
        html_pattern = r'<!DOCTYPE html[^>]*>.*?</html>'
        html_blocks = re.findall(html_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if len(html_blocks) >= 2:
            # First HTML block is Principals Edition
            html_files['Principals'] = html_blocks[0]
            # Second HTML block is Egyptian Clients Edition
            html_files['Egyptian Clients'] = html_blocks[1]
        else:
            # Fallback: create basic HTML structure
            html_files['Principals'] = self._create_fallback_html('Principals', sector, display_date)
            html_files['Egyptian Clients'] = self._create_fallback_html('Egyptian Clients', sector, display_date)
        
        return html_files
    
    def _create_fallback_html(self, edition: str, sector: str, display_date: datetime) -> str:
        """Create fallback HTML if OpenAI doesn't generate proper HTML."""
        sector_name = SECTORS[sector]['name']
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{edition} - {sector_name} Newsletter</title>
    <style>
        body {{ font-family: -apple-system, 'Segoe UI', Roboto, Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
        .container {{ max-width: 700px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #0B3D91 0%, #1F2937 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .header .date {{ margin-top: 10px; opacity: 0.9; }}
        .content {{ padding: 30px; }}
        .market-snapshot {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }}
        .metric-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #0B3D91; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #0B3D91; }}
        .metric-label {{ color: #6b7280; margin-top: 5px; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #0B3D91; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }}
        .news-card {{ border-left: 4px solid #0B3D91; background: #eff6ff; padding: 20px; border-radius: 12px; }}
        .news-title {{ font-weight: bold; color: #0B3D91; margin-bottom: 10px; }}
        .footer {{ background: linear-gradient(135deg, #0B3D91 0%, #1F2937 100%); color: white; padding: 20px; text-align: center; }}
        @media (max-width: 600px) {{ .market-snapshot {{ grid-template-columns: 1fr; }} .news-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{edition} Edition</h1>
            <div class="date">{sector_name} Newsletter - {display_date.strftime('%d %B %Y')}</div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>Market Snapshot</h2>
                <div class="market-snapshot">
                    <div class="metric-card">
                        <div class="metric-value">--</div>
                        <div class="metric-label">Market Data</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">--</div>
                        <div class="metric-label">Industry Metrics</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">--</div>
                        <div class="metric-label">Performance</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>News & Updates</h2>
                <div class="news-grid">
                    <div class="news-card">
                        <div class="news-title">Content Generation</div>
                        <p>Newsletter content is being generated. Please check back shortly for the complete {sector_name} newsletter.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>{edition} - {sector_name} Newsletter | {display_date.strftime('%d %B %Y')}</p>
            <p style="font-size: 12px; opacity: 0.8;">Confidential - For internal use only</p>
        </div>
    </div>
</body>
</html>"""
    
    def _estimate_cost(self, usage) -> float:
        """Estimate cost based on token usage (GPT-4 pricing)."""
        # GPT-4 pricing (approximate)
        input_cost_per_1k = 0.03
        output_cost_per_1k = 0.06
        
        input_cost = (usage.prompt_tokens / 1000) * input_cost_per_1k
        output_cost = (usage.completion_tokens / 1000) * output_cost_per_1k
        
        return round(input_cost + output_cost, 4)

# Initialize generator
generator = AEDCONewsletterGenerator()

@app.route('/')
def index():
    """Main editor interface."""
    return render_template('index.html', sectors=SECTORS, editions=EDITIONS, colors=AEDCO_COLORS)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for newsletter generation."""
    try:
        data = request.get_json()
        sector = data.get('sector')
        mode = data.get('mode', 'test')
        
        if sector not in SECTORS:
            return jsonify({'success': False, 'error': 'Invalid sector'}), 400
        
        # Generate newsletter
        result = generator.generate_newsletter(sector, mode)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sectors')
def api_sectors():
    """Get available sectors."""
    return jsonify(SECTORS)

@app.route('/api/past-issues/<sector>')
def api_past_issues(sector):
    """Get past issues for a sector."""
    if sector not in SECTORS:
        return jsonify({'error': 'Invalid sector'}), 400
    
    past_issues = generator.load_past_issues(sector)
    return jsonify({'past_issues': past_issues})

@app.route('/api/upload-past-issue', methods=['POST'])
def api_upload_past_issue():
    """Upload a past issue file."""
    try:
        sector = request.form.get('sector')
        edition = request.form.get('edition')
        date = request.form.get('date')
        
        if not all([sector, edition, date]) or sector not in SECTORS:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Save file
        past_issues_dir = Path(__file__).parent / 'past_issues' / sector / date
        past_issues_dir.mkdir(parents=True, exist_ok=True)
        
        filename = secure_filename(f"{edition}.txt")
        file_path = past_issues_dir / filename
        
        file.save(file_path)
        
        return jsonify({
            'success': True,
            'message': f'Past issue uploaded successfully',
            'file_path': str(file_path)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download-run/<sector>/<date>')
def api_download_run(sector, date):
    """Download a complete run as ZIP file."""
    try:
        run_dir = Path(__file__).parent / 'runs' / sector / date
        
        if not run_dir.exists():
            return jsonify({'error': 'Run not found'}), 404
        
        # Create temporary ZIP file
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
            with zipfile.ZipFile(tmp_file.name, 'w') as zipf:
                for file_path in run_dir.rglob('*'):
                    if file_path.is_file():
                        zipf.write(file_path, file_path.relative_to(run_dir))
        
        return send_file(
            tmp_file.name,
            as_attachment=True,
            download_name=f"{sector}_{date}_newsletters.zip",
            mimetype='application/zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/run-status/<sector>/<date>')
def api_run_status(sector, date):
    """Get status of a specific run."""
    try:
        run_dir = Path(__file__).parent / 'runs' / sector / date
        
        if not run_dir.exists():
            return jsonify({'error': 'Run not found'}), 404
        
        # Find manifest file
        manifest_files = list(run_dir.glob('*_manifest.json'))
        if not manifest_files:
            return jsonify({'error': 'Manifest not found'}), 404
        
        with open(manifest_files[0], 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        return jsonify(manifest)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)