# AEDCO One Platform — Newsletter Editor

A comprehensive platform for generating sector-specific newsletters with HTML-only output, designed for AEDCO (Arab Engineering & Distribution Company).

## 🎯 Purpose

The AEDCO One Platform enables editors to:

- **Upload Past Issues** per sector for deduplication and context
- **Generate Two Editions** (Principals + Egyptian Clients) for any sector
- **Enforce HTML-only Output** (no EML files)
- **Apply AEDCO Branding** consistently across all newsletters
- **Respect Cairo Timezone** dating logic for production and test runs

## 🏗️ Architecture

### 3-Pane Interface
- **Left Pane**: Sector selection & past issues management
- **Center Pane**: Generation controls & configuration
- **Right Pane**: Live HTML preview & file downloads

### Core Components
- **Flask Backend**: RESTful API for newsletter generation
- **OpenAI Integration**: GPT-4 powered content research and formatting
- **Sector Prompts**: Specialized instructions for Oil & Gas, Transportation, and Electricity
- **HTML-Only Output**: Enforced through prompt sanitization and validation

## 🚀 Features

### Sector Support
- **Oil & Gas**: Upstream, midstream, downstream, fertilizers, chemicals, projects
- **Transportation**: Metro, rail, roads, ports, logistics, Suez Canal
- **Electricity**: Generation, transmission, distribution, renewables, smart grid

### Generation Modes
- **Test Mode**: Generates for next 09:00 Africa/Cairo (same/next day)
- **Production Mode**: Generates for next Monday 09:00 Africa/Cairo

### Content Features
- **Market Snapshots**: Sector-specific metrics and indicators
- **News Cards**: 8-color rotation system with responsive 2-column layout
- **Past Issues Integration**: Deduplication and "Update:" tagging
- **Brand Consistency**: AEDCO gradient, logos, and typography

## 📁 Project Structure

```
aedco_one_platform/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── assets/               # Brand assets (logos, images)
├── prompts/              # Sector-specific generation prompts
│   ├── OilGas.txt
│   ├── Transportation.txt
│   └── Electricity.txt
├── past_issues/          # Uploaded past issues by sector/date
├── runs/                 # Generated newsletters by sector/date
├── templates/            # HTML templates
│   └── index.html        # Main editor interface
└── static/               # Static assets
    ├── css/              # Stylesheets
    └── js/               # JavaScript
        └── app.js        # Frontend application logic
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- Modern web browser

### Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aedco_one_platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   export SECRET_KEY="your-secret-key-here"
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the platform**
   Open your browser and navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for GPT-4 access
- `SECRET_KEY`: Flask secret key for session management

### OpenAI Settings
- **Model**: GPT-4
- **Temperature**: 0.2 (for consistent output)
- **Max Tokens**: 8000
- **System Message**: AEDCO newsletter researcher & formatter

## 📊 Output Contract

### 6 HTML Files Per Run
| # | Sector | Edition | File Name |
|---|--------|---------|-----------|
| 1 | Oil & Gas | Principals | `Principals-OilGas-Newsletter-[DD-Mon-YYYY]-FINAL.html` |
| 2 | Oil & Gas | Egyptian Clients | `EgyptianClients-OilGas-Newsletter-[DD-Mon-YYYY]-FINAL.html` |
| 3 | Transportation | Principals | `Principals-Transportation-Newsletter-[DD-Mon-YYYY]-FINAL.html` |
| 4 | Transportation | Egyptian Clients | `EgyptianClients-Transportation-Newsletter-[DD-Mon-YYYY]-FINAL.html` |
| 5 | Electricity | Principals | `Principals-Electricity-Newsletter-[DD-Mon-YYYY]-FINAL.html` |
| 6 | Electricity | Egyptian Clients | `EgyptianClients-Electricity-Newsletter-[DD-Mon-YYYY]-FINAL.html` |

**Note**: No EML files are produced. All sector prompts are sanitized to enforce HTML-only output.

## 🎨 Design System

### Brand Colors
- **Primary**: `#0B3D91` (AEDCO Blue)
- **Secondary**: `#1F2937` (Dark Gray)
- **Gradient**: `linear-gradient(135deg, #0B3D91 0%, #1F2937 100%)`

### Typography
- **Fonts**: -apple-system, 'Segoe UI', Roboto, Arial
- **Title**: 16px bold `#0B3D91`
- **Body**: 15px `#374151`

### Layout
- **Max Width**: 700px (responsive)
- **News Cards**: 2-column grid with odd-item full-width logic
- **Color Rotation**: 8-color system for visual variety

## 🔒 Security Features

- **Input Sanitization**: Script removal from HTML content
- **File Upload Validation**: Supported formats only (PDF, HTML, EML, TXT)
- **Rate Limiting**: API call throttling and backoff
- **Authentication**: Session-based access control

## 📈 Quality Assurance

### Content Validation
- Section and bullet count verification
- Layout logic validation (2-column + odd-item handling)
- Brand consistency checks
- Date and filename consistency

### Technical Validation
- HTML syntax validation
- Mobile responsiveness testing
- Color rotation verification
- Link integrity checks

## 🚨 Error Handling

- **Insufficient Data**: Graceful fallback with "insufficient data" indicators
- **API Failures**: Retry logic with exponential backoff
- **File Generation**: Fallback HTML templates for failed generations
- **User Feedback**: Clear error messages and status indicators

## 🔄 API Endpoints

### Core Endpoints
- `GET /` - Main editor interface
- `POST /api/generate` - Generate newsletter
- `GET /api/sectors` - Get available sectors
- `GET /api/past-issues/<sector>` - Get past issues for sector

### File Management
- `POST /api/upload-past-issue` - Upload past issue file
- `GET /api/download-run/<sector>/<date>` - Download run as ZIP
- `GET /api/run-status/<sector>/<date>` - Get run status

## 📱 Browser Support

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: Responsive design with mobile-optimized layouts
- **JavaScript**: ES6+ features with fallback support

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is proprietary software developed for AEDCO (Arab Engineering & Distribution Company).

## 🆘 Support

For technical support or questions about the AEDCO One Platform:

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs or feature requests through the issue tracker
- **Contact**: Reach out to the development team

---

**AEDCO One Platform** — Empowering newsletter generation with AI-powered research and consistent branding.