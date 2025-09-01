# Overview

Hamada Tool is an automated tender-reading and supplier-quoting productivity application designed specifically for the oil & gas procurement industry. Built for Arab Engineering & Distribution Company, this Streamlit-based tool streamlines the procurement process by automating document parsing, supplier management, email generation, and deadline tracking for bulk materials including piping, valves, flanges, fittings, bolts, gaskets, and finned tubes.

The application provides a comprehensive end-to-end solution that ingests tender documents in multiple formats (PDF, Word, Excel, text), extracts key information, manages a database of 100+ suppliers across different regions, generates professional email drafts for quotation requests, and automatically calculates supplier deadlines based on client requirements.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses **Streamlit** as the web framework, providing a clean, interactive interface with multiple modules accessible through sidebar navigation. The UI is organized into five main sections: Document Processing, Supplier Management, Email Generation, Deadline Management, and Dashboard. Session state management maintains application state across user interactions, ensuring data persistence during the session.

## Backend Architecture
The system follows a **modular architecture** with separate Python modules handling distinct functionality:

- **DocumentParser**: Handles multi-format document ingestion (PDF, Word, Excel, text) with OCR capabilities and intelligent information extraction using regex patterns for deadlines, material specifications, and requirements
- **SupplierManager**: Manages CRUD operations for the CSV-backed supplier database with filtering and search capabilities
- **EmailGenerator**: Creates professional email drafts with customizable templates and origin filtering notes
- **DeadlineCalculator**: Automatically detects client deadlines and calculates supplier deadlines with configurable buffer periods (default 2 days)

The application maintains material categories as configurable constants, allowing easy modification of supported materials (piping, valves, flanges, fittings, bolts, gaskets, finned tubes).

## Data Storage Solutions
The system uses a **CSV-based data model** for supplier information, providing:
- User-editable supplier database stored in `data/oil_gas_suppliers_consolidated.csv`
- Structured schema with fields for company details, contact information, specializations, and material categories
- In-memory DataFrame operations for fast filtering and manipulation
- Automatic file initialization with proper column structure

## Authentication and Authorization
Currently implements a **single-user model** without authentication, designed for deployment in controlled environments. The application assumes trusted user access within the corporate network.

## Processing Pipeline
The document processing pipeline implements intelligent parsing with:
- Multi-format support (native PDF, scanned PDF, Word, Excel, plain text)
- Regex-based pattern matching for deadline extraction
- Material category identification using keyword matching
- Specification extraction for technical requirements
- Automatic data validation and error handling

# External Dependencies

## Core Framework Dependencies
- **Streamlit**: Primary web application framework for UI and user interactions
- **Pandas**: Data manipulation and analysis for supplier database operations and CSV handling

## Document Processing Dependencies
- **Python standard libraries**: `re`, `datetime`, `os`, `io` for core functionality
- **File processing libraries**: Built-in support for text and CSV parsing, with extensibility for PDF and Word document processing

## Data Storage
- **CSV files**: Local file storage for supplier database with no external database dependencies
- **File system**: Local storage for uploaded documents and generated outputs

## Email and Communication
- **Email draft generation**: Pure Python implementation without external email service integration (drafts only, no auto-send capability)
- **Template system**: Built-in template engine for professional email formatting

## Future Integration Points
The architecture is designed to accommodate:
- OCR libraries for scanned document processing
- PDF processing libraries (PyPDF2, pdfplumber)
- Word document libraries (python-docx)
- External email service providers (SMTP, API-based services)
- Database systems (PostgreSQL, MySQL) for enterprise deployments