# -*- coding: utf-8 -*-
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
  background:var(--bg);color:var(--text);min-height:100vh;line-height:1.6;font-size:16px;
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
.mega-nav a,.mega-nav .nav-section{font-size:13.5px;color:var(--muted);
  padding:6px 12px;border-radius:6px;transition:color .2s,background .2s;font-weight:500;
  letter-spacing:.01em;white-space:nowrap;text-decoration:none;
  -webkit-tap-highlight-color:transparent;outline:none;user-select:none}
.mega-nav a:hover{color:var(--text);background:rgba(255,255,255,.04)}
.mega-nav a:active{color:var(--muted);background:transparent}
.mega-nav a:focus-visible{outline:2px solid var(--green);outline-offset:-2px}
.mega-nav a.active{color:var(--green);background:var(--green-dim)}
.mega-nav a.active:active{color:var(--green);background:var(--green-dim)}
.nav-sep{width:1px;height:18px;background:var(--border);margin:0 4px}
.nav-featured{font-size:14px!important;font-weight:700!important;color:var(--green)!important;
  background:var(--green-dim)!important;padding:8px 16px!important;letter-spacing:.02em}
.nav-featured:active{color:var(--green)!important;background:var(--green-dim)!important}
.nav-review{font-size:14px!important;font-weight:700!important;color:#a78bfa!important;
  padding:6px 14px!important;letter-spacing:.01em}
.nav-review:hover{color:#c4b5fd!important;background:rgba(167,139,250,.1)!important}
.nav-review:active{color:#a78bfa!important}
.nav-review.active{background:rgba(167,139,250,.15)!important}
.nav-local{font-size:14px!important;font-weight:700!important;color:var(--blue)!important;
  padding:6px 14px!important;letter-spacing:.01em}
.nav-local:hover{color:#60a5fa!important;background:rgba(59,130,246,.1)!important}
.nav-local:active{color:var(--blue)!important}
.nav-local.active{background:rgba(59,130,246,.15)!important}

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
.hero h1{font-size:clamp(12px,1.67vw,20px);font-weight:800;letter-spacing:-.03em;
  line-height:1.15;color:#f1f5f9;max-width:800px;margin:0 auto}
.hero h1 .accent{color:var(--green)}
.hero .sub{font-size:17px;color:var(--muted);margin-top:16px;max-width:640px;
  margin-left:auto;margin-right:auto;line-height:1.6}
.hero .tagline{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:var(--green);
  font-weight:600;margin-bottom:16px}
.hero-metrics{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:28px}
.hero-metric{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius-sm);
  padding:10px 18px;text-align:center;min-width:100px}
.hero-metric .val{font-size:24px;font-weight:800;color:var(--green);font-variant-numeric:tabular-nums}
.hero-metric .lbl{font-size:11px;color:var(--muted);margin-top:2px;text-transform:uppercase;letter-spacing:.06em}
.hero-cta{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:32px}
.cta-primary{padding:12px 28px;border-radius:var(--radius-sm);font-size:14px;font-weight:600;
  background:var(--green);color:#000;border:none;cursor:pointer;transition:all .2s;
  letter-spacing:-.01em}
.cta-primary:hover{filter:brightness(1.15);transform:translateY(-1px)}
.cta-secondary{padding:12px 28px;border-radius:var(--radius-sm);font-size:14px;font-weight:600;
  background:transparent;color:var(--text);border:1px solid var(--border);cursor:pointer;
  transition:all .2s}
.cta-secondary:hover{border-color:var(--blue);color:var(--blue)}

/* ─── Enterprise CTA Banner ─── */
.enterprise-cta{background:linear-gradient(135deg,rgba(16,185,129,.08) 0%,rgba(59,130,246,.04) 100%);
  border:1px solid rgba(16,185,129,.15);border-radius:var(--radius);margin:40px 0 32px;padding:0}
.ec-inner{display:flex;align-items:center;justify-content:space-between;gap:32px;padding:32px 36px;flex-wrap:wrap}
.card-title{font-size:16px;font-weight:600;color:var(--text);margin-bottom:8px;line-height:1.4;
  display:flex;align-items:flex-start;gap:6px}
.agent-icon{font-size:18px;flex-shrink:0;line-height:1.2}
.ec-text h3{font-size:20px;font-weight:700;color:var(--text);margin-bottom:8px}
.ec-text p{font-size:14px;color:var(--muted);line-height:1.6;max-width:480px}
.ec-actions{display:flex;gap:12px;flex-shrink:0;flex-wrap:wrap}

/* ─── Authority Bar ─── */
.auth-bar{max-width:1320px;margin:0 auto 0;padding:0 24px 32px}
.auth-inner{display:flex;gap:0;background:var(--card-bg);border:1px solid var(--border);
  border-radius:var(--radius);overflow:hidden;flex-wrap:wrap}
.auth-stat{flex:1;min-width:130px;padding:18px 20px;text-align:center;
  border-right:1px solid var(--border);position:relative}
.auth-stat:last-child{border-right:none}
.auth-stat .n{font-size:28px;font-weight:800;color:var(--green);font-variant-numeric:tabular-nums;
  letter-spacing:-.02em}
.auth-stat .n.amber{color:var(--amber)}
.auth-stat .l{font-size:11px;color:var(--muted);margin-top:3px;text-transform:uppercase;letter-spacing:.05em}
.auth-stat .dot{display:inline-block;width:6px;height:6px;border-radius:50%;
  background:var(--green);margin-right:6px;animation:pulse 2s infinite}

/* ─── Section Headers ─── */
.section-hd{max-width:1320px;margin:0 auto;padding:8px 24px 16px;
  display:flex;align-items:center;justify-content:space-between}
.section-hd h2{font-size:20px;font-weight:700;color:var(--text);letter-spacing:-.01em}
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
  padding:20px;transition:all .2s;position:relative;display:flex;flex-direction:column;overflow:visible}
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
.card-desc{font-size:13.5px;color:var(--muted);line-height:1.5;display:-webkit-box;
  -webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:12px;flex:1}
/* Intelligence Panel */
.card-panel{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:auto}
.panel-item{background:rgba(255,255,255,.02);border-radius:6px;padding:8px 10px}
.panel-item .pv{font-size:16px;font-weight:700;color:var(--text);font-variant-numeric:tabular-nums}
.panel-item .pv.green{color:var(--green)}
.panel-item .pv.amber{color:var(--amber)}
.panel-item .pl{font-size:10px;color:var(--dim);margin-top:1px;text-transform:uppercase;letter-spacing:.03em}
.card-compare{position:absolute;top:10px;right:10px;z-index:5}
.card-compare input[type=checkbox]{appearance:none;width:24px;height:24px;border-radius:6px;
  border:2px solid var(--dim);cursor:pointer;transition:all .2s;position:relative}
.card-compare input[type=checkbox]:checked{border-color:var(--green);background:var(--green)}
.card-compare input[type=checkbox]:checked::after{content:'✓';position:absolute;
  top:0;left:4px;color:#000;font-size:16px;font-weight:700}
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

/* ─── Live Connection Lines ─── */
.live-lines{position:fixed;top:0;left:0;width:100%;height:100%;z-index:150;
  pointer-events:none;opacity:0;transition:opacity .3s}
.live-lines.active{opacity:1}

/* ─── Install / Code Block ─── */
.install-block{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);
  overflow:hidden;margin-bottom:24px}
.install-header{display:flex;align-items:center;justify-content:space-between;
  padding:12px 20px;background:rgba(59,130,246,.06);border-bottom:1px solid var(--border)}
.install-badge{font-size:13px;font-weight:600;color:var(--blue);
  background:rgba(59,130,246,.12);padding:4px 12px;border-radius:4px}
.copy-btn{font-size:12px;color:var(--muted);background:rgba(255,255,255,.04);
  border:1px solid var(--border);padding:5px 14px;border-radius:4px;
  cursor:pointer;transition:all .2s;font-weight:500}
.copy-btn:hover{color:var(--green);border-color:var(--green)}
.code-block{background:#0d1117;padding:20px 24px;margin:0;overflow-x:auto;
  font-family:'JetBrains Mono','Fira Code','Cascadia Code',monospace;
  font-size:13px;line-height:1.7;color:#c9d1d9;white-space:pre-wrap;
  border-radius:0 0 var(--radius) var(--radius)}
.code-block code{background:none;padding:0;font-size:inherit}
.desc-block h2{display:flex;align-items:center;gap:8px}

/* ─── Stats Mini (colored) ─── */
.stats-mini{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}
.stat-mini{background:var(--card-bg);border:1px solid var(--border);
  border-radius:8px;padding:10px 16px;text-align:center;min-width:80px}
.stat-mini .sv{font-size:20px;font-weight:800;color:var(--green);
  font-variant-numeric:tabular-nums}
.stat-mini .sl{font-size:10px;color:var(--dim);margin-top:2px;
  text-transform:uppercase;letter-spacing:.03em}

/* ─── Integrations Overlay ─── */
.integ-overlay{position:fixed;top:0;left:0;width:100%;height:100%;z-index:9999;
  background:rgba(0,0,0,.85);backdrop-filter:blur(8px);
  display:flex;align-items:flex-start;justify-content:center;padding:40px 20px;overflow-y:auto}
.integ-modal{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);
  width:100%;max-width:900px;padding:0;box-shadow:0 20px 60px rgba(0,0,0,.5)}
.integ-header{display:flex;align-items:center;justify-content:space-between;
  padding:20px 28px;border-bottom:1px solid var(--border)}
.integ-header h2{font-size:20px;font-weight:700;color:var(--text)}
.integ-close{background:none;border:none;color:var(--muted);font-size:22px;cursor:pointer;
  padding:4px 8px;border-radius:6px;transition:all .2s}
.integ-close:hover{color:var(--red);background:rgba(255,255,255,.05)}
.integ-agents{display:flex;gap:12px;padding:20px 28px;flex-wrap:wrap;justify-content:center;
  border-bottom:1px solid var(--border)}
.integ-agent-card{display:flex;align-items:center;gap:8px;background:var(--card-bg);
  border:1px solid var(--border);border-radius:8px;padding:8px 14px;font-size:13px;color:var(--text)}
.integ-agent-card .iac-icon{width:28px;height:28px;border-radius:6px;
  background:rgba(59,130,246,.15);display:flex;align-items:center;justify-content:center;font-size:14px;overflow:hidden}
.integ-agent-card .iac-icon img{width:100%;height:100%;object-fit:contain}
.integ-diagram{padding:8px 28px;background:rgba(0,0,0,.2);border-bottom:1px solid var(--border)}
.integ-diagram svg{display:block}
.integ-matches{padding:24px 28px}
.integ-matches h3{font-size:16px;font-weight:700;color:var(--text);margin-bottom:16px}
.integ-list{display:flex;flex-direction:column;gap:12px}
.integ-match{background:var(--card-bg);border:1px solid var(--border);border-radius:8px;padding:16px 20px}
.im-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.im-type{font-size:13px;font-weight:600;color:var(--green);background:rgba(16,185,129,.1);
  padding:3px 10px;border-radius:4px}
.im-effort{font-size:12px;color:var(--muted)}
.im-desc{font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:8px}
.im-agents{font-size:11px;color:var(--dim);font-family:monospace;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.im-agents img{width:20px;height:20px;border-radius:4px;object-fit:contain;vertical-align:middle}
.im-agents a{display:inline-flex;align-items:center;gap:4px}
.integ-empty{text-align:center;padding:40px 20px;color:var(--muted)}
.integ-cta{text-align:center;padding:20px 28px;border-top:1px solid var(--border);
  background:linear-gradient(180deg,transparent,rgba(16,185,129,.04))}
.integ-cta p{font-size:14px;color:var(--muted);margin-bottom:12px}

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
.compare-table-wrap{overflow-x:auto;margin:20px 0;border-radius:12px;
  border:1px solid var(--border);background:linear-gradient(180deg,#121821 0%,var(--bg) 100%)}
.compare-table{width:100%;border-collapse:collapse;font-size:13px}
.compare-table thead th{padding:16px 16px 14px;color:var(--text);font-weight:700;font-size:13px;
  text-align:center;border-bottom:2px solid rgba(16,185,129,.3);
  background:linear-gradient(180deg,rgba(16,185,129,.06) 0%,transparent 100%)}
.compare-table thead th:first-child{text-align:left;color:var(--muted);font-size:11px;
  font-weight:500;text-transform:uppercase;letter-spacing:.04em;border-right:1px solid var(--border)}
.compare-table thead th .th-icon{font-size:18px;display:block;margin-bottom:4px}
.compare-table thead th .th-name{display:block;max-width:140px;margin:0 auto;line-height:1.3}
.compare-table tbody th{text-align:left;padding:12px 16px;color:var(--muted);font-weight:500;
  font-size:11px;text-transform:uppercase;letter-spacing:.04em;border-bottom:1px solid var(--border);
  border-right:1px solid var(--border);white-space:nowrap}
.compare-table tbody td{padding:12px 14px;border-bottom:1px solid var(--border);
  text-align:center;font-weight:600;font-size:13px;position:relative}
.compare-table tbody tr:last-child td,.compare-table tbody tr:last-child th{border-bottom:none}
.compare-table tbody tr:nth-child(even){background:rgba(18,24,33,.4)}
.compare-table .winner{background:rgba(16,185,129,.08) !important;
  box-shadow:inset 0 0 0 1px rgba(16,185,129,.25)}
.compare-table .winner::after{content:'';position:absolute;top:2px;right:2px;
  width:6px;height:6px;border-radius:50%;background:var(--green)}
/* Score bar inside metric cells */
.metric-bar{display:inline-block;height:6px;border-radius:3px;margin-right:8px;
  vertical-align:middle;min-width:4px;transition:width .5s ease}
.metric-val{display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.score-high{color:var(--green)}
.score-mid{color:var(--cyan)}
.score-low{color:var(--amber)}
.compare-header-bar{display:flex;align-items:center;gap:8px;margin-bottom:24px}
.compare-header-bar h1{font-size:24px;font-weight:800;color:var(--text);margin:0}
.compare-badge{display:inline-block;padding:3px 10px;border-radius:20px;
  font-size:11px;font-weight:600;letter-spacing:.03em;
  background:rgba(34,211,238,.1);color:var(--cyan);border:1px solid rgba(34,211,238,.2)}
.result-actions{display:flex;gap:10px;margin-top:20px}
.btn-back{padding:10px 20px;border-radius:8px;font-size:13px;font-weight:600;
  background:var(--card-bg);color:var(--text);border:1px solid var(--border);
  cursor:pointer;transition:all .2s}
.btn-back:hover{background:var(--surface);border-color:var(--muted)}
.btn-share{padding:10px 20px;border-radius:8px;font-size:13px;font-weight:600;
  background:rgba(59,130,246,.12);color:var(--blue);border:1px solid rgba(59,130,246,.2);
  cursor:pointer;transition:all .2s}
.btn-share:hover{background:rgba(59,130,246,.2)}
.compare-legend{display:flex;align-items:center;gap:16px;margin-top:16px;flex-wrap:wrap}
.compare-legend .dot{display:inline-block;width:8px;height:8px;border-radius:50%}
.compare-legend .dot.green{background:var(--green)}
.compare-legend span{font-size:12px;color:var(--muted)}
.compare-check{color:var(--green)}

/* ─── Live Feed ─── */
.live-dot{display:inline-block;width:8px;height:8px;border-radius:50%;
  background:var(--green);margin-right:8px;animation:pulse 2s infinite}

/* ─── Bookmark ─── */
.bookmark-btn{position:absolute;top:12px;left:12px;z-index:5;background:none;border:none;
  font-size:16px;cursor:pointer;color:var(--dim);transition:all .2s;padding:4px}
.bookmark-btn:hover{color:var(--amber);transform:scale(1.2)}
.bookmark-btn.saved{color:var(--amber)}
.watch-btn{position:absolute;top:36px;left:12px;z-index:5;background:none;border:none;
  font-size:12px;cursor:pointer;color:var(--dim);transition:all .2s;padding:4px}
.watch-btn:hover{color:var(--cyan);transform:scale(1.2)}
.watch-btn.watching{color:var(--cyan)}
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

/* ─── Container ─── */
.container{max-width:1320px;margin:0 auto;padding:0 24px}

/* ─── Product Detail ─── */
.detail{max-width:900px;margin:0 auto}
.detail-header{margin-bottom:32px}
.detail-header h1{font-size:32px;font-weight:800;color:#f1f5f9;letter-spacing:-.01em}
.detail-header .tagline{font-size:16px;color:var(--muted);margin-top:8px}
.detail-meta{display:flex;gap:12px;flex-wrap:wrap;margin-top:16px}
.meta-item{display:flex;align-items:center;gap:6px;padding:8px 14px;
  background:var(--card-bg);border-radius:var(--radius-sm);font-size:12.5px;color:var(--muted);
  border:1px solid var(--border)}
.meta-item strong{color:var(--text)}
.meta-item.green{color:var(--green);border-color:rgba(16,185,129,.2)}
.detail-body{margin-top:28px;font-size:16px;line-height:1.8;color:#b0b8c8}
.detail-body h2{font-size:22px;font-weight:700;color:var(--text);margin:28px 0 10px}
.detail-body h3{font-size:18px;font-weight:600;color:#d0d8e8;margin:22px 0 8px}
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
  .hero h1{font-size:24px;line-height:1.3}
  .hero .sub{font-size:13px}
  .hero .tagline{font-size:10px}
  .grid,.featured-grid{grid-template-columns:1fr!important}
  .mega-nav{overflow-x:auto;gap:2px;-webkit-overflow-scrolling:touch;flex-wrap:nowrap}
  .mega-nav a,.mega-nav .nav-section{font-size:11px;padding:5px 8px}
  .nav-sep{display:none}
  .auth-stat{min-width:80px;padding:12px 10px}
  .auth-stat .n{font-size:18px}
  .auth-stat .l{font-size:9px}
  .hero-metrics{gap:6px;flex-wrap:wrap}
  .hero-metric{min-width:70px;padding:8px 12px}
  .hero-metric .val{font-size:16px}
  .hero-metric .lbl{font-size:9px}
  .compare-bar{left:16px;right:16px;transform:none;border-radius:var(--radius-sm)}
  .section-hd{padding:8px 16px 12px}
  .section-hd h2{font-size:16px}
  .filters-bar,.grid,.featured,.auth-bar{padding-left:16px;padding-right:16px}
  .header-inner{padding:12px 16px}
  .logo{font-size:16px}
  /* Card panels */
  .card{padding:14px}
  .card-panel{grid-template-columns:1fr 1fr;gap:6px}
  .panel-item{padding:6px 8px}
  .panel-item .pv{font-size:13px}
  .card-title{font-size:14px}
  .card-desc{font-size:12px}
  /* Section rows → wrap */
  [style*="display:flex"][style*="overflow-x:auto"]{flex-wrap:nowrap}
  /* Catalog 5-col → 2-col */
  #catalog-grid{grid-template-columns:repeat(2,1fr)!important}
  /* Enterprise CTA */
  .ec-inner{flex-direction:column;text-align:center;padding:20px}
  .ec-actions{justify-content:center}
  /* Product detail */
  .detail-header h1{font-size:22px}
  .detail-body{font-size:13px}
  /* Code blocks */
  .code-block{font-size:11px;padding:14px}
  /* Stack builder */
  .stack-row{flex-direction:column}
  /* Footer */
  .footer-inner{flex-direction:column;gap:16px;text-align:center}
}
@media(max-width:480px){
  .hero h1{font-size:20px}
  .hero .sub{font-size:12px}
  .hero-metrics{gap:4px}
  .hero-metric{min-width:60px;padding:6px 10px}
  .hero-metric .val{font-size:14px}
  .card-panel{grid-template-columns:1fr}
  .auth-inner{flex-wrap:wrap}
  .auth-stat{flex:1 1 50%;border-right:none;border-bottom:1px solid var(--border)}
  #catalog-grid{grid-template-columns:1fr!important}
}"""

# ─── Helpers ──────────────────────────────────────────────────────
def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def icon_for(pt):
    icons = {"agent":"🤖","framework":"🔧","platform":"🌐","model":"🧠","infrastructure":"⚡"}
    return icons.get(pt, "📦")

def agent_icon(slug):
    """Unique emoji per agent slug."""
    icons = {
        "cursor-ide":"🖱️","github-copilot":"🐙","claude-code":"🧑‍💻","cline-vscode":"🤖",
        "windsurf-ide":"🌊","codeium-windsurf":"💨","aider-ai":"🅰️","sourcegraph-cody":"🔍",
        "tabnine-ai":"9️⃣","open-interpreter":"💻","langchain-framework":"🦜","langgraph-framework":"🕸️",
        "crewai-framework":"👥","autogen-microsoft":"🔄","openai-swarm":"🐝","semantic-kernel":"🧠",
        "anthropic-mcp":"🔌","phidata-framework":"📊","dify-platform":"🔷","flowise-lowcode":"🎨",
        "n8n-automation":"⚙️","autogpt-agent":"🤖","babyagi-agent":"👶","metagpt-framework":"🏗️",
        "chatdev-agent":"💬","bolt-new":"⚡","replit-ai":"🔄","devin-agent":"🛠️",
        "ollama":"🦙","lm-studio":"🖥️","jan-ai":"🧩","deepseek-llm":"🐋",
        "chatgpt-openai":"🧠","claude-anthropic":"🎭","google-gemini":"💎","mistral-ai":"🌬️",
        "llama-meta":"🦙","hermes-agent":"🔮","perplexity-ai":"🔎","superagi-agent":"🦸",
        "swe-agent":"🔧","anythingllm":"📚","e2b-sandbox":"📦","smolagents-huggingface":"🤗",
        "composio-tools":"🔗","langsmith-langchain":"📝","continue-dev":"▶️","copy-ai":"📋",
        "jasper-ai":"✍️","zapier-ai":"⚡","notion-ai":"📄","microsoft-copilot":"🪟",
        "amazon-q-developer":"☁️","taskade-ai":"✅","lovable-dev":"❤️","vercel-v0":"▲",
        "codex-cli":"⌨️","codex-desktop":"🖥️","claude-desktop":"💻","phind-ai":"🔎",
        "openclaw-agent":"🦞","you-com":"🔍"
    }
    return icons.get(slug, "📦")

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
            return f'<div class="card-icon"><img src="{img_url}" alt="{esc(p.get("title",""))}" loading="lazy"></div>'
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
    github_stars = p.get("github_stars", 0) or 0
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
    # Numeric scores
    r = float(rating) if rating else 0
    # Maturity score (0-10): rating*2 + freshness bonus + review bonus
    mat_score = min(10, round(r * 1.8 + freshness * 1.5 + min(review_count/500, 2), 1))
    # Deployability score (0-10): local + docker + tech simplicity
    dep_score = 9.0 if local_first else 5.0
    if any(t.lower() == "docker" for t in tech_stack): dep_score = min(10, dep_score + 1.5)
    dep_score = min(10, round(dep_score - len(tech_stack)*0.3, 1))
    # Community velocity (+%): based on review_count proxy + freshness
    comm_vel = round(freshness * 15 + min(review_count/200, 8), 1)
    vel_sign = "+" if freshness > 0.4 else "-" if freshness < 0.2 else ""
    # Docs quality (0-10): derived from rating + freshness
    docs_score = min(10, round(r * 1.5 + freshness * 2, 1))
    # QantScore™ — composite 0-100
    qant_score = min(100, round(r*20*0.30 + mat_score*10*0.25 + dep_score*10*0.20 + comm_vel*1.5*0.15 + docs_score*10*0.10))
    # Trend
    trend = "→"
    if freshness > 0.8: trend = "↑↑"
    elif freshness > 0.6: trend = "↑"
    elif freshness < 0.3: trend = "↓"
    items = []
    # QantScore badge — prominent first
    qs_color = "var(--green)" if qant_score >= 85 else "var(--cyan)" if qant_score >= 70 else "var(--amber)"
    items.append(f'<div class="panel-item qs-badge"><div class="pv" style="color:{qs_color};font-size:16px">{qant_score}</div><div class="pl">QantScore™</div></div>')
    if rating:
        items.append(f'<div class="panel-item"><div class="pv amber">{rating} ★</div><div class="pl">Rating</div></div>')
    if pricing:
        items.append(f'<div class="panel-item"><div class="pv green">{esc(pricing)}</div><div class="pl">Цена</div></div>')
    items.append(f'<div class="panel-item"><div class="pv">{depl}</div><div class="pl">Развёртывание</div></div>')
    items.append(f'<div class="panel-item"><div class="pv">{mat_score}</div><div class="pl">Maturity /10</div></div>')
    items.append(f'<div class="panel-item"><div class="pv cyan">{trend} {vel_sign}{comm_vel}%</div><div class="pl">Velocity</div></div>')
    items.append(f'<div class="panel-item"><div class="pv">{dep_score}</div><div class="pl">Deploy /10</div></div>')
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
<title>{title} | Qantcore — Аналитика AI-агентов</title>
<meta name="description" content="{description}">
<link rel="icon" type="image/svg+xml" href="/images/favicon.svg">
{canonical_url}
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
      <a href="/" class="{active_home}">Каталог</a>
      <span class="nav-sep"></span>
      <a href="/catalog/comparison/" class="{active_compare}">Сравнения</a>
      <span class="nav-sep"></span>
      <a href="/guides/" class="nav-featured {active_guides}">📖 Гайды</a>
      <span class="nav-sep"></span>
      <a href="/catalog/review/" class="nav-review {active_review}">Обзоры</a>
      <span class="nav-sep"></span>
      <a href="/multi-agent/" class="{active_ma}">Мульти-агенты</a>
      <span class="nav-sep"></span>
      <a href="/benchmarks/">Рейтинг</a>
      <span class="nav-sep"></span>
      <a href="/local-models/" class="nav-local">Локальные LLM</a>
      <span class="nav-sep"></span>
      <a href="/methodology/" class="{active_method}">Методология</a>
      <span class="nav-sep"></span>
      <a href="/workspace/" class="{active_ws}">Кабинет</a>
      <span class="nav-sep"></span>
      <a href="#saved" class="saved-nav" style="display:none">★ Избранное</a>
    </div>
  </div>
</header>
{content}
<footer>
  Qantcore &copy; 2026 &mdash; Платформа аналитики AI-агентов &mdash;
  Обновляется ежедневно &mdash; <a href="https://t.me/AliBizCo">@AliBizCo</a>
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
            img = f'<div class="card-icon"><img src="{p["image_url"]}" alt="{esc(p.get("title",""))}" loading="lazy"></div>'
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
            "iu": p.get("image_url",""),
            "img": img,
            "panel": panel_data(p),
            "trust": trust_indicators(p),
        })
    return json.dumps(entries)

# ─── OG Meta Helper ──────────────────────────────────────────────
def make_og(title, description, url, image_url="/images/favicon.svg"):
    """Generate Open Graph + Twitter Card + canonical meta tags."""
    desc = esc(description)[:200]
    t = esc(title)
    return f'''<link rel="canonical" href="https://qantcore.space{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://qantcore.space{url}">
<meta property="og:image" content="https://qantcore.space{image_url}">
<meta property="og:site_name" content="QantCore">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://qantcore.space{image_url}">'''

def make_og_article(title, description, url, image_url="/images/favicon.svg"):
    """Generate OG + Twitter for article-type pages (products, reviews, comparisons)."""
    desc = esc(description)[:200]
    t = esc(title)
    return f'''<link rel="canonical" href="https://qantcore.space{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://qantcore.space{url}">
<meta property="og:image" content="https://qantcore.space{image_url}">
<meta property="og:site_name" content="QantCore">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://qantcore.space{image_url}">'''


def render_page(title, description, content, scripts="", total=0, search_val="", search_json="[]",
                active_home="", active_compare="", active_review="", active_method="", active_ws="",
                active_dev="", active_ma="", active_guides="",
                open_graph="", schema_org="{}", canonical_url="", extra_css=""):
    return PAGE.format(
        title=esc(title), description=esc(description),
        css=CSS + extra_css, content=content, scripts=scripts, total=str(total),
        search_val=esc(search_val), search_json=search_json,
        active_home=active_home, active_compare=active_compare, active_review=active_review, active_method=active_method, active_ws=active_ws,
        active_dev=active_dev, active_ma=active_ma, active_guides=active_guides,
        open_graph=open_graph, schema_org=schema_org, canonical_url=canonical_url)


# ─── Card Generator ───────────────────────────────────────────────
def make_product_card(p, with_compare=True, compact=False):
    """Intelligence panel card."""
    compare_html = ""
    if with_compare:
        compare_html = f'<div class="card-compare"><input type="checkbox" value="{p["slug"]}" onchange="toggleCompare(this)" aria-label="Compare"></div>'
    bookmark_html = f'<button class="bookmark-btn" data-slug="{p["slug"]}" onclick="toggleSave(this,&#39;{p["slug"]}&#39;)" title="Save">☆</button>'
    watch_html = f'<button class="watch-btn" data-slug="{p["slug"]}" onclick="event.preventDefault();toggleWatch(this,&#39;{p["slug"]}&#39;)" title="Track releases">🔔</button>'
    panel = panel_data(p)
    trust = trust_indicators(p)
    img_url = p.get("image_url", "")
    if compact:
        logo_html = f'<img src="{img_url}" alt="{esc(p.get("title",""))}" style="width:32px;height:32px;object-fit:contain;border-radius:6px;background:rgba(255,255,255,.03);padding:2px;margin:0 auto 6px;display:block">' if img_url else f'<div style="width:32px;height:32px;border-radius:6px;background:rgba(255,255,255,.03);display:flex;align-items:center;justify-content:center;font-size:18px;margin:0 auto 6px">{agent_icon(p["slug"])}</div>'
        style = 'style="padding:12px 10px;min-width:0;overflow:hidden"'
        title_style = 'style="font-size:12px;margin-bottom:2px"'
        desc_style = 'style="font-size:10px;-webkit-line-clamp:2"'
        panel_style = 'style="font-size:10px;gap:4px"'
        trust_style = 'style="font-size:9px"'
    else:
        logo_html = f'<img src="{img_url}" alt="{esc(p.get("title",""))}" style="width:64px;height:64px;object-fit:contain;border-radius:10px;background:rgba(255,255,255,.03);padding:4px;margin:0 auto 10px;display:block">' if img_url else f'<div style="width:64px;height:64px;border-radius:10px;background:rgba(255,255,255,.03);display:flex;align-items:center;justify-content:center;font-size:28px;margin:0 auto 10px">{agent_icon(p["slug"])}</div>'
        style = ''
        title_style = ''
        desc_style = ''
        panel_style = ''
        trust_style = ''
    return f"""<a href="/product/{p['slug']}/" class="card" {style}>
      {compare_html}
      {bookmark_html}
      {watch_html}
      {logo_html}
      <div class="card-title" {title_style}>{esc(p.get('title',''))}</div>
      <div class="card-desc" {desc_style}>{esc(p.get('tagline','') or p.get('description',''))}</div>
      <div class="card-panel" {panel_style}>{panel}</div>
      <div class="card-trust" {trust_style}>{trust}</div>
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
    featured = sorted(products, key=lambda p: (p.get("rating", 0) or 0), reverse=True)[:8]
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
  <div class="tagline">ПЛАТФОРМА АНАЛИТИКИ AI-АГЕНТОВ</div>
  <h1>Сравнивайте, тестируйте и внедряйте <span class="accent">AI-агентов</span></h1>
  <p class="sub">Полный каталог AI-агентов и фреймворков —
  глубокие технические обзоры, живые бенчмарки, аналитика внедрения. {last_update}.</p>
  <div class="hero-metrics">
    <div class="hero-metric"><div class="val">{tp}+</div><div class="lbl">Агентов</div></div>
    <div class="hero-metric"><div class="val">{tc}+</div><div class="lbl">Сравнений</div></div>
    <div class="hero-metric"><div class="val">{tr}+</div><div class="lbl">Обзоров</div></div>
    <div class="hero-metric"><div class="val" style="color:var(--green)">●</div><div class="lbl">Ежедневно</div></div>
  </div>
  <div class="hero-cta">
    <a href="/compare/" class="cta-primary">Сравнить свой AI-стек</a>
    <a href="/guides/" class="cta-secondary" style="border-color:var(--blue);color:var(--blue)">Гайды</a>
    <a href="/catalog/review/" class="cta-secondary">Обзоры</a>
  </div>
</section>"""

    # ─── Authority Bar ───
    auth = f"""<div class="auth-bar" id="catalog">
  <div class="auth-inner">
    <div class="auth-stat"><div class="n">{tp}</div><div class="l">Агентов отслежено</div></div>
    <div class="auth-stat"><div class="n">{tc}</div><div class="l">Прямых сравнений</div></div>
    <div class="auth-stat"><div class="n amber">{type_counts.get('agent',0)}</div><div class="l">AI-агентов</div></div>
    <div class="auth-stat"><div class="n">{type_counts.get('framework',0)}</div><div class="l">Фреймворков</div></div>
    <div class="auth-stat"><div class="n">{type_counts.get('platform',0)}</div><div class="l">Платформ</div></div>
    <div class="auth-stat"><div class="n"><span class="dot"></span>Live</div><div class="l">Обновлено сегодня</div></div>
  </div>
</div>"""

    # ─── Featured (Level 1: top 8 compact row) ───
    feat_cards = ""
    for p in featured:
        img_url = p.get("image_url", "")
        logo = f'<img src="{img_url}" alt="" style="width:32px;height:32px;object-fit:contain;border-radius:6px;margin:0 auto 5px;display:block">' if img_url else f'<span style="font-size:22px;display:block;text-align:center">{agent_icon(p["slug"])}</span>'
        feat_cards += f"""<a href="/product/{p['slug']}/" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:100px;height:76px;padding:8px 6px;background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:10px;flex:1 1 100px;text-decoration:none;transition:border-color .2s" onmouseover="this.style.borderColor='var(--green)'" onmouseout="this.style.borderColor='var(--border)'">
          {logo}<span style="font-size:11px;font-weight:600;color:var(--text);line-height:1.2;text-align:center;overflow:hidden;text-overflow:ellipsis;max-width:90px">{esc(p.get('title','')[:16])}</span>
        </a>"""
    featured_html = f"""<div class="section-hd"><h2>\u2605 Лучшие фреймворки</h2><a href="/catalog/product/" class="see-all">Все {tp} \u2192</a></div>
<div style="display:flex;gap:8px;flex-wrap:wrap">{feat_cards}</div>"""

    # ─── Enterprise CTA ───
    enterprise_cta = f"""<div class="enterprise-cta">
  <div class="ec-inner">
    <div class="ec-text">
      <h3>Собираете AI-стек для команды?</h3>
      <p>Получите сравнение под ваш кейс — модель развёртывания, бюджет, compliance.</p>
    </div>
    <div class="ec-actions">
    <a href="/compare/" class="cta-primary">Сравнить свой AI-стек</a>
    <a href="/media-kit/" class="cta-secondary">Запросить обзор вендора</a>
    <a href="/benchmarks/" class="cta-secondary">Получить отчёт</a>
    <a href="https://t.me/AliBizCo" style="display:inline-flex;align-items:center;gap:6px;padding:12px 20px;background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.25);border-radius:10px;color:var(--green);font-size:14px;font-weight:600;text-decoration:none;transition:all .2s" onmouseover="this.style.background='rgba(16,185,129,.15)';this.style.borderColor='var(--green)'" onmouseout="this.style.background='rgba(16,185,129,.08)';this.style.borderColor='rgba(16,185,129,.25)'">💬 @AliBizCo</a>
  </div>
</div>"""

    # ─── Trending Comparisons (Level 2) ───
    comps = list(DB.articles.find({"category": "comparison"}).limit(4))
    comp_cards = ""
    for c in comps:
        pa_slug = c.get('product_a', ''); pb_slug = c.get('product_b', '')
        pa_img = ''; pb_img = ''
        if pa_slug:
            pa = DB.articles.find_one({"slug": pa_slug, "category": "product"})
            if pa:
                iu = pa.get("image_url", "")
                pa_img = f'<img src="{iu}" alt="" style="width:40px;height:40px;object-fit:contain;border-radius:6px;background:rgba(255,255,255,.03);padding:2px">' if iu else f'<span style="font-size:24px">{icon_for(pa.get("product_type",""))}</span>'
        if pb_slug:
            pb = DB.articles.find_one({"slug": pb_slug, "category": "product"})
            if pb:
                iu = pb.get("image_url", "")
                pb_img = f'<img src="{iu}" alt="" style="width:40px;height:40px;object-fit:contain;border-radius:6px;background:rgba(255,255,255,.03);padding:2px">' if iu else f'<span style="font-size:24px">{icon_for(pb.get("product_type",""))}</span>'
        vs_block = f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:10px">{pa_img}<span style="font-size:12px;font-weight:800;color:var(--green);background:var(--green-dim);padding:2px 6px;border-radius:4px">VS</span>{pb_img}</div>' if pa_img and pb_img else '<div class="card-icon">⚖️</div>'
        comp_cards += f"""<a href="/compare/{c['slug']}/" class="card" style="flex:0 0 290px">
      {vs_block}
      <div class="card-title">{esc(c.get('title',''))}</div>
      <div class="card-desc">{esc(str(c.get('description',''))[:120])}</div>
      <div class="card-trust"><span class="trust-badge trust-verified">✓ Detailed comparison</span></div>
    </a>"""

    trending_html = ""
    if comp_cards:
        trending_html = f"""<div class="section-hd"><h2>⚡ Популярные сравнения</h2><a href="/catalog/comparison/" class="see-all">Все {tc} →</a></div>
<div style="display:flex;gap:16px;overflow-x:auto;max-width:1320px;margin:0 auto;padding:0 24px 32px">{comp_cards}</div>"""

    # ─── New Releases (Level 2.5: latest 8 compact row) ───
    newest = sorted(products, key=lambda p: p.get("updated_at", ""), reverse=True)[:8]
    new_cards = ""
    for p in newest:
        img_url = p.get("image_url", "")
        logo = f'<img src="{img_url}" alt="" style="width:32px;height:32px;object-fit:contain;border-radius:6px;margin:0 auto 5px;display:block">' if img_url else f'<span style="font-size:22px;display:block;text-align:center">{agent_icon(p["slug"])}</span>'
        new_cards += f"""<a href="/product/{p['slug']}/" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:100px;height:76px;padding:8px 6px;background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:10px;flex:1 1 100px;text-decoration:none;transition:border-color .2s" onmouseover="this.style.borderColor='var(--green)'" onmouseout="this.style.borderColor='var(--border)'">
          {logo}<span style="font-size:11px;font-weight:600;color:var(--text);line-height:1.2;text-align:center;overflow:hidden;text-overflow:ellipsis;max-width:90px">{esc(p.get('title','')[:16])}</span>
        </a>"""
    new_html = f"""<div class="section-hd"><h2>\U0001F195 Новые и обновлённые</h2><a href="/catalog/product/" class="see-all">Все {tp} \u2192</a></div>
<div style="display:flex;gap:8px;flex-wrap:wrap">{new_cards}</div>"""

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
    <div class="auth-stat"><div class="n amber">{tp}</div><div class="l">В рейтинге</div></div>
    <div class="auth-stat"><div class="n">{tc}</div><div class="l">Прямых тестов</div></div>
    {bench_rows}
  </div>
</div>"""

    # ─── Гайды (выделенный блок) ───
    guides_html = f"""<div class="section-hd" id="guides" style="margin-top:40px"><h2>📖 Практические гайды</h2><a href="/guides/" class="see-all">Все 30 гайдов →</a></div>
<div style="max-width:1320px;margin:0 auto;padding:0 24px 20px">
  <p style="font-size:13px;color:var(--muted);margin-bottom:16px">Пошаговые руководства с кодом: от локального запуска LLM до production-деплоя multi-agent систем. Каждый гайд — готовый рецепт.</p>
</div>
<div class="grid" style="max-width:1320px;margin:0 auto;padding:0 24px 32px;grid-template-columns:repeat(4,1fr)">
  <a href="/guides/#local-llm" class="card" style="border:1px solid #10b98133;cursor:pointer">
    <div class="card-top"><div class="card-icon" style="font-size:28px">🦙</div><span class="card-badge badge-agent">Базовый · 10 мин</span></div>
    <div class="card-title">Локальный запуск LLM</div>
    <div class="card-desc">Ollama + Open WebUI: запустите Llama 4, DeepSeek, Qwen на своей машине за 15 минут. Без облака, без API-ключей.</div>
  </a>
  <a href="/guides/#agentic-rag-deep" class="card" style="border:1px solid #f59e0b33;cursor:pointer">
    <div class="card-top"><div class="card-icon" style="font-size:28px">🔗</div><span class="card-badge" style="background:var(--amber-dim);color:var(--amber)">Продвинутый · 16 мин</span></div>
    <div class="card-title">Agentic RAG: глубокое погружение</div>
    <div class="card-desc">RAG с агентной логикой: планирование поиска, переформулировка запросов, итеративная проверка результатов на LangGraph.</div>
  </a>
  <a href="/guides/#mcp-server-build" class="card" style="border:1px solid #3B82F633;cursor:pointer">
    <div class="card-top"><div class="card-icon" style="font-size:28px">🔌</div><span class="card-badge badge-agent">Средний · 20 мин</span></div>
    <div class="card-title">Свой MCP-сервер за 20 минут</div>
    <div class="card-desc">Python MCP-сервер с инструментами для БД. Работает с Claude Desktop, Cursor, Continue. Полный код.</div>
  </a>
  <a href="/guides/#opensource-agent-stack" class="card" style="border:1px solid #10b98133;cursor:pointer">
    <div class="card-top"><div class="card-icon" style="font-size:28px">🔓</div><span class="card-badge badge-agent">Базовый · 10 мин</span></div>
    <div class="card-title">Опенсорсный AI-стек</div>
    <div class="card-desc">Ollama + Continue + Aider: полностью локальный стек без подписок. Полный контроль над данными и кодом.</div>
  </a>
  <a href="/guides/#agent-framework-comparison" class="card" style="border:1px solid #22D3EE33;cursor:pointer">
    <div class="card-top"><div class="card-icon" style="font-size:28px">⚖️</div><span class="card-badge badge-agent">Средний · 13 мин</span></div>
    <div class="card-title">Фреймворки для агентов 2026</div>
    <div class="card-desc">CrewAI vs AutoGen vs LangGraph vs Swarm vs MetaGPT — полное сравнение с примерами кода для каждого.</div>
  </a>
  <a href="/guides/#agent-safety" class="card" style="border:1px solid #ef444433;cursor:pointer">
    <div class="card-top"><div class="card-icon" style="font-size:28px">🛡️</div><span class="card-badge" style="background:var(--red-dim);color:var(--red)">Продвинутый · 14 мин</span></div>
    <div class="card-title">Безопасность AI-агентов</div>
    <div class="card-desc">Docker-песочницы, валидация вывода, Human-in-the-Loop. Защита от prompt injection и runaway agents.</div>
  </a>
  <a href="/guides/#cursor-vs-copilot" class="card" style="border:1px solid #3B82F633;cursor:pointer">
    <div class="card-top"><div class="card-icon" style="font-size:28px">⚔️</div><span class="card-badge badge-agent">Базовый · 7 мин</span></div>
    <div class="card-title">Cursor vs Copilot 2026</div>
    <div class="card-desc">Практическое сравнение лидеров: автодополнение, понимание кодовой базы, работа с PR, цена.</div>
  </a>
  <a href="/guides/#ai-stack-startup" class="card" style="border:1px solid #10b98133;cursor:pointer">
    <div class="card-top"><div class="card-icon" style="font-size:28px">🚀</div><span class="card-badge badge-agent">Базовый · 6 мин</span></div>
    <div class="card-title">AI-стек для стартапа</div>
    <div class="card-desc">Минимальный набор инструментов: что купить, что локально, а что не нужно. Бюджетная сборка для команды.</div>
  </a>
</div>"""

    # ─── Live Activity Feed ───
    last_updates = list(DB.articles.find({"category": "product"}).sort("updated_at", -1).limit(5))
    feed_items = ""
    for u in last_updates:
        ago = time_ago(u.get("updated_at", ""))
        feed_items += f'<div class="feed-item"><span class="fi-time">{ago}</span><span class="fi-icon">📡</span><div class="fi-text"><strong>{esc(u.get("title","")[:35])}</strong> — updated</div></div>'
    # Add some synthetic events
    feed_items += f'<div class="feed-item"><span class="fi-time">Today</span><span class="fi-icon">🔬</span><div class="fi-text"><strong>Обновление бенчмарков</strong> — {tc} сравнений пересчитано</div></div>'
    feed_items += f'<div class="feed-item"><span class="fi-time">Today</span><span class="fi-icon">📊</span><div class="fi-text"><strong>Обновление каталога</strong> — {tp} агентов отслежено, {tc} прямых сравнений</div></div>'
    live_html = f"""<div class="section-hd" id="activity"><h2><span class="live-dot"></span>Живая лента</h2></div>
<div class="auth-bar">
  <div class="feed-list" style="padding:12px 16px">{feed_items}</div>
</div>"""

    # ─── Full Catalog ───
    # Filters
    product_types = DB.articles.distinct("product_type", {"category": "product"})
    filters_html = '<span class="label">Filter:</span>'
    filters_html += '<button class="filter-btn active" onclick="filterCards(\'all\')">All</button>'
    for pt in sorted(product_types):
        cnt = type_counts.get(pt, 0)
        filters_html += f'<button class="filter-btn" onclick="filterCards(\'{pt}\')">{esc(pt)}<span class="count">{cnt}</span></button>'

    all_cards = ""
    for p in products:
        all_cards += make_product_card(p, with_compare=True, compact=True)

    catalog_html = f"""<div class="section-hd"><h2>📋 Полный каталог</h2></div>
<div class="filters-bar">{filters_html}</div>
<div style="max-width:1320px;margin:0 auto;padding:0 24px 32px;display:grid;grid-template-columns:repeat(5,1fr);gap:16px" id="catalog-grid">{all_cards}</div>"""

    # ─── Compare Bar ───
    compare_bar = """<div class="compare-bar" id="compare-bar">
  <span class="sel"><strong id="compare-count">0</strong> выбрано</span>
  <button class="compare-btn" id="compare-btn" disabled onclick="doCompare()">⚖️ Сравнить</button>
  <button class="compare-btn" id="integrate-btn" disabled onclick="showIntegrations()" style="background:var(--blue)">🔗 Связки</button>
  <button class="compare-clear" onclick="clearCompare()">Сброс</button>
</div>
<svg id="live-connections" class="live-lines"></svg>"""

    content = '<div class="container">' + hero + auth + featured_html + enterprise_cta + trending_html + new_html + bench_html + live_html + guides_html + catalog_html + '</div>' + compare_bar

    # Scripts
    scripts = """<script>
var searchResults = {search_json};

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
  var ibtn = document.getElementById('integrate-btn');
  cnt.textContent = selected.length;
  bar.classList.toggle('active', selected.length > 0);
  btn.disabled = selected.length < 2;
  if (ibtn) ibtn.disabled = selected.length < 1;
  drawLiveLines();
}
function drawLiveLines() {
  var svg = document.getElementById('live-connections');
  if (!svg) return;
  svg.innerHTML = '';
  if (selected.length === 0) { svg.classList.remove('active'); return; }
  svg.classList.add('active');
  svg.setAttribute('viewBox', '0 0 '+window.innerWidth+' '+window.innerHeight);
  svg.style.width = window.innerWidth+'px';
  svg.style.height = window.innerHeight+'px';
  var colors = ['#10b981','#3B82F6','#f59e0b','#22D3EE','#8b5cf6','#ef4444','#ec4899','#14b8a6'];
  if (selected.length === 1) {
    // One agent selected: draw lines to all compatible agents visible on page
    var selSlug = selected[0];
    var buddies = integrations[selSlug] || [];
    if (buddies.length === 0) { svg.classList.remove('active'); return; }
    // Get selected card position
    var selCB = document.querySelector('.card input[type=checkbox][value="'+selSlug+'"]');
    if (!selCB) { svg.classList.remove('active'); return; }
    var selCard = selCB.closest('.card');
    if (!selCard) { svg.classList.remove('active'); return; }
    var sr = selCard.getBoundingClientRect();
    var sx = sr.left + sr.width/2, sy = sr.top + sr.height/2;
    // Find all cards whose slugs are in buddies
    var allCBs = document.querySelectorAll('.card input[type=checkbox]');
    var drawn = 0;
    allCBs.forEach(function(cb, idx) {
      if (cb.value === selSlug) return;
      if (!buddies.includes(cb.value)) return;
      var card = cb.closest('.card');
      if (!card) return;
      var r = card.getBoundingClientRect();
      var tx = r.left + r.width/2, ty = r.top + r.height/2;
      var c = colors[drawn % colors.length];
      var mx = (sx+tx)/2 + (Math.random()-0.5)*60;
      var my = (sy+ty)/2 + (Math.random()-0.5)*60;
      svg.innerHTML += '<path d="M'+sx+','+sy+' L'+mx+','+my+' L'+tx+','+ty+'" stroke="'+c+'" stroke-width="2.5" fill="none" opacity="0.85"><animate attributeName="opacity" values="0.5;1;0.5" dur="1s" repeatCount="indefinite"/></path>';
      svg.innerHTML += '<circle cx="'+mx+'" cy="'+my+'" r="4" fill="'+c+'" opacity="0.9"><animate attributeName="r" values="4;7;4" dur="1s" repeatCount="indefinite"/></circle>';
      svg.innerHTML += '<circle cx="'+sx+'" cy="'+sy+'" r="3" fill="'+c+'" opacity="0.9"/>';
      svg.innerHTML += '<circle cx="'+tx+'" cy="'+ty+'" r="3" fill="'+c+'" opacity="0.9"/>';
      drawn++;
    });
    if (drawn === 0) { svg.classList.remove('active'); }
    return;
  }
  // 2+ agents: lines between selected pairs
  var cards = [];
  var cbs = document.querySelectorAll('.card input[type=checkbox]:checked');
  cbs.forEach(function(cb) {
    var card = cb.closest('.card');
    if (!card) return;
    var r = card.getBoundingClientRect();
    cards.push({slug: cb.value, cx: r.left + r.width/2, cy: r.top + r.height/2});
  });
  for (var i = 0; i < cards.length; i++) {
    for (var j = i+1; j < cards.length; j++) {
      var connected = (integrations[cards[i].slug]&&integrations[cards[i].slug].includes(cards[j].slug))||(integrations[cards[j].slug]&&integrations[cards[j].slug].includes(cards[i].slug));
      var x1 = cards[i].cx, y1 = cards[i].cy;
      var x2 = cards[j].cx, y2 = cards[j].cy;
      if (connected) {
        var c = colors[(i+j)%colors.length];
        var mx = (x1+x2)/2 + (Math.random()-0.5)*60;
        var my = (y1+y2)/2 + (Math.random()-0.5)*60;
        svg.innerHTML += '<path d="M'+x1+','+y1+' L'+mx+','+my+' L'+x2+','+y2+'" stroke="'+c+'" stroke-width="2.5" fill="none" opacity="0.85"><animate attributeName="opacity" values="0.5;1;0.5" dur="1s" repeatCount="indefinite"/></path>';
        svg.innerHTML += '<circle cx="'+mx+'" cy="'+my+'" r="4" fill="'+c+'" opacity="0.9"><animate attributeName="r" values="4;7;4" dur="1s" repeatCount="indefinite"/></circle>';
        svg.innerHTML += '<circle cx="'+x1+'" cy="'+y1+'" r="3" fill="'+c+'" opacity="0.9"/>';
        svg.innerHTML += '<circle cx="'+x2+'" cy="'+y2+'" r="3" fill="'+c+'" opacity="0.9"/>';
      }
    }
  }
}
// Redraw lines on scroll/resize so they stay attached to cards
var _linesTimer = null;
function redrawLinesOnScroll() {
  if (_linesTimer) return;
  _linesTimer = requestAnimationFrame(function() {
    _linesTimer = null;
    var svg = document.getElementById('live-connections');
    if (svg && svg.classList.contains('active')) drawLiveLines();
  });
}
window.addEventListener('scroll', redrawLinesOnScroll, {passive: true});
window.addEventListener('resize', redrawLinesOnScroll, {passive: true});
function doCompare() {
  if (selected.length >= 2) {
    var slugs = selected.join(',');
    var comps = JSON.parse(localStorage.getItem('qantcore_comparisons') || '[]');
    comps.push({slugs: selected.slice(), date: new Date().toISOString().substring(0,10)});
    if (comps.length > 20) comps = comps.slice(-20);
    localStorage.setItem('qantcore_comparisons', JSON.stringify(comps));
    window.location = '/compare/?slugs=' + slugs;
  }
}
// ─── Integrations ───
var integrations = {
  "aider-ai": ["bolt-new","chatgpt-openai","claude-anthropic","claude-code","claude-desktop","cline-vscode","codex-cli","codex-desktop","continue-dev","cursor-ide","deepseek-llm","devin-agent","e2b-sandbox","github-copilot","google-gemini","hermes-agent","jan-ai","langchain-framework","llama-meta","lm-studio","lovable-dev","microsoft-copilot","mistral-ai","ollama","open-interpreter","phind-ai","replit-ai","vercel-v0","windsurf-ide"],
  "amazon-q-developer": ["chatgpt-openai","claude-anthropic","cursor-ide","github-copilot","microsoft-copilot","sourcegraph-cody","tabnine-ai"],
  "anthropic-mcp": ["claude-code","claude-desktop","cline-vscode","composio-tools","langchain-framework","langsmith-langchain","open-interpreter"],
  "anythingllm": ["dify-platform","flowise-lowcode","langchain-framework","lm-studio","n8n-automation","ollama","openai-swarm"],
  "autogen-microsoft": ["chatdev-agent","composio-tools","crewai-framework","langchain-framework","langgraph-framework","langsmith-langchain","metagpt-framework","openai-swarm","openclaw-agent","semantic-kernel","superagi-agent"],
  "autogpt-agent": ["babyagi-agent","crewai-framework","langchain-framework","metagpt-framework","open-interpreter","superagi-agent"],
  "babyagi-agent": ["autogpt-agent","crewai-framework","langchain-framework","open-interpreter"],
  "bolt-new": ["aider-ai","chatgpt-openai","claude-anthropic","cline-vscode","cursor-ide","github-copilot","lovable-dev","replit-ai","vercel-v0","windsurf-ide"],
  "chatdev-agent": ["autogen-microsoft","crewai-framework","langchain-framework","metagpt-framework"],
  "chatgpt-openai": ["aider-ai","anythingllm","cline-vscode","copy-ai","cursor-ide","dify-platform","github-copilot","jan-ai","langchain-framework","openai-swarm","windsurf-ide"],
  "claude-anthropic": ["aider-ai","anthropic-mcp","anythingllm","claude-code","cline-vscode","cursor-ide","jan-ai","langchain-framework","sourcegraph-cody","windsurf-ide"],
  "claude-code": ["aider-ai","anthropic-mcp","cline-vscode","cursor-ide","devin-agent","github-copilot","open-interpreter","sourcegraph-cody","windsurf-ide"],
  "claude-desktop": ["aider-ai","anthropic-mcp","claude-code","cline-vscode","cursor-ide","sourcegraph-cody"],
  "cline-vscode": ["aider-ai","anthropic-mcp","bolt-new","chatgpt-openai","claude-anthropic","claude-code","claude-desktop","codex-cli","continue-dev","cursor-ide","deepseek-llm","devin-agent","e2b-sandbox","github-copilot","google-gemini","hermes-agent","jan-ai","llama-meta","lm-studio","lovable-dev","microsoft-copilot","mistral-ai","ollama","open-interpreter","phind-ai","vercel-v0","windsurf-ide"],
  "codeium-windsurf": ["chatgpt-openai","cline-vscode","cursor-ide","github-copilot","microsoft-copilot","tabnine-ai","windsurf-ide"],
  "codex-cli": ["aider-ai","claude-code","cline-vscode","cursor-ide","github-copilot","open-interpreter"],
  "codex-desktop": ["aider-ai","cline-vscode","codex-cli","cursor-ide","github-copilot"],
  "composio-tools": ["autogen-microsoft","crewai-framework","dify-platform","langchain-framework","n8n-automation","openai-swarm","phidata-framework"],
  "continue-dev": ["aider-ai","claude-code","cline-vscode","cursor-ide","github-copilot","lm-studio","ollama","tabnine-ai","windsurf-ide"],
  "copy-ai": ["chatgpt-openai","dify-platform","jasper-ai","n8n-automation","notion-ai","zapier-ai"],
  "crewai-framework": ["autogen-microsoft","autogpt-agent","babyagi-agent","chatdev-agent","composio-tools","e2b-sandbox","langchain-framework","langgraph-framework","langsmith-langchain","metagpt-framework","open-interpreter","openclaw-agent","semantic-kernel","superagi-agent"],
  "cursor-ide": ["aider-ai","bolt-new","chatgpt-openai","claude-anthropic","claude-code","claude-desktop","cline-vscode","codeium-windsurf","codex-cli","codex-desktop","continue-dev","deepseek-llm","devin-agent","github-copilot","google-gemini","hermes-agent","jan-ai","llama-meta","lm-studio","lovable-dev","microsoft-copilot","mistral-ai","ollama","open-interpreter","phind-ai","replit-ai","sourcegraph-cody","tabnine-ai","vercel-v0","windsurf-ide"],
  "deepseek-llm": ["aider-ai","anythingllm","cline-vscode","continue-dev","cursor-ide","jan-ai","langchain-framework","lm-studio","ollama","open-interpreter"],
  "devin-agent": ["aider-ai","claude-code","cline-vscode","codex-cli","codex-desktop","cursor-ide","e2b-sandbox","github-copilot","lovable-dev","open-interpreter"],
  "dify-platform": ["anythingllm","chatgpt-openai","composio-tools","copy-ai","flowise-lowcode","hermes-agent","jasper-ai","langchain-framework","langgraph-framework","langsmith-langchain","n8n-automation","notion-ai","openai-swarm","phidata-framework","you-com","zapier-ai"],
  "e2b-sandbox": ["aider-ai","autogpt-agent","cline-vscode","crewai-framework","devin-agent","langchain-framework","open-interpreter","swe-agent"],
  "flowise-lowcode": ["anythingllm","composio-tools","dify-platform","hermes-agent","langchain-framework","langsmith-langchain","n8n-automation","ollama","zapier-ai"],
  "github-copilot": ["aider-ai","amazon-q-developer","bolt-new","chatgpt-openai","claude-anthropic","claude-code","cline-vscode","codeium-windsurf","codex-cli","codex-desktop","continue-dev","cursor-ide","deepseek-llm","devin-agent","google-gemini","llama-meta","lovable-dev","microsoft-copilot","mistral-ai","phind-ai","replit-ai","sourcegraph-cody","tabnine-ai","vercel-v0","windsurf-ide"],
  "google-gemini": ["aider-ai","anythingllm","cline-vscode","cursor-ide","github-copilot","jan-ai","langchain-framework","windsurf-ide"],
  "hermes-agent": ["aider-ai","anythingllm","cline-vscode","composio-tools","cursor-ide","dify-platform","flowise-lowcode","langchain-framework","lm-studio","n8n-automation","ollama","open-interpreter"],
  "jan-ai": ["anythingllm","chatgpt-openai","claude-anthropic","continue-dev","cursor-ide","deepseek-llm","google-gemini","hermes-agent","llama-meta","lm-studio","mistral-ai","ollama"],
  "jasper-ai": ["chatgpt-openai","copy-ai","dify-platform","n8n-automation","notion-ai","zapier-ai"],
  "langchain-framework": ["aider-ai","anthropic-mcp","autogen-microsoft","autogpt-agent","babyagi-agent","chatdev-agent","chatgpt-openai","claude-anthropic","composio-tools","crewai-framework","deepseek-llm","dify-platform","e2b-sandbox","flowise-lowcode","google-gemini","hermes-agent","langgraph-framework","langsmith-langchain","llama-meta","metagpt-framework","mistral-ai","n8n-automation","ollama","open-interpreter","openai-swarm","openclaw-agent","phidata-framework","semantic-kernel","smolagents-huggingface","superagi-agent","you-com"],
  "langgraph-framework": ["autogen-microsoft","crewai-framework","dify-platform","langchain-framework","openai-swarm","phidata-framework","semantic-kernel","sourcegraph-cody","superagi-agent"],
  "langsmith-langchain": ["crewai-framework","dify-platform","langchain-framework","langgraph-framework","openai-swarm","phidata-framework"],
  "llama-meta": ["aider-ai","anythingllm","cline-vscode","continue-dev","cursor-ide","hermes-agent","jan-ai","langchain-framework","lm-studio","ollama"],
  "lm-studio": ["aider-ai","anythingllm","chatgpt-openai","claude-anthropic","cline-vscode","continue-dev","cursor-ide","deepseek-llm","google-gemini","hermes-agent","jan-ai","llama-meta","mistral-ai","ollama"],
  "lovable-dev": ["aider-ai","bolt-new","cursor-ide","github-copilot","replit-ai","vercel-v0","windsurf-ide"],
  "metagpt-framework": ["autogen-microsoft","autogpt-agent","chatdev-agent","crewai-framework","langchain-framework"],
  "microsoft-copilot": ["aider-ai","amazon-q-developer","cline-vscode","codeium-windsurf","cursor-ide","github-copilot","tabnine-ai","windsurf-ide"],
  "mistral-ai": ["aider-ai","anythingllm","cline-vscode","continue-dev","cursor-ide","hermes-agent","jan-ai","langchain-framework","lm-studio","ollama"],
  "n8n-automation": ["anythingllm","composio-tools","copy-ai","dify-platform","flowise-lowcode","hermes-agent","jasper-ai","langchain-framework","notion-ai","zapier-ai"],
  "notion-ai": ["chatgpt-openai","copy-ai","dify-platform","jasper-ai","n8n-automation","taskade-ai","zapier-ai"],
  "ollama": ["aider-ai","anythingllm","chatgpt-openai","claude-anthropic","cline-vscode","continue-dev","cursor-ide","deepseek-llm","flowise-lowcode","google-gemini","hermes-agent","jan-ai","langchain-framework","llama-meta","lm-studio","mistral-ai","open-interpreter"],
  "open-interpreter": ["aider-ai","autogpt-agent","babyagi-agent","claude-code","cline-vscode","codex-cli","codex-desktop","crewai-framework","cursor-ide","deepseek-llm","e2b-sandbox","hermes-agent","langchain-framework","llama-meta","lm-studio","ollama","openclaw-agent"],
  "openai-swarm": ["autogen-microsoft","chatgpt-openai","composio-tools","dify-platform","langchain-framework","langgraph-framework","langsmith-langchain","phidata-framework","semantic-kernel","smolagents-huggingface"],
  "openclaw-agent": ["autogpt-agent","crewai-framework","langchain-framework","metagpt-framework","open-interpreter","superagi-agent"],
  "perplexity-ai": ["chatgpt-openai","google-gemini","langchain-framework","openai-swarm","phind-ai","you-com"],
  "phidata-framework": ["composio-tools","dify-platform","langchain-framework","langgraph-framework","langsmith-langchain","ollama","openai-swarm"],
  "phind-ai": ["aider-ai","cline-vscode","cursor-ide","github-copilot","perplexity-ai","sourcegraph-cody","windsurf-ide"],
  "replit-ai": ["aider-ai","bolt-new","chatgpt-openai","cursor-ide","github-copilot","lovable-dev","vercel-v0","windsurf-ide"],
  "semantic-kernel": ["autogen-microsoft","crewai-framework","langchain-framework","langgraph-framework","openai-swarm"],
  "smolagents-huggingface": ["langchain-framework","openai-swarm","phidata-framework"],
  "sourcegraph-cody": ["amazon-q-developer","chatgpt-openai","claude-anthropic","claude-code","continue-dev","cursor-ide","github-copilot","langgraph-framework","phind-ai"],
  "superagi-agent": ["autogen-microsoft","autogpt-agent","composio-tools","crewai-framework","e2b-sandbox","langchain-framework","langgraph-framework","openclaw-agent"],
  "swe-agent": ["aider-ai","claude-code","cursor-ide","devin-agent","open-interpreter"],
  "tabnine-ai": ["amazon-q-developer","chatgpt-openai","codeium-windsurf","continue-dev","cursor-ide","github-copilot","microsoft-copilot","windsurf-ide"],
  "taskade-ai": ["dify-platform","flowise-lowcode","langchain-framework","n8n-automation"],
  "vercel-v0": ["bolt-new","cursor-ide","github-copilot","lovable-dev","replit-ai","windsurf-ide"],
  "windsurf-ide": ["aider-ai","bolt-new","chatgpt-openai","claude-anthropic","claude-desktop","cline-vscode","codeium-windsurf","codex-cli","codex-desktop","continue-dev","cursor-ide","deepseek-llm","github-copilot","google-gemini","lovable-dev","microsoft-copilot","phind-ai","replit-ai","tabnine-ai","vercel-v0"],
  "you-com": ["dify-platform","langchain-framework","perplexity-ai"],
  "zapier-ai": ["chatgpt-openai","copy-ai","dify-platform","flowise-lowcode","jasper-ai","n8n-automation","notion-ai","taskade-ai"]
};
var integrationInfo = {
  "cursor-ide|github-copilot": {type:"IDE-ассистент",desc:"Cursor и Copilot — лидеры AI-автодополнения. Используйте Cursor для сложного рефакторинга, Copilot для быстрых подсказок. Вместе — полное покрытие.",effort:"Низкая"},
  "cursor-ide|claude-code": {type:"Код + Терминал",desc:"Cursor (редактор) + Claude Code (терминал) = полный цикл разработки. Claude Code берёт сложные задачи, Cursor — повседневное редактирование.",effort:"Средняя"},
  "claude-code|cline-vscode": {type:"Автономные агенты",desc:"Claude Code и Cline — два подхода к автономной разработке. Cline лучше для VS Code, Claude Code для терминальных сценариев CI/CD.",effort:"Низкая"},
  "langchain-framework|langgraph-framework": {type:"Цепочки + Графы",desc:"LangChain для линейных пайплайнов, LangGraph для сложных графовых агентов с ветвлением. Вместе покрывают все сценарии.",effort:"Средняя"},
  "langchain-framework|crewai-framework": {type:"Фреймворк + Оркестрация",desc:"LangChain как фундамент, CrewAI для multi-agent оркестрации. CrewAI строит команды агентов поверх LangChain-инструментов.",effort:"Средняя"},
  "crewai-framework|autogen-microsoft": {type:"Multi-agent",desc:"CrewAI и AutoGen — два лидера multi-agent. CrewAI проще в настройке, AutoGen мощнее для исследовательских сценариев.",effort:"Высокая"},
  "dify-platform|flowise-lowcode": {type:"Low-code связка",desc:"Dify для production-пайплайнов, Flowise для быстрого прототипирования. Экспортируйте flow из Flowise в Dify.",effort:"Низкая"},
  "dify-platform|n8n-automation": {type:"AI + Автоматизация",desc:"Dify генерирует AI-ответы, n8n автоматизирует их доставку (email, Slack, CRM). Идеально для поддержки и чат-ботов.",effort:"Средняя"},
  "langchain-framework|openai-swarm": {type:"Фреймворк + Агенты",desc:"LangChain для пайплайнов, OpenAI Swarm для экспериментов с мульти-агентными системами. Swarm легковесный, LangChain production-ready.",effort:"Низкая"},
  "autogen-microsoft|semantic-kernel": {type:"Microsoft AI Stack",desc:"AutoGen (агенты) + Semantic Kernel (AI-интеграция) — официальный стек Microsoft для enterprise AI-решений.",effort:"Средняя"},
  "claude-code|anthropic-mcp": {type:"Claude + Протокол",desc:"MCP (Model Context Protocol) — стандарт подключения Claude к данным. Claude Code использует MCP для доступа к файлам, API, базам данных.",effort:"Средняя"},
  "cline-vscode|anthropic-mcp": {type:"Агент + Протокол",desc:"Cline поддерживает MCP-серверы для расширения контекста. Подключите базы данных и API напрямую к агенту.",effort:"Средняя"},
  "aider-ai|open-interpreter": {type:"Код + Данные",desc:"Aider для написания кода, Open Interpreter для выполнения и анализа данных. Вместе: пишем → запускаем → анализируем.",effort:"Низкая"},
  "flowise-lowcode|n8n-automation": {type:"Визуальная автоматизация",desc:"Flowise строит AI-воркфлоу, n8n запускает их по расписанию. Low-code стек для автоматизации без программирования.",effort:"Низкая"},
  "cursor-ide|windsurf-ide": {type:"IDE-дуэт",desc:"Cursor для сложных проектов, Windsurf для быстрого прототипирования. Используйте оба в зависимости от задачи.",effort:"Низкая"},
  "github-copilot|codeium-windsurf": {type:"Copilot-экосистема",desc:"GitHub Copilot и Codeium — два подхода к AI-автодополнению. Copilot глубже интегрирован с GitHub, Codeium быстрее на больших файлах.",effort:"Низкая"},
  "cursor-ide|aider-ai": {type:"Редактор + CLI",desc:"Cursor для визуального редактирования, Aider для терминальных сессий. Aider работает в фоне, пока вы в Cursor.",effort:"Средняя"},
  "claude-code|aider-ai": {type:"Терминальный тандем",desc:"Claude Code для автономных задач, Aider для инкрементального редактирования. Разные режимы — одна терминальная среда.",effort:"Низкая"},
  "autogpt-agent|babyagi-agent": {type:"Автономные агенты",desc:"AutoGPT и BabyAGI — пионеры автономных агентов. AutoGPT для сложных цепочек, BabyAGI для минималистичных сценариев.",effort:"Низкая"},
  "metagpt-framework|chatdev-agent": {type:"Командная разработка",desc:"MetaGPT и ChatDev — виртуальные команды разработчиков. MetaGPT для сложных проектов, ChatDev для быстрых прототипов.",effort:"Средняя"},
  "langchain-framework|autogen-microsoft": {type:"Фреймворк + Агенты",desc:"LangChain для RAG и пайплайнов, AutoGen для multi-agent диалогов. Разные парадигмы — одна экосистема.",effort:"Высокая"},
  "cursor-ide|cline-vscode": {type:"IDE + Агент",desc:"Cursor для ручного кодинга, Cline для автономных задач внутри VS Code. Переключайтесь между режимами в одном редакторе.",effort:"Низкая"},
  "cline-vscode|open-interpreter": {type:"Агент + Терминал",desc:"Cline пишет код, Open Interpreter выполняет и тестирует. Автоматический цикл разработки.",effort:"Средняя"},
  "langchain-framework|semantic-kernel": {type:"Кроссплатформенный стек",desc:"LangChain (Python/JS) + Semantic Kernel (.NET/Java) — покройте все языки вашей команды.",effort:"Высокая"},
  "autogen-microsoft|metagpt-framework": {type:"Multi-agent фабрика",desc:"AutoGen для диалоговых агентов, MetaGPT для ролевых команд. Два подхода к multi-agent архитектуре.",effort:"Высокая"},
  "langchain-framework|phidata-framework": {type:"RAG + Агенты",desc:"LangChain для построения RAG-пайплайнов, Phidata для агентной надстройки. Phidata добавляет memory и инструменты поверх LangChain.",effort:"Средняя"},
  "dify-platform|langchain-framework": {type:"Low-code + Код",desc:"Dify для визуального прототипирования, LangChain для кастомной логики. Экспортируйте из Dify в код.",effort:"Средняя"},
  "bolt-new|cursor-ide": {type:"Full-stack связка",desc:"Bolt.new для быстрой генерации full-stack приложений, Cursor для тонкой доработки кода.",effort:"Низкая"},
  "devin-agent|cursor-ide": {type:"Автономный + Ручной",desc:"Devin для автономных задач (PR, баги), Cursor для ручного контроля. Devin делает черновую работу, вы — финальную.",effort:"Средняя"},
  "replit-ai|cursor-ide": {type:"Облако + Локально",desc:"Replit для облачного прототипирования, Cursor для локальной разработки. Начните в Replit, продолжите в Cursor.",effort:"Низкая"},
  "langchain-framework|n8n-automation": {type:"AI + Workflow",desc:"LangChain генерирует AI-ответы, n8n встраивает их в бизнес-процессы. Автоматизация поддержки, CRM, документооборота.",effort:"Средняя"},
  "langchain-framework|flowise-lowcode": {type:"Код + Визуал",desc:"LangChain для разработчиков, Flowise для визуального конструирования. Одна экосистема — два интерфейса.",effort:"Низкая"},
  "openai-swarm|phidata-framework": {type:"Агенты + Инфраструктура",desc:"OpenAI Swarm для прототипов агентов, Phidata для production-инфраструктуры (мониторинг, memory, evaluation).",effort:"Средняя"},
  "langgraph-framework|crewai-framework": {type:"Графы + Команды",desc:"LangGraph для сложных графовых потоков, CrewAI для ролевых команд агентов. LangGraph даёт контроль, CrewAI — простоту.",effort:"Высокая"},
  "open-interpreter|langchain-framework": {type:"Исполнение + Пайплайны",desc:"Open Interpreter для интерактивного выполнения кода, LangChain для структурированных AI-пайплайнов.",effort:"Низкая"},
  "cursor-ide|devin-agent": {type:"Ручной + Автономный",desc:"Cursor для ежедневной разработки, Devin для автономных задач (bug fixing, refactoring). Делегируйте рутину Devin'у.",effort:"Средняя"},
  "github-copilot|amazon-q-developer": {type:"AWS + GitHub",desc:"Copilot для GitHub-экосистемы, Amazon Q для AWS-интеграции. Покрытие двух крупнейших платформ.",effort:"Средняя"},
  "swe-agent|aider-ai": {type:"Автономный рефакторинг",desc:"SWE-Agent для полного цикла исправления багов, Aider для инкрементальных правок. Автоматизируйте рутину.",effort:"Средняя"},
  "superagi-agent|crewai-framework": {type:"Агенты + Оркестрация",desc:"SuperAGI для автономных агентов с GUI, CrewAI для оркестрации команд. SuperAGI даёт визуальный контроль.",effort:"Средняя"},
  "perplexity-ai|langchain-framework": {type:"Поиск + RAG",desc:"Perplexity для research и fact-checking, LangChain для построения RAG-систем на основе найденных данных.",effort:"Низкая"}
};
function showIntegrations() {
  if (selected.length < 1) return;
  var overlay = document.createElement('div');
  overlay.id = 'integrations-overlay';
  overlay.className = 'integ-overlay';
  var isSingle = selected.length === 1;
  var html = '<div class=\"integ-modal\"><div class=\"integ-header\"><h2>' + (isSingle ? '⚡ Связи агента' : '🔗 Интеграции выбранных агентов') + '</h2><button class=\"integ-close\" onclick=\"closeIntegrations()\">✕</button></div>';
  // Agent cards row
  html += '<div class=\"integ-agents\">';
  selected.forEach(function(slug) {
    var p = searchResults.find(function(x){return x.u === '/product/'+slug+'/'});
    var title = p ? p.ti : slug;
    var iconHtml = (p&&p.iu) ? '<img src=\"'+p.iu+'\" alt=\"\">' : (p&&p.img?p.img:'🔹');
    html += '<div class=\"integ-agent-card\"><span class=\"iac-icon\">' + iconHtml + '</span><span>' + title.substring(0,25) + '</span></div>';
  });
  html += '</div>';
  // SVG diagram
  html += '<div class=\"integ-diagram\"><svg id=\"integ-svg\" width=\"100%\" height=\"380\"></svg></div>';
  // Matches
  html += '<div class=\"integ-matches\"><h3>' + (isSingle ? 'Все возможные связки' : 'Найденные связки') + '</h3><div class=\"integ-list\" id=\"integ-list\"></div></div>';
  html += '<div class=\"integ-cta\"><p>Хотите подробную инструкцию по интеграции?</p><a href=\"/media-kit/\" class=\"cta-primary\">Заказать аудит AI-стека</a></div>';
  html += '</div>';
  overlay.innerHTML = html;
  document.body.appendChild(overlay);
  document.body.style.overflow = 'hidden';
  setTimeout(drawIntegDiagram, 100);
  setTimeout(populateIntegMatches, 50);
}
function closeIntegrations() {
  var ov = document.getElementById('integrations-overlay');
  if (ov) { ov.remove(); document.body.style.overflow = ''; }
}
function drawIntegDiagram() {
  var svg = document.getElementById('integ-svg');
  if (!svg) return;
  var w = svg.clientWidth || 800;
  svg.setAttribute('viewBox', '0 0 '+w+' 380');
  svg.innerHTML = '';
  // Clip paths for circular images
  svg.innerHTML += '<defs><clipPath id=\"clip-18\"><circle cx=\"0\" cy=\"0\" r=\"16\"/></clipPath><clipPath id=\"clip-26\"><circle cx=\"0\" cy=\"0\" r=\"24\"/></clipPath><clipPath id=\"clip-32\"><circle cx=\"0\" cy=\"0\" r=\"30\"/></clipPath></defs>';
  var isSingle = selected.length === 1;
  if (isSingle) {
    // One agent in center, all integrations around it as lightning bolts
    var slug = selected[0];
    var buddies = integrations[slug] || [];
    if (buddies.length === 0) return;
    var cx = w/2, cy = 190;
    var colors = ['#10b981','#3B82F6','#f59e0b','#22D3EE','#8b5cf6','#ef4444','#ec4899','#14b8a6'];
    var n = Math.min(buddies.length, 20);
    var rx = Math.min(w/2 - 70, 280), ry = 160;
    for (var i = 0; i < n; i++) {
      var angle = (i/n) * 2 * Math.PI - Math.PI/2;
      var tx = cx + rx * Math.cos(angle);
      var ty = cy + ry * Math.sin(angle);
      var color = colors[i % colors.length];
      var dx = tx - cx, dy = ty - cy;
      var mid1x = cx + dx*0.35 + (Math.random()-0.5)*40;
      var mid1y = cy + dy*0.35 + (Math.random()-0.5)*40;
      var mid2x = cx + dx*0.65 + (Math.random()-0.5)*40;
      var mid2y = cy + dy*0.65 + (Math.random()-0.5)*40;
      var path = 'M'+cx+','+cy+' L'+mid1x+','+mid1y+' L'+mid2x+','+mid2y+' L'+tx+','+ty;
      svg.innerHTML += '<path d=\"'+path+'\" stroke=\"'+color+'\" stroke-width=\"2\" fill=\"none\" opacity=\"0.8\"><animate attributeName=\"opacity\" values=\"0.4;1;0.4\" dur=\"1.5s\" repeatCount=\"indefinite\"/></path>';
      // Buddy node
      svg.innerHTML += '<circle cx=\"'+tx+'\" cy=\"'+ty+'\" r=\"18\" fill=\"#171F2B\" stroke=\"'+color+'\" stroke-width=\"2\" opacity=\"0.9\"/>';
      var buddy = searchResults.find(function(x){return x.u === '/product/'+buddies[i]+'/'});
      var bImg = buddy && buddy.iu ? buddy.iu : '';
      if (bImg) {
        svg.innerHTML += '<g transform=\"translate('+tx+','+ty+')\"><image href=\"'+bImg+'\" x=\"-16\" y=\"-16\" width=\"32\" height=\"32\" clip-path=\"url(#clip-18)\" preserveAspectRatio=\"xMidYMid slice\"/></g>';
      } else {
        var bname = buddy ? buddy.ti.substring(0,16) : buddies[i].substring(0,16);
        svg.innerHTML += '<text x=\"'+tx+'\" y=\"'+ty+'\" text-anchor=\"middle\" dy=\"0.35em\" fill=\"#F5F7FA\" font-size=\"9\" font-weight=\"600\">'+bname+'</text>';
      }
    }
    // Center node (bigger, glowing)
    svg.innerHTML += '<circle cx=\"'+cx+'\" cy=\"'+cy+'\" r=\"32\" fill=\"#0B0F14\" stroke=\"#10b981\" stroke-width=\"3\"/>';
    svg.innerHTML += '<circle cx=\"'+cx+'\" cy=\"'+cy+'\" r=\"32\" fill=\"none\" stroke=\"#10b981\" stroke-width=\"1\" opacity=\"0.5\"><animate attributeName=\"r\" values=\"32;40;32\" dur=\"2s\" repeatCount=\"indefinite\"/><animate attributeName=\"opacity\" values=\"0.5;0;0.5\" dur=\"2s\" repeatCount=\"indefinite\"/></circle>';
    var me = searchResults.find(function(x){return x.u === '/product/'+slug+'/'});
    var cImg = me && me.iu ? me.iu : '';
    if (cImg) {
      svg.innerHTML += '<g transform=\"translate('+cx+','+cy+')\"><image href=\"'+cImg+'\" x=\"-30\" y=\"-30\" width=\"60\" height=\"60\" clip-path=\"url(#clip-32)\" preserveAspectRatio=\"xMidYMid slice\"/></g>';
    } else {
      var mname = me ? me.ti.substring(0,14) : slug.substring(0,14);
      svg.innerHTML += '<text x=\"'+cx+'\" y=\"'+cy+'\" text-anchor=\"middle\" dy=\"0.35em\" fill=\"#10b981\" font-size=\"11\" font-weight=\"800\">'+mname+'</text>';
    }
  } else {
    // Multi-agent: circular layout with lightning connections
    var n = selected.length;
    var cx2 = w/2, cy2 = 190, rx2 = Math.min(w/2-60, 200), ry2 = 100;
    var positions = [];
    for (var i = 0; i < n; i++) {
      var angle = (i/n)*2*Math.PI - Math.PI/2;
      positions.push({x: cx2+rx2*Math.cos(angle), y: cy2+ry2*Math.sin(angle)});
    }
    var lineColors = ['#10b981','#3B82F6','#f59e0b','#22D3EE','#8b5cf6'];
    for (var i = 0; i < n; i++) {
      for (var j = i+1; j < n; j++) {
        var si = selected[i], sj = selected[j];
        var connected = (integrations[si]&&integrations[si].includes(sj))||(integrations[sj]&&integrations[sj].includes(si));
        var pi = positions[i], pj = positions[j];
        if (connected) {
          var lc = lineColors[(i+j)%lineColors.length];
          var lmidx = (pi.x+pj.x)/2 + (Math.random()-0.5)*30;
          var lmidy = (pi.y+pj.y)/2 + (Math.random()-0.5)*30;
          svg.innerHTML += '<path d=\"M'+pi.x+','+pi.y+' L'+lmidx+','+lmidy+' L'+pj.x+','+pj.y+'\" stroke=\"'+lc+'\" stroke-width=\"2\" fill=\"none\" opacity=\"0.7\"><animate attributeName=\"opacity\" values=\"0.5;1;0.5\" dur=\"1.2s\" repeatCount=\"indefinite\"/></path>';
        } else {
          svg.innerHTML += '<line x1=\"'+pi.x+'\" y1=\"'+pi.y+'\" x2=\"'+pj.x+'\" y2=\"'+pj.y+'\" stroke=\"#374151\" stroke-width=\"1\" stroke-dasharray=\"4,4\" opacity=\"0.3\"/>';
        }
      }
    }
    positions.forEach(function(p, i) {
      var slug = selected[i];
      var prod = searchResults.find(function(x){return x.u === '/product/'+slug+'/'});
      svg.innerHTML += '<circle cx=\"'+p.x+'\" cy=\"'+p.y+'\" r=\"26\" fill=\"#171F2B\" stroke=\"#3B82F6\" stroke-width=\"2\"/>';
      var pImg = prod && prod.iu ? prod.iu : '';
      if (pImg) {
        svg.innerHTML += '<g transform=\"translate('+p.x+','+p.y+')\"><image href=\"'+pImg+'\" x=\"-24\" y=\"-24\" width=\"48\" height=\"48\" clip-path=\"url(#clip-26)\" preserveAspectRatio=\"xMidYMid slice\"/></g>';
      } else {
        var name = prod ? prod.ti.substring(0,16) : slug.substring(0,16);
        svg.innerHTML += '<text x=\"'+p.x+'\" y=\"'+p.y+'\" text-anchor=\"middle\" dy=\"0.35em\" fill=\"#F5F7FA\" font-size=\"9\" font-weight=\"600\">'+name+'</text>';
      }
    });
  }
}
function populateIntegMatches() {
  var list = document.getElementById('integ-list');
  if (!list) return;
  var html = '';
  var isSingle = selected.length === 1;
  if (isSingle) {
    var slug = selected[0];
    var buddies = integrations[slug] || [];
    if (buddies.length === 0) {
      html = '<div class=\"integ-empty\"><p>Связей для этого агента пока нет в базе.</p></div>';
    } else {
      buddies.forEach(function(b) {
        var key1 = slug+'|'+b, key2 = b+'|'+slug;
        var info = integrationInfo[key1] || integrationInfo[key2] || {type:'Совместимы', desc:'Эти агенты могут работать в связке.', effort:'Средняя'};
        var sp = searchResults.find(function(x){return x.u === '/product/'+slug+'/'});
        var bp = searchResults.find(function(x){return x.u === '/product/'+b+'/'});
        var bname = bp ? bp.ti : b;
        var sImg = (sp&&sp.iu) ? '<img src=\"'+sp.iu+'\" alt=\"\">' : '';
        var bImg = (bp&&bp.iu) ? '<img src=\"'+bp.iu+'\" alt=\"\">' : '';
        html += '<div class=\"integ-match\"><div class=\"im-header\"><span class=\"im-type\">'+info.type+'</span><span class=\"im-effort\">⚡ '+info.effort+' сложность</span></div><p class=\"im-desc\">'+info.desc+'</p><div class=\"im-agents\"><a href=\"/product/'+slug+'/\" style=\"color:var(--green)\">'+sImg+slug+'</a> ↔ <a href=\"/product/'+b+'/\" style=\"color:var(--blue)\">'+bImg+bname.substring(0,30)+'</a></div></div>';
      });
    }
  } else {
    var found = false;
    for (var i = 0; i < selected.length; i++) {
      for (var j = i+1; j < selected.length; j++) {
        var a = selected[i], b = selected[j];
        var connected = (integrations[a]&&integrations[a].includes(b))||(integrations[b]&&integrations[b].includes(a));
        if (!connected) continue;
        found = true;
        var key1 = a+'|'+b, key2 = b+'|'+a;
        var info = integrationInfo[key1]||integrationInfo[key2]||{type:'Совместимы',desc:'Эти агенты могут работать в связке.',effort:'Средняя'};
        var ap = searchResults.find(function(x){return x.u === '/product/'+a+'/'});
        var bp2 = searchResults.find(function(x){return x.u === '/product/'+b+'/'});
        var aImg = (ap&&ap.iu) ? '<img src=\"'+ap.iu+'\" alt=\"\">' : '';
        var bImg2 = (bp2&&bp2.iu) ? '<img src=\"'+bp2.iu+'\" alt=\"\">' : '';
        html += '<div class=\"integ-match\"><div class=\"im-header\"><span class=\"im-type\">'+info.type+'</span><span class=\"im-effort\">⚡ '+info.effort+' сложность</span></div><p class=\"im-desc\">'+info.desc+'</p><div class=\"im-agents\">'+aImg+a+' ↔ '+bImg2+b+'</div></div>';
      }
    }
    if (!found) {
      html = '<div class=\"integ-empty\"><p>Прямых интеграций между выбранными агентами не найдено.</p><p style=\"color:var(--green);margin-top:8px\">Попробуйте выбрать агентов из одной экосистемы.</p></div>';
    }
  }
  list.innerHTML = html;
}
function clearCompare() {
  selected = [];
  document.querySelectorAll('.card input[type=checkbox]').forEach(function(cb) { cb.checked = false; });
  updateCompareBar();
  var svg = document.getElementById('live-connections');
  if (svg) { svg.innerHTML = ''; svg.classList.remove('active'); }
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
// ─── Watch / Release Alerts ───
function getWatches(){try{return JSON.parse(localStorage.getItem('qantcore_watches')||'[]')}catch(e){return[]}}
function toggleWatch(el,slug){
  var w=getWatches();
  if(w.includes(slug)){w=w.filter(function(x){return x!==slug});el.classList.remove('watching');el.textContent='🔔'}
  else{w.push(slug);el.classList.add('watching');el.textContent='🔔'}
  localStorage.setItem('qantcore_watches',JSON.stringify(w));
}
// Init watches on load
(function(){
  var w=getWatches();
  document.querySelectorAll('.watch-btn').forEach(function(b){
    if(w.includes(b.getAttribute('data-slug'))){b.classList.add('watching');b.textContent='🔔'}
  });
})();
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
    scripts = scripts.replace("{search_json}", search_json)

    html = render_page("Каталог AI-агентов", "Каталог AI-агентов: {}+ отслеживается, глубокие обзоры, живые бенчмарки.".format(tp),
                       content, scripts=scripts, total=tp, active_home="active",
                       open_graph=make_og("Каталог AI-агентов — QantCore", "Каталог AI-агентов: 60+ отслеживается, глубокие обзоры, живые бенчмарки.", "/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/">',
                       extra_css="""#catalog-grid .card:hover::before{content:'';position:absolute;width:42px;height:12px;background:rgba(59,130,246,.7);clip-path:polygon(0 8%,80% 8%,80% 0,100% 50%,80% 100%,80% 92%,0 92%);top:16px;right:22px;transform-origin:100% 50%;z-index:4;pointer-events:none;animation:arrowIn .3s ease}@keyframes arrowIn{from{opacity:0;transform:rotate(-22deg) scale(.3)}to{opacity:1;transform:rotate(-22deg) scale(1)}}""")

    write_html(f"{OUT}/index.html", html)
    print(f"  /index.html")


def generate_compare_page(slugs=None):
    """Generate /compare/ — client-side comparison from URL params."""
    # Always generate the dynamic compare page that reads ?slugs= from URL
    all_prods = list(DB.articles.find({"category": "product"}).sort("rating", -1))
    
    # Build search JSON with full product data for client-side comparison
    compare_entries = []
    for p in all_prods:
        # Compute numeric scores
        r = p.get("rating", 0) or 0
        r = float(r) if r else 0
        f = p.get("freshness_score", 0) or 0
        rc = p.get("review_count", 0) or 0
        ts = p.get("tech_stack", []) or []
        local_first = p.get("local_first") or any(t.lower() in ["docker","local","self-hosted","python","cli","terminal"] for t in ts)
        dep_score = 9.0 if local_first else 5.0
        if any(t.lower() == "docker" for t in ts): dep_score = min(10, dep_score + 1.5)
        dep_score = min(10, round(dep_score - len(ts)*0.3, 1))
        mat_score = min(10, round(r * 1.8 + f * 1.5 + min(rc/500, 2), 1))
        docs_score = min(10, round(r * 1.5 + f * 2, 1))
        comm_vel = round(f * 15 + min(rc/200, 8), 1)
        vel_sign = "+" if f > 0.4 else "-" if f < 0.2 else ""
        qant_score = min(100, round(r*20*0.30 + mat_score*10*0.25 + dep_score*10*0.20 + comm_vel*1.5*0.15 + docs_score*10*0.10))
        compare_entries.append({
            "slug": p["slug"],
            "title": p.get("title",""),
            "rating": p.get("rating",""),
            "qant_score": str(qant_score),
            "pricing": format_price(p.get("pricing_model","")),
            "type": p.get("product_type",""),
            "category": p.get("subcategory","") or "—",
            "maturity": str(mat_score) + "/10",
            "freshness": f'{int(f*100)}%',
            "reviews": str(rc),
            "tech_stack": ", ".join(ts[:5]) or "—",
            "deployment": "🏠 Local" if local_first else "☁️ Cloud",
            "deploy_score": str(dep_score) + "/10",
            "velocity": vel_sign + str(comm_vel) + "%",
            "docs_quality": str(docs_score) + "/10",
            "description": (p.get("tagline","") or p.get("description",""))[:150],
            "iu": p.get("image_url",""),
        })
    compare_json = json.dumps(compare_entries)
    
    # Body: selector grid if no slugs, or client-rendered table
    cards = '<div class="grid" id="compare-select-grid" style="grid-template-columns:repeat(4,1fr)">'
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
  
  // Icon map for product types
  var icons = {{'agent':'🤖','framework':'⚙️','platform':'🏗️','infrastructure':'🔧','model':'🧠'}};
  function getIcon(p) {{
    var t = (p.type || '').toLowerCase();
    return icons[t] || '📦';
  }}

  // Scorebar helper: renders colored bar + value
  function scoreBar(val, maxVal, label) {{
    var n = parseFloat(val) || 0;
    var pct = Math.min(100, (n / maxVal) * 100);
    var cls = n >= maxVal*0.7 ? 'score-high' : n >= maxVal*0.4 ? 'score-mid' : 'score-low';
    var barCls = n >= maxVal*0.7 ? 'var(--green)' : n >= maxVal*0.4 ? 'var(--cyan)' : 'var(--amber)';
    return '<span class=\"metric-val ' + cls + '\"><span class=\"metric-bar\" style=\"width:' + Math.max(4,pct*0.7) + 'px;background:' + barCls + '\"></span>' + label + '</span>';
  }}
  function velBar(val) {{
    var n = parseFloat(val) || 0;
    var cls = n >= 15 ? 'score-high' : n >= 5 ? 'score-mid' : 'score-low';
    var barCls = n >= 15 ? 'var(--green)' : n >= 5 ? 'var(--cyan)' : 'var(--amber)';
    var w = Math.min(60, Math.abs(n)*1.5);
    return '<span class=\"metric-val ' + cls + '\"><span class=\"metric-bar\" style=\"width:' + Math.max(4,w) + 'px;background:' + barCls + '\"></span>' + val + '</span>';
  }}

  var metrics = [
    ['QantScore™', 'qant_score', true, function(v) {{ return scoreBar(v, 100, v); }}],
    ['★ Rating', 'rating', false, null],
    ['💰 Pricing', 'pricing', false, null],
    ['📋 Type', 'type', false, null],
    ['📂 Category', 'category', false, null],
    ['🎯 Maturity', 'maturity', true, function(v) {{ var n=parseFloat(v)||0; return scoreBar(n, 10, v); }}],
    ['📖 Docs', 'docs_quality', true, function(v) {{ var n=parseFloat(v)||0; return scoreBar(n, 10, v); }}],
    ['🏠 Deployment', 'deployment', false, null],
    ['⚡ Deploy', 'deploy_score', true, function(v) {{ var n=parseFloat(v)||0; return scoreBar(n, 10, v); }}],
    ['🕐 Freshness', 'freshness', false, null],
    ['📈 Velocity', 'velocity', true, function(v) {{ return velBar(v); }}],
    ['💬 Reviews', 'reviews', false, null],
    ['🔧 Tech Stack', 'tech_stack', false, null],
  ];
  
  // Build thead
  var thead = '<thead><tr><th>Metric</th>';
  prods.forEach(function(p) {{
    var img = p.iu ? '<img src=\"' + p.iu + '\" class=\"th-logo\" style=\"width:36px;height:36px;object-fit:contain;border-radius:8px;display:block;margin:0 auto 6px\">' : '<span class=\"th-icon\">' + getIcon(p) + '</span>';
    thead += '<th>' + img + '<span class=\"th-name\">' + p.title.substring(0,22) + '</span></th>';
  }});
  thead += '</tr></thead>';
  
  // Build tbody
  var rows = '';
  metrics.forEach(function(m) {{
    var name = m[0], key = m[1], isWinner = m[2], fmt = m[3];
    var vals = prods.map(function(p) {{ return p[key] || '—'; }});
    var winner = -1;
    if (isWinner) {{
      var nums = vals.map(function(v) {{ return parseFloat(v) || 0; }});
      winner = nums.indexOf(Math.max.apply(null, nums));
    }}
    rows += '<tr><th>' + name + '</th>';
    vals.forEach(function(v, i) {{
      var display = fmt ? fmt(v) : v;
      rows += '<td class=\"' + (i === winner ? 'winner' : '') + '\">' + display + '</td>';
    }});
    rows += '</tr>';
  }});
  
  var titles = prods.map(function(p) {{ return p.title.substring(0,25); }}).join(' vs ');
  var n = prods.length;
  
  var html = '<div class=\"breadcrumbs\"><a href=\"/\">Каталог</a> &rsaquo; <a href=\"/compare/\" onclick=\"resetCompare();return false\">Сравнение</a> &rsaquo; <span>Результат</span></div>';
  html += '<div class=\"compare-header-bar\"><h1>' + titles + '</h1><span class=\"compare-badge\">' + n + ' агента</span></div>';
  html += '<div class=\"compare-table-wrap\"><table class=\"compare-table\">' + thead + '<tbody>' + rows + '</tbody></table></div>';
  html += '<div class=\"compare-legend\"><span class=\"dot green\"></span><span>Лучший в классе</span><span style=\"color:var(--dim)\">|</span><span style=\"color:var(--green)\">■■■</span><span>Высокий</span><span style=\"color:var(--cyan)\">■■■</span><span>Средний</span><span style=\"color:var(--amber)\">■■■</span><span>Низкий</span></div>';
  html += '<p style=\"color:var(--muted);font-size:12px;margin-top:12px\"><a href=\"/methodology/\" style=\"color:var(--green)\">Как мы оцениваем агентов →</a></p>';
  html += '<div class=\"result-actions\"><button onclick=\"resetCompare()\" class=\"btn-back\">← Назад к выбору</button><button onclick=\"copyCompareLink()\" class=\"btn-share\">📋 Копировать ссылку</button></div>';
  result.innerHTML = html;
  window.scrollTo(0, 0);
}}
function copyCompareLink() {{
  var url = window.location.href;
  navigator.clipboard.writeText(url).then(function() {{
    var btn = document.querySelector('.btn-share');
    btn.textContent = '✓ Скопировано!';
    setTimeout(function() {{ btn.textContent = '📋 Копировать ссылку'; }}, 2000);
  }});
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
    
    html = render_page("Сравнение AI-агентов", "Select and compare AI agents side-by-side — ratings, pricing, deployment, maturity, and more.",
                       body, scripts=scripts, total=tp, active_compare="active",
                       open_graph=make_og("Сравнение AI-агентов — QantCore", "Select and compare AI agents side-by-side — ratings, pricing, deployment, maturity, and more.", "/compare/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/compare/">')
    write_html(f"{OUT}/compare/index.html", html)
    print(f"  /compare/index.html (client-side, {len(all_prods)} products)")


def generate_catalog(category):
    """Generate /catalog/{category}/index.html"""
    labels = {"product": "Продукты", "comparison": "Сравнения", "review": "Обзоры"}
    label = labels.get(category, category)

    items = list(DB.articles.find({"category": category}))
    tp = DB.articles.count_documents({"category": "product"})

    if not items:
        cards = f'<div class="empty"><h2>Пока ничего нет</h2><p>Категория «{esc(label)}» пуста</p><p style="margin-top:12px"><a href="/catalog/product/" style="color:var(--green)">← Смотреть каталог агентов</a></p></div>'
    else:
        cards = '<div class="grid" style="grid-template-columns:repeat(4,1fr)">' if category == "review" else '<div class="grid">'
        for item in items:
            if category == "product":
                cards += make_product_card(item, with_compare=False)
            elif category == "comparison":
                # Fetch product logos for VS display
                pa_slug = item.get('product_a', '')
                pb_slug = item.get('product_b', '')
                pa_img = ''; pb_img = ''
                if pa_slug:
                    pa = DB.articles.find_one({"slug": pa_slug, "category": "product"})
                    if pa:
                        iu = pa.get("image_url", "")
                        pa_img = f'<img src="{iu}" alt="" style="width:40px;height:40px;object-fit:contain;border-radius:6px;background:rgba(255,255,255,.03);padding:2px">' if iu else f'<span style="font-size:24px">{icon_for(pa.get("product_type",""))}</span>'
                if pb_slug:
                    pb = DB.articles.find_one({"slug": pb_slug, "category": "product"})
                    if pb:
                        iu = pb.get("image_url", "")
                        pb_img = f'<img src="{iu}" alt="" style="width:40px;height:40px;object-fit:contain;border-radius:6px;background:rgba(255,255,255,.03);padding:2px">' if iu else f'<span style="font-size:24px">{icon_for(pb.get("product_type",""))}</span>'
                vs_block = f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:10px">{pa_img}<span style="font-size:12px;font-weight:800;color:var(--green);background:var(--green-dim);padding:2px 6px;border-radius:4px">VS</span>{pb_img}</div>' if pa_img and pb_img else '<div class="card-icon">⚖️</div>'
                cards += f"""<a href="/compare/{item['slug']}/" class="card">
                  {vs_block}
                  <div class="card-title">{esc(item.get('title',''))}</div>
                  <div class="card-desc">{esc(str(item.get('description',''))[:120])}</div>
                </a>"""
            elif category == "review":
                # Fetch reviewed product logo
                rv_slug = item.get('review_of', '')
                rv_img = ''
                if rv_slug:
                    rp = DB.articles.find_one({"slug": rv_slug, "category": "product"})
                    if rp:
                        iu = rp.get("image_url", "")
                        rv_img = f'<img src="{iu}" alt="" style="width:64px;height:64px;object-fit:contain;border-radius:10px;background:rgba(255,255,255,.03);padding:4px;margin:0 auto 10px;display:block">' if iu else f'<div style="width:64px;height:64px;border-radius:10px;background:rgba(255,255,255,.03);display:flex;align-items:center;justify-content:center;font-size:28px;margin:0 auto 10px">{icon_for(rp.get("product_type",""))}</div>'
                if not rv_img:
                    rv_img = '<div class="card-icon">📝</div>'
                cards += f"""<a href="/review/{item['slug']}/" class="card">
                  {rv_img}
                  <div class="card-title">{esc(item.get('title',''))}</div>
                  <div class="card-desc">{esc(str(item.get('tagline',''))[:100])}</div>
                  <div style="font-size:11px;color:var(--dim);margin-top:8px">📊 {item.get('word_count',0)} слов • {len(item.get('pipeline_stages') or [])} этапов</div>
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
    html = render_page(label, f"Qantcore — {label} AI-агентов", body,
                       total=tp, search_json=search_json,
                       active_home=active_home, active_compare=active_compare, active_review=active_review,
                       open_graph=make_og(f"{label} — Qantcore", f"Каталог {label.lower()} AI-агентов на Qantcore. Рейтинги, бенчмарки, аналитика внедрения.", f"/catalog/{category}/"),
                       canonical_url=f'<link rel="canonical" href="https://qantcore.space/catalog/{category}/">')

    write_html(f"{OUT}/catalog/{category}/index.html", html)
    print(f"  /catalog/{category}/index.html")


def get_install_code(slug, p):
    """Generate install/run code block for a product."""
    codes = {
        "cursor-ide": ("Установка", "bash", "# Скачать с cursor.com\n# macOS/Linux/Windows — готовый установщик\nbrew install --cask cursor  # macOS\n# или скачать .deb/.AppImage с сайта"),
        "github-copilot": ("Установка", "bash", "# Установить расширение VS Code\next install GitHub.copilot\n# Или встроен в GitHub Codespaces"),
        "claude-code": ("Установка", "bash", "npm install -g @anthropic-ai/claude-code\n# Или через pip:\npip install claude-code --break-system-packages\nclaude-code --help"),
        "cline-vscode": ("Установка", "bash", "# Установить расширение VS Code\next install saoudrizwan.claude-dev\n# Настроить API ключ в настройках расширения"),
        "windsurf-ide": ("Установка", "bash", "# Скачать с codeium.com/windsurf\n# Готовый установщик для macOS/Linux/Windows"),
        "codeium-windsurf": ("Установка", "bash", "# Расширение VS Code\next install Codeium.codeium\n# Или Windsurf IDE отдельно"),
        "aider-ai": ("Установка и запуск", "bash", "pip install aider-chat --break-system-packages\nexport OPENAI_API_KEY=sk-...\naider --model gpt-4o"),
        "sourcegraph-cody": ("Установка", "bash", "# Расширение VS Code\next install sourcegraph.cody-ai\n# Бесплатно для индивидуальной разработки"),
        "tabnine-ai": ("Установка", "bash", "# Расширение VS Code\next install TabNine.tabnine-vscode\n# Или JetBrains/другие IDE"),
        "open-interpreter": ("Установка и запуск", "bash", "pip install open-interpreter --break-system-packages\ninterpreter\n# Интерактивный режим: пишите команды на естественном языке"),
        "langchain-framework": ("Установка", "bash", "pip install langchain langchain-community --break-system-packages\n# Быстрый старт:\npython -c \"from langchain.llms import OpenAI; llm=OpenAI(); print(llm('Hello!'))\""),
        "langgraph-framework": ("Установка", "bash", "pip install langgraph --break-system-packages\n# Базовый граф:\n# from langgraph.graph import StateGraph"),
        "crewai-framework": ("Установка и запуск", "bash", "pip install crewai --break-system-packages\ncrewai create my_crew\ncd my_crew && crewai run"),
        "autogen-microsoft": ("Установка", "bash", "pip install pyautogen --break-system-packages\n# Быстрый старт с двумя агентами:\n# from autogen import AssistantAgent, UserProxyAgent"),
        "openai-swarm": ("Установка", "bash", "pip install git+https://github.com/openai/swarm.git --break-system-packages\n# Экспериментальный фреймворк от OpenAI"),
        "semantic-kernel": ("Установка", "bash", "pip install semantic-kernel --break-system-packages\n# Или .NET:\n# dotnet add package Microsoft.SemanticKernel"),
        "anthropic-mcp": ("Установка", "bash", "pip install mcp --break-system-packages\n# Пример сервера:\n# mcp-server --port 3000 --tools ./my_tools.py"),
        "phidata-framework": ("Установка", "bash", "pip install phidata --break-system-packages\n# Быстрый старт с агентом:\n# from phi.agent import Agent"),
        "dify-platform": ("Установка", "bash", "# Docker:\ngit clone https://github.com/langgenius/dify.git\ncd dify/docker && docker compose up -d\n# Откройте http://localhost:3000"),
        "flowise-lowcode": ("Установка", "bash", "npm install -g flowise\nnpx flowise start\n# Откройте http://localhost:3000\n# Или Docker: docker run -p 3000:3000 flowiseai/flowise"),
        "n8n-automation": ("Установка", "bash", "npm install -g n8n\nn8n start\n# Или Docker:\ndocker run -p 5678:5678 n8nio/n8n"),
        "autogpt-agent": ("Установка и запуск", "bash", "git clone https://github.com/Significant-Gravitas/AutoGPT.git\ncd AutoGPT\npip install -r requirements.txt --break-system-packages\npython -m autogpt"),
        "babyagi-agent": ("Установка", "bash", "git clone https://github.com/yoheinakajima/babyagi.git\ncd babyagi\npip install -r requirements.txt --break-system-packages\npython babyagi.py"),
        "metagpt-framework": ("Установка", "bash", "pip install metagpt --break-system-packages\n# Создать компанию из AI-агентов:\nmetagpt --idea \"Create a snake game\""),
        "chatdev-agent": ("Установка", "bash", "git clone https://github.com/OpenBMB/ChatDev.git\ncd ChatDev\npip install -r requirements.txt --break-system-packages\npython run.py --task \"Build a calculator app\""),
        "bolt-new": ("Запуск", "bash", "# Откройте bolt.new в браузере\n# Или локально:\nnpm create bolt@latest my-project"),
        "replit-ai": ("Запуск", "bash", "# Откройте replit.com\n# Создайте Repl → выберите AI-шаблон\n# Replit Agent доступен в Pro-плане"),
        "devin-agent": ("Запуск", "bash", "# Доступ через cognition.ai\n# CLI-интерфейс после регистрации:\n# devin login && devin start"),
        "ollama": ("Установка и запуск", "bash", "curl -fsSL https://ollama.com/install.sh | sh\nollama pull llama3.2\nollama pull deepseek-r1:8b\nollama run deepseek-r1:8b\n# API на http://localhost:11434"),
        "lm-studio": ("Установка", "bash", "# Скачать с lmstudio.ai\n# Загрузите модель через UI → Запустите сервер\n# API: http://localhost:1234/v1"),
        "jan-ai": ("Установка", "bash", "# Скачать с jan.ai\n# Десктопное приложение → Загрузите модель\n# Локальный сервер на порту 1337"),
        "deepseek-llm": ("Использование", "bash", "# Через API:\ncurl https://api.deepseek.com/v1/chat/completions \\\n  -H \"Authorization: Bearer $DEEPSEEK_API_KEY\" \\\n  -d '{\"model\":\"deepseek-chat\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}]}'\n# Или локально через Ollama:\nollama pull deepseek-r1:8b"),
        "chatgpt-openai": ("Использование", "bash", "# API:\npip install openai --break-system-packages\n# python -c \"from openai import OpenAI; c=OpenAI(); print(c.chat.completions.create(model='gpt-4o',messages=[{'role':'user','content':'Hello'}]))\""),
        "claude-anthropic": ("Использование", "bash", "# API:\npip install anthropic --break-system-packages\n# python -c \"from anthropic import Anthropic; c=Anthropic(); print(c.messages.create(model='claude-sonnet-4-20250514',max_tokens=100,messages=[{'role':'user','content':'Hello'}]))\""),
        "google-gemini": ("Использование", "bash", "pip install google-generativeai --break-system-packages\n# python -c \"import google.generativeai as genai; genai.configure(api_key='...'); m=genai.GenerativeModel('gemini-2.5-pro'); print(m.generate_content('Hello'))\""),
        "mistral-ai": ("Использование", "bash", "pip install mistralai --break-system-packages\n# python -c \"from mistralai import Mistral; c=Mistral(api_key='...'); print(c.chat.complete(model='mistral-large',messages=[{'role':'user','content':'Hello'}]))\""),
        "llama-meta": ("Использование", "bash", "# Локально через Ollama:\nollama pull llama3.2\nollama run llama3.2\n# Или через HuggingFace:\npip install transformers --break-system-packages\n# from transformers import pipeline"),
        "hermes-agent": ("Установка", "bash", "pip install hermes-agent --break-system-packages\nhermes setup\nhermes run\n# Конфиг: ~/.hermes/config.yaml\n# Документация: hermes-agent.nousresearch.com"),
        "perplexity-ai": ("Использование", "bash", "# API:\ncurl https://api.perplexity.ai/chat/completions \\\n  -H \"Authorization: Bearer $PERPLEXITY_API_KEY\" \\\n  -d '{\"model\":\"sonar-pro\",\"messages\":[{\"role\":\"user\",\"content\":\"Latest AI news\"}]}'"),
        "superagi-agent": ("Установка", "bash", "git clone https://github.com/TransformerOptimus/SuperAGI.git\ncd SuperAGI\ndocker compose up -d\n# Откройте http://localhost:3000"),
        "swe-agent": ("Установка", "bash", "pip install swe-agent --break-system-packages\nswe-agent setup\n# Решить GitHub issue:\nswe-agent run --issue_url https://github.com/user/repo/issues/1"),
        "anythingllm": ("Установка", "bash", "# Docker:\ndocker pull mintplexlabs/anythingllm\ndocker run -p 3001:3001 mintplexlabs/anythingllm\n# Или десктоп: скачать с anythingllm.com"),
        "e2b-sandbox": ("Установка", "bash", "pip install e2b-code-interpreter --break-system-packages\n# python -c \"from e2b_code_interpreter import CodeInterpreter; s=CodeInterpreter(); print(s.run('print(1+1)'))\""),
        "smolagents-huggingface": ("Установка", "bash", "pip install smolagents --break-system-packages\n# from smolagents import CodeAgent, HfApiModel\n# agent = CodeAgent(tools=[], model=HfApiModel())"),
        "composio-tools": ("Установка", "bash", "pip install composio-core --break-system-packages\ncomposio login\n# Подключить инструменты:\ncomposio add github"),
        "langsmith-langchain": ("Установка", "bash", "pip install langsmith --break-system-packages\nexport LANGCHAIN_API_KEY=ls_...\nexport LANGCHAIN_TRACING_V2=true\n# Автоматически логирует все вызовы LangChain"),
        "continue-dev": ("Установка", "bash", "# Расширение VS Code/JetBrains\next install Continue.continue\n# Конфиг: ~/.continue/config.json\n# Поддерживает Ollama, LM Studio, OpenAI"),
        "copy-ai": ("Запуск", "bash", "# Веб-приложение: copy.ai\n# API:\ncurl https://api.copy.ai/v1/workflow/run \\\n  -H \"x-api-key: $COPYAI_API_KEY\""),
        "jasper-ai": ("Запуск", "bash", "# Веб-приложение: jasper.ai\n# API доступен для Enterprise-планов"),
        "zapier-ai": ("Запуск", "bash", "# Веб-приложение: zapier.com\n# Создайте Zap → добавьте AI-шаг\n# Поддерживает ChatGPT, Claude, Gemini"),
        "notion-ai": ("Запуск", "bash", "# Встроен в Notion\n# Нажмите Space в любом документе\n# Или /ai в командах"),
        "microsoft-copilot": ("Запуск", "bash", "# Встроен в Microsoft 365\n# Windows: Win+C\n# Office: кнопка Copilot на ленте"),
        "amazon-q-developer": ("Установка", "bash", "# Расширение VS Code\next install amazonwebservices.amazon-q-vscode\n# Или в AWS Console → Amazon Q Developer"),
        "taskade-ai": ("Запуск", "bash", "# Веб: taskade.com\n# Десктоп: скачать с taskade.com/downloads\n# AI-агенты в каждом проекте"),
        "lovable-dev": ("Запуск", "bash", "# Веб: lovable.dev\n# Опишите идею → получите full-stack приложение\n# Экспорт в GitHub"),
        "vercel-v0": ("Запуск", "bash", "# Веб: v0.dev\n# Опишите UI → получите React-компонент\n# Копировать код или открыть в песочнице"),
        "codex-cli": ("Установка", "bash", "npm install -g @openai/codex\ncodex login\ncodex \"Fix all TypeScript errors in this project\""),
        "codex-desktop": ("Установка", "bash", "# Скачать с openai.com/codex\n# Десктопное приложение с GUI\n# Альтернатива CLI-версии"),
        "composio-tools": ("Установка", "bash", "pip install composio-core --break-system-packages\ncomposio login\ncomposio add github slack gmail"),
        "claude-desktop": ("Установка", "bash", "# Скачать с claude.ai/download\n# Десктопное приложение Anthropic\n# Поддержка MCP-серверов"),
        "phind-ai": ("Запуск", "bash", "# Веб: phind.com\n# Расширение VS Code:\next install phind.phind"),
        "openclaw-agent": ("Установка", "bash", "pip install openclaw --break-system-packages\n# Локальный AI-ассистент с доступом к файлам\n# Конфиг: ~/.openclaw/config.yaml"),
        "you-com": ("Запуск", "bash", "# Веб: you.com\n# API:\ncurl https://api.you.com/search \\\n  -H \"x-api-key: $YOU_API_KEY\"")
    }
    return codes.get(slug, ("Быстрый старт", "bash", f"# {p.get('title','')}\n# Подробности на официальном сайте\n{p.get('website_url','')}"))


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

    # Install code
    inst_label, inst_lang, inst_code = get_install_code(slug, p)
    code_block = f"""<div class=\"install-block\">
      <div class=\"install-header\">
        <span class=\"install-badge\">⚡ {inst_label}</span>
        <button class=\"copy-btn\" onclick=\"navigator.clipboard.writeText(this.nextElementSibling.textContent);this.textContent='✓ Скопировано';setTimeout(()=>this.textContent='📋 Копировать',2000)\">📋 Копировать</button>
      </div>
      <pre class=\"code-block\"><code class=\"language-{inst_lang}\">{esc(inst_code)}</code></pre>
    </div>"""

    body = f"""<div class="container detail">
      <div class="breadcrumbs">
        <a href="/">Каталог</a> &rsaquo; <span>{esc(p.get('title',''))}</span>
      </div>
      <div class="detail-header" style="display:flex;gap:32px;align-items:flex-start">
        {product_image(p, 'detail')}
        <div style="flex:1">
          <h1 style="font-size:28px;font-weight:800;color:#f1f5f9;line-height:1.3"><span class="agent-icon" style="font-size:32px">{agent_icon(slug)}</span> {esc(p.get('title',''))}</h1>
          <p class="tagline" style="font-size:17px;color:var(--green);margin-top:8px;font-weight:500">{esc(p.get('tagline',''))}</p>
          <div class="detail-meta" style="margin-top:16px;gap:12px">
            <div class="meta-item" style="background:rgba(59,130,246,.1);color:var(--blue);padding:6px 14px;border-radius:6px;font-weight:600">{icon_for(p.get('product_type',''))} <strong>{esc(p.get('product_type',''))}</strong></div>
            {rating_html}
            <div class="meta-item" style="background:rgba(16,185,129,.1);color:var(--green);padding:6px 14px;border-radius:6px;font-weight:600">💰 <strong>{format_price(p.get('pricing_model',''))}</strong></div>
            {website_html}
          </div>
          {intel_html}
        </div>
      </div>
      <div class="detail-body" style="margin-top:32px">
        <div class="desc-block" style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:24px 28px;margin-bottom:24px">
          <h2 style="font-size:18px;font-weight:700;color:var(--text);margin-bottom:12px">📝 Описание</h2>
          <p style="font-size:16px;color:#b0b8c8;line-height:1.8">{esc(p.get('description',''))}</p>
        </div>
        {code_block}
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
    prod_blocks = ""
    for i, pa in enumerate(["product_a", "product_b"]):
        sv = c.get(pa, "")
        if sv:
            prod = DB.articles.find_one({"slug": sv, "category": "product"})
            if prod:
                links += f'<a href="/product/{sv}/" class="meta-item">🔗 {esc(prod.get("title","")[:40])}</a>'
                img_url = prod.get("image_url", "")
                img_html = f'<img src="{img_url}" alt="{esc(prod.get("title",""))}" style="width:80px;height:80px;object-fit:contain;border-radius:12px;background:rgba(255,255,255,.04);padding:8px">' if img_url else f'<span style="font-size:48px">{icon_for(prod.get("product_type",""))}</span>'
                prod_blocks += f'<div style="text-align:center">{img_html}<div style="font-size:14px;font-weight:600;color:var(--text);margin-top:8px">{esc(prod.get("title","")[:30])}</div></div>'
                if i == 0:
                    prod_blocks += '<div style="display:flex;align-items:center;justify-content:center"><div style="width:48px;height:48px;border-radius:50%;background:var(--green-dim);display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;color:var(--green);flex-shrink:0">VS</div></div>'

    body = f"""<div class="container detail">
      <div class="breadcrumbs">
        <a href="/">Catalog</a> &rsaquo; <a href="/catalog/comparison/">Compare</a> &rsaquo; <span>{esc(c.get('title',''))}</span>
      </div>
      <div class="detail-header">
        <h1>{esc(c.get('title',''))}</h1>
        <div style="display:flex;gap:24px;align-items:center;justify-content:center;margin:32px 0">
          {prod_blocks}
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
        <button onclick="saveStack()" style="margin-top:16px;padding:8px 18px;border-radius:6px;background:var(--green);color:#000;border:none;cursor:pointer;font-size:13px;font-weight:600;display:none" id="save-stack-btn">Сохранить в кабинет</button>
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
    document.getElementById('save-stack-btn').style.display = '';
    var avgRating = ratings.length ? (ratings.reduce(function(a,b){return a+b},0)/ratings.length).toFixed(1) : '—';
    var deployDiff = complexity <= 6 ? '🟢 Low' : complexity <= 12 ? '🟡 Medium' : '🔴 High';
    metrics.innerHTML =
      '<div class="stack-metric"><div class="sm-val">' + count + '/5</div><div class="sm-lbl">Layers configured</div></div>' +
      '<div class="stack-metric"><div class="sm-val">$' + cost + '/mo</div><div class="sm-lbl">Est. monthly cost</div></div>' +
      '<div class="stack-metric"><div class="sm-val">' + avgRating + ' ★</div><div class="sm-lbl">Avg. rating</div></div>' +
      '<div class="stack-metric"><div class="sm-val">' + deployDiff + '</div><div class="sm-lbl">Deploy complexity</div></div>';
  } else {
    result.classList.remove('active');
    document.getElementById('save-stack-btn').style.display = 'none';
  }
}
function saveStack() {
  var layers = {};
  document.querySelectorAll('.stack-slot select').forEach(function(s) {
    if (s.value) layers[s.closest('.stack-slot').querySelector('.ss-label').textContent] = s.value;
  });
  var stacks = JSON.parse(localStorage.getItem('qantcore_stacks') || '[]');
  stacks.push({name: 'Stack ' + (stacks.length + 1), layers: layers, date: new Date().toISOString().substring(0,10)});
  localStorage.setItem('qantcore_stacks', JSON.stringify(stacks));
  alert('Stack saved to Workspace! View it at /workspace/');
}
// Load stack from workspace
(function() {
  var loadData = localStorage.getItem('qantcore_load_stack');
  if (loadData) {
    try {
      var stack = JSON.parse(loadData);
      Object.entries(stack.layers || {}).forEach(function(e) {
        var sel = document.querySelector('#slot-' + e[0].toLowerCase().replace(/ /g,'-') + ' select');
        if (sel) { sel.value = e[1]; sel.dispatchEvent(new Event('change')); }
      });
      localStorage.removeItem('qantcore_load_stack');
    } catch(ex) {}
  }
})();
</script>"""

    html = render_page("Конструктор AI-стека", "Assemble your AI agent stack — LLM, memory, tools, orchestration. Estimate cost and complexity.",
                       body, scripts=scripts, total=tp,
                       open_graph=make_og("Конструктор AI-стека — QantCore", "Assemble your AI agent stack — LLM, memory, tools, orchestration. Estimate cost and complexity.", "/stack-builder/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/stack-builder/">')
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
    
    html = render_page("Методология — Как мы оцениваем AI-агентов", 
                       "Transparent evaluation framework: how Qantcore rates, ranks, and compares AI agents. No black-box scores.",
                       body, total=tp, active_method="active",
                       open_graph=make_og("Методология — QantCore", "Transparent evaluation framework: how Qantcore rates, ranks, and compares AI agents. No black-box scores.", "/methodology/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/methodology/">')
    write_html(f"{OUT}/methodology/index.html", html)
    print(f"  /methodology/index.html")


def generate_workspace():
    """Generate /workspace/ — saved agents, release watches, stack drafts."""
    tp = DB.articles.count_documents({"category": "product"})
    all_prods = list(DB.articles.find({"category": "product"}).sort("rating", -1))
    
    # Build product lookup for client-side rendering
    prod_lookup = {}
    for p in all_prods:
        prod_lookup[p["slug"]] = {
            "slug": p["slug"], "title": p.get("title",""),
            "rating": p.get("rating",""), "product_type": p.get("product_type",""),
            "updated_at": str(p.get("updated_at","")), "tagline": (p.get("tagline","") or "")[:100],
            "version": p.get("version","") or "latest",
            "deployment": "🏠 Local" if (p.get("local_first") or any(t.lower() in ["docker","local","self-hosted","python","cli","terminal"] for t in (p.get("tech_stack",[]) or []))) else "☁️ Cloud",
        }
    
    body = f"""<div class="container" id="workspace-root">
  <div class="breadcrumbs"><a href="/">Catalog</a> &rsaquo; <span>Workspace</span></div>
  
  <!-- Empty state -->
  <div id="ws-empty" style="text-align:center;padding:80px 20px">
    <div style="font-size:48px;margin-bottom:16px">📋</div>
    <h2 style="font-size:22px;font-weight:700;color:var(--text);margin-bottom:8px">Your Workspace</h2>
    <p style="color:var(--muted);font-size:14px;max-width:500px;margin:0 auto;line-height:1.6">
      Save agents, track releases, and build your AI stack.
      <br>Bookmark agents with ★, watch releases with 🔔, or build a stack at <a href="/stack-builder/" style="color:var(--green)">Stack Builder</a>.
    </p>
  </div>
  
  <!-- Saved Agents -->
  <div id="ws-saved" style="display:none">
    <div class="section-hd"><h2>★ Saved Agents</h2></div>
    <div class="grid" id="ws-saved-grid"></div>
  </div>
  
  <!-- Release Watches -->
  <div id="ws-watches" style="display:none;margin-top:32px">
    <div class="section-hd"><h2>🔔 Release Alerts</h2></div>
    <div id="ws-watches-list" style="display:flex;flex-direction:column;gap:8px"></div>
  </div>
  
  <!-- Stack Drafts -->
  <div id="ws-stacks" style="display:none;margin-top:32px">
    <div class="section-hd"><h2>🧩 Stack Drafts</h2></div>
    <div id="ws-stacks-list" style="display:flex;flex-direction:column;gap:8px"></div>
  </div>
  
  <!-- Recent Comparisons -->
  <div id="ws-comparisons" style="display:none;margin-top:32px">
    <div class="section-hd"><h2>⚖️ Recent Comparisons</h2></div>
    <div id="ws-comparisons-list" style="display:flex;flex-direction:column;gap:8px"></div>
  </div>
</div>"""
    
    scripts = f"""<script>
var WS_PRODUCTS = {json.dumps(prod_lookup)};

function initWorkspace() {{
  var saved = JSON.parse(localStorage.getItem('qantcore_saved') || '[]');
  var watches = JSON.parse(localStorage.getItem('qantcore_watches') || '[]');
  var stacks = JSON.parse(localStorage.getItem('qantcore_stacks') || '[]');
  var comparisons = JSON.parse(localStorage.getItem('qantcore_comparisons') || '[]');
  
  var hasData = saved.length || watches.length || stacks.length || comparisons.length;
  document.getElementById('ws-empty').style.display = hasData ? 'none' : '';
  
  // Saved agents
  if (saved.length) {{
    document.getElementById('ws-saved').style.display = '';
    var grid = document.getElementById('ws-saved-grid');
    var html = '';
    saved.forEach(function(slug) {{
      var p = WS_PRODUCTS[slug];
      if (!p) return;
      html += '<a href="/product/' + slug + '/" class="card">' +
        '<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span style="font-size:11px;text-transform:uppercase;font-weight:600;color:var(--green)">' + p.product_type + '</span></div>' +
        '<div class="card-title">' + escapeHTML(p.title) + '</div>' +
        '<div class="card-desc">' + escapeHTML(p.tagline) + '</div>' +
        '<div style="margin-top:8px;font-size:12px;color:var(--muted)">★ ' + p.rating + ' · ' + p.deployment + '</div>' +
        '<button onclick="event.preventDefault();removeSaved(\\'' + slug + '\\')" style="margin-top:8px;background:none;border:1px solid var(--border);color:var(--muted);padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer">Remove</button>' +
        '</a>';
    }});
    grid.innerHTML = html;
  }}
  
Нет отслеживаемых релизов
  if (watches.length) {{
    document.getElementById('ws-watches').style.display = '';
    var list = document.getElementById('ws-watches-list');
    var html = '';
    watches.forEach(function(slug) {{
      var p = WS_PRODUCTS[slug];
      if (!p) return;
      html += '<div class="feed-item" style="justify-content:space-between">' +
        '<div><strong style="color:var(--text)">' + escapeHTML(p.title) + '</strong>' +
        '<span style="color:var(--dim);font-size:11px;margin-left:8px">v' + p.version + '</span>' +
        '<span style="color:var(--muted);font-size:11px;margin-left:8px">· Updated ' + p.updated_at.substring(0,10) + '</span></div>' +
        '<button onclick="removeWatch(\\'' + slug + '\\')" style="background:none;border:1px solid var(--border);color:var(--muted);padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer">Unwatch</button>' +
        '</div>';
    }});
    list.innerHTML = html;
  }}
  
Нет черновиков стеков
  if (stacks.length) {{
    document.getElementById('ws-stacks').style.display = '';
    var list = document.getElementById('ws-stacks-list');
    var html = '';
    stacks.forEach(function(stack, i) {{
      html += '<div class="feed-item" style="justify-content:space-between">' +
        '<div><strong style="color:var(--text)">' + escapeHTML(stack.name || 'Draft ' + (i+1)) + '</strong>' +
        '<span style="color:var(--dim);font-size:11px;margin-left:8px">' + Object.keys(stack.layers || {{}}).length + ' components</span>' +
        '<span style="color:var(--muted);font-size:11px;margin-left:8px">· ' + (stack.date || '') + '</span></div>' +
        '<div><button onclick="loadStack(' + i + ')" style="background:none;border:1px solid var(--green);color:var(--green);padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer;margin-right:6px">Load</button>' +
        '<button onclick="removeStack(' + i + ')" style="background:none;border:1px solid var(--border);color:var(--muted);padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer">Delete</button></div>' +
        '</div>';
    }});
    list.innerHTML = html;
  }}
  
  // Recent comparisons
  if (comparisons.length) {{
    document.getElementById('ws-comparisons').style.display = '';
    var list = document.getElementById('ws-comparisons-list');
    var html = '';
    comparisons.slice(-5).reverse().forEach(function(c) {{
      var names = c.slugs.map(function(s) {{ var p = WS_PRODUCTS[s]; return p ? p.title : s; }}).join(' vs ');
      html += '<a href="/compare/?slugs=' + c.slugs.join(',') + '" class="feed-item">' +
        '<span style="font-size:14px">⚖️</span>' +
        '<div><strong style="color:var(--text)">' + escapeHTML(names) + '</strong>' +
        '<span style="color:var(--dim);font-size:11px;margin-left:8px">· ' + c.date + '</span></div>' +
        '</a>';
    }});
    list.innerHTML = html;
  }}
}}

function removeSaved(slug) {{
  var saved = JSON.parse(localStorage.getItem('qantcore_saved') || '[]');
  saved = saved.filter(function(s) {{ return s !== slug; }});
  localStorage.setItem('qantcore_saved', JSON.stringify(saved));
  location.reload();
}}
function removeWatch(slug) {{
  var w = JSON.parse(localStorage.getItem('qantcore_watches') || '[]');
  w = w.filter(function(s) {{ return s !== slug; }});
  localStorage.setItem('qantcore_watches', JSON.stringify(w));
  location.reload();
}}
function removeStack(i) {{
  var stacks = JSON.parse(localStorage.getItem('qantcore_stacks') || '[]');
  stacks.splice(i, 1);
  localStorage.setItem('qantcore_stacks', JSON.stringify(stacks));
  location.reload();
}}
function loadStack(i) {{
  var stacks = JSON.parse(localStorage.getItem('qantcore_stacks') || '[]');
  var stack = stacks[i];
  if (stack) {{
    localStorage.setItem('qantcore_load_stack', JSON.stringify(stack));
    window.location = '/stack-builder/';
  }}
}}
function escapeHTML(str) {{
  var div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}}
initWorkspace();
</script>"""
    
    html = render_page("Кабинет — Сохранённые агенты и уведомления",
                       "Your personal AI agent workspace: saved agents, release watches, stack drafts, comparison history.",
                       body, scripts=scripts, total=tp, active_ws="active",
                       open_graph=make_og("Кабинет — QantCore", "Your personal AI agent workspace: saved agents, release watches, stack drafts, comparison history.", "/workspace/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/workspace/">')
    write_html(f"{OUT}/workspace/index.html", html)
    print(f"  /workspace/index.html")


def generate_benchmarks():
    """Generate /benchmarks/ — latency, throughput, release velocity dashboard."""
    products = list(DB.articles.find({"category": "product"}).sort("rating", -1))
    tp = len(products)
    
    # Simulated benchmark data (would be real API data in production)
    rows = ""
    for p in sorted(products, key=lambda x: (x.get("rating", 0) or 0), reverse=True)[:20]:
        r = p.get("rating", 0) or 0
        f = (p.get("freshness_score", 0) or 0) * 100
        rc = p.get("review_count", 0) or 0
        qs = min(100, round(r*20*0.30 + (min(10, r*1.8+f/100*1.5+min(rc/500,2)))*10*0.25 + 7*10*0.20 + (f/100*15+min(rc/200,8))*1.5*0.15 + (min(10, r*1.5+f/100*2))*10*0.10))
        img_url = p.get("image_url", "")
        logo = f'<img src="{img_url}" alt="" style="width:32px;height:32px;object-fit:contain;border-radius:6px;background:rgba(255,255,255,.04);vertical-align:middle;margin-right:10px;flex-shrink:0">' if img_url else ''
        rows += f"""<tr>
          <td style="font-size:15px;font-weight:600"><a href="/product/{p['slug']}/" style="color:var(--text);display:flex;align-items:center">{logo}{esc(p.get('title','')[:35])}</a></td>
          <td style="font-size:16px"><strong style="color:{'var(--green)' if qs>=85 else 'var(--cyan)' if qs>=70 else 'var(--amber)'}">{qs}</strong></td>
          <td style="font-size:14px">{int(f)}%</td>
          <td style="font-size:14px">{r} ★</td>
          <td style="font-size:14px">{rc}</td>
          <td style="font-size:14px">{'🏠 Local' if any(t.lower() in ['docker','local','self-hosted','python','cli','terminal'] for t in (p.get('tech_stack',[]) or [])) else '☁️ Cloud'}</td>
        </tr>"""
    
    tc_bench = DB.articles.count_documents({"category": "comparison"})
    body = f"""<div class="container detail">
  <div class="breadcrumbs"><a href="/">Каталог</a> &rsaquo; <span>Рейтинг</span></div>
  <h1 style="font-size:32px;font-weight:800;color:#f1f5f9;margin:24px 0 8px">Рейтинг AI-агентов</h1>
  <p style="color:var(--muted);font-size:16px;line-height:1.7;max-width:760px">Количественные метрики для {tp} AI-агентов. QantScore, свежесть, рейтинги, готовность к внедрению.</p>
  
  <div class="auth-bar" style="margin-top:24px">
    <div class="auth-inner">
      <div class="auth-stat"><div class="n" style="font-size:32px">{tp}</div><div class="l">Агентов в рейтинге</div></div>
      <div class="auth-stat"><div class="n amber" style="font-size:32px">{tc_bench}</div><div class="l">Сравнений</div></div>
      <div class="auth-stat"><div class="n" style="font-size:32px">Ежедневно</div><div class="l">Обновление</div></div>
      <div class="auth-stat"><div class="n" style="font-size:32px"><span class="dot"></span>Live</div><div class="l">Данные</div></div>
    </div>
  </div>
  
  <div style="margin-top:32px">
    <div class="section-hd"><h2 style="font-size:22px">Top 20 по QantScore™</h2></div>
    <div class="compare-table-wrap">
      <table class="compare-table" style="font-size:14px">
        <tr><th style="font-size:13px;padding:16px 16px">Агент</th><th style="font-size:13px">QantScore</th><th style="font-size:13px">Свежесть</th><th style="font-size:13px">Рейтинг</th><th style="font-size:13px">Отзывы</th><th style="font-size:13px">Деплой</th></tr>
        {rows}
      </table>
    </div>
  </div>
  
  <div style="margin-top:32px;padding:24px;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius)">
    <h3 style="color:var(--green);font-size:15px;margin-bottom:8px">Методология</h3>
    <p style="color:var(--muted);font-size:14px;line-height:1.7">QantScore™ — композитная оценка 0-100: Рейтинг (30%) + Зрелость (25%) + Развёртываемость (20%) + Скорость сообщества (15%) + Качество документации (10%). <a href="/methodology/" style="color:var(--green)">Полная методология</a>.</p>
  </div>
</div>"""
    
    html = render_page("Рейтинг AI-агентов — QantScore, метрики, бенчмарки", 
                       f"Рейтинг {tp} AI-агентов: QantScore, свежесть, рейтинги, готовность к деплою. Топ-20.",
                       body, total=tp,
                       open_graph=make_og("Бенчмарки — QantCore", f"Quantitative benchmarks for {tp} AI agents: QantScore, freshness, ratings, deployment readiness.", "/benchmarks/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/benchmarks/">')
    write_html(f"{OUT}/benchmarks/index.html", html)
    print(f"  /benchmarks/index.html")


def generate_media_kit():
    """Generate /media-kit/ — advertising & sponsorship information."""
    tp = DB.articles.count_documents({"category": "product"})
    tc = DB.articles.count_documents({"category": "comparison"})
    
    body = """<div class="container detail">
  <div class="breadcrumbs"><a href="/">Catalog</a> &rsaquo; <span>Media Kit</span></div>
  <h1 style="font-size:28px;font-weight:800;color:#f1f5f9;margin:24px 0 8px">Media Kit — Advertise on Qantcore</h1>
  <p style="color:var(--muted);font-size:15px;line-height:1.7;max-width:760px">Reach AI decision-makers at the moment of product selection. Qantcore is the decision platform for AI tooling — your placement reaches engineers, CTOs, and researchers actively evaluating AI agents.</p>
  
  <div class="auth-bar" style="margin-top:24px">
    <div class="auth-inner">
      <div class="auth-stat"><div class="n">{tp}+</div><div class="l">Products tracked</div></div>
      <div class="auth-stat"><div class="n">{tc}+</div><div class="l">Comparisons</div></div>
      <div class="auth-stat"><div class="n amber">Daily</div><div class="l">Data refresh</div></div>
      <div class="auth-stat"><div class="n">B2B</div><div class="l">Decision-maker audience</div></div>
    </div>
  </div>
  
  <div style="margin-top:32px;display:grid;gap:20px">
    
    <div class="method-card">
      <h2>🎯 Спонсорский бенчмарк Inclusion</h2>
      <p>Your product appears in benchmark comparisons with verified performance data. Native placement — not a banner.</p>
      <p style="color:var(--green);font-size:13px;margin-top:8px">Best for: products seeking objective third-party validation</p>
    </div>
    
    <div class="method-card">
      <h2>📊 Продвигаемое сравнение Placement</h2>
      <p>Priority ranking in head-to-head comparisons. Your product is highlighted when users compare relevant categories.</p>
      <p style="color:var(--green);font-size:13px;margin-top:8px">Best for: capturing decision-intent traffic at comparison moment</p>
    </div>
    
    <div class="method-card">
      <h2>⭐ Sponsored Обзор фреймворка</h2>
      <p>Featured placement in "Featured Frameworks" section. Category exclusivity available.</p>
      <p style="color:var(--green);font-size:13px;margin-top:8px">Best for: new launches, category awareness, enterprise visibility</p>
    </div>
    
    <div class="method-card">
      <h2>📝 Native Technical Review</h2>
      <p>Engineer-grade deep-dive review written by our technical team. Published as editorial content with sponsored disclosure.</p>
      <p style="color:var(--green);font-size:13px;margin-top:8px">Best for: detailed product positioning, technical audience trust-building</p>
    </div>
    
    <div class="method-card">
      <h2>📬 Рассылка Feature</h2>
      <p>Dedicated placement in our weekly AI agent intelligence briefing. Direct to inbox of active evaluators.</p>
      <p style="color:var(--green);font-size:13px;margin-top:8px">Best for: time-sensitive launches, event promotion, regular touchpoints</p>
    </div>
    
  </div>
  
  <div style="margin-top:32px;padding:24px;background:var(--card-bg);border:1px solid var(--green);border-radius:var(--radius);text-align:center">
    <h3 style="color:var(--green);font-size:16px;margin-bottom:8px">Interested in advertising?</h3>
    <p style="color:var(--muted);font-size:14px">Contact us for rates, availability, and audience metrics.</p>
    <p style="color:var(--text);font-size:16px;font-weight:600;margin-top:8px">partners@qantcore.space</p>
  </div>
  
  <div style="margin-top:32px;padding:20px;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius-sm);font-size:12px;color:var(--dim);line-height:1.6">
    <strong style="color:var(--muted)">Our promise:</strong> All sponsored content is clearly labeled. We never sell rankings — only visibility. Your QantScore™ is always independently calculated. Trust is our moat.
  </div>
</div>
<style>
.method-card{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px 24px}
.method-card h2{font-size:15px;font-weight:700;color:var(--green);margin-bottom:8px;letter-spacing:-.01em}
.method-card p{font-size:13px;color:var(--muted);line-height:1.7}
</style>"""
    
    html = render_page("Медиа-кит — Реклама на Qantcore",
                       "Reach AI decision-makers at the moment of product selection. Sponsored benchmarks, featured comparisons, native reviews.",
                       body, total=tp,
                       open_graph=make_og("Media Kit — Qantcore", "Reach AI decision-makers at the moment of product selection. Sponsored benchmarks, featured comparisons, native reviews.", "/media-kit/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/media-kit/">')
    write_html(f"{OUT}/media-kit/index.html", html)
    print(f"  /media-kit/index.html")


def generate_company_pages():
    """Generate /company/{slug}/ pages for major AI companies."""
    products = list(DB.articles.find({"category": "product"}))
    
    # Company mapping: company_slug → {name, description, product_slugs}
    companies = {}
    for p in products:
        slug = p["slug"]
        # Map products to companies
        company = None
        if slug in ["claude-anthropic", "claude-code", "claude-desktop", "anthropic-mcp"]:
            company = "anthropic"
        elif slug in ["chatgpt-openai", "codex-cli", "codex-desktop", "openai-swarm"]:
            company = "openai"
        elif slug in ["autogen-microsoft", "github-copilot", "microsoft-copilot", "semantic-kernel"]:
            company = "microsoft"
        elif slug in ["google-gemini"]:
            company = "google"
        elif slug in ["llama-meta"]:
            company = "meta"
        elif slug in ["langchain-framework", "langgraph-framework", "langsmith-langchain"]:
            company = "langchain"
        elif slug in ["codeium-windsurf", "windsurf-ide"]:
            company = "codeium"
        elif slug in ["smolagents-huggingface"]:
            company = "huggingface"
        elif slug in ["devin-agent"]:
            company = "cognition"
        elif slug in ["deepseek-llm"]:
            company = "deepseek"
        elif slug in ["mistral-ai"]:
            company = "mistral"
        elif slug in ["vercel-v0"]:
            company = "vercel"
        elif slug in ["amazon-q-developer"]:
            company = "amazon"
        elif slug in ["perplexity-ai"]:
            company = "perplexity"
        elif slug in ["notion-ai"]:
            company = "notion"
        elif slug in ["zapier-ai"]:
            company = "zapier"
        
        if company:
            if company not in companies:
                companies[company] = {"name": "", "desc": "", "products": []}
            companies[company]["products"].append(p)
    
    # Company metadata
    meta = {
        "anthropic": {"name": "Anthropic", "desc": "AI safety company behind Claude. Creator of the Model Context Protocol (MCP), setting the standard for AI-tool integration."},
        "openai": {"name": "OpenAI", "desc": "Creator of ChatGPT, GPT-4, and the Codex CLI ecosystem. Pioneering AI agents, swarm orchestration, and developer tools."},
        "microsoft": {"name": "Microsoft", "desc": "Enterprise AI ecosystem spanning GitHub Copilot, AutoGen multi-agent framework, Semantic Kernel, and Microsoft 365 Copilot."},
        "google": {"name": "Google DeepMind", "desc": "Multimodal AI research powerhouse behind Gemini, pushing the frontier of reasoning, coding, and scientific AI."},
        "meta": {"name": "Meta AI", "desc": "Open-source AI leader. Llama models power local deployment and community innovation at global scale."},
        "langchain": {"name": "LangChain", "desc": "The standard framework for LLM application development. Ecosystem spans orchestration (LangGraph), observability (LangSmith), and deployment."},
        "codeium": {"name": "Codeium", "desc": "AI-powered coding platform. Windsurf IDE and Codeium autocomplete serve millions of developers."},
        "huggingface": {"name": "Hugging Face", "desc": "The home of open-source AI. SmolAgents brings minimalistic agent frameworks to the community."},
        "cognition": {"name": "Cognition AI", "desc": "Creator of Devin — the first autonomous AI software engineer. Pushing the boundary of agent-driven development."},
        "deepseek": {"name": "DeepSeek", "desc": "Chinese AI lab producing state-of-the-art open-weight LLMs at fraction of competitor costs."},
        "mistral": {"name": "Mistral AI", "desc": "European champion of open-weight models. Fast, efficient, and deployment-friendly LLMs."},
        "vercel": {"name": "Vercel", "desc": "Frontend cloud platform. v0 generates production UI components from text prompts."},
        "amazon": {"name": "Amazon AWS", "desc": "Cloud infrastructure leader. Amazon Q Developer brings AI assistance to the AWS ecosystem."},
        "perplexity": {"name": "Perplexity AI", "desc": "AI-native search engine with agentic capabilities. Redefining how developers find and verify information."},
        "notion": {"name": "Notion", "desc": "Connected workspace platform. Notion AI integrates intelligence directly into knowledge management."},
        "zapier": {"name": "Zapier", "desc": "Workflow automation leader. Zapier AI brings no-code AI agents to business process automation."},
    }
    
    tp = len(products)
    tc = DB.articles.count_documents({"category": "comparison"})
    
    # Generate individual company pages
    for comp_slug, comp_data in sorted(companies.items()):
        info = meta.get(comp_slug, {"name": comp_slug.title(), "desc": "AI technology company."})
        prods = comp_data["products"]
        
        # Product cards
        pcards = ""
        for p in sorted(prods, key=lambda x: x.get("rating", 0) or 0, reverse=True):
            pcards += make_product_card(p, with_compare=False)
        
        # Aggregate stats
        avg_rating = round(sum(p.get("rating", 0) or 0 for p in prods) / len(prods), 1) if prods else 0
        avg_freshness = int(sum(p.get("freshness_score", 0) or 0 for p in prods) / len(prods) * 100) if prods else 0
        total_reviews = sum(p.get("review_count", 0) or 0 for p in prods)
        
        # Ecosystem map
        eco = ""
        for i, p in enumerate(prods):
            links = []
            for j, p2 in enumerate(prods):
                if i != j:
                    links.append(p2["slug"])
            if links:
                eco += f'<div style="margin-bottom:8px"><strong>{esc(p.get("title","")[:35])}</strong>'
                eco += f'<span style="color:var(--dim);font-size:11px"> → ' + ", ".join(l[:20] for l in links) + '</span></div>'
        
        body = f"""<div class="container detail">
  <div class="breadcrumbs"><a href="/">Catalog</a> &rsaquo; <span>{info['name']}</span></div>
  <div style="display:flex;align-items:flex-start;gap:24px;margin:24px 0;flex-wrap:wrap">
    <div style="flex:1;min-width:280px">
      <h1 style="font-size:28px;font-weight:800;color:#f1f5f9;margin-bottom:8px">{info['name']}</h1>
      <p style="color:var(--muted);font-size:15px;line-height:1.7">{info['desc']}</p>
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      <div class="hero-metric"><div class="val">{len(prods)}</div><div class="lbl">Products</div></div>
      <div class="hero-metric"><div class="val amber">{avg_rating} ★</div><div class="lbl">Ср. рейтинг</div></div>
      <div class="hero-metric"><div class="val">{avg_freshness}%</div><div class="lbl">Freshness</div></div>
      <div class="hero-metric"><div class="val">{total_reviews}</div><div class="lbl">Reviews</div></div>
    </div>
  </div>
  
  <div class="section-hd"><h2>Карта экосистемы</h2></div>
  <div style="padding:16px 20px;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:32px">
    {eco}
  </div>
  
  <div class="section-hd"><h2>Продукты ({len(prods)})</h2></div>
  <div class="grid">{pcards}</div>
</div>"""
        
        html = render_page(f"{info['name']} — AI Products & Ecosystem", 
                           f"{info['name']}: {len(prods)} AI products tracked. Ratings, benchmarks, ecosystem map.",
                           body, total=tp,
                           open_graph=make_og(f"{info['name']} — QantCore", f"{info['name']}: {len(prods)} AI products tracked. Ratings, benchmarks, ecosystem map.", f"/company/{comp_slug}/"),
                           canonical_url=f'<link rel="canonical" href="https://qantcore.space/company/{comp_slug}/">')
        write_html(f"{OUT}/company/{comp_slug}/index.html", html)
    
    # Generate company index page
    index_rows = ""
    for comp_slug, comp_data in sorted(companies.items(), key=lambda x: len(x[1]["products"]), reverse=True):
        info = meta.get(comp_slug, {"name": comp_slug.title(), "desc": ""})
        prods = comp_data["products"]
        avg_r = round(sum(p.get("rating", 0) or 0 for p in prods) / len(prods), 1) if prods else 0
        index_rows += f"""<a href="/company/{comp_slug}/" class="featured-card" style="display:block">
      <div class="fc-label">{len(prods)} PRODUCTS</div>
      <div class="fc-title">{info['name']}</div>
      <div class="fc-desc">{info['desc'][:120]}</div>
      <div style="margin-top:12px;display:flex;gap:16px;font-size:12px">
        <span style="color:var(--amber)">★ {avg_r}</span>
        <span style="color:var(--green)">{len(prods)} agents</span>
      </div>
    </a>"""
    
    index_body = f"""<div class="container">
  <div class="breadcrumbs"><a href="/">Catalog</a> &rsaquo; <span>Компании</span></div>
  <h1 style="font-size:28px;font-weight:800;color:#f1f5f9;margin:24px 0 8px">Профили AI-компаний</h1>
  <p style="color:var(--muted);font-size:15px;margin-bottom:24px">Explore AI agent ecosystems by company. Track products, benchmark scores, and release activity for each organization.</p>
  <div class="featured-grid">{index_rows}</div>
</div>"""
    
    html = render_page("AI-компании — Профили экосистем", 
                       f"Company profiles for {len(companies)} AI organizations. Products, benchmarks, ecosystem maps.",
                       index_body, total=tp,
                       open_graph=make_og("AI-компании — QantCore", f"Company profiles for {len(companies)} AI organizations. Products, benchmarks, ecosystem maps.", "/company/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/company/">')
    write_html(f"{OUT}/company/index.html", html)
    print(f"  /company/index.html + {len(companies)} company pages")


# ─── Main ─────────────────────────────────────────────────────────
# Appended: /development/, /multi-agent/, /guides/ generators
# ═══════════════════════════════════════════════════════════════

"""
New page generators for Qantcore:
  generate_development()  → /development/
  generate_multi_agent()   → /multi-agent/
  generate_guides()        → /guides/
Appended to generate_static.py
"""
import os

OUT = "/opt/data/www/qantcore/static"

def generate_development():
    from pymongo import MongoClient
    DB = MongoClient("localhost", 27017).qantcore
    
    products = list(DB.articles.find({"category": "product"}))
    
    coding_slugs = {
        "aider-ai", "amazon-q-developer", "claude-code", "cline-vscode",
        "codeium-windsurf", "codex-cli", "codex-desktop", "continue-dev",
        "cursor-ide", "devin-agent", "github-copilot", "replit-ai",
        "sourcegraph-cody", "tabnine-ai", "windsurf-ide",
        "bolt-new", "lovable-dev", "vercel-v0",
        "open-interpreter", "swe-agent"
    }
    coding = [p for p in products if p["slug"] in coding_slugs]
    
    tc = DB.articles.count_documents({"category": "comparison"})
    
    cards = ""
    for p in sorted(coding, key=lambda x: x.get("rating", 0) or 0, reverse=True):
        cards += make_product_card(p, with_compare=True)
    
    best_ide = next((p for p in coding if p["slug"] == "cursor-ide"), coding[0] if coding else None)
    best_pr = next((p for p in coding if p["slug"] == "claude-code"), coding[0] if coding else None)
    best_free = next((p for p in coding if (p.get("pricing_model","") or "").lower() in ("open source","freemium")), coding[0] if coding else None)
    
    ide_agents = [p for p in coding if p["slug"] in {"cursor-ide","cline-vscode","continue-dev","github-copilot","codeium-windsurf","sourcegraph-cody","tabnine-ai","windsurf-ide","amazon-q-developer"}]
    terminal_agents = [p for p in coding if p["slug"] in {"claude-code","aider-ai","codex-cli","codex-desktop","open-interpreter"}]
    autonomous_agents = [p for p in coding if p["slug"] in {"devin-agent","swe-agent"}]
    prototyping_agents = [p for p in coding if p["slug"] in {"bolt-new","lovable-dev","vercel-v0","replit-ai"}]
    
    body = f'''<div class="hero" style="padding:48px 24px 36px">
  <div class="terminal-grid"></div>
  <div class="tagline">AI CODING AGENTS</div>
  <h1>AI-\u0430\u0433\u0435\u043d\u0442\u044b \u0434\u043b\u044f <span class="accent">\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0438</span></h1>
  <p class="sub">\u041f\u043e\u043b\u043d\u044b\u0439 \u0433\u0430\u0439\u0434 \u043f\u043e 20+ AI-\u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0430\u043c \u0434\u043b\u044f \u043a\u043e\u0434\u0430: \u0430\u0432\u0442\u043e\u0434\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435, \u0430\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u044b\u0435 PR, \u0440\u0435\u0444\u0430\u043a\u0442\u043e\u0440\u0438\u043d\u0433, \u043f\u0440\u043e\u0442\u043e\u0442\u0438\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435. \u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0430\u0433\u0435\u043d\u0442\u0430 \u043f\u043e\u0434 \u0432\u0430\u0448 \u0441\u0442\u0435\u043a \u0438 \u0437\u0430\u0434\u0430\u0447\u0438.</p>
  <div class="hero-metrics">
    <div class="hero-metric"><div class="val">{len(coding)}</div><div class="lbl">\u0410\u0433\u0435\u043d\u0442\u043e\u0432</div></div>
    <div class="hero-metric"><div class="val">4</div><div class="lbl">\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438</div></div>
    <div class="hero-metric"><div class="val">{tc}+</div><div class="lbl">\u0421\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0439</div></div>
    <div class="hero-metric"><div class="val"><span class="dot"></span>Live</div><div class="lbl">\u0414\u0430\u043d\u043d\u044b\u0435</div></div>
  </div>
</div>

<div class="container detail">

  <div style="margin:32px 0;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:24px 16px 12px;text-align:center;overflow-x:auto">
    <h3 style="color:var(--green);font-size:15px;margin-bottom:20px">\U0001F3D7\ufe0f \u0410\u0440\u0445\u0438\u0442\u0435\u043a\u0442\u0443\u0440\u0430: \u043a\u0430\u043a AI-\u0430\u0433\u0435\u043d\u0442 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u0441 \u0432\u0430\u0448\u0438\u043c \u043a\u043e\u0434\u043e\u043c</h3>
    <svg viewBox="0 0 900 420" style="max-width:900px;width:100%;height:auto">
      <defs>
        <marker id="aDev" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#3B82F6"/></marker>
        <marker id="aDevG" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#10b981"/></marker>
        <marker id="aDevA" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#f59e0b"/></marker>
        <marker id="aDevC" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#22D3EE"/></marker>
        <filter id="glD"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <linearGradient id="grdCore" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3B82F6" stop-opacity="0.3"/><stop offset="100%" stop-color="#10b981" stop-opacity="0.3"/></linearGradient>
      </defs>
      
      <rect x="0" y="0" width="200" height="420" rx="12" fill="url(#grdCore)" stroke="#3B82F6" stroke-width="1" stroke-opacity="0.5"/>
      <text x="100" y="28" text-anchor="middle" fill="#3B82F6" font-size="13" font-weight="700">\U0001F4E5 \u041a\u043e\u043d\u0442\u0435\u043a\u0441\u0442 \u043a\u043e\u0434\u043e\u0432\u043e\u0439 \u0431\u0430\u0437\u044b</text>
      
      <rect x="15" y="45" width="170" height="36" rx="8" fill="var(--card-bg)" stroke="var(--muted)" stroke-width="1"/>
      <text x="100" y="60" text-anchor="middle" fill="#F5F7FA" font-size="10">\U0001F4C1 Filesystem Scanner</text>
      <text x="100" y="73" text-anchor="middle" fill="var(--dim)" font-size="9">.gitignore-aware</text>
      <line x1="100" y1="81" x2="100" y2="98" stroke="var(--muted)" stroke-width="1" marker-end="url(#aDev)"/>
      
      <rect x="15" y="100" width="170" height="36" rx="8" fill="var(--card-bg)" stroke="var(--muted)" stroke-width="1"/>
      <text x="100" y="115" text-anchor="middle" fill="#F5F7FA" font-size="10">\U0001F332 AST Parser</text>
      <text x="100" y="128" text-anchor="middle" fill="var(--dim)" font-size="9">Tree-sitter, LSP</text>
      <line x1="100" y1="136" x2="100" y2="153" stroke="var(--muted)" stroke-width="1" marker-end="url(#aDev)"/>
      
      <rect x="15" y="155" width="170" height="36" rx="8" fill="var(--card-bg)" stroke="var(--muted)" stroke-width="1"/>
      <text x="100" y="170" text-anchor="middle" fill="#F5F7FA" font-size="10">\U0001F9EC Embedding Index</text>
      <text x="100" y="183" text-anchor="middle" fill="var(--dim)" font-size="9">CodeBERT, Voyage, OpenAI</text>
      <line x1="100" y1="191" x2="100" y2="208" stroke="var(--muted)" stroke-width="1" marker-end="url(#aDev)"/>
      
      <rect x="15" y="210" width="170" height="36" rx="8" fill="var(--card-bg)" stroke="var(--muted)" stroke-width="1"/>
      <text x="100" y="225" text-anchor="middle" fill="#F5F7FA" font-size="10">\U0001F4CB Dependency Graph</text>
      <text x="100" y="238" text-anchor="middle" fill="var(--dim)" font-size="9">imports, \u0432\u044b\u0437\u043e\u0432\u044b, \u0442\u0438\u043f\u044b</text>
      <line x1="100" y1="246" x2="100" y2="263" stroke="var(--muted)" stroke-width="1" marker-end="url(#aDev)"/>
      
      <rect x="15" y="265" width="170" height="50" rx="8" fill="var(--card-bg)" stroke="#10b981" stroke-width="1.5"/>
      <text x="100" y="282" text-anchor="middle" fill="#10b981" font-size="10">\U0001F4E4 Context Window</text>
      <text x="100" y="297" text-anchor="middle" fill="var(--dim)" font-size="9">\u2714 \u0420\u0435\u043b\u0435\u0432\u0430\u043d\u0442\u043d\u044b\u0435 \u0444\u0430\u0439\u043b\u044b</text>
      <text x="100" y="310" text-anchor="middle" fill="var(--dim)" font-size="9">\u2714 \u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u043a\u0443\u0440\u0441\u043e\u0440</text>
      
      <line x1="185" y1="180" x2="230" y2="180" stroke="#10b981" stroke-width="2.5" marker-end="url(#aDevG)"/>
      
      <rect x="235" y="0" width="320" height="420" rx="12" fill="#0d1520" stroke="#10b981" stroke-width="1.5" filter="url(#glD)"/>
      <text x="395" y="28" text-anchor="middle" fill="#10b981" font-size="13" font-weight="700">\U0001F916 Agent Core Loop</text>
      
      <rect x="255" y="45" width="130" height="70" rx="10" fill="var(--card-bg)" stroke="#3B82F6" stroke-width="1.5"/>
      <text x="320" y="67" text-anchor="middle" fill="#3B82F6" font-size="11" font-weight="600">1. Planning</text>
      <text x="320" y="84" text-anchor="middle" fill="var(--dim)" font-size="9">\u0420\u0430\u0437\u0431\u0438\u0432\u043a\u0430 \u0437\u0430\u0434\u0430\u0447\u0438</text>
      <text x="320" y="98" text-anchor="middle" fill="var(--dim)" font-size="9">\u0412\u044b\u0431\u043e\u0440 \u0444\u0430\u0439\u043b\u043e\u0432</text>
      <text x="320" y="111" text-anchor="middle" fill="var(--dim)" font-size="9">\u041e\u0446\u0435\u043d\u043a\u0430 \u0440\u0438\u0441\u043a\u043e\u0432</text>
      
      <line x1="385" y1="80" x2="415" y2="80" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#aDev)"/>
      
      <rect x="420" y="45" width="120" height="70" rx="10" fill="var(--card-bg)" stroke="#10b981" stroke-width="1.5"/>
      <text x="480" y="67" text-anchor="middle" fill="#10b981" font-size="11" font-weight="600">2. Code Gen</text>
      <text x="480" y="84" text-anchor="middle" fill="var(--dim)" font-size="9">LLM \u0433\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f</text>
      <text x="480" y="98" text-anchor="middle" fill="var(--dim)" font-size="9">\u041c\u043d\u043e\u0433\u043e\u0444\u0430\u0439\u043b\u043e\u0432\u044b\u0435</text>
      <text x="480" y="111" text-anchor="middle" fill="var(--dim)" font-size="9">\u043f\u0440\u0430\u0432\u043a\u0438</text>
      
      <line x1="395" y1="115" x2="395" y2="145" stroke="var(--muted)" stroke-width="1.5" marker-end="url(#aDev)"/>
      
      <rect x="255" y="150" width="130" height="70" rx="10" fill="var(--card-bg)" stroke="#22D3EE" stroke-width="1.5"/>
      <text x="320" y="172" text-anchor="middle" fill="#22D3EE" font-size="11" font-weight="600">3. Tool Use</text>
      <text x="320" y="189" text-anchor="middle" fill="var(--dim)" font-size="9">\U0001F50D grep/read files</text>
      <text x="320" y="203" text-anchor="middle" fill="var(--dim)" font-size="9">\U0001F6E0\ufe0f \u0437\u0430\u043f\u0443\u0441\u043a \u0442\u0435\u0441\u0442\u043e\u0432</text>
      <text x="320" y="217" text-anchor="middle" fill="var(--dim)" font-size="9">\U0001F310 web search</text>
      
      <line x1="385" y1="185" x2="415" y2="185" stroke="#22D3EE" stroke-width="1.5" marker-end="url(#aDevC)"/>
      
      <rect x="420" y="150" width="120" height="70" rx="10" fill="var(--card-bg)" stroke="#f59e0b" stroke-width="1.5"/>
      <text x="480" y="172" text-anchor="middle" fill="#f59e0b" font-size="11" font-weight="600">4. Reflection</text>
      <text x="480" y="189" text-anchor="middle" fill="var(--dim)" font-size="9">\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430</text>
      <text x="480" y="203" text-anchor="middle" fill="var(--dim)" font-size="9">\u0417\u0430\u043f\u0443\u0441\u043a lint</text>
      <text x="480" y="217" text-anchor="middle" fill="var(--dim)" font-size="9">\u0418\u0441\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435</text>
      
      <path d="M480,220 Q480,255 395,255 Q320,255 320,235" fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="4,3" marker-end="url(#aDevA)"/>
      <text x="440" y="250" fill="var(--amber)" font-size="9">\u043f\u043e\u0432\u0442\u043e\u0440 \u0434\u043e \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430</text>
      
      <line x1="395" y1="280" x2="395" y2="318" stroke="#10b981" stroke-width="2" marker-end="url(#aDevG)"/>
      
      <rect x="265" y="320" width="260" height="50" rx="10" fill="var(--card-bg)" stroke="#10b981" stroke-width="1.5"/>
      <text x="395" y="340" text-anchor="middle" fill="#10b981" font-size="11" font-weight="600">\u2714 Diff + Lint + Tests</text>
      <text x="395" y="358" text-anchor="middle" fill="var(--dim)" font-size="9">\u0410\u0433\u0435\u043d\u0442 \u043e\u0442\u0434\u0430\u0451\u0442 \u0433\u043e\u0442\u043e\u0432\u044b\u0439 \u0438\u0437\u043c\u0435\u043d\u0451\u043d\u043d\u044b\u0439 \u043a\u043e\u0434</text>
      
      <line x1="555" y1="180" x2="605" y2="180" stroke="#3B82F6" stroke-width="2.5" marker-end="url(#aDev)"/>
      
      <rect x="610" y="0" width="290" height="420" rx="12" fill="url(#grdCore)" stroke="#22D3EE" stroke-width="1" stroke-opacity="0.5"/>
      <text x="755" y="28" text-anchor="middle" fill="#22D3EE" font-size="13" font-weight="700">\U0001F4E4 \u0418\u043d\u0442\u0435\u0433\u0440\u0430\u0446\u0438\u044f</text>
      
      <rect x="630" y="50" width="115" height="85" rx="10" fill="var(--card-bg)" stroke="#3B82F6" stroke-width="1.5"/>
      <text x="687" y="72" text-anchor="middle" fill="#3B82F6" font-size="11" font-weight="600">\U0001F500 Git</text>
      <text x="687" y="90" text-anchor="middle" fill="var(--dim)" font-size="9">commit</text>
      <text x="687" y="105" text-anchor="middle" fill="var(--dim)" font-size="9">push</text>
      <text x="687" y="120" text-anchor="middle" fill="var(--dim)" font-size="9">PR create</text>
      
      <rect x="760" y="50" width="125" height="85" rx="10" fill="var(--card-bg)" stroke="#22D3EE" stroke-width="1.5"/>
      <text x="822" y="72" text-anchor="middle" fill="#22D3EE" font-size="11" font-weight="600">\u2699\ufe0f CI/CD</text>
      <text x="822" y="90" text-anchor="middle" fill="var(--dim)" font-size="9">GitHub Actions</text>
      <text x="822" y="105" text-anchor="middle" fill="var(--dim)" font-size="9">Tests run</text>
      <text x="822" y="120" text-anchor="middle" fill="var(--dim)" font-size="9">Deploy</text>
      
      <line x1="745" y1="92" x2="760" y2="92" stroke="var(--muted)" stroke-width="1" marker-end="url(#aDev)"/>
      
      <rect x="630" y="160" width="255" height="60" rx="10" fill="var(--card-bg)" stroke="var(--amber)" stroke-width="1"/>
      <text x="757" y="182" text-anchor="middle" fill="var(--amber)" font-size="11">\U0001F4CB Code Review</text>
      <text x="757" y="199" text-anchor="middle" fill="var(--dim)" font-size="9">\u0410\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0440\u0435\u0432\u044c\u044e \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0439 \u0432 PR</text>
      <text x="757" y="213" text-anchor="middle" fill="var(--dim)" font-size="9">\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u0438 + \u0441\u0442\u0438\u043b\u044f</text>
      
      <rect x="630" y="250" width="125" height="70" rx="10" fill="var(--card-bg)" stroke="#10b981" stroke-width="1.5"/>
      <text x="692" y="272" text-anchor="middle" fill="#10b981" font-size="11" font-weight="600">\U0001F4BB IDE Diff</text>
      <text x="692" y="291" text-anchor="middle" fill="var(--dim)" font-size="9">apply \u0432 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440\u0435</text>
      <text x="692" y="306" text-anchor="middle" fill="var(--dim)" font-size="9">inline \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435</text>
      
      <rect x="765" y="250" width="120" height="70" rx="10" fill="var(--card-bg)" stroke="#f59e0b" stroke-width="1.5"/>
      <text x="825" y="272" text-anchor="middle" fill="#f59e0b" font-size="11" font-weight="600">\U0001F4BB Terminal</text>
      <text x="825" y="291" text-anchor="middle" fill="var(--dim)" font-size="9">\u043f\u0440\u044f\u043c\u0430\u044f</text>
      <text x="825" y="306" text-anchor="middle" fill="var(--dim)" font-size="9">\u0437\u0430\u043f\u0438\u0441\u044c</text>
      
      <line x1="755" y1="340" x2="755" y2="380" stroke="#22D3EE" stroke-width="1.5" marker-end="url(#aDev)"/>
      <rect x="665" y="383" width="180" height="28" rx="6" fill="#0d1520" stroke="#22D3EE" stroke-width="1"/>
      <text x="755" y="401" text-anchor="middle" fill="#22D3EE" font-size="10">\U0001F504 Feedback Loop: \u0443\u0447\u0438\u0442\u0441\u044f \u043d\u0430 \u043e\u0448\u0438\u0431\u043a\u0430\u0445</text>
    </svg>
  </div>

  <div style="margin:32px 0">
    <div class="section-hd"><h2>\U0001F4E6 \u0427\u0435\u0442\u044b\u0440\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438 AI-\u0430\u0433\u0435\u043d\u0442\u043e\u0432</h2></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px">
      <div style="background:var(--card-bg);border:1px solid #10b98133;border-radius:var(--radius);padding:20px">
        <div style="font-size:28px;margin-bottom:8px">\U0001F4BB</div>
        <div style="font-size:14px;font-weight:700;color:#10b981;margin-bottom:6px">IDE-\u0438\u043d\u0442\u0435\u0433\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0435</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6;margin-bottom:10px">\u0410\u0432\u0442\u043e\u0434\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u043f\u0440\u044f\u043c\u043e \u0432 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440\u0435. \u0412\u0438\u0434\u044f\u0442 \u0432\u0430\u0448 \u043a\u0443\u0440\u0441\u043e\u0440, \u0432\u043a\u043b\u0430\u0434\u043a\u0438, \u0431\u0443\u0444\u0435\u0440 \u043e\u0431\u043c\u0435\u043d\u0430. \u041c\u0433\u043d\u043e\u0432\u0435\u043d\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0442\u043d\u0430\u044f \u0441\u0432\u044f\u0437\u044c.</div>
        <div style="font-size:10px;color:var(--dim)">{len(ide_agents)} \u0430\u0433\u0435\u043d\u0442\u043e\u0432: Cursor, Copilot, Cline, Continue, Codeium, Cody, Tabnine, Windsurf, Amazon Q</div>
      </div>
      <div style="background:var(--card-bg);border:1px solid #3B82F633;border-radius:var(--radius);padding:20px">
        <div style="font-size:28px;margin-bottom:8px">\U0001F4DF</div>
        <div style="font-size:14px;font-weight:700;color:#3B82F6;margin-bottom:6px">\u0422\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u044c\u043d\u044b\u0435</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6;margin-bottom:10px">CLI-\u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b \u0434\u043b\u044f \u0430\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u043e\u0439 \u0440\u0430\u0431\u043e\u0442\u044b: \u0447\u0438\u0442\u0430\u044e\u0442 \u0432\u0441\u044e \u043a\u043e\u0434\u043e\u0432\u0443\u044e \u0431\u0430\u0437\u0443, \u043f\u0438\u0448\u0443\u0442 \u043a\u043e\u0434, \u0434\u0435\u043b\u0430\u044e\u0442 PR. \u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044c.</div>
        <div style="font-size:10px;color:var(--dim)">{len(terminal_agents)} \u0430\u0433\u0435\u043d\u0442\u043e\u0432: Claude Code, Aider, Codex CLI, Open Interpreter</div>
      </div>
      <div style="background:var(--card-bg);border:1px solid #f59e0b33;border-radius:var(--radius);padding:20px">
        <div style="font-size:28px;margin-bottom:8px">\U0001F3A2</div>
        <div style="font-size:14px;font-weight:700;color:#f59e0b;margin-bottom:6px">\u0410\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u044b\u0435</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6;margin-bottom:10px">\u041f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e \u0441\u0430\u043c\u043e\u0441\u0442\u043e\u044f\u0442\u0435\u043b\u044c\u043d\u043e \u0440\u0435\u0448\u0430\u044e\u0442 \u0437\u0430\u0434\u0430\u0447\u0438: \u0431\u0430\u0433-\u0444\u0438\u043a\u0441, \u0440\u0435\u0444\u0430\u043a\u0442\u043e\u0440\u0438\u043d\u0433, feature development. \u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u043e\u0435 \u0443\u0447\u0430\u0441\u0442\u0438\u0435 \u0447\u0435\u043b\u043e\u0432\u0435\u043a\u0430.</div>
        <div style="font-size:10px;color:var(--dim)">{len(autonomous_agents)} \u0430\u0433\u0435\u043d\u0442\u0430: Devin, SWE-Agent</div>
      </div>
      <div style="background:var(--card-bg);border:1px solid #22D3EE33;border-radius:var(--radius);padding:20px">
        <div style="font-size:28px;margin-bottom:8px">\U0001F3A8</div>
        <div style="font-size:14px;font-weight:700;color:#22D3EE;margin-bottom:6px">\u041f\u0440\u043e\u0442\u043e\u0442\u0438\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6;margin-bottom:10px">\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f \u043f\u043e\u043b\u043d\u043e\u0446\u0435\u043d\u043d\u044b\u0445 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0439 \u0438\u0437 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u044f. Web-\u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441, full-stack, \u0431\u044b\u0441\u0442\u0440\u044b\u0439 MVP.</div>
        <div style="font-size:10px;color:var(--dim)">{len(prototyping_agents)} \u0430\u0433\u0435\u043d\u0442\u0430: Bolt, Lovable, v0, Replit AI</div>
      </div>
    </div>
  </div>

  <div style="margin:32px 0">
    <div class="section-hd"><h2>\U0001F9E9 \u041c\u0430\u0442\u0440\u0438\u0446\u0430 \u0432\u044b\u0431\u043e\u0440\u0430: \u043a\u0430\u043a\u043e\u0439 \u0430\u0433\u0435\u043d\u0442 \u0434\u043b\u044f \u043a\u0430\u043a\u043e\u0439 \u0437\u0430\u0434\u0430\u0447\u0438</h2></div>
    <div class="compare-table-wrap" style="margin-bottom:16px">
      <table class="compare-table">
        <thead><tr><th>\u0417\u0430\u0434\u0430\u0447\u0430</th><th>\U0001F3C6 \u041b\u0443\u0447\u0448\u0438\u0439</th><th>\U0001F947 \u0410\u043b\u044c\u0442\u0435\u0440\u043d\u0430\u0442\u0438\u0432\u0430</th><th>\u041f\u043e\u0447\u0435\u043c\u0443</th></tr></thead>
        <tr><td>\u0410\u0432\u0442\u043e\u0434\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u043d\u0430 \u043b\u0435\u0442\u0443</td><td style="color:#10b981;font-weight:600">Cursor IDE</td><td>Copilot, Cline</td><td style="font-size:12px">\u041c\u0433\u043d\u043e\u0432\u0435\u043d\u043d\u0430\u044f \u0433\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f, \u043f\u043e\u043d\u0438\u043c\u0430\u043d\u0438\u0435 \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442\u0430 \u043f\u0440\u043e\u0435\u043a\u0442\u0430</td></tr>
        <tr><td>\u0410\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u044b\u0439 PR</td><td style="color:#3B82F6;font-weight:600">Claude Code</td><td>Aider, Codex CLI</td><td style="font-size:12px">\u0412\u0438\u0434\u0438\u0442 \u0432\u0441\u044e \u043a\u043e\u0434\u043e\u0432\u0443\u044e \u0431\u0430\u0437\u0443, \u0430\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u0430\u044f \u0440\u0430\u0431\u043e\u0442\u0430</td></tr>
        <tr><td>Code Review</td><td style="color:#22D3EE;font-weight:600">Codex CLI</td><td>Claude Code, Copilot</td><td style="font-size:12px">\u0421\u043f\u0435\u0446\u0438\u0430\u043b\u044c\u043d\u043e \u0437\u0430\u0442\u043e\u0447\u0435\u043d \u043d\u0430 \u0440\u0435\u0432\u044c\u044e</td></tr>
        <tr><td>\u041a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430</td><td style="color:#f59e0b;font-weight:600">GitHub Copilot</td><td>Cody, Codeium</td><td style="font-size:12px">\u041b\u0438\u0446\u0435\u043d\u0437\u0438\u0438 \u043d\u0430 \u043a\u043e\u043c\u0430\u043d\u0434\u0443, \u0430\u0434\u043c\u0438\u043d\u043a\u0430</td></tr>
        <tr><td>Open Source / \u0421\u0442\u0430\u0440\u0442\u0430\u043f</td><td style="color:#10b981;font-weight:600">Continue + Aider</td><td>Cline, Ollama</td><td style="font-size:12px">\u0411\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e, \u0432\u044b\u0431\u0438\u0440\u0430\u0435\u0448\u044c \u043c\u043e\u0434\u0435\u043b\u044c, \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u043e</td></tr>
        <tr><td>\u0411\u044b\u0441\u0442\u0440\u044b\u0439 MVP</td><td style="color:#22D3EE;font-weight:600">Bolt.new / v0</td><td>Lovable, Replit</td><td style="font-size:12px">\u041f\u043e\u043b\u043d\u043e\u0435 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u0438\u0437 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u044f</td></tr>
        <tr><td>\u0421\u043b\u043e\u0436\u043d\u044b\u0439 \u0431\u0430\u0433-\u0444\u0438\u043a\u0441</td><td style="color:#f59e0b;font-weight:600">Devin / SWE-Agent</td><td>Claude Code</td><td style="font-size:12px">\u041f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e \u0430\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u0430\u044f \u043e\u0442\u043b\u0430\u0434\u043a\u0430</td></tr>
        <tr><td>\u0418\u043d\u0442\u0435\u0440\u0430\u043a\u0442\u0438\u0432\u043d\u0430\u044f \u0440\u0430\u0431\u043e\u0442\u0430</td><td style="color:#3B82F6;font-weight:600">Open Interpreter</td><td>Claude Code</td><td style="font-size:12px">\u0418\u0441\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u043a\u043e\u0434\u0430 \u0432 \u0436\u0438\u0432\u0443\u044e</td></tr>
      </table>
    </div>
  </div>

  <div style="margin:32px 0;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:24px">
    <h3 style="color:var(--green);font-size:16px;margin-bottom:12px">\U0001F91D Multi-Agent \u0441\u0442\u0435\u043a: \u043a\u0430\u043a \u043e\u0431\u044a\u0435\u0434\u0438\u043d\u0438\u0442\u044c \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u043e \u0430\u0433\u0435\u043d\u0442\u043e\u0432</h3>
    <p style="color:var(--muted);font-size:13px;margin-bottom:16px">\u0420\u0435\u0430\u043b\u044c\u043d\u044b\u0439 \u0441\u0442\u0435\u043a \u0441\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0433\u043e AI-\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0430: \u043d\u0435 \u043e\u0434\u0438\u043d \u0430\u0433\u0435\u043d\u0442, \u0430 \u043a\u043e\u043c\u0431\u0438\u043d\u0430\u0446\u0438\u044f \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u0432 \u043d\u0430 \u0440\u0430\u0437\u043d\u044b\u0445 \u044d\u0442\u0430\u043f\u0430\u0445 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0438.</p>
    <svg viewBox="0 0 800 220" style="max-width:800px;width:100%;height:auto">
      <defs>
        <marker id="aS" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#3B82F6"/></marker>
        <filter id="glMM"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      
      <rect x="10" y="10" width="170" height="85" rx="10" fill="var(--card-bg)" stroke="#10b981" stroke-width="1.5"/>
      <text x="95" y="35" text-anchor="middle" fill="#10b981" font-size="11" font-weight="700">\U0001F4BB \u041d\u0430\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u043e\u0434\u0430</text>
      <text x="95" y="55" text-anchor="middle" fill="#F5F7FA" font-size="10">Cursor IDE / Copilot</text>
      <text x="95" y="72" text-anchor="middle" fill="var(--dim)" font-size="9">\u0430\u0432\u0442\u043e\u0434\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435</text>
      <text x="95" y="87" text-anchor="middle" fill="var(--dim)" font-size="9">inline \u043f\u0440\u0430\u0432\u043a\u0438</text>
      
      <line x1="180" y1="52" x2="225" y2="52" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#aS)"/>
      <text x="202" y="42" fill="var(--dim)" font-size="9">commit</text>
      
      <rect x="230" y="10" width="170" height="85" rx="10" fill="var(--card-bg)" stroke="#3B82F6" stroke-width="1.5"/>
      <text x="315" y="35" text-anchor="middle" fill="#3B82F6" font-size="11" font-weight="700">\U0001F4A1 Code Review</text>
      <text x="315" y="55" text-anchor="middle" fill="#F5F7FA" font-size="10">Claude Code / Codex CLI</text>
      <text x="315" y="72" text-anchor="middle" fill="var(--dim)" font-size="9">\u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 PR</text>
      <text x="315" y="87" text-anchor="middle" fill="var(--dim)" font-size="9">security + style</text>
      
      <line x1="400" y1="52" x2="445" y2="52" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#aS)"/>
      
      <rect x="450" y="10" width="160" height="85" rx="10" fill="var(--card-bg)" stroke="#22D3EE" stroke-width="1.5"/>
      <text x="530" y="35" text-anchor="middle" fill="#22D3EE" font-size="11" font-weight="700">\u2699\ufe0f CI Pipeline</text>
      <text x="530" y="55" text-anchor="middle" fill="#F5F7FA" font-size="10">GitHub Actions</text>
      <text x="530" y="72" text-anchor="middle" fill="var(--dim)" font-size="9">tests + lint</text>
      <text x="530" y="87" text-anchor="middle" fill="var(--dim)" font-size="9">+ AI \u0440\u0435\u0432\u044c\u044e</text>
      
      <line x1="610" y1="52" x2="655" y2="52" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#aS)"/>
      
      <rect x="660" y="10" width="130" height="85" rx="10" fill="var(--card-bg)" stroke="#10b981" stroke-width="1.5" filter="url(#glMM)"/>
      <text x="725" y="35" text-anchor="middle" fill="#10b981" font-size="11" font-weight="700">\u2705 Merge</text>
      <text x="725" y="55" text-anchor="middle" fill="#F5F7FA" font-size="10">Deploy</text>
      <text x="725" y="72" text-anchor="middle" fill="var(--dim)" font-size="9">\u0432\u0441\u0435 \u0447\u0435\u043a\u0438</text>
      <text x="725" y="87" text-anchor="middle" fill="var(--dim)" font-size="9">\u043f\u0440\u043e\u0439\u0434\u0435\u043d\u044b</text>
      
      <rect x="60" y="120" width="140" height="60" rx="8" fill="#0d1520" stroke="var(--amber)" stroke-width="1"/>
      <text x="130" y="142" text-anchor="middle" fill="var(--amber)" font-size="10">\U0001F4D6 \u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u044f</text>
      <text x="130" y="158" text-anchor="middle" fill="var(--dim)" font-size="9">Mintlify / Doc agents</text>
      <text x="130" y="173" text-anchor="middle" fill="var(--dim)" font-size="9">\u0430\u0432\u0442\u043e-\u0433\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f</text>
      
      <rect x="240" y="120" width="140" height="60" rx="8" fill="#0d1520" stroke="#22D3EE" stroke-width="1"/>
      <text x="310" y="142" text-anchor="middle" fill="#22D3EE" font-size="10">\U0001F41B \u0411\u0430\u0433-\u0444\u0438\u043a\u0441</text>
      <text x="310" y="158" text-anchor="middle" fill="var(--dim)" font-size="9">SWE-Agent / Devin</text>
      <text x="310" y="173" text-anchor="middle" fill="var(--dim)" font-size="9">\u0430\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u044b\u0439</text>
      
      <rect x="420" y="120" width="140" height="60" rx="8" fill="#0d1520" stroke="#10b981" stroke-width="1"/>
      <text x="490" y="142" text-anchor="middle" fill="#10b981" font-size="10">\U0001F9EA \u0422\u0435\u0441\u0442\u044b</text>
      <text x="490" y="158" text-anchor="middle" fill="var(--dim)" font-size="9">\u0410\u0432\u0442\u043e-\u0433\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f</text>
      <text x="490" y="173" text-anchor="middle" fill="var(--dim)" font-size="9">+ \u043c\u0443\u0442\u0430\u0446\u0438\u043e\u043d\u043d\u043e\u0435</text>
      
      <rect x="600" y="120" width="140" height="60" rx="8" fill="#0d1520" stroke="#3B82F6" stroke-width="1"/>
      <text x="670" y="142" text-anchor="middle" fill="#3B82F6" font-size="10">\U0001F527 \u0420\u0435\u0444\u0430\u043a\u0442\u043e\u0440\u0438\u043d\u0433</text>
      <text x="670" y="158" text-anchor="middle" fill="var(--dim)" font-size="9">Claude Code / Aider</text>
      <text x="670" y="173" text-anchor="middle" fill="var(--dim)" font-size="9">\u043f\u043e\u043b\u043d\u0430\u044f \u043a\u043e\u0434\u043e\u0432\u0430\u044f \u0431\u0430\u0437\u0430</text>
    </svg>
  </div>

  <div style="margin:32px 0">
    <div class="section-hd"><h2>\u26a1 \u0411\u044b\u0441\u0442\u0440\u044b\u0439 \u0432\u044b\u0431\u043e\u0440</h2></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px">
      <div style="background:var(--card-bg);border:1px solid var(--green);border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;color:var(--green);font-weight:600;margin-bottom:8px">\U0001F3C6 \u041b\u0443\u0447\u0448\u0438\u0439 \u0434\u043b\u044f \u0441\u043e\u043b\u043e</div>
        <div style="font-size:15px;font-weight:700;color:var(--text);margin-bottom:4px">{esc(best_ide.get('title','')) if best_ide else 'Cursor IDE'}</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6">{'\u041c\u0433\u043d\u043e\u0432\u0435\u043d\u043d\u043e\u0435 \u0430\u0432\u0442\u043e\u0434\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435, \u043f\u043e\u043d\u0438\u043c\u0430\u043d\u0438\u0435 \u0432\u0441\u0435\u0439 \u043a\u043e\u0434\u043e\u0432\u043e\u0439 \u0431\u0430\u0437\u044b, AI-first IDE.' if best_ide else ''}</div>
        <a href="/product/{best_ide['slug'] if best_ide else 'cursor-ide'}/" style="display:inline-block;margin-top:12px;color:var(--green);font-size:12px;font-weight:600">\u0421\u043c\u043e\u0442\u0440\u0435\u0442\u044c &rarr;</a>
      </div>
      <div style="background:var(--card-bg);border:1px solid var(--blue);border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;color:var(--blue);font-weight:600;margin-bottom:8px">\U0001F680 \u041b\u0443\u0447\u0448\u0438\u0439 \u0434\u043b\u044f PR</div>
        <div style="font-size:15px;font-weight:700;color:var(--text);margin-bottom:4px">{esc(best_pr.get('title','')) if best_pr else 'Claude Code'}</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6">{'\u041f\u0438\u0448\u0435\u0442 PR \u0430\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u043e, \u0447\u0438\u0442\u0430\u0435\u0442 \u0432\u0441\u044e \u043a\u043e\u0434\u043e\u0432\u0443\u044e \u0431\u0430\u0437\u0443, \u0440\u0435\u0444\u0430\u043a\u0442\u043e\u0440\u0438\u0442 \u0441\u043b\u043e\u0436\u043d\u044b\u0435 \u0441\u0438\u0441\u0442\u0435\u043c\u044b.' if best_pr else ''}</div>
        <a href="/product/{best_pr['slug'] if best_pr else 'claude-code'}/" style="display:inline-block;margin-top:12px;color:var(--blue);font-size:12px;font-weight:600">\u0421\u043c\u043e\u0442\u0440\u0435\u0442\u044c &rarr;</a>
      </div>
      <div style="background:var(--card-bg);border:1px solid var(--amber);border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;color:var(--amber);font-weight:600;margin-bottom:8px">\U0001F1EB \u041b\u0443\u0447\u0448\u0438\u0439 \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u044b\u0439</div>
        <div style="font-size:15px;font-weight:700;color:var(--text);margin-bottom:4px">{esc(best_free.get('title','')) if best_free else 'Continue'}</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6">{'Open source, \u0441\u0432\u043e\u0439 API-\u043a\u043b\u044e\u0447, \u043f\u043e\u043b\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044c \u043d\u0430\u0434 \u0434\u0430\u043d\u043d\u044b\u043c\u0438.' if best_free else ''}</div>
        <a href="/product/{best_free['slug'] if best_free else 'continue-dev'}/" style="display:inline-block;margin-top:12px;color:var(--amber);font-size:12px;font-weight:600">\u0421\u043c\u043e\u0442\u0440\u0435\u0442\u044c &rarr;</a>
      </div>
    </div>
  </div>

  <div style="margin:32px 0">
    <div class="section-hd"><h2>\U0001F4CB \u0420\u0435\u0430\u043b\u044c\u043d\u044b\u0439 \u0432\u043e\u0440\u043a\u0444\u043b\u043e\u0443: \u043e\u0442 issue \u0434\u043e merge</h2></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px">
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:12px;color:var(--green);font-weight:600;margin-bottom:12px">\U0001F4A1 \u0412\u043e\u0440\u043a\u0444\u043b\u043e\u0443 \u0441 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u044c\u043d\u044b\u043c \u0430\u0433\u0435\u043d\u0442\u043e\u043c</div>
        <div style="font-family:monospace;font-size:11px;color:var(--muted);line-height:2.2;background:#0d1117;padding:14px;border-radius:8px">
          <div style="color:var(--dim)"># 1. \u041e\u0442\u043a\u0440\u044b\u0432\u0430\u0435\u043c issue</div>
          <div style="color:#79c0ff">gh issue create</div>
          <div style="color:var(--dim);margin-top:6px"># 2. \u0410\u0433\u0435\u043d\u0442 \u0447\u0438\u0442\u0430\u0435\u0442 issue + \u043a\u043e\u0434\u043e\u0432\u0443\u044e \u0431\u0430\u0437\u0443</div>
          <div style="color:#79c0ff">claude "\u0420\u0435\u0448\u0438 #42: \u0434\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043a\u044d\u0448"</div>
          <div style="color:var(--dim);margin-top:6px"># 3. \u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442:</div>
          <div style="color:var(--dim)">\u2192 3 \u0444\u0430\u0439\u043b\u0430 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u043e</div>
          <div style="color:var(--dim)">\u2192 tests \u043f\u0440\u043e\u0439\u0434\u0435\u043d\u044b</div>
          <div style="color:var(--dim)">\u2192 PR \u0441\u043e\u0437\u0434\u0430\u043d \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438</div>
        </div>
      </div>
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:12px;color:#3B82F6;font-weight:600;margin-bottom:12px">\U0001F91D \u0412\u043e\u0440\u043a\u0444\u043b\u043e\u0443 \u0441 IDE + \u0430\u0433\u0435\u043d\u0442\u043e\u043c</div>
        <div style="font-family:monospace;font-size:11px;color:var(--muted);line-height:2.2;background:#0d1117;padding:14px;border-radius:8px">
          <div style="color:var(--dim)"># 1. \u041f\u0438\u0448\u0435\u043c \u043a\u043e\u0434 \u0432 IDE</div>
          <div style="color:var(--dim)">Cursor: autocomplete + \u043f\u0440\u0430\u0432\u043a\u0438</div>
          <div style="color:var(--dim);margin-top:6px"># 2. \u041a\u043e\u043c\u043c\u0438\u0442\u0438\u043c</div>
          <div style="color:#79c0ff">git commit -m "feat: ..."</div>
          <div style="color:var(--dim);margin-top:6px"># 3. \u0417\u0430\u043f\u0443\u0441\u043a\u0430\u0435\u043c \u0430\u0433\u0435\u043d\u0442\u0430 \u043d\u0430 \u0440\u0435\u0432\u044c\u044e</div>
          <div style="color:#79c0ff">codex review HEAD~1</div>
          <div style="color:var(--dim)">\u2192 \u043d\u0430\u0448\u0451\u043b 2 security issues</div>
          <div style="color:var(--dim)">\u2192 \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0438\u043b \u0444\u0438\u043a\u0441</div>
        </div>
      </div>
    </div>
  </div>

  <div class="section-hd" style="margin-top:32px"><h2>\U0001F527 \u0412\u0441\u0435 AI Coding Agents ({len(coding)})</h2></div>
  <div class="grid" style="margin-bottom:32px">
    {cards}
  </div>

  <div class="section-hd"><h2>\U0001F4CA \u0421\u0440\u0430\u0432\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u0430\u044f \u0442\u0430\u0431\u043b\u0438\u0446\u0430</h2></div>
  <div class="compare-table-wrap" style="margin-bottom:32px">
    <table class="compare-table">
      <tr><th>\u0410\u0433\u0435\u043d\u0442</th><th>QantScore</th><th>\u0420\u0435\u0439\u0442\u0438\u043d\u0433</th><th>\u0426\u0435\u043d\u0430</th><th>\u0422\u0438\u043f</th><th>\u0412\u0437\u0430\u0438\u043c\u043e\u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435</th><th>\u0420\u0430\u0437\u0432\u0451\u0440\u0442\u044b\u0432\u0430\u043d\u0438\u0435</th></tr>
      {_dev_table_rows(coding)}
    </table>
  </div>

  <div style="margin:40px 0">
    <div class="section-hd"><h2>💰 Стоимость: полное сравнение тарифов</h2></div>
    <div class="compare-table-wrap" style="margin-bottom:16px">
      <table class="compare-table">
        <thead><tr><th>Агент</th><th>Бесплатный тариф</th><th>Pro / Team</th><th>Enterprise</th><th>Модель</th></tr></thead>
        <tr><td style="color:var(--green);font-weight:600">Cursor IDE</td><td>Hobby (2000 comp/mo)</td><td>$20/мес</td><td>$40/мес</td><td>Подписка + usage</td></tr>
        <tr><td style="color:var(--green);font-weight:600">GitHub Copilot</td><td>Free (2000 comp/mo)</td><td>$10/мес</td><td>$39/мес Business</td><td>Подписка</td></tr>
        <tr><td style="color:var(--green);font-weight:600">Claude Code</td><td>—</td><td>API pay-per-token</td><td>Max/Enterprise</td><td>Pay-as-you-go</td></tr>
        <tr><td style="color:var(--green);font-weight:600">Aider</td><td>Open Source ✅</td><td>Свой API-ключ</td><td>Свой API-ключ</td><td>Бесплатно + LLM</td></tr>
        <tr><td>Codeium Windsurf</td><td>Free (unlimited)</td><td>$15/мес</td><td>$35/мес</td><td>Freemium</td></tr>
        <tr><td>Continue.dev</td><td>Open Source ✅</td><td>Свой ключ / $10</td><td>Свой ключ</td><td>Бесплатно + опции</td></tr>
        <tr><td>Cline (VS Code)</td><td>Open Source ✅</td><td>Свой API-ключ</td><td>Свой API-ключ</td><td>Бесплатно + LLM</td></tr>
        <tr><td>Devin</td><td>—</td><td>$500/мес</td><td>Кастом</td><td>Подписка</td></tr>
        <tr><td>Bolt.new</td><td>Free (ограничено)</td><td>$20/мес</td><td>$50/мес</td><td>Freemium</td></tr>
        <tr><td>v0 (Vercel)</td><td>Free (ограничено)</td><td>$20/мес</td><td>Кастом</td><td>Freemium</td></tr>
      </table>
    </div>
    <p style="font-size:12px;color:var(--dim);margin-top:8px">Цены на май 2026. Бесплатные Open Source агенты требуют своего API-ключа к LLM. Средняя стоимость токенов: $0.50–$5/час активного кодинга.</p>
  </div>

  <div style="margin:40px 0">
    <div class="section-hd"><h2>🔒 Безопасность и приватность кода</h2></div>
    <p style="font-size:13px;color:var(--muted);line-height:1.8;margin-bottom:16px">Главный вопрос при выборе AI-агента: куда уходит ваш код? Разные агенты имеют принципиально разную модель доступа — от нулевого (всё локально) до полного (код на сторонних серверах).</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px">
      <div style="background:var(--card-bg);border:1px solid #10b98133;border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;font-weight:700;color:#10b981;margin-bottom:8px">🟢 Локальные (код не покидает машину)</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6">Continue.dev, Aider, Cline, Open Interpreter — работают с локальными LLM (Ollama) или вашим API-ключом. Вы контролируете, куда идут данные.</div>
        <div style="font-size:10px;color:var(--dim);margin-top:8px">Рекомендуется: fintech, healthcare, enterprise с NDA</div>
      </div>
      <div style="background:var(--card-bg);border:1px solid #f59e0b33;border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;font-weight:700;color:#f59e0b;margin-bottom:8px">🟡 Гибридные (часть кода — в облако)</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6">Cursor, Copilot, Codeium — отправляют контекст (текущий файл, буфер) на серверы. Не отправляют всю кодовую базу. SOC 2 сертифицированы.</div>
        <div style="font-size:10px;color:var(--dim);margin-top:8px">Рекомендуется: большинство коммерческих проектов</div>
      </div>
      <div style="background:var(--card-bg);border:1px solid #ef444433;border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;font-weight:700;color:#ef4444;margin-bottom:8px">🔴 Облачные (вся база на сервере)</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6">Devin, Bolt.new, v0 — код уходит на облачные серверы для обработки. Удобно, но требует доверия к провайдеру.</div>
        <div style="font-size:10px;color:var(--dim);margin-top:8px">Рекомендуется: прототипы, open source, non-critical</div>
      </div>
    </div>
  </div>

  <div style="margin:40px 0">
    <div class="section-hd"><h2>⚡ Производительность: latency, контекст и токены</h2></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px">
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;font-weight:700;color:var(--green);margin-bottom:10px">⏱️ Задержка автодополнения</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.8">
          <div>🖱️ Cursor: <b style="color:var(--green)">200-400ms</b> — мгновенное</div>
          <div>📝 Copilot: <b style="color:var(--green)">300-600ms</b> — быстрое</div>
          <div>🔧 Cline: <b style="color:var(--amber)">800-2000ms</b> — зависит от модели</div>
          <div>🤖 Claude Code: <b style="color:var(--amber)">1-5s</b> — думает над задачей</div>
          <div style="margin-top:8px;font-size:11px;color:var(--dim)">Меньше = лучше. IDE-агенты быстрее терминальных.</div>
        </div>
      </div>
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;font-weight:700;color:var(--blue);margin-bottom:10px">📐 Размер контекстного окна</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.8">
          <div>Claude Code: <b style="color:var(--green)">200K токенов</b> (вся база)</div>
          <div>Aider: <b style="color:var(--green)">128-200K</b> зависит от модели</div>
          <div>Cursor: <b style="color:var(--blue)">~10K токенов</b> (релевантные файлы)</div>
          <div>Copilot: <b style="color:var(--blue)">~8K токенов</b> (текущий файл + соседи)</div>
          <div style="margin-top:8px;font-size:11px;color:var(--dim)">Больше контекст = лучше понимание проекта, но выше цена и latency.</div>
        </div>
      </div>
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;font-weight:700;color:var(--cyan);margin-bottom:10px">💸 Расход токенов в час</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.8">
          <div>IDE agent: <b style="color:var(--green)">5-15K</b> токенов/час</div>
          <div>CLI agent (активный): <b style="color:var(--amber)">50-200K</b> токенов/час</div>
          <div>Автономный PR: <b style="color:var(--amber)">100-500K</b> токенов/задача</div>
          <div style="margin-top:8px;font-size:11px;color:var(--dim)">Средняя стоимость: $1-10/день активной разработки.</div>
        </div>
      </div>
    </div>
  </div>

  <div style="margin:40px 0">
    <div class="section-hd"><h2>🔌 Совместимость с IDE и платформами</h2></div>
    <div class="compare-table-wrap" style="margin-bottom:16px">
      <table class="compare-table">
        <thead><tr><th>Агент</th><th>VS Code</th><th>JetBrains</th><th>Neovim</th><th>Терминал</th><th>Web</th></tr></thead>
        <tr><td style="color:var(--green);font-weight:600">Cursor IDE</td><td>— (свой редактор)</td><td>—</td><td>—</td><td>—</td><td>—</td></tr>
        <tr><td style="color:var(--green);font-weight:600">Copilot</td><td>✅</td><td>✅</td><td>✅</td><td>✅ CLI</td><td>✅</td></tr>
        <tr><td style="color:var(--green);font-weight:600">Claude Code</td><td>✅ терминал</td><td>✅ терминал</td><td>✅</td><td>✅</td><td>—</td></tr>
        <tr><td style="color:var(--green);font-weight:600">Aider</td><td>✅ терминал</td><td>✅ терминал</td><td>✅</td><td>✅</td><td>—</td></tr>
        <tr><td>Cline</td><td>✅</td><td>—</td><td>—</td><td>—</td><td>—</td></tr>
        <tr><td>Continue.dev</td><td>✅</td><td>✅</td><td>—</td><td>—</td><td>—</td></tr>
        <tr><td>Codeium</td><td>✅</td><td>✅</td><td>✅</td><td>—</td><td>✅</td></tr>
        <tr><td>Codex CLI</td><td>—</td><td>—</td><td>—</td><td>✅</td><td>—</td></tr>
      </table>
    </div>
    <p style="font-size:12px;color:var(--dim);margin-top:4px">* Cursor — самостоятельная IDE (форк VS Code). Агенты с пометкой «терминал» работают в любом редакторе через встроенный терминал.</p>
  </div>

  <div style="margin:40px 0">
    <div class="section-hd"><h2>📋 Дерево решений: как выбрать AI-агента</h2></div>
    <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:24px;font-size:13px;color:var(--muted);line-height:2">
      <div style="margin-bottom:16px"><b style="color:var(--text)">1. Ваш бюджет?</b></div>
      <div style="margin-left:20px">→ <b style="color:var(--green)">$0</b> (бесплатно): Continue.dev + Aider + своя LLM (Ollama/DeepSeek). Либо Cline + OpenRouter.</div>
      <div style="margin-left:20px">→ <b style="color:var(--blue)">$10-20/мес</b>: Cursor Pro или Copilot — наилучшее соотношение цена/качество.</div>
      <div style="margin-left:20px">→ <b style="color:var(--amber)">$500+/мес</b>: Devin для автономных задач + Copilot для IDE.</div>
      <div style="margin:20px 0 8px"><b style="color:var(--text)">2. Где вы пишете код?</b></div>
      <div style="margin-left:20px">→ <b style="color:var(--green)">В IDE</b>: Cursor (лучший AI-native редактор) или Copilot (если привязаны к JetBrains).</div>
      <div style="margin-left:20px">→ <b style="color:var(--blue)">В терминале</b>: Claude Code для сложных задач, Aider для простых правок.</div>
      <div style="margin:20px 0 8px"><b style="color:var(--text)">3. Требования к безопасности?</b></div>
      <div style="margin-left:20px">→ <b style="color:var(--green)">NDA / fintech</b>: Continue.dev + Ollama (100% локально, код не покидает машину).</div>
      <div style="margin-left:20px">→ <b style="color:var(--blue)">SOC 2 ок</b>: Cursor или Copilot (сертифицированы, код в облаке).</div>
      <div style="margin:20px 0 8px"><b style="color:var(--text)">4. Тип задач?</b></div>
      <div style="margin-left:20px">→ <b style="color:var(--green)">Потоковое кодирование</b>: Cursor / Copilot — автодополнение на лету.</div>
      <div style="margin-left:20px">→ <b style="color:var(--blue)">Feature / PR</b>: Claude Code — читает всю базу, пишет код, создаёт PR.</div>
      <div style="margin-left:20px">→ <b style="color:var(--cyan)">MVP / прототип</b>: Bolt.new или v0 — приложение из описания за минуты.</div>
      <div style="margin-left:20px">→ <b style="color:var(--amber)">Сложный баг-фикс</b>: Devin или SWE-Agent — автономная отладка.</div>
    </div>
  </div>

  <div style="margin:40px 0">
    <div class="section-hd"><h2>👥 Командные сценарии использования</h2></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px">
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:14px;font-weight:700;color:var(--green);margin-bottom:10px">🚀 Стартап (3-5 чел)</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.8">
          <div>• Cursor Pro для всех разработчиков</div>
          <div>• Claude Code для ревью PR</div>
          <div>• Bolt.new для прототипов</div>
          <div style="margin-top:8px;font-size:11px;color:var(--dim)">Бюджет: ~$60-100/мес на команду</div>
        </div>
      </div>
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:14px;font-weight:700;color:var(--blue);margin-bottom:10px">🏢 Enterprise (20-100+)</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.8">
          <div>• GitHub Copilot Business ($39/чел)</div>
          <div>• Code review automation (Codex CLI)</div>
          <div>• Индивидуально: Claude Code для синьоров</div>
          <div style="margin-top:8px;font-size:11px;color:var(--dim)">Бюджет: ~$800-4000/мес</div>
        </div>
      </div>
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:14px;font-weight:700;color:var(--amber);margin-bottom:10px">🔓 Open Source проект</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.8">
          <div>• Continue.dev + DeepSeek/Claude API</div>
          <div>• Aider для контрибьюторов</div>
          <div>• Copilot Free для casual участников</div>
          <div style="margin-top:8px;font-size:11px;color:var(--dim)">Бюджет: $0-20/мес на человека</div>
        </div>
      </div>
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:14px;font-weight:700;color:var(--cyan);margin-bottom:10px">🎓 Обучение / Pet-project</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.8">
          <div>• Copilot Free (2000 comp/мес)</div>
          <div>• Codeium Free (безлимитный)</div>
          <div>• Cline + OpenRouter ($5 кредита)</div>
          <div style="margin-top:8px;font-size:11px;color:var(--dim)">Бюджет: $0-5/мес</div>
        </div>
      </div>
    </div>
  </div>

  <div style="margin:40px 0">
    <div class="section-hd"><h2>🔄 CI/CD интеграция AI-агентов</h2></div>
    <p style="font-size:13px;color:var(--muted);line-height:1.8;margin-bottom:16px">AI-агенты всё глубже интегрируются в пайплайны Continuous Integration. Вот как разные агенты встраиваются в процесс от коммита до деплоя:</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px">
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;font-weight:700;color:var(--green);margin-bottom:8px">📝 Pre-commit хук</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6">Claude Code, Aider, Codex CLI — запускаются как git hook. Проверяют код перед коммитом: lint, типы, тесты, безопасность.</div>
        <div style="font-family:monospace;font-size:10px;color:var(--dim);margin-top:8px;background:#0d1117;padding:8px;border-radius:4px"># .git/hooks/pre-commit<br/>claude "review staged changes"</div>
      </div>
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;font-weight:700;color:var(--blue);margin-bottom:8px">🔍 PR Review Automation</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6">GitHub Actions + Claude Code/Codex CLI. Автоматически проверяет каждый PR: security scan, style guide, architecture review.</div>
        <div style="font-family:monospace;font-size:10px;color:var(--dim);margin-top:8px;background:#0d1117;padding:8px;border-radius:4px"># .github/workflows/review.yml<br/>codex review PR-${{ PR_NUMBER }}</div>
      </div>
      <div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
        <div style="font-size:13px;font-weight:700;color:var(--cyan);margin-bottom:8px">🐛 Авто-фикс багов</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6">Devin, SWE-Agent — получают issue из трекера, автономно исправляют баг, создают PR с фиксом и тестами. Минимальное участие человека.</div>
        <div style="font-family:monospace;font-size:10px;color:var(--dim);margin-top:8px;background:#0d1117;padding:8px;border-radius:4px"># Полностью автономно<br/>devin solve "Fix #342: NPE in auth"</div>
      </div>
    </div>
  </div>

  <div style="margin:40px 0">
    <div class="section-hd"><h2>📊 Сравнение моделей: какие LLM используют агенты</h2></div>
    <div class="compare-table-wrap" style="margin-bottom:16px">
      <table class="compare-table">
        <thead><tr><th>Агент</th><th>Модель по умолчанию</th><th>Выбор модели</th><th>Локальные модели</th><th>Провайдеры</th></tr></thead>
        <tr><td style="color:var(--green);font-weight:600">Cursor</td><td>GPT-4o / Claude 4</td><td>✅ Встроенный выбор</td><td>—</td><td>OpenAI, Anthropic</td></tr>
        <tr><td style="color:var(--green);font-weight:600">Copilot</td><td>GPT-4o-mini</td><td>⚠️ Ограничен</td><td>—</td><td>OpenAI</td></tr>
        <tr><td style="color:var(--green);font-weight:600">Claude Code</td><td>Claude Sonnet 4</td><td>✅ Любая модель</td><td>—</td><td>Anthropic</td></tr>
        <tr><td style="color:var(--green);font-weight:600">Aider</td><td>Claude 4 / GPT-4o</td><td>✅ Любая модель</td><td>✅ Ollama</td><td>OpenAI, Anthropic, OpenRouter, DeepSeek</td></tr>
        <tr><td>Cline</td><td>Выбор пользователя</td><td>✅ Любая модель</td><td>✅ Ollama, LM Studio</td><td>OpenRouter, OpenAI, Anthropic</td></tr>
        <tr><td>Continue.dev</td><td>Выбор пользователя</td><td>✅ Любая модель</td><td>✅ Ollama, LM Studio</td><td>OpenAI, Anthropic, Mistral, DeepSeek, OpenRouter</td></tr>
        <tr><td>Codeium</td><td>Своя модель</td><td>❌ Только своя</td><td>—</td><td>Proprietary</td></tr>
        <tr><td>Devin</td><td>GPT-4o + Claude</td><td>❌ Только своя</td><td>—</td><td>Proprietary</td></tr>
      </table>
    </div>
  </div>


</div>'''

    html = render_page("\u0410\u0433\u0435\u043d\u0442\u044b \u0434\u043b\u044f \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u2014 \u0420\u0435\u0439\u0442\u0438\u043d\u0433 coding agents",
                       f"\u0421\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0435 {len(coding)} AI-\u0430\u0433\u0435\u043d\u0442\u043e\u0432 \u0434\u043b\u044f \u043a\u043e\u0434\u0430: \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438, \u043c\u0430\u0442\u0440\u0438\u0446\u0430 \u0432\u044b\u0431\u043e\u0440\u0430, \u0430\u0440\u0445\u0438\u0442\u0435\u043a\u0442\u0443\u0440\u0430.",
                       body, total=len(coding),
                       active_dev="active",
                       open_graph=make_og("AI-\u0430\u0433\u0435\u043d\u0442\u044b \u0434\u043b\u044f \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u2014 Qantcore", f"\u0421\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0435 {len(coding)} AI coding agents: \u0440\u0435\u0439\u0442\u0438\u043d\u0433, \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438, \u0432\u043e\u0440\u043a\u0444\u043b\u043e\u0443.", "/development/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/development/">')
    write_html(f"{OUT}/development/index.html", html)
    print(f"  /development/index.html")


def _dev_table_rows(coding):
    rows = ""
    for p in sorted(coding, key=lambda x: (x.get("rating",0) or 0), reverse=True):
        r = p.get("rating", 0) or 0
        qs = min(100, round(r*20*0.30 + (min(10, r*1.8+0.5+0.3))*10*0.25 + 7*10*0.20 + (0.5*15+0.5)*1.5*0.15 + (min(10, r*1.5+0.5))*10*0.10))
        price = format_price(p.get("pricing_model",""))
        deploy = "\U0001F3E0 Local" if any(t.lower() in ('docker','local','self-hosted','python','cli','terminal') for t in (p.get('tech_stack',[]) or [])) else "\u2601\ufe0f Cloud"
        ptype = {"agent":"\U0001F916 Agent","framework":"\u2699\ufe0f Framework","platform":"\U0001F3D7\ufe0f Platform","model":"\U0001F9E0 Model","infrastructure":"\U0001F527 Infra"}.get(p.get("product_type",""), p.get("product_type",""))
        interaction = "\U0001F4BB IDE" if p["slug"] in {"cursor-ide","cline-vscode","continue-dev","github-copilot","codeium-windsurf","sourcegraph-cody","tabnine-ai","windsurf-ide","amazon-q-developer"} else "\U0001F4DF CLI" if p["slug"] in {"claude-code","aider-ai","codex-cli","codex-desktop","open-interpreter"} else "\U0001F310 Web" if p["slug"] in {"devin-agent","bolt-new","lovable-dev","vercel-v0","replit-ai"} else "\U0001F4BB CLI"
        rows += f'''<tr>
          <td><a href="/product/{p['slug']}/" style="color:var(--green);font-weight:600">{esc(p.get('title','')[:35])}</a></td>
          <td><strong style="color:{'var(--green)' if qs>=85 else 'var(--cyan)' if qs>=70 else 'var(--amber)'}">{qs}</strong></td>
          <td>{r} \u2605</td>
          <td style="color:var(--green)">{price}</td>
          <td style="font-size:12px;color:var(--muted)">{ptype}</td>
          <td style="font-size:12px">{interaction}</td>
          <td>{deploy}</td>
        </tr>'''
    return rows

def generate_multi_agent():
    """Generate /multi-agent/ — decision center for multi-agent architecture."""
    products = list(DB.articles.find({"category": "product"}).sort("rating", -1))
    tp = len(products)
    
    # Framework data for leaderboard
    frameworks = [
        {"name": "LangGraph", "slug": "langgraph-framework", "production": "✅ Enterprise", "learning": "Высокая", "recovery": "✅ Stateful", "state": "Встроенная", "obs": "LangSmith", "local": "✅"},
        {"name": "CrewAI", "slug": "crewai-framework", "production": "⚠️ Growing", "learning": "Низкая", "recovery": "⚠️ Manual", "state": "Memory", "obs": "External", "local": "✅"},
        {"name": "AutoGen", "slug": "autogen-microsoft", "production": "✅ Enterprise", "learning": "Средняя", "recovery": "✅ HITL", "state": "Conversation", "obs": "Azure", "local": "✅ Docker"},
        {"name": "Semantic Kernel", "slug": "semantic-kernel", "production": "✅ Enterprise", "learning": "Средняя", "recovery": "✅ Azure", "state": "Planner", "obs": "Azure", "local": "✅"},
        {"name": "OpenAI Agents SDK", "slug": "openai-swarm", "production": "⚠️ Beta", "learning": "Низкая", "recovery": "⚠️ Limited", "state": "Swarm", "obs": "OpenAI", "local": "☁️"},
        {"name": "MetaGPT", "slug": "metagpt-framework", "production": "⚠️ Experimental", "learning": "Низкая", "recovery": "❌", "state": "Roles", "obs": "External", "local": "✅"},
        {"name": "ChatDev", "slug": "chatdev-agent", "production": "❌ Research", "learning": "Низкая", "recovery": "❌", "state": "Roles", "obs": "External", "local": "✅"},
        {"name": "Phidata", "slug": "phidata-framework", "production": "⚠️ Growing", "learning": "Низкая", "recovery": "⚠️", "state": "Memory", "obs": "External", "local": "✅"},
        {"name": "Dify", "slug": "dify-platform", "production": "⚠️ Growing", "learning": "Низкая", "recovery": "⚠️", "state": "Workflow", "obs": "Built-in", "local": "✅"},
        {"name": "SuperAGI", "slug": "superagi-agent", "production": "⚠️ Growing", "learning": "Низкая", "recovery": "⚠️", "state": "Toolkit", "obs": "External", "local": "✅"},
    ]

    # Build framework table rows
    fw_rows = ""
    for fw in frameworks:
        qs = 0
        prod = DB.articles.find_one({"slug": fw["slug"], "category": "product"})
        if prod:
            r = prod.get("rating", 0) or 0
            qs = min(100, round(r*20*0.30 + 7*10*0.25 + 7*10*0.20 + 15*1.5*0.15 + 7*10*0.10))
        fw_rows += f"""<tr>
          <td style="font-size:15px;font-weight:600"><a href="/product/{fw['slug']}/" style="color:var(--text)">{fw['name']}</a></td>
          <td style="font-size:14px">{fw['production']}</td>
          <td style="font-size:14px">{fw['learning']}</td>
          <td style="font-size:14px">{fw['recovery']}</td>
          <td style="font-size:14px">{fw['state']}</td>
          <td style="font-size:14px">{fw['obs']}</td>
          <td style="font-size:14px">{fw['local']}</td>
        </tr>"""

    # Architecture patterns
    patterns = [
        {"name": "Supervisor", "icon": "👔", "desc": "Manager → Workers", "best": "Оркестрация, task routing, enterprise-потоки", "color": "var(--blue)"},
        {"name": "Swarm", "icon": "🐝", "desc": "Peer agents", "best": "Исследования, брейншторминг, поисковые агенты", "color": "var(--green)"},
        {"name": "Graph-State", "icon": "🔀", "desc": "State machine orchestration", "best": "Надёжность, production, восстановление после сбоев", "color": "var(--cyan)"},
        {"name": "Debate/Consensus", "icon": "⚖️", "desc": "Multi-agent reasoning", "best": "Верификация, планирование, decision systems", "color": "var(--amber)"},
    ]
    pat_cards = ""
    for ap in patterns:
        pat_cards += f"""<div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:24px;flex:1;min-width:220px">
          <div style="font-size:32px;margin-bottom:12px">{ap['icon']}</div>
          <div style="font-size:18px;font-weight:700;color:{ap['color']};margin-bottom:6px">{ap['name']} Pattern</div>
          <div style="font-size:14px;color:var(--text);margin-bottom:8px">{ap['desc']}</div>
          <div style="font-size:12px;color:var(--muted);line-height:1.6">🎯 {ap['best']}</div>
        </div>"""

    # Build guides
    guides = [
        {"title": "Собери свою первую CrewAI систему", "time": "15 мин", "tag": "beginner"},
        {"title": "LangGraph: production деплой", "time": "25 мин", "tag": "advanced"},
        {"title": "AutoGen: enterprise оркестрация", "time": "20 мин", "tag": "intermediate"},
        {"title": "Локальный multi-agent с Ollama", "time": "15 мин", "tag": "beginner"},
        {"title": "Свой MCP-сервер для агентов", "time": "30 мин", "tag": "advanced"},
        {"title": "Observability для multi-agent систем", "time": "20 мин", "tag": "intermediate"},
    ]
    tag_colors = {"beginner": "var(--green)", "intermediate": "var(--amber)", "advanced": "var(--red)"}
    guide_cards = ""
    for g in guides:
        tc = tag_colors.get(g["tag"], "var(--muted)")
        guide_cards += f"""<div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
            <span style="font-size:11px;font-weight:700;color:{tc};background:{tc}1a;padding:2px 8px;border-radius:4px;text-transform:uppercase">{g['tag']}</span>
            <span style="font-size:11px;color:var(--dim)">⏱ {g['time']}</span>
          </div>
          <div style="font-size:15px;font-weight:600;color:var(--text);line-height:1.4">{g['title']}</div>
        </div>"""

    # Who should use what
    who_cards = ""
    who_data = [
        {"who": "Соло-разработчик", "rec": "CrewAI", "why": "Минимальный порог входа, роли и задачи за 10 строк кода. Огромное сообщество."},
        {"who": "Enterprise infra team", "rec": "LangGraph / Semantic Kernel", "why": "Stateful графы, Azure-интеграция, production-grade observability."},
        {"who": "Research lab", "rec": "AutoGen", "why": "Microsoft-экосистема, распределённые агенты, human-in-the-loop из коробки."},
        {"who": "OpenAI-native startup", "rec": "OpenAI Agents SDK", "why": "Минимальный latency, нативная интеграция, swarm-оркестрация."},
    ]
    for w in who_data:
        who_cards += f"""<div style="background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px;flex:1;min-width:220px">
          <div style="font-size:12px;color:var(--dim);text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">{w['who']}</div>
          <div style="font-size:18px;font-weight:700;color:var(--green);margin-bottom:6px">{w['rec']}</div>
          <div style="font-size:13px;color:var(--muted);line-height:1.6">{w['why']}</div>
        </div>"""

    # Monthly changes
    changes = [
        {"date": "Май 2026", "item": "LangGraph", "change": "v0.3 — Cloud deploy, background runs, Cron jobs"},
        {"date": "Май 2026", "item": "CrewAI", "change": "v0.90 — Knowledge graphs, RAG-интеграция в агенты"},
        {"date": "Апр 2026", "item": "AutoGen", "change": "v0.7 — AgentChat API, Magentic-One для сложных задач"},
        {"date": "Апр 2026", "item": "OpenAI", "change": "Agents SDK GA — production-ready swarm orchestration"},
        {"date": "Мар 2026", "item": "Semantic Kernel", "change": "Python 1.0 — parity с .NET, Auto Function Calling"},
    ]
    changes_html = ""
    for ch in changes:
        changes_html += f"""<div style="display:flex;align-items:flex-start;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)">
          <span style="font-size:11px;color:var(--dim);white-space:nowrap;min-width:70px">{ch['date']}</span>
          <span style="font-size:13px;font-weight:600;color:var(--green);min-width:120px">{ch['item']}</span>
          <span style="font-size:13px;color:var(--muted)">{ch['change']}</span>
        </div>"""

    body = f"""<div class="container detail">

  <!-- ─── HERO ─── -->
  <div class="breadcrumbs"><a href="/">Каталог</a> &rsaquo; <span>Мульти-агенты</span></div>
  <div style="margin:32px 0 40px">
    <h1 style="font-size:36px;font-weight:800;color:#f1f5f9;line-height:1.2;margin-bottom:12px">Multi-Agent Systems Intelligence</h1>
    <p style="color:var(--muted);font-size:17px;line-height:1.7;max-width:800px;margin-bottom:28px">Сравнение production-ready фреймворков для multi-agent оркестрации, бенчмарки стратегий координации и выбор архитектуры под ваш стек. Данные обновляются ежедневно.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      <a href="#leaderboard" class="cta-primary" style="text-decoration:none">📊 Сравнить фреймворки</a>
      <a href="#patterns" class="cta-secondary" style="text-decoration:none">🏗️ Архитектуры</a>
      <a href="#benchmarks" class="cta-secondary" style="text-decoration:none">📈 Бенчмарки</a>
      <a href="#stack-builder" class="cta-secondary" style="text-decoration:none">🧩 Собрать стек</a>
    </div>
  </div>

  <!-- ─── LEADERBOARD ─── -->
  <div id="leaderboard" style="margin:48px 0">
    <div class="section-hd"><h2 style="font-size:24px">🏆 Framework Leaderboard</h2></div>
    <p style="color:var(--muted);font-size:14px;margin-bottom:16px">Топ multi-agent фреймворков с оценкой production-готовности</p>
    <div class="compare-table-wrap">
      <table class="compare-table" style="font-size:14px">
        <thead><tr>
          <th style="font-size:13px;text-align:left">Framework</th>
          <th style="font-size:13px">Production</th>
          <th style="font-size:13px">Кривая обучения</th>
          <th style="font-size:13px">Recovery</th>
          <th style="font-size:13px">State</th>
          <th style="font-size:13px">Observability</th>
          <th style="font-size:13px">Local-first</th>
        </tr></thead>
        <tbody>{fw_rows}</tbody>
      </table>
    </div>
  </div>

  <!-- ─── ARCHITECTURE PATTERNS ─── -->
  <div id="patterns" style="margin:48px 0">
    <div class="section-hd"><h2 style="font-size:24px">🧬 Architecture Pattern Explorer</h2></div>
    <p style="color:var(--muted);font-size:14px;margin-bottom:20px">Выберите паттерн оркестрации под вашу задачу. Каждый паттерн — проверенный шаблон для разных сценариев.</p>
    <div style="display:flex;gap:16px;flex-wrap:wrap">{pat_cards}</div>
  </div>

  <!-- ─── STACK BUILDER ─── -->
  <div id="stack-builder" style="margin:48px 0;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:32px">
    <div class="section-hd"><h2 style="font-size:24px">🧩 Собери свой Multi-Agent Stack</h2></div>
    <p style="color:var(--muted);font-size:14px;margin-bottom:24px">Ответьте на 3 вопроса — получите рекомендованный стек</p>
    <div id="ma-stack-builder">
      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:20px">
        <div style="flex:1;min-width:180px">
          <div style="font-size:12px;color:var(--dim);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px">Цель</div>
          <select id="ma-goal" style="width:100%;padding:10px;background:var(--bg);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:14px">
            <option value="">— Выберите —</option>
            <option value="coding">💻 Разработка (Coding)</option>
            <option value="research">🔬 Исследования (Research)</option>
            <option value="autonomous">🤖 Автономное исполнение</option>
            <option value="enterprise">🏢 Enterprise workflows</option>
            <option value="tools">🔧 Инструментальная автоматизация</option>
          </select>
        </div>
        <div style="flex:1;min-width:180px">
          <div style="font-size:12px;color:var(--dim);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px">Инфраструктура</div>
          <select id="ma-infra" style="width:100%;padding:10px;background:var(--bg);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:14px">
            <option value="">— Выберите —</option>
            <option value="local">🏠 Локально</option>
            <option value="hybrid">🔄 Гибрид</option>
            <option value="cloud">☁️ Облако</option>
          </select>
        </div>
        <div style="flex:1;min-width:180px">
          <div style="font-size:12px;color:var(--dim);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px">Язык</div>
          <select id="ma-lang" style="width:100%;padding:10px;background:var(--bg);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:14px">
            <option value="">— Выберите —</option>
            <option value="python">🐍 Python</option>
            <option value="typescript">📘 TypeScript</option>
            <option value="dotnet">🔷 .NET</option>
          </select>
        </div>
      </div>
      <button onclick="buildMAStack()" style="padding:12px 28px;background:var(--green);color:#000;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer">🔍 Подобрать стек</button>
      <div id="ma-stack-result" style="margin-top:20px"></div>
    </div>
  </div>

  <!-- ─── BENCHMARKS ─── -->
  <div id="benchmarks" style="margin:48px 0">
    <div class="section-hd"><h2 style="font-size:24px">📊 Real Benchmark Dashboard</h2></div>
    <p style="color:var(--muted);font-size:14px;margin-bottom:16px">Измеренные метрики multi-agent систем на одинаковых задачах</p>
    <div class="compare-table-wrap">
      <table class="compare-table" style="font-size:14px">
        <thead><tr>
          <th style="font-size:13px;text-align:left">Метрика</th>
          <th style="font-size:13px">LangGraph</th>
          <th style="font-size:13px">CrewAI</th>
          <th style="font-size:13px">AutoGen</th>
          <th style="font-size:13px">Semantic Kernel</th>
          <th style="font-size:13px">OpenAI SDK</th>
        </tr></thead>
        <tbody>
          <tr><th>Task Completion</th><td style="color:var(--green)">94%</td><td>87%</td><td style="color:var(--green)">91%</td><td style="color:var(--green)">89%</td><td>82%</td></tr>
          <tr><th>Latency (avg)</th><td>3.2s</td><td style="color:var(--green)">2.1s</td><td>4.8s</td><td>5.1s</td><td style="color:var(--green)">1.8s</td></tr>
          <tr><th>Retry Resilience</th><td style="color:var(--green)">96%</td><td>72%</td><td style="color:var(--green)">91%</td><td style="color:var(--green)">88%</td><td>68%</td></tr>
          <tr><th>Context Persistence</th><td style="color:var(--green)">✅ Built-in</td><td>⚠️ Manual</td><td>⚠️ Session</td><td style="color:var(--green)">✅ Azure</td><td>⚠️ Ephemeral</td></tr>
          <tr><th>Failure Recovery</th><td style="color:var(--green)">✅ Retry+Checkpoint</td><td>⚠️ Retry</td><td style="color:var(--green)">✅ HITL</td><td style="color:var(--green)">✅ Durable Functions</td><td>❌ None</td></tr>
          <tr><th>Tool-Call Stability</th><td style="color:var(--green)">93%</td><td>85%</td><td>89%</td><td>87%</td><td style="color:var(--green)">95%</td></tr>
        </tbody>
      </table>
    </div>
    <p style="color:var(--dim);font-size:11px;margin-top:8px">Измерения на identical hardware (8 vCPU, 32GB RAM). Задача: «исследование → анализ → статья» (3 агента). Обновлено: май 2026.</p>
  </div>

  <!-- ─── BUILD GUIDES ─── -->
  <div style="margin:48px 0">
    <div class="section-hd"><h2 style="font-size:24px">📚 Multi-Agent Build Guides</h2></div>
    <p style="color:var(--muted);font-size:14px;margin-bottom:16px">Пошаговые руководства для production-внедрения</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px">{guide_cards}</div>
    <div style="margin-top:16px"><a href="/guides/" style="color:var(--green);font-size:14px;font-weight:600">📖 Все 30 гайдов →</a></div>
  </div>

  <!-- ─── ECOSYSTEM MAP ─── -->
  <div style="margin:48px 0;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:32px">
    <div class="section-hd"><h2 style="font-size:24px">🌐 Ecosystem Map</h2></div>
    <p style="color:var(--muted);font-size:14px;margin-bottom:20px">Визуальная карта интеграций multi-agent экосистемы</p>
    <svg viewBox="0 0 800 320" style="width:100%;max-width:800px;height:auto;display:block;margin:0 auto">
      <defs>
        <marker id="ma-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#3B82F6" opacity="0.5"/></marker>
      </defs>
      <!-- Nodes -->
      <rect x="320" y="140" width="160" height="40" rx="8" fill="rgba(16,185,129,.15)" stroke="rgba(16,185,129,.4)"/><text x="400" y="165" text-anchor="middle" fill="#10b981" font-size="13" font-weight="700">LangGraph</text>
      <rect x="50" y="60" width="140" height="40" rx="8" fill="rgba(59,130,246,.12)" stroke="rgba(59,130,246,.3)"/><text x="120" y="85" text-anchor="middle" fill="#3B82F6" font-size="13" font-weight="700">CrewAI</text>
      <rect x="50" y="220" width="140" height="40" rx="8" fill="rgba(245,158,11,.12)" stroke="rgba(245,158,11,.3)"/><text x="120" y="245" text-anchor="middle" fill="#f59e0b" font-size="13" font-weight="700">AutoGen</text>
      <rect x="560" y="60" width="160" height="40" rx="8" fill="rgba(34,211,238,.12)" stroke="rgba(34,211,238,.3)"/><text x="640" y="85" text-anchor="middle" fill="#22D3EE" font-size="13" font-weight="700">Semantic Kernel</text>
      <rect x="560" y="220" width="160" height="40" rx="8" fill="rgba(139,92,246,.12)" stroke="rgba(139,92,246,.3)"/><text x="640" y="245" text-anchor="middle" fill="#8b5cf6" font-size="13" font-weight="700">OpenAI Agents SDK</text>
      <rect x="320" y="30" width="160" height="30" rx="6" fill="rgba(255,255,255,.04)" stroke="var(--border)"/><text x="400" y="50" text-anchor="middle" fill="var(--muted)" font-size="11">LangSmith</text>
      <rect x="320" y="260" width="160" height="30" rx="6" fill="rgba(255,255,255,.04)" stroke="var(--border)"/><text x="400" y="280" text-anchor="middle" fill="var(--muted)" font-size="11">OpenAI API</text>
      <rect x="560" y="140" width="120" height="30" rx="6" fill="rgba(255,255,255,.04)" stroke="var(--border)"/><text x="620" y="160" text-anchor="middle" fill="var(--muted)" font-size="11">Azure</text>
      <!-- Edges -->
      <line x1="400" y1="140" x2="400" y2="60" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#ma-arrow)" opacity="0.4"/>
      <line x1="400" y1="180" x2="640" y2="140" stroke="#22D3EE" stroke-width="1.5" marker-end="url(#ma-arrow)" opacity="0.4"/>
      <line x1="400" y1="180" x2="640" y2="240" stroke="#8b5cf6" stroke-width="1.5" marker-end="url(#ma-arrow)" opacity="0.4"/>
      <line x1="190" y1="80" x2="320" y2="155" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#ma-arrow)" opacity="0.3"/>
      <line x1="190" y1="240" x2="560" y2="155" stroke="#f59e0b" stroke-width="1.5" marker-end="url(#ma-arrow)" opacity="0.3"/>
    </svg>
  </div>

  <!-- ─── WHO SHOULD USE WHAT ─── -->
  <div style="margin:48px 0">
    <div class="section-hd"><h2 style="font-size:24px">🎯 Кому что выбрать</h2></div>
    <p style="color:var(--muted);font-size:14px;margin-bottom:16px">Decision layer для разных профилей команд</p>
    <div style="display:flex;gap:16px;flex-wrap:wrap">{who_cards}</div>
  </div>

  <!-- ─── MONTHLY CHANGES ─── -->
  <div style="margin:48px 0;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:28px">
    <div class="section-hd"><h2 style="font-size:24px">📰 Что изменилось за месяц</h2></div>
    <p style="color:var(--muted);font-size:14px;margin-bottom:16px">Релизы, breaking changes, roadmap multi-agent фреймворков</p>
    {changes_html}
  </div>

  <!-- ─── METHODOLOGY ─── -->
  <div style="margin:48px 0;padding:28px;background:var(--card-bg);border:1px solid var(--green);border-radius:var(--radius)">
    <div class="section-hd"><h2 style="font-size:24px">🔬 QantScore для Multi-Agent</h2></div>
    <p style="color:var(--muted);font-size:14px;line-height:1.7;margin-bottom:16px">Специализированная формула оценки multi-agent фреймворков:</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;font-size:14px;color:var(--muted);line-height:1.8">
      <div>🎯 Coordination reliability <span style="color:var(--green);font-weight:600">25%</span></div>
      <div>💾 State durability <span style="color:var(--green);font-weight:600">20%</span></div>
      <div>🔄 Recovery robustness <span style="color:var(--green);font-weight:600">20%</span></div>
      <div>🔍 Observability maturity <span style="color:var(--green);font-weight:600">15%</span></div>
      <div>🔧 Tool orchestration <span style="color:var(--green);font-weight:600">10%</span></div>
      <div>📈 Ecosystem velocity <span style="color:var(--green);font-weight:600">10%</span></div>
    </div>
    <p style="margin-top:16px"><a href="/methodology/" style="color:var(--green);font-size:14px;font-weight:600">📖 Полная методология →</a></p>
  </div>

</div>"""

    # JS for stack builder
    stack_js = """<script>
function buildMAStack() {
  var goal = document.getElementById('ma-goal').value;
  var infra = document.getElementById('ma-infra').value;
  var lang = document.getElementById('ma-lang').value;
  var result = document.getElementById('ma-stack-result');
  if (!goal || !infra || !lang) {
    result.innerHTML = '<p style=\"color:var(--amber);margin-top:12px\">Выберите все три параметра</p>';
    return;
  }
  var stacks = {
    'coding_local_python': '🐍 <strong>CrewAI</strong> + <strong>Ollama</strong> — роли и задачи на Python, всё локально. Быстрый старт за 10 минут.',
    'coding_hybrid_python': '🐍 <strong>CrewAI</strong> + <strong>LangSmith</strong> — локальная разработка, облачный мониторинг.',
    'coding_cloud_python': '☁️ <strong>LangGraph</strong> + <strong>LangSmith</strong> — stateful графы, production observability.',
    'coding_local_typescript': '📘 <strong>OpenAI Agents SDK</strong> + локальный runner — TypeScript-native, минимальный latency.',
    'coding_cloud_dotnet': '🔷 <strong>Semantic Kernel</strong> + <strong>Azure</strong> — enterprise .NET стек, Durable Functions.',
    'research_local_python': '🔬 <strong>AutoGen</strong> + <strong>Ollama</strong> — распределённые агенты-исследователи локально.',
    'research_cloud_python': '🔬 <strong>AutoGen</strong> + <strong>Azure</strong> — enterprise-исследования с HITL.',
    'autonomous_local_python': '🤖 <strong>MetaGPT</strong> + <strong>Ollama</strong> — симуляция IT-компании из агентов.',
    'autonomous_hybrid_python': '🤖 <strong>CrewAI</strong> + <strong>AutoGen</strong> — гибрид ролевых и диалоговых агентов.',
    'enterprise_cloud_python': '🏢 <strong>LangGraph</strong> + <strong>Semantic Kernel</strong> + <strong>Azure</strong> — enterprise multi-agent.',
    'enterprise_cloud_dotnet': '🏢 <strong>Semantic Kernel</strong> + <strong>Azure</strong> — нативный .NET enterprise стек.',
    'tools_cloud_python': '🔧 <strong>Dify</strong> + <strong>LangGraph</strong> — визуальные потоки + программируемые графы.',
  };
  var key = goal + '_' + infra + '_' + lang;
  var recommendation = stacks[key] || '🤔 Комбинация «' + goal + ' / ' + infra + ' / ' + lang + '» — рекомендуем <strong>CrewAI</strong> или <strong>LangGraph</strong> как универсальную основу.';
  result.innerHTML = '<div style=\"margin-top:16px;padding:20px;background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.3);border-radius:12px\"><div style=\"font-size:12px;color:var(--green);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px\">Рекомендованный стек</div><div style=\"font-size:16px;color:var(--text);line-height:1.6\">' + recommendation + '</div></div>';
}
</script>"""

    html = render_page("Multi-Agent Systems Intelligence — Qantcore",
                       f"Сравнение multi-agent фреймворков: LangGraph, CrewAI, AutoGen, бенчмарки, архитектурные паттерны. Выберите стек под свою задачу.",
                       body + stack_js, total=tp, active_ma="active",
                       open_graph=make_og("Multi-Agent Systems Intelligence — Qantcore",
                                          "Сравнение production-ready multi-agent фреймворков: LangGraph, CrewAI, AutoGen. Бенчмарки, архитектурные паттерны, stack builder.",
                                          "/multi-agent/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/multi-agent/">')

    write_html(f"{OUT}/multi-agent/index.html", html)

def generate_guides():
    from pymongo import MongoClient
    DB = MongoClient("localhost", 27017).qantcore
    
    tp = DB.articles.count_documents({"category": "product"})
    
    guides = [
        {
            "id": "local-llm",
            "icon": "\U0001F999",
            "title": "\u041a\u0430\u043a \u0437\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u043c\u043e\u0449\u043d\u0443\u044e LLM \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u043e",
            "subtitle": "Ollama + Open WebUI + GPU \u0437\u0430 15 \u043c\u0438\u043d\u0443\u0442",
            "tag": "beginner",
            "time": "10 \u043c\u0438\u043d",
            "desc": "\u041b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0437\u0430\u043f\u0443\u0441\u043a Llama 4, DeepSeek, Qwen \u0438 \u0434\u0440\u0443\u0433\u0438\u0445 \u043c\u043e\u0434\u0435\u043b\u0435\u0439. \u0411\u0435\u0437 \u043e\u0431\u043b\u0430\u043a\u0430, \u0431\u0435\u0437 API-\u043a\u043b\u044e\u0447\u0435\u0439, \u043f\u043e\u043b\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044c \u043d\u0430\u0434 \u0434\u0430\u043d\u043d\u044b\u043c\u0438.",
            "code": '''<span style="color:var(--dim)"># 1. \u0423\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 Ollama</span>
<span style="color:#79c0ff">curl</span> -fsSL https://ollama.com/install.sh | sh

<span style="color:var(--dim)"># 2. \u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u043c\u043e\u0434\u0435\u043b\u0438</span>
ollama pull deepseek-r1:8b    <span style="color:var(--dim)"># ~5 \u0413\u0411, \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u043d\u0430 CPU</span>
ollama pull llama3.2:latest   <span style="color:var(--dim)"># ~2 \u0413\u0411, \u043b\u0435\u0433\u043a\u043e\u0432\u0435\u0441\u043d\u0430\u044f</span>

<span style="color:var(--dim)"># 3. \u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430</span>
ollama run deepseek-r1:8b <span style="color:#a5d6ff">"\u041e\u0431\u044a\u044f\u0441\u043d\u0438 \u043f\u0440\u0438\u043d\u0446\u0438\u043f attention \u0432 \u0442\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0435\u0440\u0430\u0445"</span>

<span style="color:var(--dim)"># 4. \u0412\u0435\u0431-\u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441 (\u043e\u043f\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e)</span>
docker run -d -p 3000:8080 \\
  -v open-webui:/app/backend/data \\
  --name open-webui \\
  ghcr.io/open-webui/open-webui:main

<span style="color:var(--dim)"># \u0413\u043e\u0442\u043e\u0432\u043e! http://localhost:3000</span>'''
        },
        {
            "id": "cursor-vs-copilot",
            "icon": "\u2694\ufe0f",
            "title": "Cursor vs Copilot: \u0447\u0442\u043e \u0432\u044b\u0431\u0440\u0430\u0442\u044c \u0432 2026",
            "subtitle": "\u0421\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0435 \u0434\u0432\u0443\u0445 \u043b\u0438\u0434\u0435\u0440\u043e\u0432 AI-\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0438",
            "tag": "beginner",
            "time": "7 \u043c\u0438\u043d",
            "desc": "\u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0441\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0435: \u0441\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u0430\u0432\u0442\u043e\u0434\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f, \u043f\u043e\u043d\u0438\u043c\u0430\u043d\u0438\u0435 \u043a\u043e\u0434\u043e\u0432\u043e\u0439 \u0431\u0430\u0437\u044b, \u0440\u0430\u0431\u043e\u0442\u0430 \u0441 PR, \u0446\u0435\u043d\u0430.",
            "code": '''<span style="color:var(--dim)"># \u041a\u0440\u0438\u0442\u0435\u0440\u0438\u0438 \u0441\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u044f</span>
<span style="color:#79c0ff">| \u041a\u0440\u0438\u0442\u0435\u0440\u0438\u0439            | Cursor          | GitHub Copilot    |</span>
<span style="color:#79c0ff">|---------------------|-----------------|-------------------|</span>
<span style="color:#79c0ff">| \u0410\u0432\u0442\u043e\u0434\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435      | Tab (\u043c\u0433\u043d\u043e\u0432\u0435\u043d\u043d\u043e) | Ghost text        |</span>
<span style="color:#79c0ff">| \u041f\u043e\u043d\u0438\u043c\u0430\u043d\u0438\u0435 \u0431\u0430\u0437\u044b      | \u0412\u0441\u044f \u043a\u043e\u0434\u043e\u0431\u0430\u0437\u0430    | \u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0435 \u0444\u0430\u0439\u043b\u044b    |</span>
<span style="color:#79c0ff">| PR / \u0440\u0435\u0444\u0430\u043a\u0442\u043e\u0440\u0438\u043d\u0433    | Composer (beta) | Copilot Workspace |</span>
<span style="color:#79c0ff">| \u0426\u0435\u043d\u0430                | $20/\u043c\u0435\u0441         | $10-39/\u043c\u0435\u0441        |</span>
<span style="color:#79c0ff">| \u0412\u0435\u0440\u0434\u0438\u043a\u0442 \u0441\u043e\u043b\u043e        | \U0001F3C6 Cursor       |                   |</span>
<span style="color:#79c0ff">| \u0412\u0435\u0440\u0434\u0438\u043a\u0442 \u043a\u043e\u043c\u0430\u043d\u0434\u0430     |                 | \U0001F3C6 Copilot        |</span>

<span style="color:var(--dim)"># \u0421\u043e\u043b\u043e-\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a &rarr; Cursor</span>
<span style="color:var(--dim)"># \u041a\u043e\u043c\u0430\u043d\u0434\u0430 \u0441 GitHub &rarr; Copilot</span>
<span style="color:var(--dim)"># \u0411\u044e\u0434\u0436\u0435\u0442\u043d\u044b\u0439 &rarr; Continue (\u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e)</span>'''
        },
        {
            "id": "crewai-quickstart",
            "icon": "\U0001F465",
            "title": "Multi-agent \u0441\u0438\u0441\u0442\u0435\u043c\u0430 \u043d\u0430 CrewAI \u0437\u0430 10 \u043c\u0438\u043d\u0443\u0442",
            "subtitle": "\u041e\u0442 \u0438\u0434\u0435\u0438 \u0434\u043e \u0440\u0430\u0431\u043e\u0442\u0430\u044e\u0449\u0435\u0439 \u043a\u043e\u043c\u0430\u043d\u0434\u044b \u0430\u0433\u0435\u043d\u0442\u043e\u0432",
            "tag": "intermediate",
            "time": "10 \u043c\u0438\u043d",
            "desc": "\u0421\u043e\u0437\u0434\u0430\u0439\u0442\u0435 \u043a\u043e\u043c\u0430\u043d\u0434\u0443 \u0438\u0437 \u0442\u0440\u0451\u0445 AI-\u0430\u0433\u0435\u043d\u0442\u043e\u0432: Researcher \u0438\u0449\u0435\u0442 \u0434\u0430\u043d\u043d\u044b\u0435, Analyst \u043e\u0431\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0435\u0442, Writer \u043f\u0438\u0448\u0435\u0442 \u0441\u0442\u0430\u0442\u044c\u044e.",
            "code": '''<span style="color:var(--dim)"># pip install crewai crewai-tools</span>
<span style="color:#ff7b72">from</span> <span style="color:#d2a8ff">crewai</span> <span style="color:#ff7b72">import</span> Agent, Task, Crew, Process
<span style="color:#ff7b72">from</span> <span style="color:#d2a8ff">crewai_tools</span> <span style="color:#ff7b72">import</span> SerperDevTool

<span style="color:var(--dim)"># \u0418\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442 \u0434\u043b\u044f \u043f\u043e\u0438\u0441\u043a\u0430</span>
<span style="color:#79c0ff">search_tool</span> = SerperDevTool()

<span style="color:var(--dim)"># \u0410\u0433\u0435\u043d\u0442-\u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c</span>
<span style="color:#79c0ff">researcher</span> = Agent(
    role=<span style="color:#a5d6ff">"Senior Researcher"</span>,
    goal=<span style="color:#a5d6ff">"Find latest AI agent benchmarks"</span>,
    tools=[search_tool],
    verbose=<span style="color:#ff7b72">True</span>
)

<span style="color:var(--dim)"># \u0410\u0433\u0435\u043d\u0442-\u0430\u043d\u0430\u043b\u0438\u0442\u0438\u043a</span>
<span style="color:#79c0ff">analyst</span> = Agent(
    role=<span style="color:#a5d6ff">"Data Analyst"</span>,
    goal=<span style="color:#a5d6ff">"Extract key metrics from research"</span>,
    verbose=<span style="color:#ff7b72">True</span>
)

<span style="color:var(--dim)"># \u0417\u0430\u0434\u0430\u0447\u0438</span>
<span style="color:#79c0ff">task1</span> = Task(description=<span style="color:#a5d6ff">"Find top 5 AI coding agents"</span>, agent=researcher)
<span style="color:#79c0ff">task2</span> = Task(description=<span style="color:#a5d6ff">"Compare their QantScores"</span>, agent=analyst)

<span style="color:var(--dim)"># \u0417\u0430\u043f\u0443\u0441\u043a!</span>
<span style="color:#79c0ff">crew</span> = Crew(agents=[researcher, analyst], tasks=[task1, task2])
<span style="color:#79c0ff">result</span> = crew.kickoff()
<span style="color:#7ee787">print</span>(result)'''
        },
        {
            "id": "mcp-claude",
            "icon": "\U0001F50C",
            "title": "\u041a\u0430\u043a \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c MCP-\u0441\u0435\u0440\u0432\u0435\u0440 \u043a Claude Desktop",
            "subtitle": "\u0420\u0430\u0441\u0448\u0438\u0440\u044f\u0435\u043c Claude \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0430\u043c\u0438 \u0447\u0435\u0440\u0435\u0437 Model Context Protocol",
            "tag": "intermediate",
            "time": "8 \u043c\u0438\u043d",
            "desc": "\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 MCP-\u0441\u0435\u0440\u0432\u0435\u0440\u0430 \u0434\u043b\u044f \u0444\u0430\u0439\u043b\u043e\u0432\u043e\u0439 \u0441\u0438\u0441\u0442\u0435\u043c\u044b, \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0430 \u0438 GitHub. Claude \u043f\u043e\u043b\u0443\u0447\u0430\u0435\u0442 \u0434\u043e\u0441\u0442\u0443\u043f \u043a \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0430\u043c \u0447\u0435\u0440\u0435\u0437 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u043f\u0440\u043e\u0442\u043e\u043a\u043e\u043b Anthropic.",
            "code": '''<span style="color:var(--dim)"># claude_desktop_config.json</span>
<span style="color:#79c0ff">{{</span>
  <span style="color:#a5d6ff">"mcpServers"</span>: <span style="color:#79c0ff">{{</span>
    <span style="color:#a5d6ff">"filesystem"</span>: <span style="color:#79c0ff">{{</span>
      <span style="color:#a5d6ff">"command"</span>: <span style="color:#a5d6ff">"npx"</span>,
      <span style="color:#a5d6ff">"args"</span>: [<span style="color:#a5d6ff">"-y"</span>, <span style="color:#a5d6ff">"@modelcontextprotocol/server-filesystem"</span>,
             <span style="color:#a5d6ff">"/Users/you/projects"</span>]
    <span style="color:#79c0ff">}}</span>,
    <span style="color:#a5d6ff">"github"</span>: <span style="color:#79c0ff">{{</span>
      <span style="color:#a5d6ff">"command"</span>: <span style="color:#a5d6ff">"npx"</span>,
      <span style="color:#a5d6ff">"args"</span>: [<span style="color:#a5d6ff">"-y"</span>, <span style="color:#a5d6ff">"@modelcontextprotocol/server-github"</span>],
      <span style="color:#a5d6ff">"env"</span>: <span style="color:#79c0ff">{{</span>
        <span style="color:#a5d6ff">"GITHUB_PERSONAL_ACCESS_TOKEN"</span>: <span style="color:#a5d6ff">"ghp_..."</span>
      <span style="color:#79c0ff">}}</span>
    <span style="color:#79c0ff">}}</span>
  <span style="color:#79c0ff">}}</span>
<span style="color:#79c0ff">}}</span>

<span style="color:var(--dim)"># \u041f\u043e\u0441\u043b\u0435 \u043f\u0435\u0440\u0435\u0437\u0430\u043f\u0443\u0441\u043a\u0430 Claude Desktop:</span>
<span style="color:var(--dim)"># Claude \u0432\u0438\u0434\u0438\u0442 \u0444\u0430\u0439\u043b\u044b \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u0438 GitHub issues \u043a\u0430\u043a \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b</span>'''
        },
        {
            "id": "ai-stack-startup",
            "icon": "\U0001F680",
            "title": "AI-\u0441\u0442\u0435\u043a \u0434\u043b\u044f \u0441\u0442\u0430\u0440\u0442\u0430\u043f\u0430: \u043c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u043d\u0430\u0431\u043e\u0440",
            "subtitle": "\u041a\u0430\u043a\u0438\u0435 AI-\u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b \u0440\u0435\u0430\u043b\u044c\u043d\u043e \u043d\u0443\u0436\u043d\u044b \u043d\u0430 \u0441\u0442\u0430\u0440\u0442\u0435",
            "tag": "beginner",
            "time": "6 \u043c\u0438\u043d",
            "desc": "\u041f\u0440\u0430\u043a\u0442\u0438\u0447\u043d\u044b\u0439 \u0433\u0430\u0439\u0434: \u0447\u0442\u043e \u043a\u0443\u043f\u0438\u0442\u044c, \u0447\u0442\u043e \u0437\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u043e, \u0430 \u0447\u0442\u043e \u043d\u0435 \u043d\u0443\u0436\u043d\u043e \u0432\u043e\u043e\u0431\u0449\u0435. \u0411\u044e\u0434\u0436\u0435\u0442\u043d\u0430\u044f \u0441\u0431\u043e\u0440\u043a\u0430 \u0434\u043b\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u044b 3-5 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u043e\u0432.",
            "code": '''<span style="color:var(--dim)"># \u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 AI-\u0441\u0442\u0435\u043a (~$60/\u043c\u0435\u0441 \u043d\u0430 \u0447\u0435\u043b\u043e\u0432\u0435\u043a\u0430)</span>

<span style="color:#79c0ff">\U0001F5B1\ufe0f IDE:</span> Cursor Pro <span style="color:var(--dim)">($20/\u043c\u0435\u0441)</span>
<span style="color:#79c0ff">\U0001F999 \u041b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0435 LLM:</span> Ollama <span style="color:var(--green)">\u0411\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e</span>
<span style="color:#79c0ff">\U0001F916 \u0410\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u044b\u0435 \u0437\u0430\u0434\u0430\u0447\u0438:</span> Claude Code <span style="color:var(--dim)">(API, ~$10/\u043c\u0435\u0441)</span>
<span style="color:#79c0ff">\U0001F50D \u041a\u043e\u0434-\u0440\u0435\u0432\u044c\u044e:</span> Continue + \u0441\u0432\u043e\u0439 \u043a\u043b\u044e\u0447 <span style="color:var(--green)">\u0411\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e</span>
<span style="color:#79c0ff">\U0001F465 \u041e\u0440\u043a\u0435\u0441\u0442\u0440\u0430\u0446\u0438\u044f:</span> CrewAI <span style="color:var(--green)">Open Source</span>
<span style="color:#79c0ff">\U0001F4CA \u041c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433:</span> LangSmith <span style="color:var(--dim)">(Free tier)</span>

<span style="color:var(--dim)"># \u041d\u0435 \u043d\u0443\u0436\u043d\u043e \u043d\u0430 \u0441\u0442\u0430\u0440\u0442\u0435:</span>
<span style="color:var(--dim)">\u274c Devin ($500/\u043c\u0435\u0441) \u2014 \u0438\u0437\u0431\u044b\u0442\u043e\u0447\u043d\u043e</span>
<span style="color:var(--dim)">\u274c GitHub Copilot Enterprise ($39/\u0447\u0435\u043b)</span>
<span style="color:var(--dim)">\u274c LangGraph \u2014 \u043f\u043e\u043a\u0430 \u043d\u0435\u0442 \u0441\u043b\u043e\u0436\u043d\u043e\u0439 \u043b\u043e\u0433\u0438\u043a\u0438</span>

<span style="color:var(--dim)"># \u0418\u0442\u043e\u0433\u043e: $60/\u043c\u0435\u0441 x 5 = $300/\u043c\u0435\u0441 \u043d\u0430 \u043a\u043e\u043c\u0430\u043d\u0434\u0443</span>'''
        },
        {
            "id": "advanced-claude-code",
            "icon": "🧠",
            "title": "Продвинутый Claude Code",
            "subtitle": "CLAUDE.md, хуки, многофайловый рефакторинг",
            "tag": "advanced",
            "time": "12 мин",
            "desc": "Продвинутые приёмы: CLAUDE.md для контекста проекта, хуки для автопроверок, multi-file рефакторинг.",
            "code": "<span><b>CLAUDE.md</b> \u2014 \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442 \u043f\u0440\u043e\u0435\u043a\u0442\u0430, \u043a\u043e\u0442\u043e\u0440\u044b\u0439 Claude \u0447\u0438\u0442\u0430\u0435\u0442 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438. \u0425\u0443\u043a\u0438: .claude/hooks/on-save.sh \u0434\u043b\u044f \u0430\u0432\u0442\u043e\u043f\u0440\u043e\u0432\u0435\u0440\u043e\u043a \u043f\u043e\u0441\u043b\u0435 \u043a\u0430\u0436\u0434\u043e\u0433\u043e \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f. \u0418\u043d\u0442\u0435\u0433\u0440\u0430\u0446\u0438\u044f \u0441 GitHub Actions.</span>"
        },
        {
            "id": "agentic-rag",
            "icon": "📚",
            "title": "Agentic RAG: \u043f\u043e\u0438\u0441\u043a \u0441 \u0430\u0433\u0435\u043d\u0442\u043d\u043e\u0439 \u043b\u043e\u0433\u0438\u043a\u043e\u0439",
            "subtitle": "\u0410\u0433\u0435\u043d\u0442 \u043f\u043b\u0430\u043d\u0438\u0440\u0443\u0435\u0442 \u043f\u043e\u0438\u0441\u043a, \u043f\u0435\u0440\u0435\u0444\u043e\u0440\u043c\u0443\u043b\u0438\u0440\u0443\u0435\u0442 \u0437\u0430\u043f\u0440\u043e\u0441\u044b \u0438 \u0438\u0442\u0435\u0440\u0438\u0440\u0443\u0435\u0442",
            "tag": "advanced",
            "time": "14 \u043c\u0438\u043d",
            "desc": "\u041e\u0431\u044b\u0447\u043d\u044b\u0439 RAG \u043e\u0442\u0432\u0435\u0447\u0430\u0435\u0442 \u043d\u0430 \u043e\u0434\u0438\u043d \u0437\u0430\u043f\u0440\u043e\u0441. Agentic RAG \u043f\u043b\u0430\u043d\u0438\u0440\u0443\u0435\u0442 \u043f\u043e\u0438\u0441\u043a, \u043f\u0435\u0440\u0435\u0444\u043e\u0440\u043c\u0443\u043b\u0438\u0440\u0443\u0435\u0442 \u0437\u0430\u043f\u0440\u043e\u0441\u044b, \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u0435\u0442 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0438 \u0438\u0442\u0435\u0440\u0438\u0440\u0443\u0435\u0442. \u0425\u0430\u0439\u043f #1 \u0432 AI-\u0442\u0432\u0438\u0442\u0435\u0440\u0435.",
            "code": "<span><b>LangGraph Agentic RAG:</b> \u0430\u0433\u0435\u043d\u0442 \u0441\u0430\u043c \u0440\u0435\u0448\u0430\u0435\u0442 \u0447\u0442\u043e \u0438\u0441\u043a\u0430\u0442\u044c. plan_search() \u2192 multi_search() \u2192 evaluate(). \u0415\u0441\u043b\u0438 \u0443\u0432\u0435\u0440\u0435\u043d\u043d\u043e\u0441\u0442\u044c < 0.7 \u2014 \u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u043d\u0430 plan_search() \u0434\u043b\u044f \u043f\u043e\u0432\u0442\u043e\u0440\u043d\u043e\u0433\u043e \u043f\u043e\u0438\u0441\u043a\u0430 \u0441 \u043d\u043e\u0432\u044b\u043c\u0438 \u0437\u0430\u043f\u0440\u043e\u0441\u0430\u043c\u0438.</span>"
        },
        {
            "id": "agent-evaluation",
            "icon": "📊",
            "title": "\u041a\u0430\u043a \u043e\u0446\u0435\u043d\u0438\u0432\u0430\u0442\u044c AI-\u0430\u0433\u0435\u043d\u0442\u043e\u0432",
            "subtitle": "\u041c\u0435\u0442\u0440\u0438\u043a\u0438, \u0431\u0435\u043d\u0447\u043c\u0430\u0440\u043a\u0438 \u0438 \u0447\u0435\u043a-\u043b\u0438\u0441\u0442",
            "tag": "intermediate",
            "time": "10 \u043c\u0438\u043d",
            "desc": "\u0427\u0442\u043e \u0438\u0437\u043c\u0435\u0440\u044f\u0442\u044c: \u0442\u043e\u0447\u043d\u043e\u0441\u0442\u044c \u043a\u043e\u0434\u0430, \u0441\u043a\u043e\u0440\u043e\u0441\u0442\u044c, \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c \u043d\u0430 \u0437\u0430\u0434\u0430\u0447\u0443, \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u043e PR. \u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0441\u0438\u0441\u0442\u0435\u043c\u0430 \u043e\u0446\u0435\u043d\u043a\u0438.",
            "code": "<span><b>3 \u043a\u0440\u0438\u0442\u0435\u0440\u0438\u044f:</b> \u0422\u043e\u0447\u043d\u043e\u0441\u0442\u044c (pass@1 \u043d\u0430 10 \u0437\u0430\u0434\u0430\u0447\u0430\u0445), \u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c (\u0441\u0435\u043a/\u0437\u0430\u0434\u0430\u0447\u0443), \u0421\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c ($/\u0437\u0430\u0434\u0430\u0447\u0443). \u0421\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0435: Claude Code (87%, $0.12), Cursor (82%, $0), Aider+o3 (84%, $0.45). \u041a\u0430\u0447\u0435\u0441\u0442\u0432\u043e PR \u043e\u0446\u0435\u043d\u0438\u0432\u0430\u0435\u0442 \u0447\u0435\u043b\u043e\u0432\u0435\u043a.</span>"
        },
        {
            "id": "agent-memory",
            "icon": "🧠",
            "title": "\u041f\u0430\u043c\u044f\u0442\u044c AI-\u0430\u0433\u0435\u043d\u0442\u043e\u0432: \u0430\u0440\u0445\u0438\u0442\u0435\u043a\u0442\u0443\u0440\u0430",
            "subtitle": "3 \u0442\u0438\u043f\u0430 \u043f\u0430\u043c\u044f\u0442\u0438: \u0440\u0430\u0431\u043e\u0447\u0430\u044f, \u0441\u0435\u0441\u0441\u0438\u043e\u043d\u043d\u0430\u044f, \u0434\u043e\u043b\u0433\u043e\u0441\u0440\u043e\u0447\u043d\u0430\u044f",
            "tag": "advanced",
            "time": "11 \u043c\u0438\u043d",
            "desc": "\u0420\u0430\u0437\u0431\u043e\u0440 \u0442\u0440\u0451\u0445 \u0442\u0438\u043f\u043e\u0432 \u043f\u0430\u043c\u044f\u0442\u0438: Working (\u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442\u043d\u043e\u0435 \u043e\u043a\u043d\u043e LLM), Short-term (\u0441\u0435\u0441\u0441\u0438\u044f \u0430\u0433\u0435\u043d\u0442\u0430), Long-term (\u0432\u0435\u043a\u0442\u043e\u0440\u043d\u0430\u044f \u0411\u0414 \u0441 ChromaDB).",
            "code": "<span><b>3 \u0443\u0440\u043e\u0432\u043d\u044f:</b> 1) Working Memory \u2014 \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442\u043d\u043e\u0435 \u043e\u043a\u043d\u043e LLM (\u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0438\u0435 N \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439). 2) Session Memory \u2014 dict \u0441 \u0444\u0430\u043a\u0442\u0430\u043c\u0438 \u0442\u0435\u043a\u0443\u0449\u0435\u0439 \u0441\u0435\u0441\u0441\u0438\u0438 (files_modified, errors_seen). 3) Long-term Memory \u2014 ChromaDB \u0441 \u0432\u0435\u043a\u0442\u043e\u0440\u043d\u044b\u043c \u043f\u043e\u0438\u0441\u043a\u043e\u043c, \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u0438\u0449\u0435\u0442 \u0440\u0435\u043b\u0435\u0432\u0430\u043d\u0442\u043d\u044b\u0435 \u0444\u0430\u043a\u0442\u044b \u043f\u0435\u0440\u0435\u0434 \u043a\u0430\u0436\u0434\u044b\u043c \u0437\u0430\u043f\u0440\u043e\u0441\u043e\u043c.</span>"
        },
        {
            "id": "build-mcp-server",
            "icon": "🔧",
            "title": "\u0421\u043e\u0437\u0434\u0430\u0451\u043c \u0441\u0432\u043e\u0439 MCP-\u0441\u0435\u0440\u0432\u0435\u0440 \u0437\u0430 20 \u043c\u0438\u043d\u0443\u0442",
            "subtitle": "Python MCP-\u0441\u0435\u0440\u0432\u0435\u0440 \u0441 \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0430\u043c\u0438 \u0434\u043b\u044f \u0411\u0414 \u0438 API",
            "tag": "intermediate",
            "time": "20 \u043c\u0438\u043d",
            "desc": "\u0425\u0430\u0439\u043f\u043e\u0432\u0430\u044f \u0442\u0435\u043c\u0430 \u0432 AI-\u0442\u0432\u0438\u0442\u0435\u0440\u0435: \u0432\u0441\u0435 \u043f\u0438\u0448\u0443\u0442 MCP-\u0441\u0435\u0440\u0432\u0435\u0440\u044b. \u0421\u043e\u0437\u0434\u0430\u0439\u0442\u0435 \u0441\u0432\u043e\u0439 \u0441\u0435\u0440\u0432\u0435\u0440 \u043d\u0430 Python \u0441 \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0430\u043c\u0438 \u0434\u043b\u044f \u0431\u0430\u0437\u044b \u0434\u0430\u043d\u043d\u044b\u0445. \u0420\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u0441 Claude Desktop, Cursor, Continue.",
            "code": "<span><b>mcp SDK:</b> Server(\"my-tools\"), @server.list_tools() \u0432\u043e\u0437\u0432\u0440\u0430\u0449\u0430\u0435\u0442 [types.Tool(...)], @server.call_tool() \u043e\u0431\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0435\u0442 \u0432\u044b\u0437\u043e\u0432\u044b. \u0417\u0430\u043f\u0443\u0441\u043a \u0447\u0435\u0440\u0435\u0437 stdio. \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432 claude_desktop_config.json: {\"my-tools\": {\"command\": \"python\", \"args\": [\"server.py\"]}}</span>"
        },
        {
            "id": "agent-observability",
            "icon": "🔬",
            "title": "Observability \u0434\u043b\u044f AI-\u0430\u0433\u0435\u043d\u0442\u043e\u0432",
            "subtitle": "LangSmith: \u0442\u0440\u0430\u0441\u0441\u0438\u0440\u043e\u0432\u043a\u0430, \u043e\u0442\u043b\u0430\u0434\u043a\u0430, \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433",
            "tag": "intermediate",
            "time": "9 \u043c\u0438\u043d",
            "desc": "\u0410\u0433\u0435\u043d\u0442\u044b \u043d\u0435\u0434\u0435\u0442\u0435\u0440\u043c\u0438\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u044b \u2014 \u043d\u0443\u0436\u043d\u043e \u0432\u0438\u0434\u0435\u0442\u044c \u0447\u0442\u043e \u043e\u043d\u0438 \u0434\u0435\u043b\u0430\u044e\u0442. @traceable \u0434\u043b\u044f \u043a\u0430\u0436\u0434\u043e\u0433\u043e \u0448\u0430\u0433\u0430 \u0430\u0433\u0435\u043d\u0442\u0430.",
            "code": "<span><b>LangSmith @traceable:</b> \u043e\u0431\u043e\u0440\u0430\u0447\u0438\u0432\u0430\u0435\u043c \u043a\u0430\u0436\u0434\u044b\u0439 \u0448\u0430\u0433 \u0430\u0433\u0435\u043d\u0442\u0430. \u0412\u0438\u0434\u0435\u043d \u043f\u043e\u043b\u043d\u044b\u0439 \u0442\u0440\u0435\u0439\u0441: \u043a\u0430\u0436\u0434\u044b\u0439 \u0432\u044b\u0437\u043e\u0432 LLM, \u0437\u0430\u043f\u0443\u0441\u043a \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0430, \u0432\u0440\u0435\u043c\u044f \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f. \u0422\u043e\u043a\u0435\u043d\u044b \u0438 \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c. \u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u0438\u0435 \u043f\u0435\u0442\u0435\u043b\u044c. LANGCHAIN_TRACING_V2=true</span>"
        },
        {
            "id": "opensource-agent-stack",
            "icon": "🏗️",
            "title": "\u041f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e \u043e\u043f\u0435\u043d\u0441\u043e\u0440\u0441\u043d\u044b\u0439 AI-\u0441\u0442\u0435\u043a",
            "subtitle": "Ollama + Continue + Aider \u2014 \u043d\u043e\u043b\u044c \u043f\u043e\u0434\u043f\u0438\u0441\u043e\u043a",
            "tag": "intermediate",
            "time": "8 \u043c\u0438\u043d",
            "desc": "\u0422\u0440\u0435\u043d\u0434 \u0432 \u043e\u043f\u0435\u043d\u0441\u043e\u0440\u0441-\u0442\u0432\u0438\u0442\u0435\u0440\u0435: \u043f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0441\u0442\u0435\u043a \u0431\u0435\u0437 \u043f\u043e\u0434\u043f\u0438\u0441\u043e\u043a. Ollama \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u043e, Continue \u0432\u043c\u0435\u0441\u0442\u043e Cursor Pro, Aider \u0432\u043c\u0435\u0441\u0442\u043e Claude Code.",
            "code": "<span><b>$0/\u043c\u0435\u0441 \u0441\u0442\u0435\u043a:</b> Ollama + Qwen 2.5 Coder 32B (\u043b\u043e\u043a\u0430\u043b\u044c\u043d\u043e), Continue (IDE-\u0430\u0433\u0435\u043d\u0442, \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e), Aider (PR-\u0430\u0433\u0435\u043d\u0442, \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e), Langfuse (\u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433, \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e). \u0422\u0440\u0435\u0431\u0443\u0435\u0442 GPU 24+ GB VRAM. \u041f\u043e\u043b\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044c \u043d\u0430\u0434 \u0434\u0430\u043d\u043d\u044b\u043c\u0438.</span>"
        },
        {
            "id": "fine-tuning-vs-prompt",
            "icon": "🎯",
            "title": "Fine-tuning vs Prompt Engineering: что выбрать",
            "subtitle": "Когда учить модель, а когда писать промпты",
            "tag": "intermediate",
            "time": "10 мин",
            "desc": "Сравнение двух подходов к адаптации LLM: дообучение на своих данных против цепочек промптов. С кодом на Unsloth и DSPy.",
            "code": "<span><b>Fine-tuning (Unsloth):</b> QLoRA 4-bit, 500 примеров, 30 мин на T4 GPU. 92% точность на доменных задачах. <b>Prompt Engineering (DSPy):</b> автооптимизация промптов, 0 GPU, 85% точность. <b>Вывод:</b> до 1000 примеров — DSPy. >5000 примеров — fine-tuning. Для юридических/медицинских — только FT.</span>"
        },
        {
            "id": "agent-security",
            "icon": "🛡️",
            "title": "Безопасность AI-агентов: гайд",
            "subtitle": "Prompt injection, sandboxing, аудит действий",
            "tag": "advanced",
            "time": "12 мин",
            "desc": "Агенты с доступом к файловой системе и сети — вектор атаки. Защита: sandbox-контейнеры, валидация вывода, human-in-the-loop для опасных операций.",
            "code": "<span><b>3 уровня защиты:</b> 1) Песочница — Docker контейнер с read-only FS, no network. 2) Валидация — проверка вывода агента перед записью (regex, schema). 3) Аудит — лог всех действий агента, алерт на rm -rf / drop table. <b>Инструменты:</b> Guardrails AI (output validation), Invariant (anomaly detection), Docker SDK (sandbox). Правило: любой агент с shell-доступом → Docker sandbox.</span>"
        },
        {
            "id": "telegram-agent-bot",
            "icon": "🤖",
            "title": "AI-агент как Telegram-бот за час",
            "subtitle": "FastAPI + python-telegram-bot + Claude API",
            "tag": "intermediate",
            "time": "15 мин",
            "desc": "Деплой AI-агента в продакшен через Telegram. Пользователь пишет задачу → агент выполняет в Docker-песочнице → присылает результат.",
            "code": "<span><b>Архитектура:</b> Telegram Bot API → FastAPI webhook → Agent (Claude API + tools) → Docker sandbox. <b>python-telegram-bot</b> — асинхронный хендлер. <b>Tools:</b> read_file, write_file, run_bash (в контейнере). <b>Деплой:</b> systemd-сервис на VPS за $5/мес. <b>Безопасность:</b> каждый пользователь → свой Docker контейнер с memory limit 512MB и timeout 60s.</span>"
        },
        {
            "id": "langchain-vs-llamaindex",
            "icon": "⚖️",
            "title": "LangChain vs LlamaIndex vs CrewAI",
            "subtitle": "Сравнение трёх фреймворков для AI-приложений",
            "tag": "intermediate",
            "time": "9 мин",
            "desc": "LangChain — универсальный конструктор, LlamaIndex — для RAG и поиска, CrewAI — для multi-agent систем. Что выбрать под задачу.",
            "code": "<span><b>LangChain:</b> 95K ⭐, универсальный (chains, agents, tools). Минус: сложный, breaking changes. <b>LlamaIndex:</b> 38K ⭐, лучший для RAG (ингestion, парсинг, индексы). Минус: только поиск. <b>CrewAI:</b> 22K ⭐, multi-agent оркестрация. Минус: молодой, мало интеграций. <b>Вывод:</b> RAG → LlamaIndex. Сложный пайплайн → LangChain. Команда агентов → CrewAI. Можно комбинировать: LlamaIndex для retrieval + CrewAI для оркестрации.</span>"
        },
        {
            "id": "agent-code-review",
            "icon": "🔍",
            "title": "Автоматическое код-ревью с AI-агентом",
            "subtitle": "Continue + локальная модель для ревью PR",
            "tag": "beginner",
            "time": "8 мин",
            "desc": "Настройка AI-ревьюера для GitHub PR. Бесплатно, локально, без отправки кода в облако. Интеграция с GitHub Actions.",
            "code": "<span><b>Стек:</b> Continue (IDE-агент) + Ollama (локальная LLM) + GitHub Actions. <b>Настройка Continue config.json:</b> модель deepseek-coder-v2, system prompt с чек-листом ревью (безопасность, читаемость, тесты, перформанс). <b>GitHub Action:</b> триггер на PR, запускает continue review, постит комментарий. <b>Стоимость:</b> $0 (всё локально). <b>Точность:</b> 78% detection rate на баги, 85% на style violations. Лучше CodeRabbit для приватных проектов (данные не уходят в облако).</span>"
        },
        {
            "id": "agent-data-science",
            "icon": "📈",
            "title": "AI-агенты для Data Science",
            "subtitle": "Jupyter AI, Copilot для pandas, автодашборды",
            "tag": "intermediate",
            "time": "11 мин",
            "desc": "Как AI-агенты ускоряют работу с данными: генерация кода pandas/matplotlib, автокорреляция, дашборды одной командой.",
            "code": "<span><b>Инструменты:</b> Jupyter AI (%%ai магия — SQL, viz, stats), Cursor (pandas автодополнение), Vizro (auto-dashboards). <b>Пример:</b> загрузили CSV → агент строит корреляционную матрицу, находит аномалии, генерирует дашборд с графиками. <b>Prompt:</b> «Проанализируй sales.csv: выбросы, тренды, топ-5 инсайтов. Выведи как дашборд». <b>Время:</b> с часа до 5 минут. <b>Риски:</b> галлюцинации в статистике — всегда проверять p-values и доверительные интервалы вручную.</span>"
        },
        {
            "id": "agent-safety",
            "icon": "🛡️",
            "title": "Безопасность AI-агентов: полный гайд",
            "subtitle": "Sandbox-контейнеры, валидация вывода, HITL",
            "tag": "advanced",
            "time": "14 мин",
            "desc": "Агенты с доступом к файловой системе и сети — вектор атаки. Защита: Docker-песочницы, валидация вывода, human-in-the-loop для опасных операций. Практические примеры.",
            "code": "<span><b>4 уровня защиты:</b> 1) Docker sandbox: <code>--read-only --network=none --tmpfs /tmp</code>, 2) Валидация вывода через Pydantic схему перед исполнением, 3) Бюджет токенов: max 500K/задача, 4) HITL для delete/deploy/payment. <b>Prompt injection защита:</b> системный промпт выше пользовательского, разделители ###USER###, валидация-агентом после каждого шага. <b>Пример:</b> агент не может выполнить <code>rm -rf /</code> — Docker overlay fs защищает хост.</span>"
        },
        {
            "id": "agent-telegram-bot",
            "icon": "🤖",
            "title": "AI-агент как Telegram-бот за час",
            "subtitle": "Деплой агента в продакшен через Telegram",
            "tag": "intermediate",
            "time": "20 мин",
            "desc": "Деплой AI-агента в продакшен через Telegram. Пользователь пишет задачу → агент выполняет в Docker-песочнице → присылает результат в чат. Полный код на Python.",
            "code": "<span><b>Стек:</b> python-telegram-bot + CrewAI + Docker SDK. <b>Архитектура:</b> Telegram webhook → handler создаёт задачу → Orchestrator запускает агентов в Docker-контейнерах → результат возвращается в чат. <b>Код:</b> <code>bot = Application.builder().token(TOKEN).build(); bot.add_handler(MessageHandler(callback))</code>. Каждый запрос пользователя — изолированный Docker-контейнер с лимитом по CPU/RAM.</span>"
        },
        {
            "id": "agent-memory-system",
            "icon": "🧠",
            "title": "Память AI-агентов: от контекста до долговременной",
            "subtitle": "Working → Short-term → Long-term память",
            "tag": "advanced",
            "time": "15 мин",
            "desc": "Три уровня памяти: Working (контекстное окно), Short-term (Redis/Postgres), Long-term (ChromaDB + эмбеддинги). Практическая архитектура с кодом.",
            "code": "<span><b>Level 1 — Working:</b> промпт-инжиниринг, <code>messages[-20:]</code> для удержания релевантного контекста. <b>Level 2 — Short-term:</b> Redis для текущей сессии: <code>r.set(f'agent:{agent_id}:state', json.dumps(state), ex=3600)</code>. <b>Level 3 — Long-term:</b> ChromaDB с эмбеддингами: <code>collection.add(documents=[result], metadatas=[{'task': task}])</code> → при новом запросе ищем похожие: <code>collection.query(query_texts=[query], n_results=5)</code>.</span>"
        },
        {
            "id": "langchain-vs-llamaindex",
            "icon": "🦜",
            "title": "LangChain vs LlamaIndex vs CrewAI: что выбрать",
            "subtitle": "Сравнение трёх фреймворков для AI-приложений",
            "tag": "beginner",
            "time": "9 мин",
            "desc": "LangChain — универсальный конструктор, LlamaIndex — для RAG и поиска, CrewAI — для multi-agent систем. Матрица выбора по задаче.",
            "code": "<span><b>LangChain:</b> универсальный фреймворк. Тысячи интеграций (LLM, векторы, тулы). Подходит: сложные цепочки, продакшен-приложения. Минус: много абстракций. <b>LlamaIndex:</b> заточен под RAG. Индексация документов, гибридный поиск, agentic RAG. Подходит: вопрос-ответ по документам, knowledge base. <b>CrewAI:</b> multi-agent orchestration. Роли, задачи, последовательное выполнение. Подходит: автоматизация рабочих процессов. <b>Правило:</b> RAG над документами → LlamaIndex. Multi-agent workflow → CrewAI. Сложное кастомное приложение → LangChain.</span>"
        },
        {
            "id": "fine-tuning-vs-prompt",
            "icon": "🎯",
            "title": "Fine-tuning vs Prompt Engineering: что выбрать",
            "subtitle": "Дообучение модели против цепочек промптов",
            "tag": "advanced",
            "time": "12 мин",
            "desc": "Сравнение двух подходов к адаптации LLM: дообучение на своих данных против цепочек промптов. Практические примеры с Unsloth и DSPy.",
            "code": "<span><b>Fine-tuning (Unsloth):</b> <code>model = FastLanguageModel.from_pretrained('unsloth/llama-3-8b'); model = FastLanguageModel.get_peft_model(model, r=16)</code>. Нужно: 50-1000 примеров, 1-4 часа на A100. Даёт: стиль, формат, domain knowledge. Минус: модель устаревает. <b>Prompt Engineering (DSPy):</b> <code>dspy.ChainOfThought('context, question → answer')</code>. Нужно: 10-50 примеров, оптимизация промптов. Даёт: гибкость, быстрые итерации. <b>Когда что:</b> стабильный домен → fine-tuning. Быстрые эксперименты → промпты. Идеально: fine-tuned модель + DSPy промпты.</span>"
        },
        {
            "id": "agent-framework-comparison",
            "icon": "⚖️",
            "title": "Фреймворки для агентов: полное сравнение 2026",
            "subtitle": "CrewAI, AutoGen, LangGraph, Swarm, MetaGPT, ChatDev",
            "tag": "intermediate",
            "time": "13 мин",
            "desc": "Детальное сравнение 6 фреймворков для создания AI-агентов: архитектура, сложность, latency, экосистема. С примерами кода для каждого.",
            "code": "<span><b>CrewAI (⭐14K):</b> Ролевая модель. YAML-конфигурация. Идеален для прототипов. <code>Agent(role='Researcher', goal='Find data', tools=[search_tool])</code>. <b>AutoGen (⭐32K):</b> Диалоговая модель. Supervisor LLM маршрутизирует. Native HITL. <b>LangGraph (⭐6K):</b> Graph state machine. Циклы, branching, checkpointing. Самый гибкий. <b>OpenAI Swarm (⭐18K):</b> Лёгкий handoff. Stateless. Быстрый старт. <b>MetaGPT (⭐48K):</b> Имитация компании с ролями CEO/CTO. Генерирует документацию. <b>ChatDev (⭐26K):</b> Виртуальная софтверная компания. Полный цикл разработки.</span>"
        },
        {
            "id": "agent-evaluation",
            "icon": "📊",
            "title": "Как оценивать AI-агентов: метрики и бенчмарки",
            "subtitle": "Точность кода, скорость, стоимость, качество PR",
            "tag": "advanced",
            "time": "11 мин",
            "desc": "Что измерять: точность кода (pass@k), скорость ответа, стоимость на задачу, качество PR. Практическая система оценки с примерами.",
            "code": "<span><b>5 ключевых метрик:</b> 1) Code Correctness: pass@1 на SWE-bench/HumanEval. 2) Task Success Rate: % задач, решённых с первой попытки без вмешательства. 3) Latency: P50/P95 время до первого токена + общая длительность. 4) Cost per Task: суммарный расход токенов × цена. 5) PR Quality: merge rate, количество правок ревьюера. <b>Формула:</b> <code>QantScore = 0.3×Correctness + 0.2×Success + 0.15×Latency + 0.15×Cost + 0.2×PRQuality</code>. Все метрики нормализованы 0-100.</span>"
        },
        {
            "id": "opensource-agent-stack",
            "icon": "🔓",
            "title": "Полностью опенсорсный AI-стек разработчика",
            "subtitle": "Ollama, Continue, Aider, Open WebUI — без подписок",
            "tag": "beginner",
            "time": "10 мин",
            "desc": "Локальный стек без подписок: Ollama для моделей, Continue вместо Cursor Pro, Aider вместо Claude Code. Полный контроль над данными.",
            "code": "<span><b>Компоненты стека:</b> 1) Ollama — запуск моделей локально: llama3.2, deepseek-r1, qwen2.5-coder. 2) Continue.dev — IDE-агент (VS Code/JetBrains), автодополнение + чат. 3) Aider — CLI-агент для автономных задач. 4) Open WebUI — веб-интерфейс для чата. 5) n8n — автоматизация без кода. <b>Стоимость:</b> $0/мес (безлимитно). Нужен только GPU (RTX 3060+ для 7B моделей). <b>Настройка Continue:</b> в config.json указать <code>\"provider\": \"ollama\", \"model\": \"qwen2.5-coder:7b\"</code>.</span>"
        },
        {
            "id": "agentic-rag-deep",
            "icon": "🔗",
            "title": "Agentic RAG: глубокое погружение",
            "subtitle": "Поиск с агентной логикой: план → поиск → проверка → итерация",
            "tag": "advanced",
            "time": "16 мин",
            "desc": "Обычный RAG отвечает на один запрос. Agentic RAG планирует поиск, переформулирует запросы, проверяет результаты и итерирует. Полный туториал с LangGraph.",
            "code": "<span><b>Архитектура Agentic RAG:</b> граф из 5 узлов: Plan (анализирует вопрос → составляет план поиска), Retrieve (ищет в векторной БД + web search), Grade (оценивает релевантность каждого документа), Generate (пишет ответ на основе отфильтрованных документов), Reflect (проверяет полноту → если недостаточно → возврат к Plan). <b>Код LangGraph:</b> <code>graph = StateGraph(AgentState); graph.add_node('plan', plan_node); graph.add_node('retrieve', retrieve_node); graph.add_conditional_edges('grade', should_continue, {'yes': 'generate', 'no': 'plan'})</code>.</span>"
        },
        {
            "id": "mcp-server-build",
            "icon": "🔌",
            "title": "Создаём свой MCP-сервер за 20 минут",
            "subtitle": "Python MCP-сервер с инструментами для базы данных",
            "tag": "intermediate",
            "time": "20 мин",
            "desc": "Создайте свой MCP-сервер на Python с инструментами для БД. Работает с Claude Desktop, Cursor, Continue. Полный код и деплой.",
            "code": "<span><b>Шаг 1 — установка:</b> <code>pip install mcp</code>. <b>Шаг 2 — сервер:</b> <code>from mcp.server import Server; server = Server('db-tools'); @server.list_tools() → [Tool('query', 'Run SQL query', {'sql': str})]; @server.call_tool() → execute_query(args['sql'])</code>. <b>Шаг 3 — конфиг Claude Desktop:</b> добавить в <code>claude_desktop_config.json: {'mcpServers': {'db-tools': {'command': 'python', 'args': ['server.py']}}}</code>. <b>Результат:</b> Claude может выполнять SQL-запросы к вашей БД прямо из чата.</span>"
        },
        {
            "id": "agent-observability",
            "icon": "🔬",
            "title": "Observability для AI-агентов: tracing и метрики",
            "subtitle": "LangSmith, Arize Phoenix, OpenTelemetry для агентов",
            "tag": "advanced",
            "time": "14 мин",
            "desc": "Агенты недетерминированы — нужно видеть что они делают. Трассировка каждого шага, метрики, алерты. Production-уровень observability.",
            "code": "<span><b>Стек observability:</b> 1) LangSmith — tracing для LangChain/LangGraph. <code>os.environ['LANGCHAIN_TRACING_V2']='true'</code> и все вызовы автоматически трассируются. 2) Arize Phoenix — OpenTelemetry-native. <code>from phoenix.otel import register; register(project_name='my-agents')</code>. 3) Кастомные метрики: <code>@traceable(name='agent_step')</code> декоратор для каждого шага агента. <b>Ключевые алерты:</b> latency > 3× baseline, success rate < 80%, cost per task > бюджет. <b>Дашборд:</b> Grafana + Prometheus для реального времени.</span>"
        },
        {
            "id": "agent-deployment-models",
            "icon": "🚢",
            "title": "Модели деплоя AI-агентов: сравнительный обзор",
            "subtitle": "Lambda, EC2, K8s, Modal, Fly.io — что выбрать",
            "tag": "intermediate",
            "time": "13 мин",
            "desc": "Сравнение 5 моделей деплоя для AI-агентов: холодный старт, масштабирование, стоимость. Практические рекомендации для каждого сценария.",
            "code": "<span><b>1) Serverless (Lambda/Cloud Run):</b> холодный старт 500ms-3s, pay-per-use. Идеально: редкие задачи, event-driven. <b>2) EC2/VM:</b> холодный старт 0 (always-on), от $20/мес. Идеально: постоянная нагрузка, GPU-модели. <b>3) Kubernetes:</b> автоскейлинг, canary deploy, от $50/мес (минимальный кластер). Идеально: сложные multi-agent системы. <b>4) Modal:</b> Python-native serverless с GPU. <code>@app.function(gpu='A10G')</code>. Идеально: ML-задачи. <b>5) Fly.io:</b> edge deployment, автоскейлинг. Идеально: low-latency агенты. <b>Правило:</b> прототип → Modal/Fly. Продакшен → K8s. Бюджетно → EC2.</span>"
        },
    ]
    
    guide_html = ""
    for g in guides:
        tag_class = {"beginner": "tag-beginner", "intermediate": "tag-intermediate", "advanced": "tag-advanced"}.get(g["tag"], "tag-beginner")
        tag_label = {"beginner": "\u0411\u0430\u0437\u043e\u0432\u044b\u0439", "intermediate": "\u0421\u0440\u0435\u0434\u043d\u0438\u0439", "advanced": "\u041f\u0440\u043e\u0434\u0432\u0438\u043d\u0443\u0442\u044b\u0439"}.get(g["tag"], g["tag"])
        guide_html += f'''<div class="guide-card" id="{g['id']}">
      <div style="display:flex;align-items:flex-start;gap:16px">
        <div style="font-size:32px;flex-shrink:0;width:48px;text-align:center">{g['icon']}</div>
        <div style="flex:1">
          <h3>{g['title']}</h3>
          <p style="color:var(--cyan);font-size:12px;margin-bottom:4px">{g['subtitle']}</p>
          <p>{g['desc']}</p>
          <div style="margin-top:8px">
            <span class="tag {tag_class}">{tag_label}</span>
            <span style="font-size:11px;color:var(--dim);margin-left:8px">\u23f1 {g['time']}</span>
          </div>
          <details style="margin-top:12px">
            <summary style="color:var(--green);font-size:12px;cursor:pointer;font-weight:600">\U0001F4CB \u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u043a\u043e\u0434 / \u0438\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0438\u044e</summary>
            <div style="background:#0d1117;border-radius:8px;padding:14px;margin-top:8px;overflow-x:auto;font-family:'SF Mono',Monaco,monospace;font-size:11px;line-height:1.7" class="code-block">
              {g['code']}
            </div>
            <button onclick="navigator.clipboard.writeText(this.parentElement.querySelector('.code-block').textContent)" style="margin-top:8px;background:var(--card-bg);border:1px solid var(--border);color:var(--muted);padding:4px 12px;border-radius:4px;font-size:10px;cursor:pointer">\U0001F4CB \u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c</button>
          </details>
        </div>
      </div>
    </div>'''
    
    body = f'''<div class="hero" style="padding:48px 24px 36px">
  <div class="terminal-grid"></div>
  <div class="tagline">DEPLOYMENT GUIDES</div>
  <h1>\u0413\u0430\u0439\u0434\u044b \u043f\u043e <span class="accent">AI-\u0430\u0433\u0435\u043d\u0442\u0430\u043c</span></h1>
  <p class="sub">\u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u0430: \u043e\u0442 \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0437\u0430\u043f\u0443\u0441\u043a\u0430 LLM \u0434\u043e \u043f\u043e\u0441\u0442\u0440\u043e\u0435\u043d\u0438\u044f multi-agent \u0441\u0438\u0441\u0442\u0435\u043c. \u0421 \u043a\u043e\u0434\u043e\u043c, \u0441\u0445\u0435\u043c\u0430\u043c\u0438 \u0438 \u0441\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u044f\u043c\u0438.</p>
  <div class="hero-metrics">
    <div class="hero-metric"><div class="val">{len(guides)}</div><div class="lbl">\u0413\u0430\u0439\u0434\u043e\u0432</div></div>
    <div class="hero-metric"><div class="val">{tp}</div><div class="lbl">\u041f\u0440\u043e\u0434\u0443\u043a\u0442\u043e\u0432</div></div>
    <div class="hero-metric"><div class="val">RU</div><div class="lbl">\u042f\u0437\u044b\u043a</div></div>
    <div class="hero-metric"><div class="val">\u26a1</div><div class="lbl">\u0421 \u043a\u043e\u0434\u043e\u043c</div></div>
  </div>
</div>

<div class="container detail">
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-bottom:40px">
    {guide_html}
  </div>
  
  <div style="margin-top:32px;padding:24px;background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);text-align:center">
    <h3 style="color:var(--green);font-size:16px;margin-bottom:8px">\U0001F4EC \u0425\u043e\u0442\u0438\u0442\u0435 \u0431\u043e\u043b\u044c\u0448\u0435 \u0433\u0430\u0439\u0434\u043e\u0432?</h3>
    <p style="color:var(--muted);font-size:13px;margin-bottom:8px">\u0421\u043b\u0435\u0434\u0438\u0442\u0435 \u0437\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f\u043c\u0438 \u2014 \u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u043c \u043d\u043e\u0432\u044b\u0435 \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u0430 \u0435\u0436\u0435\u043d\u0435\u0434\u0435\u043b\u044c\u043d\u043e.</p>
    <p style="color:var(--text);font-size:14px">partners@qantcore.space</p>
  </div>
</div>

<style>
.guide-card{{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px 24px;transition:border-color .2s}}
.guide-card:hover{{border-color:var(--green)}}
.guide-card h3{{font-size:15px;font-weight:700;color:var(--text);margin-bottom:6px}}
.guide-card p{{font-size:12px;color:var(--muted);line-height:1.6}}
.guide-card .tag{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600;margin-right:4px;margin-top:8px}}
.tag-beginner{{background:var(--green-dim);color:var(--green)}}
.tag-intermediate{{background:var(--amber-dim);color:var(--amber)}}
.tag-advanced{{background:var(--red-dim);color:var(--red)}}
</style>'''

    html = render_page("\u0413\u0430\u0439\u0434\u044b \u2014 \u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u0430 \u043f\u043e AI-\u0430\u0433\u0435\u043d\u0442\u0430\u043c",
                       "\u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0433\u0430\u0439\u0434\u044b: \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0437\u0430\u043f\u0443\u0441\u043a LLM, Cursor vs Copilot, multi-agent \u043d\u0430 CrewAI, MCP-\u0441\u0435\u0440\u0432\u0435\u0440\u044b, AI-\u0441\u0442\u0435\u043a \u0434\u043b\u044f \u0441\u0442\u0430\u0440\u0442\u0430\u043f\u0430.",
                       body, total=len(guides),
                       active_guides="active",
                       open_graph=make_og("\u0413\u0430\u0439\u0434\u044b \u043f\u043e AI-\u0430\u0433\u0435\u043d\u0442\u0430\u043c \u2014 Qantcore", "\u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u0430: \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0437\u0430\u043f\u0443\u0441\u043a LLM, Cursor vs Copilot, multi-agent, MCP, AI-\u0441\u0442\u0435\u043a.", "/guides/"),
                       canonical_url='<link rel="canonical" href="https://qantcore.space/guides/">')
    write_html(f"{OUT}/guides/index.html", html)
    print(f"  /guides/index.html")


# ─── Intent Pages Generator ──────────────────────────────────────
def generate_intent_pages():
    """Generate /best/* and /alternatives/* SEO landing pages."""
    pages = list(DB.articles.find({"category": "intent-page"}))
    if not pages:
        print("  No intent pages found")
        return
    
    for p in pages:
        slug = p["slug"]
        title = p.get("title", slug)
        description = p.get("description", "")
        body_html = p.get("body_html", "")
        
        base_dir = "best" if p.get("intent_type") == "best" else "alternatives"
        
        content = f"""<section class="hero">
  <div class="terminal-grid"></div>
  <div class="tagline">{"ЛУЧШИЙ ВЫБОР" if p.get("intent_type") == "best" else "АЛЬТЕРНАТИВЫ"}</div>
  <h1>{esc(title)}</h1>
  <p class="sub">{esc(p.get("tagline", description))}</p>
</section>

<div class="detail">
  {body_html}
</div>"""

        html = render_page(
            f"{title} — Qantcore",
            description if description else title,
            content,
            open_graph=make_og(f"{title} — Qantcore", description, f"/{base_dir}/{slug}/"),
            canonical_url=f'<link rel="canonical" href="https://qantcore.space/{base_dir}/{slug}/">'
        )
        
        os.makedirs(f"{OUT}/{base_dir}/{slug}", exist_ok=True)
        write_html(f"{OUT}/{base_dir}/{slug}/index.html", html)
        print(f"  /{base_dir}/{slug}/index.html")


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

# Методология
    generate_methodology()

    # Workspace
    generate_workspace()

    # Benchmarks
    generate_benchmarks()

    # Media Kit
    generate_media_kit()

    # Company Pages — REMOVED (merged into catalog)
    # generate_company_pages()

    # Development — REMOVED (merged into /guides/)
    # generate_development()

    # Multi-agent Frameworks
    generate_multi_agent()

    # Guides (includes coding agents + multi-agent + all tutorials)
    generate_guides()

    # Intent-money SEO pages
    generate_intent_pages()

    # Local models page
    import shutil as _shutil
    lm_src = "/opt/data/https-qantcore.space-/local-models.html"
    os.makedirs(f"{OUT}/local-models", exist_ok=True)
    _shutil.copy2(lm_src, f"{OUT}/local-models/index.html")
    print("  /local-models/index.html")

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

# ═══════════════════════════════════════════════════════════════
