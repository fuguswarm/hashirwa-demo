# HashiRWA - RWA Tokenization Demo

## Overview

HashiRWA is a Real World Asset (RWA) tokenization demonstration platform focused on Japanese agricultural products. The application simulates blockchain integration for tokenizing agricultural assets like rice, green tea, apples, and strawberries. It provides a complete workflow from producer onboarding through administrative review to public marketplace listing, with simulated blockchain proof generation using cryptographic hashes and testnet transaction IDs.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
- **Single-file Flask application** (`main.py`) for simplicity and easy deployment on Replit
- **JSON file-based persistence** (`db.json`) for lightweight data storage without external database dependencies
- **Template rendering** using `render_template_string` to keep everything self-contained

### Core Workflow Architecture
The system implements a three-stage pipeline:
1. **Onboarding** - Producers submit agricultural product information
2. **Administrative Review** - Admin approval/rejection of submissions with queue management
3. **Public Marketplace** - Approved items displayed in a searchable public listing

### Data Model Design
- **Metadata Structure**: Standardized JSON format following "hashirwa-demo" standard with RWA version tracking
- **Proof Generation**: SHA-256 hash of sorted metadata JSON for integrity verification
- **Blockchain Simulation**: Testnet transaction IDs generated from hash prefixes to simulate on-chain integration
- **Status Management**: Three-state system (pending, approved, rejected) with timestamp tracking

### Authentication & Authorization
- **Admin Access Control**: Simple key-based authentication using query parameters
- **Environment Configuration**: Admin key configurable via environment variables with fallback defaults
- **Public Access**: No authentication required for marketplace and listing views

### User Interface Architecture
- **Responsive Design**: Dark theme CSS with modern card-based layouts
- **Bilingual Support**: English primary with Japanese descriptive elements
- **Form Validation**: HTML5 client-side validation with server-side sanitization
- **Navigation Flow**: Clear user journey from landing page through onboarding to marketplace

### API Design
- **RESTful Routes**: Standard HTTP methods for CRUD operations
- **JSON Metadata Endpoint**: Machine-readable metadata accessible via `/metadata/<id>.json`
- **Status Management**: Dedicated admin endpoints for approval/rejection workflow

## External Dependencies

### Core Framework
- **Flask**: Python web framework for HTTP handling, routing, and template rendering
- **Python Standard Library**: JSON manipulation, datetime handling, hashlib for cryptographic functions, os for environment variables

### Deployment Platform
- **Replit Integration**: Configured for zero-setup deployment with environment variable support
- **Port Configuration**: Flexible port binding via PORT environment variable (default 8080)
- **Host Binding**: Configured for 0.0.0.0 to enable external access on Replit

### Data Persistence
- **File System Storage**: JSON file persistence with automatic creation and error handling
- **No External Database**: Eliminates need for database setup or connection management

### Regional Data
- **Japanese Prefecture System**: Hardcoded support for Japanese administrative divisions
- **Agricultural Product Categories**: Predefined categories specific to Japanese agriculture (Rice, Green Tea, Apple, Strawberry, etc.)
- **Certification Standards**: Support for Japanese agricultural certifications (JA, JGAP, JAS Organic)

### Blockchain Simulation
- **Hash Generation**: SHA-256 for creating tamper-evident proofs
- **Testnet Integration**: Simulated blockchain transaction IDs for demonstration purposes
- **No External Blockchain**: Self-contained simulation without requiring actual blockchain connectivity