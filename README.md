# HashiRWA: Japan Agri-RWA Gateway with AI

**A prototype bridging Japanese agriculture to Web3**

## Overview

HashiRWA is a working prototype demonstrating how Japanese agricultural producers can onboard their products as real-world assets (RWA). The demo simulates the flow from producer onboarding → admin review → public marketplace → cryptographic proof of listing.

## Key Features

🌱 **Onboarding** — Producers register with product, certification, harvest date, lot size.

✅ **Admin Review** — Submissions can be approved or rejected for compliance.

🛒 **Marketplace** — Approved products are listed publicly with details.

🔗 **Proof of Listing** — Each listing generates a SHA-256 hash + downloadable JSON metadata (simulated "on-chain").

## Tech Stack

- **Python + Flask** (backend)
- **JSON** for data persistence (local simulation)
- **Minimal CSS** dark theme UI
- **Cryptographic hashing** for proof generation
- **Simulated blockchain** integration via testnet transaction IDs

## Quick Start

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Access the platform:**
   - Open browser to the provided URL (default: http://localhost:8080)
   - Use admin key 'hashirwa' or set ADMIN_KEY env var
   - Port defaults to 8080 or use PORT env var

3. **Platform workflow:**
   - Visit homepage to understand the process
   - Use "Start Onboarding" to register agricultural products
   - Access admin panel with `?k=hashirwa` to review submissions
   - Browse approved products in the marketplace
   - View individual listings with cryptographic proof

## Platform Pages

- **/** - Landing page with platform explanation and tanuki mascot
- **/onboard** - Producer registration form with Japanese prefectures
- **/admin** - Administrative review panel (requires admin key)
- **/market** - Public marketplace of approved products
- **/listing/<id>** - Individual product details with proof
- **/metadata/<id>.json** - Machine-readable JSON metadata

## Features

### Producer Onboarding
- Comprehensive form with Japanese prefecture selection
- Product categories: Rice, Green Tea, Apple, Strawberry, Vegetable, Fruit, Other
- Certification support: JA, JGAP, JAS Organic, Other
- Contact information and blockchain wallet integration

### Administrative Review
- Queue management for pending submissions
- Approval/rejection workflow with timestamps
- Status tracking and audit trail

### Marketplace
- Public listing of verified agricultural products
- Search and browse functionality
- Cryptographic proof display
- Responsive design with dark theme

### Blockchain Simulation
- SHA-256 hash generation for tamper-evident proofs
- Simulated testnet transaction IDs
- Downloadable JSON metadata for each asset
- RWA standard compliance with version tracking

## Sample Data

The platform comes pre-seeded with three verified agricultural products:
- **Shizuoka Green Tea Co.** - JAS Organic certified green tea
- **Aomori Apple Farmers Union** - JGAP certified apples
- **Hokkaidō Rice Collective** - JA certified premium rice

## Access

**GitHub Repo** (code + documentation): https://github.com/fuguswarm/hashirwa-demo

## Disclaimer

This is a proof-of-concept demo. "On-chain" functionality is simulated via cryptographic hashing. A full blockchain deployment will be implemented in later phases.

---

*Demo document prepared for proposal review • © 2025 HashiRWA*