HashiRWA Demo

HashiRWA is a prototype platform for onboarding Japanese agricultural products into blockchain as real-world assets (RWA).

This demo shows the basic flow: producer onboarding → admin review → public marketplace → proof hash (simulated on-chain).

Routes

/ — Landing page

/onboard — Producer onboarding form

/admin?k=hashirwa — Admin panel (review + approve)

/market — Public marketplace of approved listings

/listing/<id> — Detail page for a specific product

/metadata/<id>.json — JSON metadata with proof hash

How to Run
pip install flask
python main.py


Runs on http://localhost:8080 (Replit auto-runs if deployed there).

Notes

Data stored locally in db.json (not included in repo).

“On-chain” behavior is simulated via cryptographic hashing for proof-of-concept only.

Built with Python + Flask, minimal CSS for responsive dark-theme UI.
