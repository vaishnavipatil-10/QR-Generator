from flask import Flask, request, send_file, render_template_string
import qrcode
import io

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Forge</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg:       #080a0f;
            --surface:  #0e1118;
            --border:   #1e2433;
            --border-hi:#2e3a52;
            --accent:   #4af0c4;
            --accent2:  #3b7fff;
            --text:     #e8edf5;
            --muted:    #5a6580;
        }
        html, body { height: 100%; background: var(--bg); color: var(--text); font-family: 'Syne', sans-serif; overflow-x: hidden; }
        body::before {
            content: '';
            position: fixed; inset: 0;
            background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px);
            background-size: 48px 48px;
            opacity: .45; pointer-events: none; z-index: 0;
        }
        body::after {
            content: '';
            position: fixed; top: -20%; left: 50%; transform: translateX(-50%);
            width: 900px; height: 700px;
            background: radial-gradient(ellipse, rgba(74,240,196,.07) 0%, transparent 65%);
            pointer-events: none; z-index: 0;
        }
        .shell { position: relative; z-index: 1; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 20px; }
        .badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(74,240,196,.07); border: 1px solid rgba(74,240,196,.2); border-radius: 100px; padding: 6px 16px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--accent); letter-spacing: .08em; text-transform: uppercase; margin-bottom: 28px; animation: fadeDown .5s ease both; }
        .badge-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); animation: pulse 2s ease-in-out infinite; }
        h1 { font-size: clamp(40px, 8vw, 76px); font-weight: 800; line-height: 1; letter-spacing: -.03em; text-align: center; margin-bottom: 12px; animation: fadeDown .55s .05s ease both; }
        h1 span { background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .sub { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--muted); text-align: center; margin-bottom: 52px; letter-spacing: .04em; animation: fadeDown .6s .1s ease both; }
        .card { width: 100%; max-width: 560px; background: var(--surface); border: 1px solid var(--border); border-radius: 20px; padding: 40px; position: relative; animation: fadeUp .65s .15s ease both; transition: border-color .3s; }
        .card:hover { border-color: var(--border-hi); }
        .card::before { content: ''; position: absolute; top: -1px; left: -1px; width: 18px; height: 18px; border-top: 2px solid var(--accent); border-left: 2px solid var(--accent); border-radius: 4px 0 0 0; }
        .card::after  { content: ''; position: absolute; bottom: -1px; right: -1px; width: 18px; height: 18px; border-bottom: 2px solid var(--accent2); border-right: 2px solid var(--accent2); border-radius: 0 0 4px 0; }
        .field-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin-bottom: 10px; }
        .input-row { display: flex; gap: 12px; margin-bottom: 28px; }
        .input-wrap { flex: 1; position: relative; }
        .input-wrap svg { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--muted); pointer-events: none; transition: color .2s; }
        .input-wrap:focus-within svg { color: var(--accent); }
        input[type="text"] { width: 100%; background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 14px 14px 14px 42px; color: var(--text); font-family: 'JetBrains Mono', monospace; font-size: 13px; outline: none; transition: border-color .2s, box-shadow .2s; }
        input[type="text"]::placeholder { color: var(--muted); }
        input[type="text"]:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(74,240,196,.1); }
        .btn { flex-shrink: 0; background: var(--accent); color: #080a0f; border: none; border-radius: 12px; padding: 14px 22px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; letter-spacing: .04em; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; transition: background .2s, transform .15s, box-shadow .2s; white-space: nowrap; }
        .btn:hover { background: #6ef5d0; box-shadow: 0 0 24px rgba(74,240,196,.4); transform: translateY(-1px); }
        .btn:active { transform: translateY(0); }
        .btn.loading { opacity: .7; pointer-events: none; }
        .divider { display: flex; align-items: center; gap: 14px; margin-bottom: 28px; color: var(--muted); font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: .1em; }
        .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--border); }
        .qr-wrap { display: none; flex-direction: column; align-items: center; gap: 24px; animation: zoomIn .4s cubic-bezier(.34,1.56,.64,1); }
        .qr-wrap.visible { display: flex; }
        .qr-frame { position: relative; padding: 4px; border-radius: 16px; background: linear-gradient(135deg, var(--accent), var(--accent2)); }
        .qr-inner { background: #fff; border-radius: 13px; overflow: hidden; line-height: 0; }
        .qr-inner img { width: 220px; height: 220px; display: block; }
        .qr-scan { position: absolute; inset: 4px; border-radius: 13px; overflow: hidden; pointer-events: none; }
        .qr-scan::after { content: ''; position: absolute; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--accent), transparent); animation: scan 2s ease-in-out infinite; opacity: .8; }
        .btn-dl { background: transparent; border: 1px solid var(--border-hi); color: var(--text); border-radius: 10px; padding: 11px 20px; font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; transition: border-color .2s, background .2s, transform .15s; text-decoration: none; }
        .btn-dl:hover { border-color: var(--accent); background: rgba(74,240,196,.06); transform: translateY(-1px); }
        .url-tag { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted); background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 6px 12px; max-width: 320px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .footer { margin-top: 40px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted); text-align: center; animation: fadeUp .7s .3s ease both; }
        @keyframes fadeDown { from { opacity: 0; transform: translateY(-16px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeUp   { from { opacity: 0; transform: translateY(16px);  } to { opacity: 1; transform: translateY(0); } }
        @keyframes zoomIn   { from { opacity: 0; transform: scale(.85); } to { opacity: 1; transform: scale(1); } }
        @keyframes pulse    { 0%, 100% { opacity: 1; } 50% { opacity: .3; } }
        @keyframes scan     { 0% { top: 0%; } 50% { top: calc(100% - 2px); } 100% { top: 0%; } }
        @keyframes spin     { to { transform: rotate(360deg); } }
        .spinner { display: none; width: 14px; height: 14px; border: 2px solid rgba(8,10,15,.3); border-top-color: #080a0f; border-radius: 50%; animation: spin .6s linear infinite; }
        .btn.loading .spinner { display: block; }
        .btn.loading .btn-icon { display: none; }
    </style>
</head>
<body>
<div class="shell">
    <div class="badge"><span class="badge-dot"></span>QR Forge &mdash; v1.0</div>
    <h1>Generate<br><span>QR Codes</span></h1>
    <p class="sub">// encode any url or text in seconds</p>
    <div class="card">
        <div class="field-label">Input URL or text</div>
        <div class="input-row">
            <div class="input-wrap">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                <input type="text" id="urlInput" placeholder="https://example.com" value="https://github.com/" onkeydown="if(event.key==='Enter') generateQR()">
            </div>
            <button class="btn" id="genBtn" onclick="generateQR()">
                <svg class="btn-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM17 17h3v3h-3zM14 20h3"/></svg>
                <div class="spinner"></div>
                Generate
            </button>
        </div>
        <div class="divider">output</div>
        <div class="qr-wrap" id="qrWrap">
            <div class="qr-frame">
                <div class="qr-inner"><img id="qrImage" alt="QR Code"></div>
                <div class="qr-scan"></div>
            </div>
            <p class="url-tag" id="urlTag"></p>
            <a class="btn-dl" id="dlBtn" download="qr-code.png">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                Download PNG
            </a>
        </div>
    </div>
    <p class="footer">QR Forge &mdash; built with Flask + qrcode</p>
</div>
<script>
    async function generateQR() {
        const input  = document.getElementById('urlInput');
        const btn    = document.getElementById('genBtn');
        const wrap   = document.getElementById('qrWrap');
        const img    = document.getElementById('qrImage');
        const dlBtn  = document.getElementById('dlBtn');
        const urlTag = document.getElementById('urlTag');
        const url    = input.value.trim();
        if (!url) { input.focus(); return; }
        btn.classList.add('loading');
        wrap.classList.remove('visible');
        try {
            const res  = await fetch('/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url }) });
            const blob = await res.blob();
            const src  = URL.createObjectURL(blob);
            img.src    = src;
            dlBtn.href = src;
            urlTag.textContent = url.length > 48 ? url.slice(0, 45) + '...' : url;
            wrap.classList.add('visible');
        } catch(e) {
            alert('Something went wrong. Please try again.');
        } finally {
            btn.classList.remove('loading');
        }
    }
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/generate", methods=["POST"])
def generate_qr():
    data = request.get_json()
    url  = data.get("url", "")
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img    = qr.make_image(fill_color="black", back_color="white")
    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
