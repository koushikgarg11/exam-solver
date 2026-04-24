# ◎ Solana Exam Solver — Precision Transfer

A Streamlit app for the **Blockchains in Practice (3 marks)** exam question.
Sends the exact SOL + Memo dual-instruction transaction to the exam vault from your Phantom wallet.

---

## 🚀 Deploy to Streamlit Cloud

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/solana-exam-solver.git
git branch -M main
git push -u origin main
```

### Step 2 — Deploy
1. Go to share.streamlit.io
2. Click "Create app"
3. Set Main file path: app.py
4. Click Deploy ✅

No secrets or API keys needed — pure browser JS talking to Solana Devnet RPC.

---

## 💻 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Files
```
solana-exam-solver/
├── app.py              ← Streamlit app (embeds full HTML/JS)
├── requirements.txt    ← streamlit only
├── README.md
└── .streamlit/
    └── config.toml
```

## ⚠️ Prerequisites
- Phantom wallet installed (phantom.app)
- Phantom on Solana Devnet (Settings → Developer Settings → Testnet Mode)
- 0.02+ SOL on Devnet from faucet.solana.com
