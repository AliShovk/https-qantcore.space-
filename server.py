"""
Qantcore — AI Agents Review Platform
FastAPI server: каталог, сравнения, обзоры
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
import re, os

app = FastAPI(title="Qantcore", version="1.0.0")
DB = MongoClient("localhost", 27017).qantcore

STATIC_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/images", StaticFiles(directory=STATIC_DIR), name="images")

# ─── CSS ───────────────────────────────────────────────────────────
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Inter',sans-serif;
     background:#08080f;color:#c8c8d4;min-height:100vh;line-height:1.6}
a{color:inherit;text-decoration:none}
::-webkit-scrollbar{width:6px}::-webkit-scrollbar-track{background:#0a0a14}
::-webkit-scrollbar-thumb{background:#2a2a3a;border-radius:3px}

header{position:sticky;top:0;z-index:100;backdrop-filter:blur(20px);
       background:rgba(8,8,15,.85);border-bottom:1px solid rgba(255,255,255,.06)}
.header-inner{max-width:1280px;margin:0 auto;padding:16px 24px;
              display:flex;align-items:center;justify-content:space-between}
.logo{font-size:22px;font-weight:800;background:linear-gradient(135deg,#a78bfa,#60a5fa);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent}
nav{display:flex;gap:24px;align-items:center}
nav a{font-size:14px;color:#8b8b9e;transition:color .2s;font-weight:500}
nav a:hover,nav a.active{color:#e0e0f0}
.badge{font-size:11px;padding:2px 8px;border-radius:10px;
       background:rgba(167,139,250,.15);color:#a78bfa;font-weight:600}

.search-bar{max-width:1280px;margin:0 auto;padding:24px 24px 0}
.search-bar input{width:100%;padding:14px 20px;border-radius:14px;
    background:#12121e;border:1px solid rgba(255,255,255,.08);
    color:#e0e0f0;font-size:15px;outline:none;transition:border-color .2s}
.search-bar input:focus{border-color:#a78bfa}
.search-bar input::placeholder{color:#555}

.container{max-width:1280px;margin:0 auto;padding:32px 24px}
.hero{text-align:center;padding:60px 24px 40px}
.hero h1{font-size:48px;font-weight:800;letter-spacing:-.02em;
         background:linear-gradient(135deg,#a78bfa,#60a5fa);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{font-size:18px;color:#6b6b82;margin-top:12px;max-width:600px;margin-left:auto;margin-right:auto}

.filters{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:28px}
.filter-btn{padding:8px 18px;border-radius:20px;font-size:13px;font-weight:500;
            border:1px solid rgba(255,255,255,.08);background:transparent;
            color:#8b8b9e;cursor:pointer;transition:all .2s}
.filter-btn:hover,.filter-btn.active{border-color:#a78bfa;color:#a78bfa;
                                       background:rgba(167,139,250,.08)}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}

.card{background:#11111e;border:1px solid rgba(255,255,255,.06);border-radius:16px;
      padding:24px;transition:all .25s;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,#a78bfa,#60a5fa);opacity:0;transition:opacity .25s}
.card:hover{transform:translateY(-4px);border-color:rgba(167,139,250,.3);
            box-shadow:0 12px 40px rgba(0,0,0,.4)}
.card:hover::before{opacity:1}
.card-header{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px}
.card-icon{width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,rgba(167,139,250,.2),rgba(96,165,250,.1));
           display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;overflow:hidden}
.card-icon img{width:100%;height:100%;object-fit:contain;padding:4px}
.card-img{width:100%;height:180px;border-radius:12px;overflow:hidden;margin-bottom:16px;
          background:linear-gradient(135deg,rgba(167,139,250,.1),rgba(96,165,250,.05));
          display:flex;align-items:center;justify-content:center}
.card-img img{width:100%;height:100%;object-fit:contain;padding:16px}
.detail-image{width:120px;height:120px;border-radius:16px;overflow:hidden;flex-shrink:0;
              background:linear-gradient(135deg,rgba(167,139,250,.15),rgba(96,165,250,.08));
              display:flex;align-items:center;justify-content:center}
.detail-image img{width:100%;height:100%;object-fit:contain;padding:12px}
.card-badge{padding:3px 10px;border-radius:10px;font-size:11px;font-weight:600}
.badge-agent{background:rgba(96,165,250,.15);color:#60a5fa}
.badge-framework{background:rgba(167,139,250,.15);color:#a78bfa}
.badge-platform{background:rgba(74,222,128,.15);color:#4ade80}
.badge-model{background:rgba(251,191,36,.15);color:#fbbf24}
.badge-infra{background:rgba(248,113,113,.15);color:#f87171}
.card-title{font-size:17px;font-weight:700;color:#e8e8f0;margin-bottom:8px;line-height:1.3}
.card-desc{font-size:13px;color:#6b6b82;line-height:1.5;display:-webkit-box;
           -webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card-meta{display:flex;gap:16px;margin-top:16px;font-size:12px;color:#555}
.card-meta span{display:flex;align-items:center;gap:4px}
.rating{color:#fbbf24;font-weight:700;font-size:14px}
.price{font-weight:600;color:#4ade80}

.detail{max-width:900px;margin:0 auto}
.detail-header{margin-bottom:40px}
.detail-header h1{font-size:36px;font-weight:800;color:#e8e8f0;letter-spacing:-.01em}
.detail-header .tagline{font-size:17px;color:#6b6b82;margin-top:8px}
.detail-meta{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}
.meta-item{display:flex;align-items:center;gap:6px;padding:8px 16px;
           background:#11111e;border-radius:10px;font-size:13px;color:#8b8b9e;
           border:1px solid rgba(255,255,255,.05)}
.meta-item strong{color:#e0e0f0}
.detail-body{margin-top:32px;font-size:15px;line-height:1.8;color:#b0b0c0}
.detail-body h2{font-size:22px;font-weight:700;color:#e0e0f0;margin:32px 0 12px}
.detail-body h3{font-size:18px;font-weight:600;color:#d0d0e0;margin:24px 0 8px}
.detail-body p{margin-bottom:16px}
.detail-body ul,.detail-body ol{padding-left:24px;margin-bottom:16px}
.detail-body li{margin-bottom:6px}
.detail-body code{background:#1a1a2e;padding:2px 8px;border-radius:4px;font-size:13px;color:#a78bfa}
.detail-body strong{color:#e0e0f0}
.detail-body table{width:100%;border-collapse:collapse;margin:16px 0}
.detail-body td,.detail-body th{border:1px solid rgba(255,255,255,.08);padding:10px 14px;text-align:left;font-size:13px}
.detail-body th{background:#11111e;color:#a78bfa;font-weight:600}

.vs-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 16px;
          background:rgba(167,139,250,.1);border-radius:20px;font-size:14px;color:#a78bfa;margin:12px 0}
.vs-badge .vs{font-weight:800;color:#c084fc}

.breadcrumbs{font-size:13px;color:#555;margin-bottom:24px}
.breadcrumbs a{color:#8b8b9e;transition:color .2s}
.breadcrumbs a:hover{color:#a78bfa}
.breadcrumbs span{color:#e0e0f0}

.stats{display:flex;gap:24px;flex-wrap:wrap;margin-bottom:32px}
.stat{padding:16px 24px;background:#11111e;border-radius:12px;
      border:1px solid rgba(255,255,255,.05);text-align:center}
.stat-val{font-size:28px;font-weight:800;background:linear-gradient(135deg,#a78bfa,#60a5fa);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stat-label{font-size:12px;color:#555;margin-top:4px}

.empty{text-align:center;padding:80px 24px}
.empty h2{font-size:28px;color:#6b6b82;margin-bottom:8px}
.empty p{color:#444}

footer{text-align:center;padding:40px 24px;color:#3a3a4a;font-size:13px;
       border-top:1px solid rgba(255,255,255,.04);margin-top:40px}

@media(max-width:640px){
  .hero h1{font-size:32px}
  .grid{grid-template-columns:1fr}
  nav{gap:12px}
  .header-inner{padding:12px 16px}
  .container,.search-bar{padding-left:16px;padding-right:16px}
}
"""

# ─── Template Engine (safe from {} in data) ─────────────────────────
def render(template, **kwargs):
    """Replace {{key}} placeholders — safe for content with curly braces."""
    result = template
    for key, value in kwargs.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result


PAGE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{title}} | Qantcore</title>
<meta name="description" content="{{description}}">
<link rel="icon" type="image/svg+xml" href="/images/favicon.svg">
{{open_graph}}
<style>{{css}}</style>
<script type="application/ld+json">
{{schema_org}}
</script>
</head>
<body>
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
(function(m,e,t,r,i,k,a){
m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
m[i].l=1*new Date();
for (var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}
k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
})(window,document,'script','https://mc.yandex.ru/metrika/tag.js?id=109327472','ym');
ym(109327472,'init',{ssr:true,webvisor:true,clickmap:true,ecommerce:"dataLayer",referrer:document.referrer,url:location.href,accurateTrackBounce:true,trackLinks:true});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/109327472" style="position:absolute;left:-9999px" alt=""/></div></noscript>
<!-- /Yandex.Metrika counter -->
<header>
  <div class="header-inner">
    <a href="/" class="logo">Qantcore</a>
    <nav>
      <a href="/" class="{{active_home}}">Каталог</a>
      <a href="/catalog?category=comparison" class="{{active_compare}}">Сравнения</a>
      <a href="/catalog?category=review" class="{{active_review}}">Обзоры</a>
      <span class="badge">{{total}} продуктов</span>
    </nav>
  </div>
</header>
<div class="search-bar">
  <input type="text" id="search" placeholder="Поиск по агентам, фреймворкам, платформам..."
         value="{{search_val}}" autofocus oninput="debounceSearch(this.value)">
</div>
{{content}}
<footer>
  Qantcore &copy; 2026 &mdash; AI Agents Review Platform &mdash;
  <a href="https://t.me/nousresearch" style="color:#a78bfa">@nousresearch</a>
</footer>
<script>
function debounceSearch(v){{clearTimeout(this._t);this._t=setTimeout(()=>{{let u=new URL(location);u.searchParams.set('q',v);u.searchParams.set('page','1');location=u}},300)}}
document.getElementById('search')?.focus()
</script>
</body>
</html>"""

# ─── Helpers ──────────────────────────────────────────────────────
def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def product_type_badge(pt):
    mapping = {"agent":"badge-agent","framework":"badge-framework","platform":"badge-platform",
               "model":"badge-model","infrastructure":"badge-infra"}
    labels = {"agent":"Агент","framework":"Фреймворк","platform":"Платформа",
              "model":"Модель","infrastructure":"Инфраструктура"}
    cls = mapping.get(pt, "badge-agent")
    lbl = labels.get(pt, pt)
    return f'<span class="card-badge {cls}">{esc(lbl)}</span>'

def product_image(p, size="icon"):
    """Generate image HTML for a product. size: icon, card, detail."""
    img_url = p.get("image_url", "")
    if img_url:
        if size == "card":
            return f'<div class="card-img"><img src="{img_url}" alt="{esc(p.get("title",""))}" loading="lazy"></div>'
        elif size == "detail":
            return f'<div class="detail-image"><img src="{img_url}" alt="{esc(p.get("title",""))}"></div>'
        else:  # icon
            return f'<div class="card-icon"><img src="{img_url}" alt="" loading="lazy"></div>'
    # Fallback: emoji
    return f'<div class="card-icon">{icon_for(p.get("product_type",""))}</div>'

def icon_for(pt):
    icons = {"agent":"🤖","framework":"🔧","platform":"🌐","model":"🧠","infrastructure":"⚡"}
    return icons.get(pt, "📦")

def rating_stars(rating):
    if not rating: return ""
    stars = round(float(rating))
    return "★" * stars + "☆" * (5 - stars)

def format_price(pricing):
    prices = {"freemium":"Freemium","open-source":"Open Source","paid":"Платный","usage-based":"По использованию"}
    return prices.get(pricing, pricing)

def page_nav(page, total_pages, base_url):
    if total_pages <= 1: return ""
    h = '<div style="display:flex;gap:8px;justify-content:center;margin-top:32px">'
    sep = "&" if "?" in base_url else "?"
    for p in range(1, total_pages + 1):
        cls = "filter-btn active" if p == page else "filter-btn"
        h += f'<a href="{base_url}{sep}page={p}" class="{cls}">{p}</a>'
    h += "</div>"
    return h

def make_page(title, description, content, search_val="", total=0,
              active_home="", active_compare="", active_review="",
              open_graph="", schema_org=""):
    return render(PAGE,
        title=title, description=description, css=CSS, content=content,
        search_val=search_val, total=str(total),
        active_home=active_home, active_compare=active_compare, active_review=active_review,
        open_graph=open_graph, schema_org=schema_org)

# ─── Data helpers ──────────────────────────────────────────────────
def get_total_products():
    return DB.articles.count_documents({"category": "product"})

def not_found(msg, slug=""):
    return HTMLResponse(make_page(
        "Не найдено", "", f'<div class="container empty"><h2>{msg}</h2><p>{esc(slug)}</p></div>',
        total=get_total_products()))

# ─── Routes ────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    q = request.query_params.get("q", "").strip()
    ptype = request.query_params.get("type", "")
    page = int(request.query_params.get("page", "1"))
    per_page = 24

    query = {"category": "product"}
    if q:
        query["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"tagline": {"$regex": q, "$options": "i"}},
            {"product_type": {"$regex": q, "$options": "i"}},
        ]
    if ptype:
        query["product_type"] = ptype

    total = DB.articles.count_documents(query)
    total_pages = max(1, (total + per_page - 1) // per_page)
    products = list(DB.articles.find(query).sort("rating", -1).skip((page - 1) * per_page).limit(per_page))

    tp = get_total_products()
    tc = DB.articles.count_documents({"category": "comparison"})
    tr = DB.articles.count_documents({"category": "review"})

    # Filters
    filters_html = ""
    product_types = DB.articles.distinct("product_type", {"category": "product"})
    for pt in product_types:
        active_cls = "active" if ptype == pt else ""
        filters_html += f'<a href="/?type={pt}" class="filter-btn {active_cls}">{esc(pt)}</a>'
    filters_html += f'<a href="/" class="filter-btn {"active" if not ptype else ""}">Все</a>'

    # Stats
    stats_html = f"""
    <div class="stats">
      <div class="stat"><div class="stat-val">{tp}</div><div class="stat-label">Продуктов</div></div>
      <div class="stat"><div class="stat-val">{tc}</div><div class="stat-label">Сравнений</div></div>
      <div class="stat"><div class="stat-val">{tr}</div><div class="stat-label">Обзоров</div></div>
    </div>"""

    cards = ""
    if not products:
        cards = '<div class="empty"><h2>Ничего не найдено</h2><p>Попробуйте изменить запрос</p></div>'
    else:
        cards = '<div class="grid">'
        for p in products:
            cards += f"""
            <a href="/product/{p['slug']}" class="card">
              <div class="card-header">
                {product_image(p)}
                {product_type_badge(p.get('product_type',''))}
              </div>
              <div class="card-title">{esc(p.get('title',''))}</div>
              <div class="card-desc">{esc(p.get('tagline','') or p.get('description',''))}</div>
              <div class="card-meta">
                <span class="rating">{rating_stars(p.get('rating'))} {p.get('rating','')}</span>
                <span class="price">{format_price(p.get('pricing_model',''))}</span>
              </div>
            </a>"""
        cards += "</div>"
        cards += page_nav(page, total_pages, f"/?q={q}&type={ptype}")

    content = f"""
    <div class="container">
      {stats_html}
      <div class="filters">{filters_html}</div>
      {cards}
    </div>"""

    return HTMLResponse(make_page(
        "Каталог AI-агентов", "Каталог, сравнения и обзоры AI-агентов для бизнеса",
        content, search_val=q, total=tp, active_home="active"))


@app.get("/product/{slug}", response_class=HTMLResponse)
async def product_page(request: Request, slug: str):
    p = DB.articles.find_one({"slug": slug, "category": "product"})
    if not p:
        return not_found("Продукт не найден", slug)

    comparisons = list(DB.articles.find(
        {"category": "comparison", "$or": [{"product_a": slug}, {"product_b": slug}]}).limit(5))
    reviews = list(DB.articles.find({"category": "review", "review_of": slug}).limit(3))

    comp_links = ""
    if comparisons:
        comp_links = '<div style="margin-top:20px"><h3 style="color:#a78bfa;font-size:15px;margin-bottom:10px">Сравнения</h3><div class="grid">'
        for c in comparisons:
            comp_links += f"""
            <a href="/compare/{c['slug']}" class="card">
              <div class="card-title">{esc(c.get('title',''))}</div>
              <div class="card-desc">{esc(str(c.get('description',''))[:120])}</div>
            </a>"""
        comp_links += "</div></div>"

    review_links = ""
    if reviews:
        review_links = '<div style="margin-top:20px"><h3 style="color:#a78bfa;font-size:15px;margin-bottom:10px">Обзоры</h3>'
        for r in reviews:
            review_links += f"""<a href="/review/{r['slug']}" class="card" style="display:block;margin-bottom:12px">
              <div class="card-title">{esc(r.get('title',''))}</div>
              <div class="card-desc">{esc(r.get('tagline',''))} · {r.get('word_count',0)} слов</div>
            </a>"""
        review_links += "</div>"

    rating_html = f'<div class="meta-item">⭐ <strong>{p.get("rating","")}</strong> / 5</div>' if p.get('rating') else ''
    website_html = f'<a href="{p.get("website_url","")}" class="meta-item" target="_blank">🔗 Сайт</a>' if p.get('website_url') else ''

    body = f"""
    <div class="container detail">
      <div class="breadcrumbs">
        <a href="/">Каталог</a> &rsaquo; <span>{esc(p.get('title',''))}</span>
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
        </div>
      </div>
      <div class="detail-body">
        <p style="font-size:16px;color:#c0c0d0">{esc(p.get('description',''))}</p>
        {comp_links}
        {review_links}
      </div>
    </div>"""

    desc = esc((p.get('tagline','') or p.get('description',''))[:160])
    return HTMLResponse(make_page(
        esc(p.get('title','')), desc, body, total=get_total_products(), active_home="active",
        open_graph=p.get('open_graph',''), schema_org=p.get('schema_org','')))


@app.get("/compare/{slug}", response_class=HTMLResponse)
async def comparison_page(request: Request, slug: str):
    c = DB.articles.find_one({"slug": slug, "category": "comparison"})
    if not c:
        return not_found("Сравнение не найдено", slug)

    body_html = c.get("body", "").replace("\n", "<br>") if c.get("body") else c.get("description", "")
    # Link to products
    links = ""
    prod_images = ""
    for pa in ["product_a", "product_b"]:
        sv = c.get(pa, "")
        if sv:
            prod = DB.articles.find_one({"slug": sv, "category": "product"})
            if prod:
                links += f'<a href="/product/{sv}" class="meta-item">🔗 {esc(prod.get("title","")[:40])}</a>'
                pi = product_image(prod, "icon")
                prod_images += f'<div style="text-align:center">{pi}<div style="font-size:13px;color:#8b8b9e;margin-top:8px">{esc(prod.get("title","")[:30])}</div></div>'

    body = f"""
    <div class="container detail">
      <div class="breadcrumbs">
        <a href="/">Каталог</a> &rsaquo; <a href="/catalog?category=comparison">Сравнения</a> &rsaquo; <span>{esc(c.get('title',''))}</span>
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

    return HTMLResponse(make_page(
        esc(c.get('title','')), esc(str(c.get('description',''))[:160]), body,
        total=get_total_products(), active_compare="active",
        open_graph=c.get('open_graph',''), schema_org=c.get('schema_org','')))


@app.get("/review/{slug}", response_class=HTMLResponse)
async def review_page(request: Request, slug: str):
    r = DB.articles.find_one({"slug": slug, "category": "review"})
    if not r:
        return not_found("Обзор не найден", slug)

    body_html = r.get("body", "").replace("\n", "<br>") if r.get("body") else ""
    if r.get("body_html"):
        body_html = r["body_html"]

    prod_link = ""
    prod_image_html = ""
    if r.get("review_of"):
        prod = DB.articles.find_one({"slug": r["review_of"], "category": "product"})
        if prod:
            prod_link = f'<a href="/product/{r["review_of"]}" class="meta-item">🔗 {esc(prod.get("title","")[:40])}</a>'
            prod_image_html = product_image(prod, "icon")

    wc_html = f'<div class="meta-item">📝 {r.get("word_count",0)} слов</div>' if r.get('word_count') else ''

    body = f"""
    <div class="container detail">
      <div class="breadcrumbs">
        <a href="/">Каталог</a> &rsaquo; <a href="/catalog?category=review">Обзоры</a> &rsaquo; <span>{esc(r.get('title',''))}</span>
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

    return HTMLResponse(make_page(
        esc(r.get('title','')), esc(str(r.get('tagline','') or r.get('description',''))[:160]), body,
        total=get_total_products(), active_review="active",
        open_graph=r.get('open_graph',''), schema_org=r.get('schema_org','')))


@app.get("/catalog", response_class=HTMLResponse)
async def catalog(request: Request):
    category = request.query_params.get("category", "product")
    q = request.query_params.get("q", "").strip()
    page = int(request.query_params.get("page", "1"))
    per_page = 24

    query = {"category": category}
    if q:
        query["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"tagline": {"$regex": q, "$options": "i"}},
        ]

    total = DB.articles.count_documents(query)
    total_pages = max(1, (total + per_page - 1) // per_page)
    items = list(DB.articles.find(query).skip((page - 1) * per_page).limit(per_page))

    labels = {"product": "Продукты", "comparison": "Сравнения", "review": "Обзоры"}
    label = labels.get(category, category)

    cards = ""
    if not items:
        cards = f'<div class="empty"><h2>Ничего не найдено</h2><p>В категории «{esc(label)}» пока пусто</p></div>'
    else:
        cards = '<div class="grid">'
        for item in items:
            if category == "product":
                cards += f"""
                <a href="/product/{item['slug']}" class="card">
                  <div class="card-header">
                    {product_image(item)}
                    {product_type_badge(item.get('product_type',''))}
                  </div>
                  <div class="card-title">{esc(item.get('title',''))}</div>
                  <div class="card-desc">{esc(item.get('tagline','') or item.get('description',''))}</div>
                  <div class="card-meta">
                    <span class="rating">{rating_stars(item.get('rating'))} {item.get('rating','')}</span>
                  </div>
                </a>"""
            elif category == "comparison":
                cards += f"""
                <a href="/compare/{item['slug']}" class="card">
                  <div class="card-header">
                    <div class="card-icon">⚖️</div>
                    <span class="card-badge badge-agent">VS</span>
                  </div>
                  <div class="card-title">{esc(item.get('title',''))}</div>
                  <div class="card-desc">{esc(str(item.get('description',''))[:120])}</div>
                </a>"""
            elif category == "review":
                cards += f"""
                <a href="/review/{item['slug']}" class="card">
                  <div class="card-header">
                    <div class="card-icon">📝</div>
                    <span class="card-badge badge-agent">{item.get('word_count',0)} слов</span>
                  </div>
                  <div class="card-title">{esc(item.get('title',''))}</div>
                  <div class="card-desc">{esc(str(item.get('tagline',''))[:100])}</div>
                </a>"""
        cards += "</div>"
        cards += page_nav(page, total_pages, f"/catalog?category={category}&q={q}")

    active_home = "active" if category == "product" else ""
    active_compare = "active" if category == "comparison" else ""
    active_review = "active" if category == "review" else ""

    body = f"""
    <div class="container">
      <h2 style="font-size:24px;font-weight:700;color:#e0e0f0;margin-bottom:20px">{esc(label)}</h2>
      {cards}
    </div>"""

    return HTMLResponse(make_page(
        label, f"Qantcore — {label} AI-агентов", body, search_val=q, total=get_total_products(),
        active_home=active_home, active_compare=active_compare, active_review=active_review))


# ─── Sitemap & robots.txt ──────────────────────────────────────

@app.get("/sitemap.xml")
async def sitemap():
    """Serve generated sitemap.xml"""
    sitemap_path = os.path.join(os.path.dirname(__file__), "sitemap.xml")
    if os.path.exists(sitemap_path):
        from fastapi.responses import Response
        with open(sitemap_path) as f:
            return Response(content=f.read(), media_type="application/xml")
    return Response(content="<error>Sitemap not found</error>", media_type="application/xml", status_code=404)


@app.get("/robots.txt")
async def robots():
    """Serve robots.txt"""
    from fastapi.responses import Response
    robots_txt = """User-agent: *
Allow: /
Sitemap: https://qantcore.space/sitemap.xml
"""
    return Response(content=robots_txt, media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
