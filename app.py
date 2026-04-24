import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Solana Exam Solver — Precision Transfer",
    page_icon="◎",
    layout="centered",
)

# Hide Streamlit default chrome for a cleaner look
st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<script src="https://unpkg.com/@solana/web3.js@1.98.0/lib/index.iife.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
  :root {
    --bg:#0a0d0f; --surface:#111518; --surface2:#181d21;
    --border:rgba(255,255,255,0.07); --border-bright:rgba(20,241,149,0.3);
    --green:#14f195; --green-dim:rgba(20,241,149,0.12); --green-glow:rgba(20,241,149,0.06);
    --purple:#9945ff; --text:#e8edf2; --text-muted:#6b7a8a; --text-dim:#3d4d5c;
    --mono:'Space Mono',monospace; --sans:'DM Sans',sans-serif;
    --radius:12px; --radius-sm:8px;
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{font-family:var(--sans);background:var(--bg);color:var(--text);padding:28px 20px 60px;overflow-x:hidden}
  body::before{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(20,241,149,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(20,241,149,.03) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;z-index:0}
  body::after{content:'';position:fixed;top:-200px;right:-200px;width:600px;height:600px;background:radial-gradient(circle,rgba(153,69,255,.08) 0%,transparent 70%);pointer-events:none;z-index:0}
  .wrap{position:relative;z-index:1;max-width:700px;margin:0 auto}

  /* HEADER */
  .network-badge{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:11px;color:var(--green);background:var(--green-dim);border:1px solid rgba(20,241,149,.2);border-radius:100px;padding:5px 14px;margin-bottom:20px;letter-spacing:.08em}
  .dot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:pulse 2s ease-in-out infinite}
  @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(.85)}}
  h1{font-family:var(--mono);font-size:clamp(22px,4vw,34px);font-weight:700;color:var(--text);line-height:1.2;margin-bottom:10px;letter-spacing:-.02em}
  h1 span{color:var(--green)}
  .subtitle{font-size:14px;color:var(--text-muted);line-height:1.6;margin-bottom:32px}

  /* CARD */
  .card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:22px;margin-bottom:12px;animation:fadeUp .5s ease both}
  .card:nth-child(2){animation-delay:.08s}.card:nth-child(3){animation-delay:.16s}.card:nth-child(4){animation-delay:.24s}.card:nth-child(5){animation-delay:.32s}
  @keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
  .card-title{font-family:var(--mono);font-size:11px;letter-spacing:.12em;color:var(--text-muted);text-transform:uppercase;margin-bottom:16px;display:flex;align-items:center;gap:10px}
  .card-title::after{content:'';flex:1;height:1px;background:var(--border)}

  /* TX GRID */
  .tx-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}
  @media(max-width:500px){.tx-grid{grid-template-columns:1fr}}
  .tx-item{background:var(--surface2);border:1px solid var(--border);border-radius:var(--radius-sm);padding:12px 14px}
  .tx-item.full{grid-column:1/-1}
  .tx-label{font-size:11px;color:var(--text-dim);font-family:var(--mono);letter-spacing:.08em;text-transform:uppercase;margin-bottom:5px}
  .tx-value{font-family:var(--mono);font-size:13px;color:var(--text);word-break:break-all;line-height:1.5}
  .tx-value.highlight{color:var(--green);font-size:20px;font-weight:700;letter-spacing:-.02em}
  .tx-value.memo-code{color:var(--purple);font-size:20px;font-weight:700;letter-spacing:.1em}

  /* FIELDS */
  .field-group{margin-bottom:13px}
  .field-label{font-size:12px;color:var(--text-muted);font-family:var(--mono);letter-spacing:.06em;text-transform:uppercase;margin-bottom:7px;display:block}
  input[type="text"]{width:100%;background:var(--surface2);border:1px solid var(--border);border-radius:var(--radius-sm);padding:10px 13px;font-family:var(--mono);font-size:13px;color:var(--text);outline:none;transition:border-color .2s}
  input[type="text"]:focus{border-color:rgba(20,241,149,.4);box-shadow:0 0 0 3px rgba(20,241,149,.06)}
  .input-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:13px}
  @media(max-width:500px){.input-row{grid-template-columns:1fr}}

  /* BUTTON */
  .btn-connect{width:100%;padding:14px;background:var(--green);color:#0a0d0f;border:none;border-radius:var(--radius-sm);font-family:var(--mono);font-size:14px;font-weight:700;letter-spacing:.06em;cursor:pointer;transition:all .2s;display:flex;align-items:center;justify-content:center;gap:10px}
  .btn-connect:hover:not(:disabled){background:#0dcc7a;transform:translateY(-1px);box-shadow:0 8px 24px rgba(20,241,149,.25)}
  .btn-connect:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}
  .spinner{width:16px;height:16px;border:2px solid rgba(0,0,0,.2);border-top-color:#0a0d0f;border-radius:50%;animation:spin .7s linear infinite}
  @keyframes spin{to{transform:rotate(360deg)}}

  /* STATUS */
  .status-box{margin-top:13px;padding:12px 14px;border-radius:var(--radius-sm);font-size:13px;line-height:1.6;display:none}
  .status-box.info   {display:block;background:rgba(20,100,255,.08);border:1px solid rgba(20,100,255,.2);color:#7aadff}
  .status-box.success{display:block;background:var(--green-dim);border:1px solid rgba(20,241,149,.25);color:var(--green)}
  .status-box.error  {display:block;background:rgba(255,60,60,.08);border:1px solid rgba(255,60,60,.2);color:#ff7a7a}

  /* RESULT */
  .result-card{background:var(--surface);border:1px solid rgba(20,241,149,.25);border-radius:var(--radius);padding:22px;margin-bottom:12px;display:none;animation:fadeUp .5s ease both;position:relative;overflow:hidden}
  .result-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--green),var(--purple))}
  .result-card.visible{display:block}
  .check{width:42px;height:42px;border-radius:50%;background:var(--green-dim);display:flex;align-items:center;justify-content:center;font-size:18px;margin:0 0 12px;animation:popIn .4s cubic-bezier(.175,.885,.32,1.275) both}
  @keyframes popIn{from{transform:scale(0);opacity:0}to{transform:scale(1);opacity:1}}
  .success-title{font-family:var(--mono);font-size:17px;font-weight:700;color:var(--green);margin-bottom:4px}
  .success-subtitle{font-size:13px;color:var(--text-muted);margin-bottom:13px}
  .txid-box{background:var(--surface2);border:1px solid var(--border);border-radius:var(--radius-sm);padding:13px;margin:13px 0;position:relative}
  .txid-text{font-family:var(--mono);font-size:11px;color:var(--text);word-break:break-all;line-height:1.7;padding-right:55px}
  .copy-btn{position:absolute;top:10px;right:10px;background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:5px 10px;font-family:var(--mono);font-size:11px;color:var(--text-muted);cursor:pointer;transition:all .2s}
  .copy-btn:hover{border-color:var(--green);color:var(--green)}
  .copy-btn.copied{background:var(--green-dim);border-color:var(--green);color:var(--green)}
  .btn-explorer{display:inline-flex;align-items:center;gap:8px;background:transparent;border:1px solid var(--border);border-radius:var(--radius-sm);padding:9px 16px;font-family:var(--mono);font-size:12px;color:var(--text-muted);cursor:pointer;transition:all .2s;text-decoration:none}
  .btn-explorer:hover{border-color:var(--green);color:var(--green);background:var(--green-glow)}

  /* STEPS */
  .step{display:flex;gap:13px;padding:12px 0;border-bottom:1px solid var(--border)}
  .step:last-child{border-bottom:none}
  .step-num{width:26px;height:26px;border-radius:50%;background:var(--green-dim);border:1px solid rgba(20,241,149,.2);display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:12px;color:var(--green);flex-shrink:0;margin-top:1px}
  .step-title{font-size:14px;font-weight:500;color:var(--text);margin-bottom:3px}
  .step-desc{font-size:13px;color:var(--text-muted);line-height:1.6}
  .step-desc code{font-family:var(--mono);font-size:11px;background:var(--surface2);border:1px solid var(--border);border-radius:4px;padding:1px 5px;color:var(--green)}
  .step-desc a{color:var(--green);text-decoration:none}

  /* FAUCETS */
  .faucet-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  @media(max-width:480px){.faucet-grid{grid-template-columns:1fr}}
  .faucet-link{display:flex;flex-direction:column;background:var(--surface2);border:1px solid var(--border);border-radius:var(--radius-sm);padding:13px 14px;text-decoration:none;transition:all .2s;gap:4px}
  .faucet-link:hover{border-color:var(--green);background:var(--green-glow)}
  .faucet-name{font-size:13px;font-weight:500;color:var(--text)}
  .faucet-url{font-family:var(--mono);font-size:10px;color:var(--text-dim)}

  /* WARN */
  .warn-banner{background:rgba(255,180,0,.06);border:1px solid rgba(255,180,0,.18);border-radius:var(--radius-sm);padding:11px 14px;font-size:13px;color:#c8a030;margin-bottom:16px;display:flex;gap:10px;align-items:flex-start;line-height:1.5}

  /* WALLET STRIP */
  .wallet-strip{display:none;align-items:center;gap:10px;background:var(--surface2);border:1px solid rgba(20,241,149,.15);border-radius:var(--radius-sm);padding:9px 13px;margin-bottom:13px;font-family:var(--mono);font-size:12px;color:var(--green)}
  .wallet-strip.visible{display:flex}
  .wallet-strip .addr{color:var(--text-muted);margin-left:4px}

  .footer{text-align:center;padding-top:32px;font-size:11px;font-family:var(--mono);color:var(--text-dim);letter-spacing:.06em}
  .footer span{color:var(--green)}
</style>
</head>
<body>
<div class="wrap">

  <div class="network-badge"><div class="dot"></div>SOLANA DEVNET</div>
  <h1>Precision <span>Transfer</span><br>Exam Solver</h1>
  <p class="subtitle">Blockchains in Practice (3 marks) — sends the exact SOL + memo dual-instruction transaction required by your exam portal.</p>

  <!-- MISSION PARAMETERS -->
  <div class="card">
    <div class="card-title">Mission Parameters</div>
    <div class="tx-grid">
      <div class="tx-item">
        <div class="tx-label">Exact Amount</div>
        <div class="tx-value highlight">0.016904 <small style="font-size:12px;color:var(--text-muted)">SOL</small></div>
      </div>
      <div class="tx-item">
        <div class="tx-label">Verification Memo</div>
        <div class="tx-value memo-code" id="memoDisplay">5641-F7FF</div>
      </div>
      <div class="tx-item full">
        <div class="tx-label">Destination Vault</div>
        <div class="tx-value" style="font-size:12px">BCJCAvSV89tnGqhFSG2uD8azeQLQ5Hypn9CQyWEN7VEH</div>
      </div>
      <div class="tx-item full">
        <div class="tx-label">Memo Program v2</div>
        <div class="tx-value" style="font-size:11px;color:var(--text-muted)">MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr</div>
      </div>
    </div>
  </div>

  <!-- SEND TRANSACTION -->
  <div class="card">
    <div class="card-title">Send Transaction</div>
    <div class="warn-banner">
      <span>⚠</span>
      <div>Phantom must be on <strong>Solana Devnet</strong>: Settings → Developer Settings → Enable Testnet Mode → Solana Devnet. You need ~0.02 SOL balance.</div>
    </div>
    <div class="wallet-strip" id="walletStrip">
      <div class="dot" style="width:6px;height:6px"></div>
      Connected <span class="addr" id="walletAddr"></span>
    </div>
    <div class="field-group">
      <label class="field-label">Your Memo Code</label>
      <input type="text" id="memoInput" value="5641-F7FF" placeholder="e.g. 5641-F7FF"
             oninput="document.getElementById('memoDisplay').textContent=this.value" />
    </div>
    <div class="input-row">
      <div>
        <label class="field-label">SOL Amount</label>
        <input type="text" id="amtInput" value="0.016904" />
      </div>
      <div>
        <label class="field-label">Vault Address</label>
        <input type="text" id="vaultInput" value="BCJCAvSV89tnGqhFSG2uD8azeQLQ5Hypn9CQyWEN7VEH" style="font-size:10px" />
      </div>
    </div>
    <button class="btn-connect" id="sendBtn" onclick="connectAndSend()">
      <span id="btnIcon">◎</span>
      <span id="btnLabel">Connect Phantom &amp; Send Transaction</span>
    </button>
    <div class="status-box" id="statusBox"></div>
  </div>

  <!-- RESULT -->
  <div class="result-card" id="resultCard">
    <div class="check">✓</div>
    <div class="success-title">Transaction Confirmed!</div>
    <div class="success-subtitle">Copy your TxID and paste it into the exam portal's "Transaction Signature" field.</div>
    <div class="card-title" style="margin-top:8px">Transaction Signature (TxID)</div>
    <div class="txid-box">
      <div class="txid-text" id="txidText"></div>
      <button class="copy-btn" id="copyBtn" onclick="copyTxid()">Copy</button>
    </div>
    <a class="btn-explorer" href="#" onclick="openExplorer(event)">◎ View on Solana Explorer</a>
  </div>

  <!-- HOW IT WORKS -->
  <div class="card">
    <div class="card-title">How it Works</div>
    <div class="step">
      <div class="step-num">1</div>
      <div>
        <div class="step-title">Install & configure Phantom</div>
        <div class="step-desc">Install <a href="https://phantom.app" target="_blank">phantom.app</a>. Switch to Devnet: Settings → Developer Settings → Enable Testnet Mode → Solana Devnet.</div>
      </div>
    </div>
    <div class="step">
      <div class="step-num">2</div>
      <div>
        <div class="step-title">Get free Devnet SOL</div>
        <div class="step-desc">Use a faucet below. You need at least 0.02 SOL to cover the transfer + network fees.</div>
      </div>
    </div>
    <div class="step">
      <div class="step-num">3</div>
      <div>
        <div class="step-title">Click Connect & Send</div>
        <div class="step-desc">Builds a dual-instruction atomic transaction: <code>SystemProgram.transfer</code> (exact SOL) + <code>Memo Program v2</code> (your exam code).</div>
      </div>
    </div>
    <div class="step">
      <div class="step-num">4</div>
      <div>
        <div class="step-title">Approve & copy TxID</div>
        <div class="step-desc">Approve in Phantom. The signature appears here instantly — paste it into your exam portal.</div>
      </div>
    </div>
  </div>

  <!-- FAUCETS -->
  <div class="card">
    <div class="card-title">Devnet Faucets — Get Free SOL</div>
    <div class="faucet-grid">
      <a class="faucet-link" href="https://faucet.solana.com" target="_blank">
        <span class="faucet-name">Official Solana Faucet</span>
        <span class="faucet-url">faucet.solana.com</span>
      </a>
      <a class="faucet-link" href="https://solfaucet.com" target="_blank">
        <span class="faucet-name">Sol Faucet</span>
        <span class="faucet-url">solfaucet.com</span>
      </a>
      <a class="faucet-link" href="https://dev.to/amirsol/how-to-get-solana-devnet-sol-3b8n" target="_blank">
        <span class="faucet-name">CLI Airdrop Guide</span>
        <span class="faucet-url">solana airdrop 2</span>
      </a>
      <a class="faucet-link" href="https://explorer.solana.com/?cluster=devnet" target="_blank">
        <span class="faucet-name">Solana Explorer</span>
        <span class="faucet-url">explorer.solana.com (devnet)</span>
      </a>
    </div>
  </div>

  <div class="footer">
    Built for <span>Blockchains in Practice</span> — Precision Transfer (3 marks)<br>
    Memo Program v2 · Dual-Instruction · Solana Devnet
  </div>
</div>

<script>
const MEMO_PROGRAM_ID = 'MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr';
const DEVNET_RPC      = 'https://api.devnet.solana.com';
const solWeb3         = window.solanaWeb3;
let lastSignature     = '';

function setStatus(msg, type) {
  const b = document.getElementById('statusBox');
  b.className = 'status-box ' + type;
  b.innerHTML = msg;
}
function clearStatus() {
  const b = document.getElementById('statusBox');
  b.className = 'status-box'; b.innerHTML = '';
}
function setBtnState(label, loading) {
  document.getElementById('sendBtn').disabled = loading;
  document.getElementById('btnLabel').textContent = label;
  const icon = document.getElementById('btnIcon');
  if (loading) {
    icon.outerHTML = '<div class="spinner" id="btnIcon"></div>';
  } else {
    const sp = document.getElementById('btnIcon');
    if (sp && sp.classList.contains('spinner'))
      sp.outerHTML = '<span id="btnIcon">◎</span>';
  }
}
function showWalletStrip(addr) {
  document.getElementById('walletAddr').textContent = addr.slice(0,6)+'...'+addr.slice(-4);
  document.getElementById('walletStrip').classList.add('visible');
}
function showResult(sig) {
  document.getElementById('txidText').textContent = sig;
  document.getElementById('resultCard').classList.add('visible');
  document.getElementById('resultCard').scrollIntoView({behavior:'smooth',block:'start'});
}

async function connectAndSend() {
  const memo  = document.getElementById('memoInput').value.trim();
  const amt   = document.getElementById('amtInput').value.trim();
  const vault = document.getElementById('vaultInput').value.trim();

  if (!memo)  { setStatus('Please enter your memo code.','error'); return; }
  const solAmt = parseFloat(amt);
  if (!solAmt || isNaN(solAmt) || solAmt <= 0) { setStatus('Invalid SOL amount.','error'); return; }
  if (!vault || vault.length < 32) { setStatus('Invalid vault address.','error'); return; }

  if (!window.solana || !window.solana.isPhantom) {
    setStatus('Phantom not detected. <a href="https://phantom.app" target="_blank" style="color:inherit;font-weight:500;text-decoration:underline">Install Phantom →</a> then refresh.','error');
    return;
  }

  clearStatus();
  setBtnState('Connecting to Phantom…', true);

  try {
    const resp   = await window.solana.connect();
    const payer  = resp.publicKey;
    showWalletStrip(payer.toBase58());
    setStatus('Wallet connected. Building transaction…','info');
    setBtnState('Building transaction…', true);

    const connection     = new solWeb3.Connection(DEVNET_RPC, 'confirmed');
    const toKey          = new solWeb3.PublicKey(vault);
    const memoKey        = new solWeb3.PublicKey(MEMO_PROGRAM_ID);
    const lamports       = Math.round(solAmt * 1_000_000_000);

    const transferIx = solWeb3.SystemProgram.transfer({
      fromPubkey: payer, toPubkey: toKey, lamports,
    });
    const memoIx = new solWeb3.TransactionInstruction({
      keys:      [{ pubkey: payer, isSigner: true, isWritable: false }],
      programId: memoKey,
      data:      Buffer.from(memo, 'utf8'),
    });

    const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash('confirmed');
    const tx = new solWeb3.Transaction({ recentBlockhash: blockhash, feePayer: payer });
    tx.add(transferIx, memoIx);

    setBtnState('Waiting for Phantom approval…', true);
    setStatus('⏳ Approve in Phantom — you will see 2 instructions: SOL transfer + Memo.','info');

    const signed = await window.solana.signTransaction(tx);
    setBtnState('Sending to Devnet…', true);
    setStatus('Sending to Solana Devnet…','info');

    const sig = await connection.sendRawTransaction(signed.serialize(), {
      skipPreflight: false, preflightCommitment: 'confirmed',
    });

    setBtnState('Confirming…', true);
    setStatus('Confirming on-chain… (~5–15 seconds)','info');

    const result = await connection.confirmTransaction(
      { signature: sig, blockhash, lastValidBlockHeight }, 'confirmed'
    );
    if (result.value.err) throw new Error('On-chain error: ' + JSON.stringify(result.value.err));

    lastSignature = sig;
    clearStatus();
    setBtnState('Transaction Confirmed ✓', false);
    showResult(sig);

  } catch(err) {
    console.error(err);
    setBtnState('Connect Phantom & Send Transaction', false);
    let msg = err.message || String(err);
    if (msg.toLowerCase().includes('user rejected')||msg.toLowerCase().includes('declined'))
      msg = 'Transaction cancelled in Phantom.';
    else if (msg.toLowerCase().includes('insufficient'))
      msg = 'Insufficient SOL. Use a Devnet faucet above, then retry.';
    else if (msg.toLowerCase().includes('blockhash'))
      msg = 'Blockhash expired. Please try again.';
    setStatus('Error: '+msg,'error');
  }
}

function copyTxid() {
  if (!lastSignature) return;
  navigator.clipboard.writeText(lastSignature).then(() => {
    const btn = document.getElementById('copyBtn');
    btn.textContent = 'Copied!'; btn.classList.add('copied');
    setTimeout(()=>{ btn.textContent='Copy'; btn.classList.remove('copied'); }, 2000);
  });
}
function openExplorer(e) {
  e.preventDefault();
  if (!lastSignature) return;
  window.open('https://explorer.solana.com/tx/'+lastSignature+'?cluster=devnet','_blank');
}
window.addEventListener('load', () => {
  if (window.solana && window.solana.isPhantom) {
    window.solana.connect({ onlyIfTrusted: true })
      .then(r => showWalletStrip(r.publicKey.toBase58()))
      .catch(()=>{});
  }
});
</script>
</body>
</html>
"""

components.html(HTML, height=1650, scrolling=True)
