"""
Static HTML generator for Qantcore.
Bloomberg-terminal × Linear × Anthropic design.
Reads all articles from MongoDB, renders HTML pages, writes to output dir.
"""
from pymongo import MongoClient
import os, json, datetime

DB = MongoClient("localhost", 27017).qantcore

OUT = "/opt/data/www/qantcore/static"
os.makedirs(OUT, exist_ok=True)

# ─── CSS ──────────────────────────────────────────────────────────
CSS = """*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0B0F14;--surface:#121821;--card-bg:#171F2B;--border:rgba(255,255,255,.06);
  --text:#F5F7FA;--muted:#9AA4B2;--dim:#6B7280;
  --green:#10b981;--green-dim:rgba(16,185,129,.12);
  --blue:#3B82F6;--blue-dim:rgba(59,130,246,.12);
  --cyan:#22D3EE;--cyan-dim:rgba(34,211,238,.12);
  --amber:#f59e0b;--amber-dim:rgba(245,158,11,.12);
  --red:#ef4444;--red-dim:rgba(239,68,68,.12);
  --radius:12px;--radius-sm:8px}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Inter',sans-serif;
  background:var(--bg);color:var(--text);min-height:100vh;line-height:1.6;
  -webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#1e2233;border-radius:2px}

/* ─── Header & Mega-Nav ─── */
header{position:sticky;top:0;z-index:100;backdrop-filter:blur(20px) saturate(180%);
  background:rgba(11,15,20,.92);border-bottom:1px solid var(--border)}
.header-inner{max-width:1320px;margin:0 auto;padding:14px 24px;
  display:flex;align-items:center;justify-content:space-between}
.logo{font-size:20px;font-weight:800;letter-spacing:-.02em;color:var(--text);
  display:flex;align-items:center;gap:8px}
.logo-dot{width:8px;height:8px;border-radius:50%;background:var(--green);
  box-shadow:0 0 8px rgba(16,185,129,.5);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.mega-nav{display:flex;gap:4px;align-items:center}
.mega-nav a,.mega-nav .nav-section{font-size:12.5px;color:var(--muted);
  padding:6px 12px;border-radius:6px;transition:all .2s;font-weight:500;
  letter-spacing:.01em;white-space:nowrap}
.mega-nav a:hover{color:var(--text);background:rgba(255,255,255,.04)}
.mega-nav a.active{color:var(--green);background:var(--green-dim)}
.nav-sep{width:1px;height:18px;background:var(--border);margin:0 4px}

/* ─── Terminal Grid (hero bg) ─── */
.terminal-grid{position:absolute;top:0;left:0;right:0;bottom:0;overflow:hidden;pointer-events:none;z-index:0}
.terminal-grid::before{content:'';position:absolute;top:0;left:0;right:0;bottom:0;
  background-image:
    linear-gradient(rgba(16,185,129,.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(16,185,129,.04) 1px,transparent 1px);
  background-size:40px 40px;
  animation:grid-scroll 20s linear infinite}
@keyframes grid-scroll{0%{transform:translate(0,0)}100%{transform:translate(40px,40px)}}
.terminal-grid::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;
  background:
    radial-gradient(ellipse at 50% 0%, rgba(16,185,129,.1) 0%, transparent 60%),
    radial-gradient(circle at 20% 80%, rgba(59,130,246,.06) 0%, transparent 40%),
    radial-gradient(circle at 80% 20%, rgba(16,185,129,.05) 0%, transparent 40%);
  z-index:1}
/* ─── Hero ─── */
.hero{text-align:center;padding:72px 24px 48px;position:relative;overflow:hidden}
.hero>*{position:relative;z-index:2}
.hero h1{font-size:clamp(32px,5vw,56px);font-weight:800;letter-spacing:-.03em;
  line-height:1.15;color:#f1f5f9;max-width:800px;margin:0 auto}
.hero h1 .accent{color:var(--green)}
.hero .sub{font-size:17px;color:var(--muted);margin-top:16px;max-width:640px;
  margin-left:auto;margin-right:auto;line-height:1.6}
.hero .tagline{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:var(--green);
  font-weight:600;margin-bottom:16px}
.hero-metrics{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:28px}
.hero-metric{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius-sm);
  padding:10px 18px;text-align:center;min-width:100px}
.hero-metric .val{font-size:22px;font-weight:800;color:var(--green);font-variant-numeric:tabular-nums}
.hero-metric .lbl{font-size:11px;color:var(--muted);margin-top:2px;text-transform:uppercase;letter-spacing:.06em}
.hero-cta{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:32px}
.cta-primary{padding:12px 28px;border-radius:var(--radius-sm);font-size:14px;font-weight:600;
  background:var(--green);color:#000;border:none;cursor:pointer;transition:all .2s;
  letter-spacing:-.01em}
.cta-primary:hover{filter:brightness(1.15);transform:translateY(-1px)}
.cta-secondary{padding:12px 28px;border-radius:var(--radius-sm);font-size:14px;font-weight:600;
  background:transparent;color:var(--text);border:1px solid var(--border);cursor:pointer;
  transition:all .2s}
.cta-secondary:hover{border-color:var(--green);color:var(--green)}

/* ─── Authority Bar ─── */
.auth-bar{max-width:1320px;margin:0 auto 0;padding:0 24px 32px}
.auth-inner{display:flex;gap:0;background:var(--card-bg);border:1px solid var(--border);
  border-radius:var(--radius);overflow:hidden;flex-wrap:wrap}
.auth-stat{flex:1;min-width:130px;padding:18px 20px;text-align:center;
  border-right:1px solid var(--border);position:relative}
.auth-stat:last-child{border-right:none}
.auth-stat .n{font-size:26px;font-weight:800;color:var(--green);font-variant-numeric:tabular-nums;
  letter-spacing:-.02em}
.auth-stat .n.amber{color:var(--amber)}
.auth-stat .l{font-size:11px;color:var(--muted);margin-top:3px;text-transform:uppercase;letter-spacing:.05em}
.auth-stat .dot{display:inline-block;width:6px;height:6px;border-radius:50%;
  background:var(--green);margin-right:6px;animation:pulse 2s infinite}

/* ─── Section Headers ─── */
.section-hd{max-width:1320px;margin:0 auto;padding:8px 24px 16px;
  display:flex;align-items:center;justify-content:space-between}
.section-hd h2{font-size:18px;font-weight:700;color:var(--text);letter-spacing:-.01em}
.section-hd .see-all{font-size:13px;color:var(--green);font-weight:500}
.section-hd .see-all:hover{text-decoration:underline}

/* ─── Filters ─── */
.filters-bar{max-width:1320px;margin:0 auto;padding:0 24px 20px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.filters-bar .label{font-size:12px;color:var(--dim);text-transform:uppercase;letter-spacing:.05em;margin-right:4px}
.filter-btn{padding:6px 14px;border-radius:20px;font-size:12px;font-weight:500;
  border:1px solid var(--border);background:transparent;
  color:var(--muted);cursor:pointer;transition:all .2s;white-space:nowrap}
.filter-btn:hover,.filter-btn.active{border-color:var(--green);color:var(--green);
  background:var(--green-dim)}
.filter-btn .count{font-size:10px;color:var(--dim);margin-left:4px}

/* ─── Grid & Cards ─── */
.grid{max-width:1320px;margin:0 auto;padding:0 24px 32px;
  display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}

.card{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);
  padding:20px;transition:all .2s;position:relative;display:flex;flex-direction:column}
.card:hover{border-color:rgba(16,185,129,.25);transform:translateY(-2px);
  box-shadow:0 8px 30px rgba(0,0,0,.4)}
.card-top{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px}
.card-icon{width:40px;height:40px;border-radius:var(--radius-sm);background:rgba(255,255,255,.04);
  display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;overflow:hidden}
.card-icon img{width:100%;height:100%;object-fit:contain;padding:6px}
.card-badge{padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.badge-agent{background:var(--blue-dim);color:var(--blue)}
.badge-framework{background:var(--green-dim);color:var(--green)}
.badge-platform{background:var(--amber-dim);color:var(--amber)}
.badge-model{background:var(--red-dim);color:var(--red)}
.badge-infra{background:rgba(139,92,246,.12);color:#8b5cf6}
.card-title{font-size:15px;font-weight:700;color:#f1f5f9;margin-bottom:6px;letter-spacing:-.01em;line-height:1.3}
.card-desc{font-size:12.5px;color:var(--muted);line-height:1.5;display:-webkit-box;
  -webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:12px;flex:1}
/* Intelligence Panel */
.card-panel{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:auto}
.panel-item{background:rgba(255,255,255,.02);border-radius:6px;padding:8px 10px}
.panel-item .pv{font-size:14px;font-weight:700;color:var(--text);font-variant-numeric:tabular-nums}
.panel-item .pv.green{color:var(--green)}
.panel-item .pv.amber{color:var(--amber)}
.panel-item .pl{font-size:10px;color:var(--dim);margin-top:1px;text-transform:uppercase;letter-spacing:.03em}
.card-compare{position:absolute;top:12px;right:12px;z-index:5}
.card-compare input[type=checkbox]{appearance:none;width:18px;height:18px;border-radius:4px;
  border:2px solid var(--dim);cursor:pointer;transition:all .2s;position:relative}
.card-compare input[type=checkbox]:checked{border-color:var(--green);background:var(--green)}
.card-compare input[type=checkbox]:checked::after{content:'✓';position:absolute;
  top:-1px;left:2px;color:#000;font-size:13px;font-weight:700}
.card-trust{display:flex;gap:12px;margin-top:8px;font-size:10px;color:var(--dim)}
.card-trust span{display:flex;align-items:center;gap:3px}

/* ─── Compare Bar ─── */
.compare-bar{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);
  background:var(--card-bg);border:1px solid var(--green);
  border-radius:var(--radius);padding:12px 20px;display:none;align-items:center;gap:16px;
  z-index:200;box-shadow:0 8px 40px rgba(0,0,0,.6);backdrop-filter:blur(16px)}
.compare-bar.active{display:flex}
.compare-bar .sel{font-size:13px;color:var(--muted)}
.compare-bar .sel strong{color:var(--green)}
.compare-btn{padding:8px 20px;border-radius:6px;font-size:13px;font-weight:600;
  background:var(--green);color:#000;border:none;cursor:pointer;transition:all .2s}
.compare-btn:hover{filter:brightness(1.15)}
.compare-btn:disabled{opacity:.3;cursor:not-allowed}
.compare-clear{font-size:12px;color:var(--muted);cursor:pointer;background:none;border:none}
.compare-clear:hover{color:var(--red)}

/* ─── Featured Section ─── */
.featured{max-width:1320px;margin:0 auto;padding:0 24px 32px}
.featured-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:16px}
.featured-card{background:var(--card-bg);border:1px solid var(--border);
  border-radius:var(--radius);padding:24px;transition:all .2s;
  position:relative;overflow:hidden}
.featured-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--green),var(--blue));opacity:0;transition:opacity .2s}
.featured-card:hover::before{opacity:1}
.featured-card:hover{transform:translateY(-2px);border-color:rgba(16,185,129,.2);
  box-shadow:0 8px 30px rgba(0,0,0,.4)}
.featured-card .fc-label{font-size:10px;text-transform:uppercase;letter-spacing:.06em;
  color:var(--green);margin-bottom:8px;font-weight:600}
.featured-card .fc-title{font-size:18px;font-weight:700;color:#f1f5f9;margin-bottom:6px}
.featured-card .fc-desc{font-size:13px;color:var(--muted);line-height:1.6}

/* ─── Compare Table ─── */
.compare-table-wrap{overflow-x:auto;margin:20px 0}
.compare-table{width:100%;border-collapse:collapse;font-size:13px}
.compare-table th{text-align:left;padding:12px 16px;color:var(--muted);font-weight:500;
  font-size:11px;text-transform:uppercase;letter-spacing:.04em;border-bottom:1px solid var(--border)}
.compare-table td{padding:14px 16px;border-bottom:1px solid var(--border)}
.compare-table tr:last-child td{border-bottom:none}
.compare-table .winner{color:var(--green);font-weight:600}
.compare-check{color:var(--green)}

/* ─── Live Feed ─── */
.live-dot{display:inline-block;width:8px;height:8px;border-radius:50%;
  background:var(--green);margin-right:8px;animation:pulse 2s infinite}

/* ─── Bookmark ─── */
.bookmark-btn{position:absolute;top:12px;left:12px;z-index:5;background:none;border:none;
  font-size:16px;cursor:pointer;color:var(--dim);transition:all .2s;padding:4px}
.bookmark-btn:hover{color:var(--amber);transform:scale(1.2)}
.bookmark-btn.saved{color:var(--amber)}
.saved-section{margin-top:24px}
/* ─── Feed ─── */
.feed-list{display:flex;flex-direction:column;gap:8px}
.feed-item{display:flex;align-items:flex-start;gap:12px;padding:12px 16px;
  background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius-sm);
  transition:all .2s;font-size:13px}
.feed-item:hover{border-color:rgba(16,185,129,.2)}
.feed-item .fi-time{font-size:10px;color:var(--dim);white-space:nowrap;min-width:55px;padding-top:2px}
.feed-item .fi-icon{font-size:14px;flex-shrink:0}
.feed-item .fi-text{color:var(--muted);line-height:1.5}
.feed-item .fi-text strong{color:var(--text)}

/* ─── Trust Badges ─── */
.trust-badge{display:inline-flex;align-items:center;gap:4px;font-size:10px;
  padding:3px 8px;border-radius:4px;font-weight:500}
.trust-verified{background:var(--green-dim);color:var(--green)}
.trust-fresh{background:rgba(16,185,129,.06);color:var(--green)}
.trust-stale{background:var(--amber-dim);color:var(--amber)}

/* ─── Stack Builder ─── */
.stack-builder{max-width:1320px;margin:0 auto;padding:32px 24px}
.stack-inner{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);
  padding:32px}
.stack-inner h2{font-size:20px;font-weight:700;margin-bottom:8px}
.stack-inner .stack-sub{font-size:14px;color:var(--muted);margin-bottom:24px}
.stack-slots{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:24px}
.stack-slot{background:rgba(255,255,255,.02);border:2px dashed var(--border);
  border-radius:var(--radius-sm);padding:16px;text-align:center;cursor:pointer;transition:all .2s}
.stack-slot:hover{border-color:var(--green)}
.stack-slot.filled{border-style:solid;border-color:rgba(16,185,129,.3);background:var(--green-dim)}
.stack-slot .ss-label{font-size:10px;text-transform:uppercase;color:var(--dim);letter-spacing:.05em;margin-bottom:6px}
.stack-slot .ss-value{font-size:14px;font-weight:600;color:var(--text)}
.stack-result{background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.2);
  border-radius:var(--radius-sm);padding:20px;display:none}
.stack-result.active{display:block}
.stack-result h3{font-size:16px;color:var(--green);margin-bottom:12px}
.stack-metrics{display:flex;gap:20px;flex-wrap:wrap}
.stack-metric{text-align:center}
.stack-metric .sm-val{font-size:20px;font-weight:700;color:var(--text)}
.stack-metric .sm-lbl{font-size:11px;color:var(--dim);margin-top:2px}

/* ─── Product Detail ─── */
.detail{max-width:900px}
.detail-header{margin-bottom:32px}
.detail-header h1{font-size:32px;font-weight:800;color:#f1f5f9;letter-spacing:-.01em}
.detail-header .tagline{font-size:16px;color:var(--muted);margin-top:8px}
.detail-meta{display:flex;gap:12px;flex-wrap:wrap;margin-top:16px}
.meta-item{display:flex;align-items:center;gap:6px;padding:8px 14px;
  background:var(--card-bg);border-radius:var(--radius-sm);font-size:12.5px;color:var(--muted);
  border:1px solid var(--border)}
.meta-item strong{color:var(--text)}
.meta-item.green{color:var(--green);border-color:rgba(16,185,129,.2)}
.detail-body{margin-top:28px;font-size:14.5px;line-height:1.8;color:#b0b8c8}
.detail-body h2{font-size:20px;font-weight:700;color:var(--text);margin:28px 0 10px}
.detail-body h3{font-size:16px;font-weight:600;color:#d0d8e8;margin:22px 0 8px}
.detail-body p{margin-bottom:14px}
.detail-body ul,.detail-body ol{padding-left:22px;margin-bottom:14px}
.detail-body li{margin-bottom:5px}
.detail-body code{background:rgba(255,255,255,.06);padding:2px 6px;border-radius:4px;font-size:12.5px;color:var(--green)}
.detail-body strong{color:var(--text)}
.detail-body table{width:100%;border-collapse:collapse;margin:14px 0}
.detail-body td,.detail-body th{border:1px solid var(--border);padding:10px 14px;text-align:left;font-size:12.5px}
.detail-body th{background:rgba(255,255,255,.03);color:var(--green);font-weight:600}

.breadcrumbs{font-size:12.5px;color:var(--dim);margin-bottom:20px}
.breadcrumbs a{color:var(--muted);transition:color .2s}
.breadcrumbs a:hover{color:var(--green)}
.breadcrumbs span{color:var(--text)}

.detail-image{width:100px;height:100px;border-radius:var(--radius);overflow:hidden;flex-shrink:0;
  background:rgba(255,255,255,.03);display:flex;align-items:center;justify-content:center}
.detail-image img{width:100%;height:100%;object-fit:contain;padding:10px}

.rating{color:var(--amber);font-weight:700;font-size:13px}
.price{font-weight:600;color:var(--green)}

.stats-mini{display:flex;gap:16px;flex-wrap:wrap;margin:20px 0}
.stat-mini{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius-sm);
  padding:14px 20px;text-align:center;min-width:100px}
.stat-mini .sv{font-size:22px;font-weight:800;color:var(--green)}
.stat-mini .sl{font-size:10px;color:var(--dim);text-transform:uppercase;letter-spacing:.04em;margin-top:2px}

.empty{text-align:center;padding:80px 24px}
.empty h2{font-size:24px;color:var(--muted);margin-bottom:8px}
.empty p{color:var(--dim)}

footer{text-align:center;padding:40px 24px;color:#1e2233;font-size:12px;
  border-top:1px solid var(--border);margin-top:40px}
footer a{color:var(--green)}

/* ─── Search ─── */
.search-bar{max-width:1320px;margin:0 auto;padding:0 24px 24px}
.search-bar input{width:100%;padding:12px 18px;border-radius:var(--radius-sm);
  background:var(--card-bg);border:1px solid var(--border);
  color:var(--text);font-size:14px;outline:none;transition:border-color .2s}
.search-bar input:focus{border-color:var(--green)}
.search-bar input::placeholder{color:var(--dim)}

@media(max-width:768px){
  .hero h1{font-size:28px}
  .grid,.featured-grid{grid-template-columns:1fr}
  .mega-nav{overflow-x:auto;gap:2px;-webkit-overflow-scrolling:touch}
  .mega-nav a,.mega-nav .nav-section{font-size:11px;padding:5px 8px}
  .nav-sep{display:none}
  .auth-stat{min-width:80px;padding:12px 10px}
  .auth-stat .n{font-size:18px}
  .auth-stat .l{font-size:9px}
  .hero-metrics{gap:6px}
  .hero-metric{min-width:70px;padding:8px 12px}
  .hero-metric .val{font-size:16px}
  .hero-metric .lbl{font-size:9px}
  .compare-bar{left:16px;right:16px;transform:none;border-radius:var(--radius-sm)}
  .section-hd{padding:8px 16px 12px}
  .filters-bar,.grid,.featured,.auth-bar{padding-left:16px;padding-right:16px}
  .header-inner{padding:12px 16px}
}"""

# ─── Helpers ──────────────────────────────────────────────────────
def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def icon_for(pt):
    icons = {"agent":"🤖","framework":"🔧","platform":"🌐","model":"🧠","infrastructure":"⚡"}
    return icons.get(pt, "📦")

def product_type_badge(pt):
    mapping = {"agent":"badge-agent","framework":"badge-framework","platform":"badge-platform",
               "model":"badge-model","infrastructure":"badge-infra"}
    labels = {"agent":"Agent","framework":"Framework","platform":"Platform",
              "model":"Model","infrastructure":"Infra"}
    cls = mapping.get(pt, "badge-agent")
    lbl = labels.get(pt, pt)
    return f'<span class="card-badge {cls}">{esc(lbl)}</span>'

def product_image(p, size="icon"):
    img_url = p.get("image_url", "")
    if img_url:
        if size == "card":
            return f'<div class="card-img"><img src="{img_url}" alt="{esc(p.get("title",""))}" loading="lazy"></div>'
        elif size == "detail":
            return f'<div class="detail-image"><img src="{img_url}" alt="{esc(p.get("title",""))}"></div>'
        else:
            return f'<div class="card-icon"><img src="{img_url}" alt="" loading="lazy"></div>'
    return f'<div class="card-icon">{icon_for(p.get("product_type",""))}</div>'

def rating_stars(rating):
    if not rating: return ""
    stars = round(float(rating))
    return "★" * stars + "☆" * (5 - stars)

def format_price(pricing):
    prices = {"freemium":"Freemium","open-source":"Open Source","paid":"Paid","usage-based":"Usage-based"}
    return prices.get(pricing, pricing)

def freshness_badge(score):
    if score is None: return ""
    s = float(score)
    if s >= 0.8: return '<span class="trust-badge trust-fresh">● Fresh</span>'
    if s >= 0.5: return '<span class="trust-badge trust-stale">○ Stable</span>'
    return ""

def time_ago(ts_str):
    """Human-readable time ago."""
    try:
        dt = datetime.datetime.fromisoformat(str(ts_str).replace("Z","+00:00"))
        now = datetime.datetime.now(datetime.timezone.utc)
        diff = now - dt
        mins = int(diff.total_seconds() / 60)
        if mins < 1: return "just now"
        if mins < 60: return f"{mins}m ago"
        hours = mins // 60
        if hours < 24: return f"{hours}h ago"
        days = hours // 24
        return f"{days}d ago"
    except:
        return ""

def panel_data(p):
    """Extract intelligence panel data from product — mini-terminal card."""
    rating = p.get("rating", "")
    pricing = format_price(p.get("pricing_model", ""))
    review_count = p.get("review_count", 0) or 0
    tech_stack = p.get("tech_stack", []) or []
    freshness = p.get("freshness_score", 0) or 0
    # Deployment: local-first / cloud-only / hybrid
    local_first = p.get("local_first", False) or any(
        ts.lower() in ["docker", "local", "self-hosted", "python", "cli", "terminal"] 
        for ts in tech_stack
    )
    if p.get("local_deploy", False) is True:
        local_first = True
    depl = "🏠 Local" if local_first else "☁️ Cloud"
    # Complexity from tech stack
    complexity = "Low" if len(tech_stack) <= 2 else "Medium" if len(tech_stack) <= 5 else "High"
    # Maturity score
    maturity = ""
    if rating and float(rating) >= 4.5 and review_count > 500:
        maturity = "Enterprise"
    elif rating and float(rating) >= 4.0:
        maturity = "Production"
    elif rating:
        maturity = "Growing"
    else:
        maturity = "New"
    # Velocity signal — trend based on freshness + recency
    trend = "→"
    if freshness > 0.8: trend = "↑↑"
    elif freshness > 0.6: trend = "↑"
    elif freshness < 0.3: trend = "↓"
    items = []
    if rating:
        items.append(f'<div class="panel-item"><div class="pv amber">{rating} ★</div><div class="pl">Rating</div></div>')
    if pricing:
        items.append(f'<div class="panel-item"><div class="pv green">{esc(pricing)}</div><div class="pl">Pricing</div></div>')
    items.append(f'<div class="panel-item"><div class="pv">{depl}</div><div class="pl">Deployment</div></div>')
    items.append(f'<div class="panel-item"><div class="pv">{maturity}</div><div class="pl">Maturity</div></div>')
    items.append(f'<div class="panel-item"><div class="pv">{complexity}</div><div class="pl">Complexity</div></div>')
    items.append(f'<div class="panel-item"><div class="pv cyan">{trend} {int(freshness*100)}%</div><div class="pl">Velocity</div></div>')
    return "".join(items)

def trust_indicators(p):
    """Generate trust indicators HTML with data-iso for live timestamps."""
    parts = []
    if p.get("freshness_score"):
        parts.append(freshness_badge(p["freshness_score"]))
    if p.get("updated_at"):
        iso = str(p["updated_at"]).replace(" ", "T")
        parts.append(f'<span class="time-ago" data-iso="{iso}">🕐 {time_ago(p["updated_at"])}</span>')
    if p.get("review_count"):
        parts.append(f'<span>📊 {p["review_count"]} reviews</span>')
    if p.get("website_url"):
        parts.append('<span class="trust-badge trust-verified">✓ Verified</span>')
    return "".join(parts)


# ─── Page template ────────────────────────────────────────────────
PAGE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} | Qantcore — AI Agents Intelligence</title>
<meta name="description" content="{description}">
<link rel="icon" type="image/svg+xml" href="/images/favicon.svg">
{open_graph}
<style>{css}</style>
<script type="application/ld+json">
{schema_org}
</script>
</head>
<body>
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
(function(m,e,t,r,i,k,a){{
m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
m[i].l=1*new Date();
for (var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return;}}}}
k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
}})(window,document,'script','https://mc.yandex.ru/metrika/tag.js?id=109327472','ym');
ym(109327472,'init',{{ssr:true,webvisor:true,clickmap:true,ecommerce:"dataLayer",referrer:document.referrer,url:location.href,accurateTrackBounce:true,trackLinks:true}});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/109327472" style="position:absolute;left:-9999px" alt=""/></div></noscript>
<!-- /Yandex.Metrika counter -->
<header>
  <div class="header-inner">
    <a href="/" class="logo"><span class="logo-dot"></span>Qantcore</a>
    <div class="mega-nav">
      <a href="/" class="{active_home}">Frameworks</a>
      <span class="nav-sep"></span>
      <a href="/catalog/comparison/" class="{active_compare}">Compare</a>
      <span class="nav-sep"></span>
      <a href="/catalog/review/" class="{active_review}">Reviews</a>
      <span class="nav-sep"></span>
      <a href="#rankings">Rankings</a>
      <span class="nav-sep"></span>
      <a href="#local-ai">Local AI</a>
      <span class="nav-sep"></span>
      <a href="#coding-agents">Coding</a>
      <span class="nav-sep"></span>
      <a href="#multi-agent">Multi-Agent</a>
      <span class="nav-sep"></span>
      <a href="#guides">Guides</a>
      <span class="nav-sep"></span>
      <a href="/methodology/" class="{active_method}">Methodology</a>
      <span class="nav-sep"></span>
      <a href="#saved" class="saved-nav" style="display:none">★ Saved</a>
    </div>
  </div>
</header>
{content}
<footer>
  Qantcore &copy; 2026 &mdash; AI Agents Intelligence Platform &mdash;
  Updated daily &mdash; <a href="https://t.me/nousresearch">@nousresearch</a>
</footer>
{scripts}
</body>
</html>"""

# ─── Search index ─────────────────────────────────────────────────
def build_search_index():
    products = list(DB.articles.find({"category": "product"}))
    entries = []
    for p in products:
        img = ""
        if p.get("image_url"):
            img = f'<div class="card-icon"><img src="{p["image_url"]}" alt="" loading="lazy"></div>'
        else:
            img = f'<div class="card-icon">{icon_for(p.get("product_type",""))}</div>'
        entries.append({
            "u": f"/product/{p['slug']}/",
            "ti": esc(p.get("title","")),
            "d": esc((p.get("tagline","") or p.get("description",""))[:120]),
            "t": (p.get("title","") + " " + (p.get("tagline","") or "") + " " + p.get("product_type","") + " " + (p.get("subcategory","") or "")).lower(),
            "pt": p.get("product_type",""),
            "ptl": {"agent":"Agent","framework":"Framework","platform":"Platform","model":"Model","infrastructure":"Infra"}.get(p.get("product_type",""), p.get("product_type","")),
            "r": str(p.get("rating","")),
            "s": rating_stars(p.get("rating")),
            "pr": format_price(p.get("pricing_model","")),
            "img": img,
            "panel": panel_data(p),
            "trust": trust_indicators(p),
        })
    return json.dumps(entries)

def render_page(title, description, content, scripts="", total=0, search_val="", search_json="[]",
                active_home="", active_compare="", active_review="", active_method="",
                open_graph="", schema_org="{}"):
    return PAGE.format(
        title=esc(title), description=esc(description),
        css=CSS, content=content, scripts=scripts, total=str(total),
        search_val=esc(search_val), search_json=search_json,
        active_home=active_home, active_compare=active_compare, active_review=active_review, active_method=active_method,
        open_graph=open_graph, schema_org=schema_org)


# ─── Card Generator ───────────────────────────────────────────────
def make_product_card(p, with_compare=True):
    """Intelligence panel card."""
    compare_html = ""
    if with_compare:
        compare_html = f'<div class="card-compare"><input type="checkbox" value="{p["slug"]}" onchange="toggleCompare(this)" aria-label="Compare"></div>'
    bookmark_html = f'<button class="bookmark-btn" data-slug="{p["slug"]}" onclick="toggleSave(this,\'{p["slug"]}\')" title="Save">☆</button>'
    panel = panel_data(p)
    trust = trust_indicators(p)
    return f"""<a href="/product/{p['slug']}/" class="card">
      {compare_html}
      {bookmark_html}
      <div class="card-top">
        {product_image(p)}
        {product_type_badge(p.get('product_type',''))}
      </div>
      <div class="card-title">{esc(p.get('title',''))}</div>
      <div class="card-desc">{esc(p.get('tagline','') or p.get('description',''))}</div>
      <div class="card-panel">{panel}</div>
      <div class="card-trust">{trust}</div>
    </a>"""


# ─── Generators ───────────────────────────────────────────────────
def generate_home():
    """Generate /index.html — full redesign."""
    products = list(DB.articles.find({"category": "product"}).sort("rating", -1))
    tp = len(products)  # 60
    tc = DB.articles.count_documents({"category": "comparison"})  # 100
    tr = DB.articles.count_documents({"category": "review"})  # 0

    # Product type counts
    type_counts = {}
    for p in products:
        pt = p.get("product_type", "other")
        type_counts[pt] = type_counts.get(pt, 0) + 1

    # Top rated (featured)
    featured = sorted(products, key=lambda p: (p.get("rating", 0) or 0), reverse=True)[:6]
    # Trending: high rating + recent
    trending = sorted(products, key=lambda p: ((p.get("rating", 0) or 0) * 0.6 + (p.get("freshness_score", 0) or 0) * 0.4), reverse=True)[:8]

    # ─── Hero ───
    # Latest update timestamp for live signal
    latest = list(DB.articles.find({"category": "product"}).sort("updated_at", -1).limit(1))
    last_update = "Today"
    if latest and latest[0].get("updated_at"):
        ago = time_ago(latest[0]["updated_at"])
        last_update = f"Updated {ago}"

    hero = f"""<section class="hero">
  <div class="terminal-grid"></div>
  <div class="tagline">AI AGENT INTELLIGENCE PLATFORM</div>
  <h1>Compare, Benchmark &amp; Deploy<br><span class="accent">AI Agents</span></h1>
  <p class="sub">The definitive catalog of AI agent frameworks —
  deep technical reviews, live benchmarks, and deployment intelligence. {last_update}.</p>
  <div class="hero-metrics">
    <div class="hero-metric"><div class="val">{tp}+</div><div class="lbl">Frameworks</div></div>
    <div class="hero-metric"><div class="val">{tc}+</div><div class="lbl">Comparisons</div></div>
    <div class="hero-metric"><div class="val">{tr}+</div><div class="lbl">Reviews</div></div>
    <div class="hero-metric"><div class="val" style="color:var(--green)">●</div><div class="lbl">Daily Updates</div></div>
  </div>
  <div class="hero-cta">
    <a href="#catalog" class="cta-primary">Explore Frameworks</a>
    <a href="/catalog/comparison/" class="cta-secondary">Compare AI Agents</a>
    <a href="#guides" class="cta-secondary">Deployment Guides</a>
  </div>
</section>"""

    # ─── Authority Bar ───
    auth = f"""<div class="auth-bar" id="catalog">
  <div class="auth-inner">
    <div class="auth-stat"><div class="n">{tp}</div><div class="l">Agents tracked</div></div>
    <div class="auth-stat"><div class="n">{tc}</div><div class="l">Head-to-head comparisons</div></div>
    <div class="auth-stat"><div class="n amber">{type_counts.get('agent',0)}</div><div class="l">AI Agents</div></div>
    <div class="auth-stat"><div class="n">{type_counts.get('framework',0)}</div><div class="l">Frameworks</div></div>
    <div class="auth-stat"><div class="n">{type_counts.get('platform',0)}</div><div class="l">Platforms</div></div>
    <div class="auth-stat"><div class="n"><span class="dot"></span>Live</div><div class="l">Updated today</div></div>
  </div>
</div>"""

    # ─── Featured (Level 1: top 6 by rating) ───
    feat_cards = ""
    for p in featured:
        feat_cards += make_product_card(p)
    featured_html = f"""<div class="section-hd"><h2>★ Featured Frameworks</h2><a href="/catalog/product/" class="see-all">See all {tp} →</a></div>
<div class="grid">{feat_cards}</div>"""

    # ─── Trending Comparisons (Level 2) ───
    comps = list(DB.articles.find({"category": "comparison"}).limit(4))
    comp_cards = ""
    for c in comps:
        comp_cards += f"""<a href="/compare/{c['slug']}/" class="card">
      <div class="card-top">
        <div class="card-icon">⚖️</div>
        <span class="card-badge badge-framework">VS</span>
      </div>
      <div class="card-title">{esc(c.get('title',''))}</div>
      <div class="card-desc">{esc(str(c.get('description',''))[:120])}</div>
      <div class="card-trust"><span class="trust-badge trust-verified">✓ Detailed comparison</span></div>
    </a>"""

    trending_html = ""
    if comp_cards:
        trending_html = f"""<div class="section-hd"><h2>⚡ Trending Comparisons</h2><a href="/catalog/comparison/" class="see-all">All {tc} →</a></div>
<div class="grid">{comp_cards}</div>"""

    # ─── New Releases (Level 2.5: latest 6 by date) ───
    newest = sorted(products, key=lambda p: p.get("updated_at", ""), reverse=True)[:6]
    new_cards = ""
    for p in newest:
        new_cards += make_product_card(p)
    new_html = f"""<div class="section-hd"><h2>🆕 New & Updated</h2><a href="/catalog/product/" class="see-all">All {tp} →</a></div>
<div class="grid">{new_cards}</div>"""

    # ─── Benchmark Intelligence Snapshot ───
    cat_counts = {}
    for p in products:
        sc = p.get("subcategory", "") or "other"
        cat_counts[sc] = cat_counts.get(sc, 0) + 1
    bench_rows = ""
    for sc, n in sorted(cat_counts.items(), key=lambda x: -x[1])[:6]:
        bench_rows += f'<div class="auth-stat"><div class="n">{n}</div><div class="l">{sc}</div></div>'
    bench_html = f"""<div class="section-hd" id="rankings"><h2>📊 Benchmark Intelligence</h2></div>
<div class="auth-bar">
  <div class="auth-inner">
    <div class="auth-stat"><div class="n amber">{tp}</div><div class="l">Total Ranked</div></div>
    <div class="auth-stat"><div class="n">{tc}</div><div class="l">Side-by-Side Tests</div></div>
    {bench_rows}
  </div>
</div>"""

    # ─── Deployment Guides (placeholder) ───
    guides_html = f"""<div class="section-hd" id="guides"><h2>📖 Deployment Guides</h2><a href="#" class="see-all">Coming soon →</a></div>
<div class="featured">
  <div class="featured-grid">
    <div class="featured-card">
      <div class="fc-label">GUIDE</div>
      <div class="fc-title">Run AI Agents Locally</div>
      <div class="fc-desc">Step-by-step: deploy Ollama, Open Interpreter, and local LLMs on your machine. No cloud needed.</div>
    </div>
    <div class="featured-card">
      <div class="fc-label">GUIDE</div>
      <div class="fc-title">Multi-Agent Orchestration</div>
      <div class="fc-desc">Compare CrewAI, AutoGen, LangGraph — pick the right framework for your multi-agent system.</div>
    </div>
    <div class="featured-card">
      <div class="fc-label">GUIDE</div>
      <div class="fc-title">AI Coding Stack in 2026</div>
      <div class="fc-desc">Cursor, Cline, Copilot, Aider, Codex — which coding agent fits your workflow?</div>
    </div>
  </div>
</div>"""

    # ─── Latest (Level 3: all products) ───
    # Filters
    product_types = DB.articles.distinct("product_type", {"category": "product"})
    filters_html = '<span class="label">Filter:</span>'
    filters_html += '<button class="filter-btn active" onclick="filterCards(\'all\')">All</button>'
    for pt in sorted(product_types):
        cnt = type_counts.get(pt, 0)
        filters_html += f'<button class="filter-btn" onclick="filterCards(\'{pt}\')">{esc(pt)}<span class="count">{cnt}</span></button>'

    all_cards = ""
    for p in products:
        all_cards += make_product_card(p, with_compare=True)

    catalog_html = f"""<div class="section-hd"><h2>📋 Full Catalog</h2></div>
<div class="filters-bar">{filters_html}</div>
<div class="grid" id="catalog-grid">{all_cards}</div>"""

    # ─── Compare Bar ───
    compare_bar = """<div class="compare-bar" id="compare-bar">
  <span class="sel"><strong id="compare-count">0</strong> selected</span>
  <button class="compare-btn" id="compare-btn" disabled onclick="doCompare()">Compare</button>
  <button class="compare-clear" onclick="clearCompare()">Clear</button>
</div>"""

    content = hero + auth + featured_html + trending_html + new_html + bench_html + guides_html + catalog_html + compare_bar

    # Scripts
    scripts = """<script>
var searchResults={search_json};

// ─── Compare ───
var selected = [];
function toggleCompare(cb) {
  var slug = cb.value;
  if (cb.checked && !selected.includes(slug)) selected.push(slug);
  else selected = selected.filter(function(s) { return s !== slug; });
  updateCompareBar();
}
function updateCompareBar() {
  var bar = document.getElementById('compare-bar');
  var cnt = document.getElementById('compare-count');
  var btn = document.getElementById('compare-btn');
  cnt.textContent = selected.length;
  bar.classList.toggle('active', selected.length > 0);
  btn.disabled = selected.length < 2;
}
function doCompare() {
  if (selected.length >= 2) {
    window.location = '/compare/?slugs=' + selected.join(',');
  }
}
function clearCompare() {
  selected = [];
  document.querySelectorAll('.card input[type=checkbox]').forEach(function(cb) { cb.checked = false; });
  updateCompareBar();
}

// ─── Filter ───
function filterCards(type) {
  document.querySelectorAll('.filter-btn').forEach(function(b) { b.classList.remove('active'); });
  event.target.classList.add('active');
  var grid = document.getElementById('catalog-grid');
  var cards = grid.querySelectorAll('.card');
  cards.forEach(function(card) {
    var badge = card.querySelector('.card-badge');
    if (!badge) return;
    var pt = badge.textContent.trim().toLowerCase();
    if (type === 'all') { card.style.display = ''; return; }
    card.style.display = pt === type.toLowerCase() ? '' : 'none';
  });
}

// ─── Search ───
function debounceSearch(v){clearTimeout(this._t);this._t=setTimeout(function(){doSearch(v)},300)}
function doSearch(v){
  if(!v){window.location='/'}else{
    v=v.toLowerCase();
    var found=searchResults.filter(function(p){return p.t.indexOf(v)>=0||p.d.indexOf(v)>=0||p.pt.indexOf(v)>=0});
    var html='';
    if(found.length===0){html='<div class=\\'empty\\'><h2>Nothing found</h2><p>Try a different query</p></div>'}
    else{html='<div class=\\'grid\\'>';
    found.forEach(function(p){html+='<a href=\\''+p.u+'\\' class=\\'card\\'><div class=\\'card-top\\'>'+p.img+'<span class=\\'card-badge badge-'+p.pt+'\\'>'+p.ptl+'</span></div><div class=\\'card-title\\'>'+p.ti+'</div><div class=\\'card-desc\\'>'+p.d+'</div><div class=\\'card-panel\\'>'+p.panel+'</div><div class=\\'card-trust\\'>'+p.trust+'</div></a>'});
    html+='</div>'}
    // Replace grid content
    var container = document.querySelector('#catalog-grid') || document.querySelector('.grid');
    if(container) container.innerHTML=html;
  }
}
document.getElementById('search')?.focus()

// ─── Live Timestamps ───
function updateTimeAgo(){
  var now=new Date();
  document.querySelectorAll('.time-ago').forEach(function(el){
    var iso=el.getAttribute('data-iso');
    if(!iso)return;
    var dt=new Date(iso);
    var diff=Math.floor((now-dt)/1000);
    var txt='';
    if(diff<60)txt='just now';
    else if(diff<3600)txt=Math.floor(diff/60)+'m ago';
    else if(diff<86400)txt=Math.floor(diff/3600)+'h ago';
    else txt=Math.floor(diff/86400)+'d ago';
    el.innerHTML='🕐 '+txt;
  });
}
updateTimeAgo();
setInterval(updateTimeAgo,60000);

// ─── Bookmark / Save ───
function getSaved(){try{return JSON.parse(localStorage.getItem('qantcore_saved')||'[]')}catch(e){return[]}}
function saveSlug(slug){
  var s=getSaved();if(!s.includes(slug)){s.push(slug);localStorage.setItem('qantcore_saved',JSON.stringify(s))}
  document.querySelectorAll('.bookmark-btn').forEach(function(b){if(b.getAttribute('data-slug')===slug)b.classList.add('saved')});
  var nav=document.querySelector('.saved-nav');if(nav)nav.style.display='inline';
}
function unsaveSlug(slug){
  var s=getSaved().filter(function(x){return x!==slug});localStorage.setItem('qantcore_saved',JSON.stringify(s));
  document.querySelectorAll('.bookmark-btn').forEach(function(b){if(b.getAttribute('data-slug')===slug)b.classList.remove('saved')});
  if(getSaved().length===0){var nav=document.querySelector('.saved-nav');if(nav)nav.style.display='none'}
}
function toggleSave(el,slug){
  if(getSaved().includes(slug))unsaveSlug(slug);else saveSlug(slug);
}
function showSaved(){
  var saved=getSaved();var all=document.querySelectorAll('#catalog-grid .card, .grid .card');
  all.forEach(function(c){c.style.display=''});
  if(saved.length>0){
    all.forEach(function(c){
      var a=c.querySelector('a')||c;var href=c.getAttribute('href')||'';
      var slug=href.replace('/product/','').replace('/','');
      if(!saved.includes(slug))c.style.display='none';
    });
    document.querySelectorAll('.filter-btn').forEach(function(b){b.classList.remove('active')});
  }
}
// Init bookmarks on load
document.querySelectorAll('.bookmark-btn').forEach(function(b){
  if(getSaved().includes(b.getAttribute('data-slug')))b.classList.add('saved');
});
if(getSaved().length>0){var nav=document.querySelector('.saved-nav');if(nav)nav.style.display='inline'}
</script>"""

    search_json = build_search_index()
    scripts = scripts.replace("{search_json}", json.dumps(search_json))

    html = render_page("AI Agents Catalog", "Discover, compare and deploy AI agents. {}+ frameworks tracked, deep technical reviews, live benchmarks.".format(tp),
                       content, scripts=scripts, total=tp, active_home="active")

    write_html(f"{OUT}/index.html", html)
    print(f"  /index.html")


def generate_compare_page(slugs=None):
    """Generate /compare/ — client-side comparison from URL params."""
    # Always generate the dynamic compare page that reads ?slugs= from URL
    all_prods = list(DB.articles.find({"category": "product"}).sort("rating", -1))
    
    # Build search JSON with full product data for client-side comparison
    compare_entries = []
    for p in all_prods:
        compare_entries.append({
            "slug": p["slug"],
            "title": p.get("title",""),
            "rating": p.get("rating",""),
            "pricing": format_price(p.get("pricing_model","")),
            "type": p.get("product_type",""),
            "category": p.get("subcategory","") or "—",
            "maturity": "Enterprise" if (p.get("rating",0) or 0) >= 4.5 and (p.get("review_count",0) or 0) > 500 else "Production" if (p.get("rating",0) or 0) >= 4.0 else "Growing",
            "freshness": f'{int((p.get("freshness_score",0) or 0)*100)}%',
            "reviews": str(p.get("review_count",0) or 0),
            "tech_stack": ", ".join((p.get("tech_stack",[]) or [])[:5]) or "—",
            "deployment": "🏠 Local" if (p.get("local_first") or any(t.lower() in ["docker","local","self-hosted","python","cli","terminal"] for t in (p.get("tech_stack",[]) or []))) else "☁️ Cloud",
            "description": (p.get("tagline","") or p.get("description",""))[:150],
        })
    compare_json = json.dumps(compare_entries)
    
    # Body: selector grid if no slugs, or client-rendered table
    cards = '<div class="grid" id="compare-select-grid">'
    for p in all_prods:
        cards += make_product_card(p, with_compare=True)
    cards += '</div>'
    
    body = f"""<div class="container" id="compare-root">
  <div id="compare-selector">
    <div class="section-hd"><h2>Compare AI Agents</h2></div>
    <p style="color:var(--muted);font-size:14px;margin-bottom:20px">Select 2–5 agents to compare side-by-side</p>
    <div class="filters-bar">
      <span class="label">Filter:</span>
      <button class="filter-btn active" onclick="filterCards('all')">All</button>
      <button class="filter-btn" onclick="filterCards('agent')">Agent</button>
      <button class="filter-btn" onclick="filterCards('framework')">Framework</button>
      <button class="filter-btn" onclick="filterCards('platform')">Platform</button>
      <button class="filter-btn" onclick="filterCards('infrastructure')">Infra</button>
      <button class="filter-btn" onclick="filterCards('model')">Model</button>
    </div>
    {cards}
    <div class="compare-bar active" id="compare-bar">
      <span class="sel"><strong id="compare-count">0</strong> selected</span>
      <button class="compare-btn" id="compare-btn" disabled onclick="doCompare()">Compare Now</button>
      <button class="compare-clear" onclick="clearCompare()">Clear</button>
    </div>
  </div>
  <div id="compare-result" style="display:none"></div>
</div>"""
    
    tp = DB.articles.count_documents({"category": "product"})
    scripts = f"""<script>
var PRODUCTS = {compare_json};
var selected = [];
var currentSlugs = [];

// Init from URL
(function() {{
  var params = new URLSearchParams(window.location.search);
  var slugs = params.get('slugs');
  if (slugs) {{
    currentSlugs = slugs.split(',');
    renderComparison(currentSlugs);
    return;
  }}
}})();

function toggleCompare(cb) {{
  var s = cb.value;
  if (cb.checked && !selected.includes(s)) selected.push(s);
  else selected = selected.filter(function(x) {{ return x !== s; }});
  updateCompareBar();
}}
function updateCompareBar() {{
  var cnt = document.getElementById('compare-count');
  var btn = document.getElementById('compare-btn');
  cnt.textContent = selected.length;
  btn.disabled = selected.length < 2;
}}
function doCompare() {{
  if (selected.length >= 2) {{
    var slugs = selected.join(',');
    history.pushState(null, '', '/compare/?slugs=' + slugs);
    currentSlugs = selected.slice();
    renderComparison(currentSlugs);
  }}
}}
function clearCompare() {{
  selected = [];
  document.querySelectorAll('#compare-select-grid input[type=checkbox]').forEach(function(cb) {{ cb.checked = false; }});
  updateCompareBar();
}}
function renderComparison(slugs) {{
  var prods = slugs.map(function(s) {{
    return PRODUCTS.find(function(p) {{ return p.slug === s; }});
  }}).filter(Boolean);
  if (prods.length < 2) return;
  
  document.getElementById('compare-selector').style.display = 'none';
  var result = document.getElementById('compare-result');
  result.style.display = 'block';
  
  var metrics = [
    ['Rating', 'rating', true],
    ['Pricing', 'pricing', false],
    ['Type', 'type', false],
    ['Category', 'category', false],
    ['Maturity', 'maturity', false],
    ['Deployment', 'deployment', false],
    ['Freshness', 'freshness', false],
    ['Reviews', 'reviews', false],
    ['Tech Stack', 'tech_stack', false],
  ];
  
  var header = '<tr><th></th>' + prods.map(function(p) {{ return '<th>' + p.title.substring(0,22) + '</th>'; }}).join('') + '</tr>';
  var rows = '';
  metrics.forEach(function(m) {{
    var name = m[0], key = m[1], isWinner = m[2];
    var vals = prods.map(function(p) {{ return p[key] || '—'; }});
    var winner = -1;
    if (isWinner) {{
      var nums = vals.map(function(v) {{ return parseFloat(v) || 0; }});
      winner = nums.indexOf(Math.max.apply(null, nums));
    }}
    rows += '<tr><th>' + name + '</th>';
    vals.forEach(function(v, i) {{
      rows += '<td class=\"' + (i === winner ? 'winner' : '') + '\">' + v + '</td>';
    }});
    rows += '</tr>';
  }});
  
  var html = '<div class=\"breadcrumbs\"><a href=\"/\">Catalog</a> &rsaquo; <a href=\"/compare/\" onclick=\"resetCompare();return false\">Compare</a> &rsaquo; <span>Result</span></div>';
  html += '<h1 style=\"font-size:24px;font-weight:800;color:#f1f5f9;margin-bottom:24px\">' + prods.map(function(p) {{ return p.title.substring(0,25); }}).join(' vs ') + '</h1>';
  html += '<div class=\"compare-table-wrap\"><table class=\"compare-table\">' + header + rows + '</table></div>';
  html += '<p style=\"color:var(--muted);font-size:12px;margin-top:16px\"><span class=\"compare-check\">✓</span> Green = best-in-class. <a href=\"/methodology/\" style=\"color:var(--green)\">How we score →</a></p>';
  html += '<button onclick=\"resetCompare()\" style=\"margin-top:20px;padding:10px 20px;border-radius:6px;background:var(--card-bg);color:var(--text);border:1px solid var(--border);cursor:pointer;font-size:13px\">← Back to selection</button>';
  result.innerHTML = html;
  window.scrollTo(0, 0);
}}
function resetCompare() {{
  document.getElementById('compare-selector').style.display = 'block';
  document.getElementById('compare-result').style.display = 'none';
  history.pushState(null, '', '/compare/');
  currentSlugs = [];
}}
// Filter
function filterCards(type) {{
  document.querySelectorAll('.filter-btn').forEach(function(b) {{ b.classList.remove('active'); }});
  event.target.classList.add('active');
  document.querySelectorAll('#compare-select-grid .card').forEach(function(card) {{
    var cb = card.querySelector('.card-badge');
    if (!cb) return;
    var pt = cb.className.replace('badge-','');
    card.style.display = (type === 'all' || pt === type) ? '' : 'none';
  }});
}}
</script>"""
    
    html = render_page("Compare AI Agents", "Select and compare AI agents side-by-side — ratings, pricing, deployment, maturity, and more.",
                       body, scripts=scripts, total=tp, active_compare="active")
    write_html(f"{OUT}/compare/index.html", html)
    print(f"  /compare/index.html (client-side, {len(all_prods)} products)")


def generate_catalog(category):
    """Generate /catalog/{category}/index.html"""
    labels = {"product": "Products", "comparison": "Comparisons", "review": "Reviews"}
    label = labels.get(category, category)

    items = list(DB.articles.find({"category": category}))
    tp = DB.articles.count_documents({"category": "product"})

    if not items:
        cards = f'<div class="empty"><h2>Nothing here yet</h2><p>Category «{esc(label)}» is empty</p></div>'
    else:
        cards = '<div class="grid">'
        for item in items:
            if category == "product":
                cards += make_product_card(item, with_compare=False)
            elif category == "comparison":
                cards += f"""<a href="/compare/{item['slug']}/" class="card">
                  <div class="card-top">
                    <div class="card-icon">⚖️</div>
                    <span class="card-badge badge-framework">VS</span>
                  </div>
                  <div class="card-title">{esc(item.get('title',''))}</div>
                  <div class="card-desc">{esc(str(item.get('description',''))[:120])}</div>
                </a>"""
            elif category == "review":
                cards += f"""<a href="/review/{item['slug']}/" class="card">
                  <div class="card-top">
                    <div class="card-icon">📝</div>
                    <span class="card-badge badge-agent">{item.get('word_count',0)} words</span>
                  </div>
                  <div class="card-title">{esc(item.get('title',''))}</div>
                  <div class="card-desc">{esc(str(item.get('tagline',''))[:100])}</div>
                </a>"""
        cards += "</div>"

    active_home = "active" if category == "product" else ""
    active_compare = "active" if category == "comparison" else ""
    active_review = "active" if category == "review" else ""

    body = f"""<div class="container">
  <h2 style="font-size:22px;font-weight:700;color:#f1f5f9;margin-bottom:20px">{esc(label)}</h2>
  {cards}
</div>"""

    search_json = build_search_index() if category == "product" else "[]"
    html = render_page(label, f"Qantcore — {label} of AI agents", body,
                       total=tp, search_json=search_json,
                       active_home=active_home, active_compare=active_compare, active_review=active_review)

    write_html(f"{OUT}/catalog/{category}/index.html", html)
    print(f"  /catalog/{category}/index.html")


def generate_product(slug, p):
    """Generate /product/{slug}/index.html"""
    comparisons = list(DB.articles.find(
        {"category": "comparison", "$or": [{"product_a": slug}, {"product_b": slug}]}).limit(5))
    reviews = list(DB.articles.find({"category": "review", "review_of": slug}).limit(3))

    comp_links = ""
    if comparisons:
        comp_links = '<div style="margin-top:20px"><h3 style="color:var(--green);font-size:14px;margin-bottom:10px">Comparisons</h3><div class="grid">'
        for c in comparisons:
            comp_links += f"""<a href="/compare/{c['slug']}/" class="card">
              <div class="card-title">{esc(c.get('title',''))}</div>
              <div class="card-desc">{esc(str(c.get('description',''))[:120])}</div>
            </a>"""
        comp_links += "</div></div>"

    review_links = ""
    if reviews:
        review_links = '<div style="margin-top:20px"><h3 style="color:var(--green);font-size:14px;margin-bottom:10px">Reviews</h3>'
        for r in reviews:
            review_links += f"""<a href="/review/{r['slug']}/" class="card" style="display:block;margin-bottom:12px">
              <div class="card-title">{esc(r.get('title',''))}</div>
              <div class="card-desc">{esc(r.get('tagline',''))} · {r.get('word_count',0)} words</div>
            </a>"""
        review_links += "</div>"

    rating_html = f'<div class="meta-item green">⭐ <strong>{p.get("rating","")}</strong> / 5</div>' if p.get('rating') else ''
    website_html = f'<a href="{p.get("website_url","")}" class="meta-item" target="_blank" rel="noopener">🔗 Website</a>' if p.get('website_url') else ''

    # Intelligence stats
    intel_html = ""
    intel_items = []
    if p.get("freshness_score"):
        intel_items.append(f'<div class="stat-mini"><div class="sv">{int(float(p["freshness_score"])*100)}%</div><div class="sl">Freshness</div></div>')
    if p.get("review_count"):
        intel_items.append(f'<div class="stat-mini"><div class="sv">{p["review_count"]}</div><div class="sl">Reviews</div></div>')
    if p.get("tech_stack"):
        intel_items.append(f'<div class="stat-mini"><div class="sv">{len(p["tech_stack"])}</div><div class="sl">Tech stack</div></div>')
    if intel_items:
        intel_html = f'<div class="stats-mini">{"".join(intel_items)}</div>'

    body = f"""<div class="container detail">
      <div class="breadcrumbs">
        <a href="/">Catalog</a> &rsaquo; <span>{esc(p.get('title',''))}</span>
      </div>
      <div class="detail-header" style="display:flex;gap:24px;align-items:flex-start">
        {product_image(p, 'detail')}
        <div style="flex:1">
          <h1>{esc(p.get('title',''))}</h1>
          <p class="tagline">{esc(p.get('tagline',''))}</p>
          <div class="detail-meta">
            <div class="meta-item">{icon_for(p.get('product_type',''))} <strong>{esc(p.get('product_type',''))}</strong></div>
            {rating_html}
            <div class="meta-item">💰 <strong>{format_price(p.get('pricing_model',''))}</strong></div>
            {website_html}
          </div>
          {intel_html}
        </div>
      </div>
      <div class="detail-body">
        <p style="font-size:15px;color:#b0b8c8">{esc(p.get('description',''))}</p>
        {comp_links}
        {review_links}
      </div>
    </div>"""

    total = DB.articles.count_documents({"category": "product"})
    desc = esc((p.get('tagline','') or p.get('description',''))[:160])
    html = render_page(esc(p.get('title','')), desc, body,
                       total=total, active_home="active",
                       open_graph=p.get('open_graph',''), schema_org=p.get('schema_org','{}'))

    write_html(f"{OUT}/product/{slug}/index.html", html)


def generate_compare(slug, c):
    """Generate /compare/{slug}/index.html"""
    body_html = c.get("body", "").replace("\n", "<br>") if c.get("body") else c.get("description", "")
    links = ""
    prod_images = ""
    for pa in ["product_a", "product_b"]:
        sv = c.get(pa, "")
        if sv:
            prod = DB.articles.find_one({"slug": sv, "category": "product"})
            if prod:
                links += f'<a href="/product/{sv}/" class="meta-item">🔗 {esc(prod.get("title","")[:40])}</a>'
                pi = product_image(prod, "icon")
                prod_images += f'<div style="text-align:center">{pi}<div style="font-size:12px;color:var(--muted);margin-top:6px">{esc(prod.get("title","")[:30])}</div></div>'

    body = f"""<div class="container detail">
      <div class="breadcrumbs">
        <a href="/">Catalog</a> &rsaquo; <a href="/catalog/comparison/">Compare</a> &rsaquo; <span>{esc(c.get('title',''))}</span>
      </div>
      <div class="detail-header">
        <h1>{esc(c.get('title',''))}</h1>
        <div style="display:flex;gap:32px;align-items:center;justify-content:center;margin:24px 0">
          {prod_images}
        </div>
        <div class="detail-meta">{links}</div>
      </div>
      <div class="detail-body">{body_html}</div>
    </div>"""

    total = DB.articles.count_documents({"category": "product"})
    html = render_page(esc(c.get('title','')), esc(str(c.get('description',''))[:160]),
                       body, total=total, active_compare="active",
                       open_graph=c.get('open_graph',''), schema_org=c.get('schema_org','{}'))

    write_html(f"{OUT}/compare/{slug}/index.html", html)


def generate_review(slug, r):
    """Generate /review/{slug}/index.html"""
    body_html = r.get("body", "").replace("\n", "<br>") if r.get("body") else ""
    if r.get("body_html"):
        body_html = r["body_html"]

    prod_link = ""
    prod_image_html = ""
    if r.get("review_of"):
        prod = DB.articles.find_one({"slug": r["review_of"], "category": "product"})
        if prod:
            prod_link = f'<a href="/product/{r["review_of"]}/" class="meta-item">🔗 {esc(prod.get("title","")[:40])}</a>'
            prod_image_html = product_image(prod, "icon")

    wc_html = f'<div class="meta-item">📝 {r.get("word_count",0)} words</div>' if r.get('word_count') else ''

    body = f"""<div class="container detail">
      <div class="breadcrumbs">
        <a href="/">Catalog</a> &rsaquo; <a href="/catalog/review/">Reviews</a> &rsaquo; <span>{esc(r.get('title',''))}</span>
      </div>
      <div class="detail-header" style="display:flex;gap:24px;align-items:flex-start">
        {prod_image_html}
        <div style="flex:1">
          <h1>{esc(r.get('title',''))}</h1>
          <p class="tagline">{esc(r.get('tagline',''))}</p>
          <div class="detail-meta">
            {prod_link}
            {wc_html}
          </div>
        </div>
      </div>
      <div class="detail-body">{body_html}</div>
    </div>"""

    total = DB.articles.count_documents({"category": "product"})
    html = render_page(esc(r.get('title','')), esc(str(r.get('tagline','') or r.get('description',''))[:160]),
                       body, total=total, active_review="active",
                       open_graph=r.get('open_graph',''), schema_org=r.get('schema_org','{}'))

    write_html(f"{OUT}/review/{slug}/index.html", html)


def generate_stack_builder():
    """Generate /stack-builder/ — interactive AI stack assembly tool."""
    products = list(DB.articles.find({"category": "product"}))
    tp = DB.articles.count_documents({"category": "product"})

    # Categorize products into stack layers
    layers = {
        "LLM": [],
        "Memory": [],
        "Tools": [],
        "Orchestration": [],
        "Vector DB": [],
    }

    for p in products:
        sc = (p.get("subcategory","") or "").lower()
        pt = (p.get("product_type","") or "").lower()
        title = (p.get("title","") or "").lower()
        tagline = (p.get("tagline","") or "").lower()

        if any(kw in title + tagline for kw in ["llm","model","gpt","claude","gemini","deepseek","language model"]):
            layers["LLM"].append(p)
        elif any(kw in sc + title + tagline for kw in ["memory","storage","vector","database","db","embedding"]):
            if "vector" in title + tagline + sc or "embedding" in title + tagline:
                layers["Vector DB"].append(p)
            else:
                layers["Memory"].append(p)
        elif any(kw in sc + title + tagline for kw in ["tool","function","api","plugin","action","integration","mcp"]):
            layers["Tools"].append(p)
        elif any(kw in sc + title + tagline for kw in ["orchestrat","workflow","multi-agent","pipeline","crew","swarm"]):
            layers["Orchestration"].append(p)
        elif pt in ["platform","infrastructure"]:
            layers["Orchestration"].append(p)

    # Fill empty layers with top-rated products
    for key in layers:
        if not layers[key]:
            layers[key] = sorted(products, key=lambda p: p.get("rating", 0) or 0, reverse=True)[:4]

    # Limit each layer to 6
    for key in layers:
        layers[key] = layers[key][:6]

    # Build slot HTML
    slots_html = ""
    for layer_name, prods in layers.items():
        options = ""
        for p in prods:
            rating = p.get("rating", "")
            cost = format_price(p.get("pricing_model", ""))
            options += f'<option value="{p["slug"]}" data-cost="{cost}" data-rating="{rating}" data-complexity="{len(p.get("tech_stack",[]))}">{esc(p.get("title","")[:40])} ({cost})</option>'
        slots_html += f"""<div class="stack-slot" id="slot-{layer_name.lower().replace(' ','-')}">
  <div class="ss-label">{layer_name}</div>
  <select onchange="updateSlot(this, '{layer_name}')" style="width:100%;padding:8px;border-radius:6px;background:var(--card-bg);color:var(--text);border:1px solid var(--border);font-size:13px;margin-top:8px">
    <option value="">— Select —</option>
    {options}
  </select>
</div>"""

    body = f"""<div class="container">
  <div class="breadcrumbs"><a href="/">Catalog</a> &rsaquo; <span>Stack Builder</span></div>
  <div class="stack-builder" style="padding:0">
    <div class="stack-inner">
      <h2>🧩 AI Stack Builder</h2>
      <p class="stack-sub">Assemble your AI agent infrastructure. Select components for each layer to estimate compatibility, cost, and deployment complexity.</p>
      <div class="stack-slots">{slots_html}</div>
      <div class="stack-result" id="stack-result">
        <h3>Stack Analysis</h3>
        <div class="stack-metrics" id="stack-metrics"></div>
      </div>
    </div>
  </div>
</div>"""

    scripts = """<script>
function updateSlot(sel, layer) {
  var slot = sel.closest('.stack-slot');
  if (sel.value) {
    slot.classList.add('filled');
    slot.querySelector('.ss-value') && (slot.querySelector('.ss-value').textContent = sel.options[sel.selectedIndex].text);
  } else {
    slot.classList.remove('filled');
  }
  analyzeStack();
}
function analyzeStack() {
  var selects = document.querySelectorAll('.stack-slot select');
  var total = 0, count = 0, cost = 0, complexity = 0;
  var costs = [], ratings = [];
  selects.forEach(function(s) {
    if (s.value) {
      count++;
      var opt = s.options[s.selectedIndex];
      var c = opt.dataset.cost;
      var r = parseFloat(opt.dataset.rating) || 0;
      var cx = parseInt(opt.dataset.complexity) || 0;
      ratings.push(r);
      complexity += cx;
      if (c === 'Freemium' || c === 'Open Source') cost += 0;
      else if (c === 'Usage-based') cost += 30;
      else cost += 50;
    }
  });
  var result = document.getElementById('stack-result');
  var metrics = document.getElementById('stack-metrics');
  if (count >= 3) {
    result.classList.add('active');
    var avgRating = ratings.length ? (ratings.reduce(function(a,b){return a+b},0)/ratings.length).toFixed(1) : '—';
    var deployDiff = complexity <= 6 ? '🟢 Low' : complexity <= 12 ? '🟡 Medium' : '🔴 High';
    metrics.innerHTML =
      '<div class="stack-metric"><div class="sm-val">' + count + '/5</div><div class="sm-lbl">Layers configured</div></div>' +
      '<div class="stack-metric"><div class="sm-val">$' + cost + '/mo</div><div class="sm-lbl">Est. monthly cost</div></div>' +
      '<div class="stack-metric"><div class="sm-val">' + avgRating + ' ★</div><div class="sm-lbl">Avg. rating</div></div>' +
      '<div class="stack-metric"><div class="sm-val">' + deployDiff + '</div><div class="sm-lbl">Deploy complexity</div></div>';
  } else {
    result.classList.remove('active');
  }
}
</script>"""

    html = render_page("AI Stack Builder", "Assemble your AI agent stack — LLM, memory, tools, orchestration. Estimate cost and complexity.",
                       body, scripts=scripts, total=tp)
    write_html(f"{OUT}/stack-builder/index.html", html)
    print(f"  /stack-builder/index.html")


def write_html(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_methodology():
    """Generate /methodology/ — trust framework: how we score, rank, and verify."""
    tp = DB.articles.count_documents({"category": "product"})
    tc = DB.articles.count_documents({"category": "comparison"})
    
    body = """<div class="container detail">
  <div class="breadcrumbs"><a href="/">Catalog</a> &rsaquo; <span>Methodology</span></div>
  <h1 style="font-size:28px;font-weight:800;color:#f1f5f9;margin:24px 0 8px">How We Score &amp; Rank AI Agents</h1>
  <p style="color:var(--muted);font-size:15px;line-height:1.7;max-width:760px">Qantcore evaluates AI agents using a transparent, multi-dimensional framework. No black-box scores, no sponsored rankings.</p>
  
  <div style="margin-top:32px;display:grid;gap:20px">
    
    <div class="method-card">
      <h2>1. Rating (★ 1–5)</h2>
      <p>Composite score from: documentation quality, community activity, release cadence, API stability, and user reviews. Minimum 3 data sources required before a rating is published. Confidence interval shown when available.</p>
    </div>
    
    <div class="method-card">
      <h2>2. Maturity Classification</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-top:12px">
        <div><strong style="color:var(--green)">Enterprise</strong> — 4.5★+, 500+ reviews, production deployments at scale</div>
        <div><strong style="color:var(--blue)">Production</strong> — 4.0★+, active community, documented use cases</div>
        <div><strong style="color:var(--amber)">Growing</strong> — 3.0★+, regular updates, growing adoption</div>
        <div><strong style="color:var(--muted)">New</strong> — recently launched, data still accumulating</div>
      </div>
    </div>
    
    <div class="method-card">
      <h2>3. Freshness Score (0–100%)</h2>
      <p>Calculated from: last release date, commit frequency, documentation updates, community response time. Above 80% = actively maintained. Below 30% = stale — flagged for review.</p>
    </div>
    
    <div class="method-card">
      <h2>4. Velocity Signal</h2>
      <p>↑↑ = accelerating (freshness > 80%, weekly releases) · ↑ = growing (freshness > 60%) · → = stable · ↓ = declining (freshness < 30%, no recent updates)</p>
    </div>
    
    <div class="method-card">
      <h2>5. Deployment Intelligence</h2>
      <p><strong>Local</strong> = runs on your hardware (Docker, Python CLI, self-hosted). <strong>Cloud</strong> = SaaS-only, requires vendor infrastructure. Hybrid solutions flagged where applicable.</p>
    </div>
    
    <div class="method-card">
      <h2>6. Comparison Methodology</h2>
      <p>Head-to-head comparisons use 9 standardized metrics. Green highlights indicate best-in-class per metric. All data is refreshed daily from official sources, documentation, and community feedback. No AI-generated scores — every rating is traceable to a data source.</p>
    </div>
    
    <div class="method-card">
      <h2>7. Data Freshness</h2>
      <p>Catalog updated daily. Each card shows last-updated timestamp. Stale entries (30+ days without update) are flagged. Our pipeline runs automated checks every 24 hours.</p>
    </div>
    
  </div>
  
  <div style="margin-top:40px;padding:24px;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius)">
    <h3 style="color:var(--green);font-size:16px;margin-bottom:8px">Why Qantcore vs alternatives</h3>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-top:16px;font-size:13px;color:var(--muted);line-height:1.6">
      <div><strong style="color:var(--text)">Technical depth</strong><br>Engineer-grade analysis, not marketing copy. We test deployment, not just features.</div>
      <div><strong style="color:var(--text)">Deployment intelligence</strong><br>Local vs cloud, Docker readiness, infrastructure requirements — what you need to actually run it.</div>
      <div><strong style="color:var(--text)">Framework-first</strong><br>Organized by what matters: orchestration depth, memory model, tool-calling, extensibility.</div>
      <div><strong style="color:var(--text)">Transparent methodology</strong><br>Every score traceable. No black-box rankings. No sponsored placements.</div>
    </div>
  </div>
</div>
<style>
.method-card{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px 24px}
.method-card h2{font-size:15px;font-weight:700;color:var(--green);margin-bottom:8px;letter-spacing:-.01em}
.method-card p{font-size:13px;color:var(--muted);line-height:1.7}
</style>"""
    
    html = render_page("Methodology — How We Score AI Agents", 
                       "Transparent evaluation framework: how Qantcore rates, ranks, and compares AI agents. No black-box scores.",
                       body, total=tp)
    write_html(f"{OUT}/methodology/index.html", html)
    print(f"  /methodology/index.html")


# ─── Main ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import shutil

    # Clean output dir
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    # Copy images
    images_src = "/opt/data/www/qantcore/images"
    images_dst = f"{OUT}/images"
    if os.path.exists(images_src):
        shutil.copytree(images_src, images_dst, dirs_exist_ok=True)
        print("Copied images/")

    # Generate
    print("\nGenerating static pages...\n")

    generate_home()

    # Multi-compare page
    generate_compare_page()

    # Methodology
    generate_methodology()

    for cat in ["product", "comparison", "review"]:
        generate_catalog(cat)

    # Product pages
    products = list(DB.articles.find({"category": "product"}))
    for p in products:
        generate_product(p["slug"], p)
    print(f"  /product/* ({len(products)} pages)")

    # Stack Builder
    generate_stack_builder()

    # Comparison pages
    comparisons = list(DB.articles.find({"category": "comparison"}))
    for c in comparisons:
        generate_compare(c["slug"], c)
    if comparisons:
        print(f"  /compare/* ({len(comparisons)} pages)")

    # Review pages
    reviews = list(DB.articles.find({"category": "review"}))
    for r in reviews:
        generate_review(r["slug"], r)
    if reviews:
        print(f"  /review/* ({len(reviews)} pages)")

    # Sitemap
    sitemap_src = "/opt/data/www/qantcore/sitemap.xml"
    if os.path.exists(sitemap_src):
        shutil.copy2(sitemap_src, f"{OUT}/sitemap.xml")
        print("  /sitemap.xml")

    # Robots.txt
    with open(f"{OUT}/robots.txt", "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://qantcore.space/sitemap.xml\n")
    print("  /robots.txt")

    print(f"\nDone! Static site in {OUT}/")
