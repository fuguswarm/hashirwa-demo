"""
HashiRWA - RWA Tokenization Demo for Japanese Agricultural Products

Quick run instructions for Replit:
1. Run: python main.py
2. Open browser to the provided URL
3. Use admin key 'hashirwa' or set ADMIN_KEY env var
4. Port defaults to 8080 or use PORT env var

This demo simulates blockchain integration with hash generation and testnet transaction IDs.
"""

import os
import json
import hashlib
from datetime import datetime
from flask import Flask, request, render_template_string, redirect, url_for, jsonify, abort

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "hashirwa-demo-secret")

# Configuration
ADMIN_KEY = os.environ.get("ADMIN_KEY", "hashirwa")
PORT = int(os.environ.get("PORT", 8080))
DB_FILE = "db.json"

# Template filter for datetime formatting
@app.template_filter('datetime')
def datetime_filter(value):
    """Format datetime for display"""
    if isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return value
    return value

def load_db():
    """Load database from JSON file"""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"items": []}

def save_db(db):
    """Save database to JSON file"""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def generate_id():
    """Generate unique ID based on timestamp"""
    return int(datetime.now().timestamp() * 1000000) % 1000000

def compute_proof_hash(metadata):
    """Compute SHA256 hash of metadata"""
    metadata_str = json.dumps(metadata, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(metadata_str.encode('utf-8')).hexdigest()

def create_metadata(form_data):
    """Create metadata structure from form data"""
    return {
        "rwa_version": 1,
        "standard": "hashirwa-demo",
        "issuer": form_data["producer_name"],
        "jurisdiction": {
            "country": "Japan",
            "prefecture": form_data["prefecture"]
        },
        "asset": {
            "category": "Agriculture",
            "product": form_data["product"],
            "certification": form_data["certification"],
            "lot_size": form_data["lot_size"],
            "harvest_date": form_data["harvest_date"]
        },
        "contacts": {
            "email": form_data.get("contact_email", ""),
            "wallet": form_data.get("wallet_address", "")
        },
        "notes": form_data.get("notes", "")
    }

def seed_data():
    """Seed initial data if database is empty"""
    db = load_db()
    if not db["items"]:
        now = datetime.now().isoformat()
        
        seed_items = [
            {
                "producer_name": "Shizuoka Green Tea Co.",
                "prefecture": "静岡県",
                "product": "Green Tea",
                "certification": "JAS Organic",
                "lot_size": "500kg",
                "harvest_date": "2024-05-15",
                "contact_email": "info@shizuoka-tea.jp",
                "wallet_address": "0x1234567890abcdef1234567890abcdef12345678",
                "notes": "Premium grade sencha from mountain slopes"
            },
            {
                "producer_name": "Aomori Apple Farmers Union",
                "prefecture": "青森県",
                "product": "Apple",
                "certification": "JGAP",
                "lot_size": "1000kg",
                "harvest_date": "2024-10-20",
                "contact_email": "contact@aomori-apples.jp",
                "wallet_address": "0xabcdef1234567890abcdef1234567890abcdef12",
                "notes": "Fuji apples from certified organic farms"
            },
            {
                "producer_name": "Hokkaidō Rice Collective",
                "prefecture": "北海道",
                "product": "Rice",
                "certification": "JA",
                "lot_size": "2000kg",
                "harvest_date": "2024-09-30",
                "contact_email": "hello@hokkaido-rice.jp",
                "wallet_address": "0x567890abcdef1234567890abcdef1234567890ab",
                "notes": "Premium short-grain rice variety"
            }
        ]
        
        for seed_item in seed_items:
            item_id = generate_id()
            metadata = create_metadata(seed_item)
            proof_hash = compute_proof_hash(metadata)
            sim_testnet_txid = f"testnet:{proof_hash[:16]}"
            
            item = {
                "id": item_id,
                "status": "approved",
                "metadata": metadata,
                "proof": {
                    "hash": proof_hash,
                    "sim_testnet_txid": sim_testnet_txid
                },
                "timestamps": {
                    "created_at": now,
                    "updated_at": now
                }
            }
            db["items"].append(item)
        
        save_db(db)

# Initialize database
seed_data()

# CSS Styles
CSS_STYLES = """
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f0f0f;
    color: #e0e0e0;
    line-height: 1.6;
    min-height: 100vh;
}
.container { max-width: 1200px; margin: 0 auto; padding: 20px; }
.header { text-align: center; margin-bottom: 40px; }
.header h1 { color: #4ade80; font-size: 2.5rem; margin-bottom: 10px; }
.header p { color: #a0a0a0; font-size: 1.1rem; }
.card { 
    background: #1a1a1a; 
    border-radius: 12px; 
    padding: 24px; 
    margin-bottom: 24px;
    border: 1px solid #333;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; }
.btn {
    display: inline-block;
    padding: 12px 24px;
    background: #4ade80;
    color: #000;
    text-decoration: none;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
    margin: 4px;
}
.btn:hover { background: #22c55e; transform: translateY(-1px); }
.btn-secondary { background: #374151; color: #e0e0e0; }
.btn-secondary:hover { background: #4b5563; }
.btn-danger { background: #ef4444; color: white; }
.btn-danger:hover { background: #dc2626; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-weight: 500; color: #d0d0d0; }
.form-control {
    width: 100%;
    padding: 12px;
    background: #2a2a2a;
    border: 1px solid #444;
    border-radius: 6px;
    color: #e0e0e0;
    font-size: 16px;
}
.form-control:focus { outline: none; border-color: #4ade80; }
.badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 500;
}
.badge-pending { background: #fbbf24; color: #000; }
.badge-approved { background: #10b981; color: #000; }
.badge-rejected { background: #ef4444; color: white; }
.text-sm { font-size: 0.9rem; color: #a0a0a0; }
.text-center { text-align: center; }
.mt-4 { margin-top: 24px; }
.mb-4 { margin-bottom: 24px; }
.navigation { margin-bottom: 32px; text-align: center; }
.navigation a { 
    color: #4ade80; 
    text-decoration: none; 
    margin: 0 15px; 
    font-weight: 500;
}
.navigation a:hover { color: #22c55e; }
.proof-section {
    background: #111;
    border-radius: 8px;
    padding: 16px;
    margin-top: 16px;
}
.hash-display {
    font-family: 'Courier New', monospace;
    background: #000;
    padding: 8px 12px;
    border-radius: 4px;
    word-break: break-all;
    font-size: 0.9rem;
    border-left: 4px solid #4ade80;
}
.admin-actions { margin-top: 16px; }
.admin-actions form { display: inline; }
.jp-text { color: #888; font-style: italic; margin-top: 8px; }
@media (max-width: 768px) {
    .container { padding: 12px; }
    .header h1 { font-size: 2rem; }
    .grid { grid-template-columns: 1fr; }
}
</style>
"""

# Routes

@app.route('/')
def landing():
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HashiRWA - Real World Asset Tokenization</title>
        {CSS_STYLES}
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>HashiRWA</h1>
                <p>Real World Asset Tokenization for Japanese Agricultural Products</p>
                <div class="jp-text">日本の農産物のためのリアルワールドアセット・トークン化プラットフォーム</div>
            </div>
            
            <div class="card">
                <h2>How It Works</h2>
                <div class="grid">
                    <div>
                        <h3>🌱 1. Onboard</h3>
                        <p>Agricultural producers register their products with detailed information including certification, harvest dates, and lot sizes.</p>
                    </div>
                    <div>
                        <h3>✅ 2. Review</h3>
                        <p>Our verification team reviews submissions to ensure authenticity and compliance with Japanese agricultural standards.</p>
                    </div>
                    <div>
                        <h3>🔗 3. Publish</h3>
                        <p>Approved assets are tokenized with cryptographic proof and published to our simulated blockchain network.</p>
                    </div>
                </div>
                
                <div class="text-center mt-4">
                    <a href="/onboard" class="btn">Start Onboarding</a>
                    <a href="/market" class="btn btn-secondary">View Marketplace</a>
                </div>
                
                <div class="jp-text text-center">
                    オンチェーンの統合はハッシュによりシミュレートされています
                    <br>On-chain integration is simulated via cryptographic hashing
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(template)

@app.route('/onboard', methods=['GET', 'POST'])
def onboard():
    if request.method == 'POST':
        # Process form submission
        form_data = {
            "producer_name": request.form.get("producer_name", "").strip(),
            "prefecture": request.form.get("prefecture", "").strip(),
            "product": request.form.get("product", "").strip(),
            "certification": request.form.get("certification", "").strip(),
            "lot_size": request.form.get("lot_size", "").strip(),
            "harvest_date": request.form.get("harvest_date", "").strip(),
            "contact_email": request.form.get("contact_email", "").strip(),
            "wallet_address": request.form.get("wallet_address", "").strip(),
            "notes": request.form.get("notes", "").strip()
        }
        
        # Create item
        item_id = generate_id()
        metadata = create_metadata(form_data)
        proof_hash = compute_proof_hash(metadata)
        sim_testnet_txid = f"testnet:{proof_hash[:16]}"
        now = datetime.now().isoformat()
        
        item = {
            "id": item_id,
            "status": "pending",
            "metadata": metadata,
            "proof": {
                "hash": proof_hash,
                "sim_testnet_txid": sim_testnet_txid
            },
            "timestamps": {
                "created_at": now,
                "updated_at": now
            }
        }
        
        # Save to database
        db = load_db()
        db["items"].append(item)
        save_db(db)
        
        # Show confirmation
        template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Submission Confirmed - HashiRWA</title>
            {CSS_STYLES}
        </head>
        <body>
            <div class="container">
                <div class="navigation">
                    <a href="/">Home</a>
                    <a href="/market">Marketplace</a>
                </div>
                
                <div class="card">
                    <h1>✅ Submission Confirmed</h1>
                    <p>Your agricultural product has been successfully submitted for review.</p>
                    
                    <div class="proof-section">
                        <h3>Submission Details</h3>
                        <p><strong>ID:</strong> {item_id}</p>
                        <p><strong>Status:</strong> <span class="badge badge-pending">Pending Review</span></p>
                        
                        <h4>Cryptographic Proof</h4>
                        <div class="hash-display">{proof_hash}</div>
                        <p class="text-sm mt-4"><strong>Simulated Testnet TX:</strong> {sim_testnet_txid}</p>
                    </div>
                    
                    <div class="text-center mt-4">
                        <a href="/listing/{item_id}" class="btn">View Listing</a>
                        <a href="/metadata/{item_id}.json" class="btn btn-secondary">Download JSON</a>
                        <a href="/onboard" class="btn btn-secondary">Submit Another</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(template)
    
    # Show form
    prefectures = [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
        "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
        "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
        "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
        "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
        "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
        "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
    ]
    
    products = ["Rice", "Green Tea", "Apple", "Strawberry", "Vegetable", "Fruit", "Other"]
    certifications = ["JA", "JGAP", "JAS Organic", "Other"]
    
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Producer Onboarding - HashiRWA</title>
        {CSS_STYLES}
    </head>
    <body>
        <div class="container">
            <div class="navigation">
                <a href="/">Home</a>
                <a href="/market">Marketplace</a>
            </div>
            
            <div class="card">
                <h1>Producer Onboarding</h1>
                <p>Register your agricultural products for tokenization</p>
                
                <form method="POST">
                    <div class="form-group">
                        <label for="producer_name">Producer Name *</label>
                        <input type="text" id="producer_name" name="producer_name" class="form-control" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="prefecture">Prefecture *</label>
                        <select id="prefecture" name="prefecture" class="form-control" required>
                            <option value="">Select Prefecture</option>
                            {''.join(f'<option value="{p}">{p}</option>' for p in prefectures)}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="product">Product *</label>
                        <select id="product" name="product" class="form-control" required>
                            <option value="">Select Product</option>
                            {''.join(f'<option value="{p}">{p}</option>' for p in products)}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="certification">Certification</label>
                        <select id="certification" name="certification" class="form-control">
                            <option value="">Select Certification</option>
                            {''.join(f'<option value="{c}">{c}</option>' for c in certifications)}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="lot_size">Lot Size *</label>
                        <input type="text" id="lot_size" name="lot_size" class="form-control" 
                               placeholder="e.g., 1000kg, 500 units" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="harvest_date">Harvest Date *</label>
                        <input type="date" id="harvest_date" name="harvest_date" class="form-control" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="contact_email">Contact Email</label>
                        <input type="email" id="contact_email" name="contact_email" class="form-control">
                    </div>
                    
                    <div class="form-group">
                        <label for="wallet_address">Wallet Address</label>
                        <input type="text" id="wallet_address" name="wallet_address" class="form-control" 
                               placeholder="0x...">
                    </div>
                    
                    <div class="form-group">
                        <label for="notes">Notes</label>
                        <textarea id="notes" name="notes" class="form-control" rows="3" 
                                placeholder="Additional information about your product"></textarea>
                    </div>
                    
                    <button type="submit" class="btn">Submit for Review</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(template)

@app.route('/admin')
def admin():
    admin_key = request.args.get('k', '')
    
    if admin_key != ADMIN_KEY:
        template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin Access - HashiRWA</title>
            {CSS_STYLES}
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <h1>Admin Access Required</h1>
                    <p>Please enter the admin key to access this page.</p>
                    <p class="text-sm">Hint: Default key is "hashirwa" or check ADMIN_KEY environment variable.</p>
                    
                    <form method="GET">
                        <div class="form-group">
                            <label for="k">Admin Key</label>
                            <input type="password" id="k" name="k" class="form-control" value="{admin_key}">
                        </div>
                        <button type="submit" class="btn">Access Admin Panel</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(template)
    
    db = load_db()
    pending_items = [item for item in db["items"] if item["status"] == "pending"]
    approved_items = [item for item in db["items"] if item["status"] == "approved"]
    
    # Sort as specified
    pending_items.sort(key=lambda x: x["timestamps"]["created_at"])
    approved_items.sort(key=lambda x: x["timestamps"]["updated_at"], reverse=True)
    
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Panel - HashiRWA</title>
        {CSS_STYLES}
    </head>
    <body>
        <div class="container">
            <div class="navigation">
                <a href="/">Home</a>
                <a href="/market">Marketplace</a>
            </div>
            
            <div class="header">
                <h1>Admin Panel</h1>
                <p>Manage pending submissions and approved listings</p>
            </div>
            
            <div class="card">
                <h2>Pending Review Queue ({len(pending_items)})</h2>
                {'<p class="text-sm">No pending submissions.</p>' if not pending_items else ''}
                
                {''.join(f'''
                <div class="card" style="background: #1e1e1e;">
                    <h3>{item["metadata"]["issuer"]}</h3>
                    <p><strong>Product:</strong> {item["metadata"]["asset"]["product"]} ({item["metadata"]["asset"]["lot_size"]})</p>
                    <p><strong>Prefecture:</strong> {item["metadata"]["jurisdiction"]["prefecture"]}</p>
                    <p><strong>Certification:</strong> {item["metadata"]["asset"]["certification"]}</p>
                    <p><strong>Submitted:</strong> {datetime_filter(item["timestamps"]["created_at"])}</p>
                    
                    <div class="admin-actions">
                        <form method="POST" action="/admin/approve/{item["id"]}?k={admin_key}">
                            <button type="submit" class="btn">Approve</button>
                        </form>
                        <form method="POST" action="/admin/reject/{item["id"]}?k={admin_key}">
                            <button type="submit" class="btn btn-danger">Reject</button>
                        </form>
                        <a href="/listing/{item["id"]}" class="btn btn-secondary">View Details</a>
                    </div>
                </div>
                ''' for item in pending_items)}
            </div>
            
            <div class="card">
                <h2>Approved Assets ({len(approved_items)})</h2>
                {'<p class="text-sm">No approved assets yet.</p>' if not approved_items else ''}
                
                {''.join(f'''
                <div class="card" style="background: #1e1e1e;">
                    <h3>{item["metadata"]["issuer"]}</h3>
                    <p><strong>Product:</strong> {item["metadata"]["asset"]["product"]} ({item["metadata"]["asset"]["lot_size"]})</p>
                    <p><strong>Prefecture:</strong> {item["metadata"]["jurisdiction"]["prefecture"]}</p>
                    <p><strong>Approved:</strong> {datetime_filter(item["timestamps"]["updated_at"])}</p>
                    <span class="badge badge-approved">Approved</span>
                    <a href="/listing/{item["id"]}" class="btn btn-secondary" style="margin-left: 12px;">View Listing</a>
                </div>
                ''' for item in approved_items)}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(template)

@app.route('/admin/approve/<int:item_id>', methods=['POST'])
def admin_approve(item_id):
    admin_key = request.args.get('k', '')
    if admin_key != ADMIN_KEY:
        abort(403)
    
    db = load_db()
    item = next((item for item in db["items"] if item["id"] == item_id), None)
    if item:
        item["status"] = "approved"
        item["timestamps"]["updated_at"] = datetime.now().isoformat()
        save_db(db)
    
    return redirect(url_for('admin', k=admin_key))

@app.route('/admin/reject/<int:item_id>', methods=['POST'])
def admin_reject(item_id):
    admin_key = request.args.get('k', '')
    if admin_key != ADMIN_KEY:
        abort(403)
    
    db = load_db()
    item = next((item for item in db["items"] if item["id"] == item_id), None)
    if item:
        item["status"] = "rejected"
        item["timestamps"]["updated_at"] = datetime.now().isoformat()
        save_db(db)
    
    return redirect(url_for('admin', k=admin_key))

@app.route('/market')
def market():
    db = load_db()
    approved_items = [item for item in db["items"] if item["status"] == "approved"]
    approved_items.sort(key=lambda x: x["timestamps"]["updated_at"], reverse=True)
    
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Marketplace - HashiRWA</title>
        {CSS_STYLES}
    </head>
    <body>
        <div class="container">
            <div class="navigation">
                <a href="/">Home</a>
                <a href="/onboard">Onboard Product</a>
            </div>
            
            <div class="header">
                <h1>Agricultural Asset Marketplace</h1>
                <p>Verified and tokenized Japanese agricultural products</p>
            </div>
            
            {'<div class="card"><p class="text-center">No approved assets available yet. <a href="/onboard">Be the first to onboard!</a></p></div>' if not approved_items else ''}
            
            <div class="grid">
                {''.join(f'''
                <div class="card">
                    <h3>{item["metadata"]["issuer"]}</h3>
                    <span class="badge badge-approved">Verified</span>
                    
                    <p><strong>Product:</strong> {item["metadata"]["asset"]["product"]}</p>
                    <p><strong>Prefecture:</strong> {item["metadata"]["jurisdiction"]["prefecture"]}</p>
                    <p><strong>Certification:</strong> {item["metadata"]["asset"]["certification"]}</p>
                    <p><strong>Lot Size:</strong> {item["metadata"]["asset"]["lot_size"]}</p>
                    <p><strong>Harvest:</strong> {item["metadata"]["asset"]["harvest_date"]}</p>
                    
                    <div class="text-sm">
                        Tokenized: {datetime_filter(item["timestamps"]["updated_at"])}
                    </div>
                    
                    <div class="mt-4">
                        <a href="/listing/{item["id"]}" class="btn">View Details</a>
                    </div>
                </div>
                ''' for item in approved_items)}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(template)

@app.route('/listing/<int:item_id>')
def listing(item_id):
    db = load_db()
    item = next((item for item in db["items"] if item["id"] == item_id), None)
    
    if not item:
        abort(404)
    
    status_badge = {
        "pending": "badge-pending",
        "approved": "badge-approved", 
        "rejected": "badge-rejected"
    }.get(item["status"], "badge-pending")
    
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{item["metadata"]["issuer"]} - HashiRWA</title>
        {CSS_STYLES}
    </head>
    <body>
        <div class="container">
            <div class="navigation">
                <a href="/">Home</a>
                <a href="/market">Marketplace</a>
                <a href="/onboard">Onboard Product</a>
            </div>
            
            <div class="card">
                <h1>{item["metadata"]["issuer"]}</h1>
                <span class="badge {status_badge}">{item["status"].title()}</span>
                
                <div class="grid" style="margin-top: 24px;">
                    <div>
                        <h3>Product Information</h3>
                        <p><strong>Product:</strong> {item["metadata"]["asset"]["product"]}</p>
                        <p><strong>Category:</strong> {item["metadata"]["asset"]["category"]}</p>
                        <p><strong>Certification:</strong> {item["metadata"]["asset"]["certification"]}</p>
                        <p><strong>Lot Size:</strong> {item["metadata"]["asset"]["lot_size"]}</p>
                        <p><strong>Harvest Date:</strong> {item["metadata"]["asset"]["harvest_date"]}</p>
                    </div>
                    
                    <div>
                        <h3>Producer Details</h3>
                        <p><strong>Producer:</strong> {item["metadata"]["issuer"]}</p>
                        <p><strong>Prefecture:</strong> {item["metadata"]["jurisdiction"]["prefecture"]}</p>
                        <p><strong>Country:</strong> {item["metadata"]["jurisdiction"]["country"]}</p>
                        {f'<p><strong>Email:</strong> {item["metadata"]["contacts"]["email"]}</p>' if item["metadata"]["contacts"]["email"] else ''}
                        {f'<p><strong>Wallet:</strong> {item["metadata"]["contacts"]["wallet"]}</p>' if item["metadata"]["contacts"]["wallet"] else ''}
                    </div>
                </div>
                
                {f'<div class="mt-4"><h3>Notes</h3><p>{item["metadata"]["notes"]}</p></div>' if item["metadata"]["notes"] else ''}
                
                <div class="proof-section">
                    <h3>🔒 Cryptographic Proof</h3>
                    <p>This asset has been cryptographically verified and registered on our simulated blockchain network.</p>
                    
                    <h4>Proof Hash (SHA256)</h4>
                    <div class="hash-display">{item["proof"]["hash"]}</div>
                    
                    <p class="text-sm mt-4">
                        <strong>Simulated Testnet Transaction:</strong> {item["proof"]["sim_testnet_txid"]}
                    </p>
                    
                    <div class="text-sm">
                        <p><strong>Created:</strong> {datetime_filter(item["timestamps"]["created_at"])}</p>
                        <p><strong>Last Updated:</strong> {datetime_filter(item["timestamps"]["updated_at"])}</p>
                        <p><strong>RWA Standard:</strong> {item["metadata"]["standard"]} v{item["metadata"]["rwa_version"]}</p>
                    </div>
                </div>
                
                <div class="text-center mt-4">
                    <a href="/metadata/{item_id}.json" class="btn">Download JSON Metadata</a>
                    {f'<a href="/market" class="btn btn-secondary">Back to Marketplace</a>' if item["status"] == "approved" else ''}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(template)

@app.route('/metadata/<int:item_id>.json')
def metadata_json(item_id):
    db = load_db()
    item = next((item for item in db["items"] if item["id"] == item_id), None)
    
    if not item:
        abort(404)
    
    return jsonify({
        "id": item["id"],
        "status": item["status"],
        "metadata": item["metadata"],
        "proof": item["proof"],
        "timestamps": item["timestamps"]
    })

@app.errorhandler(404)
def not_found(error):
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Not Found - HashiRWA</title>
        {CSS_STYLES}
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>404 - Not Found</h1>
                <p>The requested resource could not be found.</p>
                <div class="text-center mt-4">
                    <a href="/" class="btn">Return Home</a>
                    <a href="/market" class="btn btn-secondary">Browse Marketplace</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(template), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
