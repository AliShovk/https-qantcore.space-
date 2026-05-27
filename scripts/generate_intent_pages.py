#!/usr/bin/env python3
"""
Intent-money page generator for Qantcore SEO.
Generates rich landing pages for high-intent search queries:
/best/coding-agents/, /alternatives/cursor/, etc.

Uses LLM to create best-in-class content, saves to MongoDB (category='intent-page'),
then generate_static.py renders them.
"""
import sys, os, json, time, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pymongo import MongoClient

DB = MongoClient("localhost", 27017).qantcore

# ─── Intent Page Definitions ────────────────────────────────────
# Each page targets a specific high-intent SEO query
INTENT_PAGES = [
    {
        "slug": "best-coding-agents",
        "category": "intent-page",
        "intent_type": "best",
        "title": "Лучшие AI-агенты для кода в 2026",
        "subtitle": "Сравнительный рейтинг: Cursor, GitHub Copilot, Claude Code, Codex CLI и другие",
        "target_keyword": "лучшие AI агенты для кода",
        "secondary_keywords": ["AI coding agents 2026", "лучшие IDE с AI", "агенты для программирования", "сравнение AI ассистентов кода", "какой AI агент выбрать для разработки"],
        "products_filter": {"product_type": {"$in": ["ide", "cli", "terminal-agent"]}},
        "sort_by": "qant_score",
        "sort_dir": -1,
        "max_products": 15,
        "sections": ["hero", "top-picks", "comparison-table", "how-to-choose", "faq"],
    },
    {
        "slug": "best-multi-agent-frameworks",
        "category": "intent-page",
        "intent_type": "best",
        "title": "Лучшие Multi-Agent фреймворки 2026",
        "subtitle": "CrewAI, AutoGen, LangGraph, OpenAI SDK — что выбрать для production",
        "target_keyword": "лучшие multi-agent фреймворки",
        "secondary_keywords": ["multi-agent frameworks 2026", "CrewAI vs AutoGen vs LangGraph", "фреймворки для multi-agent систем", "production multi-agent", "оркестрация AI агентов"],
        "products_filter": {"product_type": {"$in": ["framework", "multi-agent"]}},
        "sort_by": "qant_score",
        "sort_dir": -1,
        "max_products": 10,
        "sections": ["hero", "top-picks", "comparison-table", "how-to-choose", "faq"],
    },
    {
        "slug": "best-local-llm",
        "category": "intent-page",
        "intent_type": "best",
        "title": "Лучшие локальные LLM для запуска на своём железе",
        "subtitle": "Llama, DeepSeek, Mistral, Qwen — сравнение производительности и требований",
        "target_keyword": "лучшие локальные LLM",
        "secondary_keywords": ["локальные LLM 2026", "запуск LLM локально", "ollama модели", "бесплатные LLM", "open source LLM сравнение"],
        "products_filter": {"product_type": "llm"},
        "sort_by": "qant_score",
        "sort_dir": -1,
        "max_products": 10,
        "sections": ["hero", "top-picks", "comparison-table", "hardware-requirements", "faq"],
    },
    {
        "slug": "best-free-ai-agents",
        "category": "intent-page",
        "intent_type": "best",
        "title": "Бесплатные AI-агенты: полный список 2026",
        "subtitle": "Open-source агенты для кода, автоматизации и аналитики без оплаты",
        "target_keyword": "бесплатные AI агенты",
        "secondary_keywords": ["free AI agents 2026", "open source AI agents", "бесплатные агенты для кода", "бесплатные аналоги Cursor", "open source coding agents"],
        "products_filter": {"pricing_model": {"$in": ["free", "open-source", "freemium"]}},
        "sort_by": "qant_score",
        "sort_dir": -1,
        "max_products": 12,
        "sections": ["hero", "top-picks", "comparison-table", "how-to-choose", "faq"],
    },
    {
        "slug": "best-enterprise-ai-agents",
        "category": "intent-page",
        "intent_type": "best",
        "title": "AI-агенты для Enterprise: безопасность, масштабирование, compliance",
        "subtitle": "Корпоративные решения на базе AI-агентов — что готово к production",
        "target_keyword": "AI агенты для enterprise",
        "secondary_keywords": ["enterprise AI agents", "корпоративные AI агенты", "AI агенты production", "security AI agents", "enterprise multi-agent"],
        "products_filter": {"product_type": {"$in": ["platform", "enterprise"]}},
        "sort_by": "qant_score",
        "sort_dir": -1,
        "max_products": 10,
        "sections": ["hero", "top-picks", "comparison-table", "security", "faq"],
    },
    {
        "slug": "alternatives-cursor",
        "category": "intent-page",
        "intent_type": "alternatives",
        "title": "Аналоги Cursor IDE: 10 лучших альтернатив в 2026",
        "subtitle": "Бесплатные, open-source и enterprise-альтернативы Cursor для разработки",
        "target_keyword": "аналоги Cursor IDE",
        "secondary_keywords": ["Cursor alternatives", "замена Cursor", "бесплатный аналог Cursor", "Cursor vs Windsurf", "альтернативы Cursor 2026"],
        "base_product": "cursor-ide",
        "exclude_slug": "cursor-ide",
        "products_filter": {"product_type": {"$in": ["ide", "cli", "terminal-agent"]}},
        "sort_by": "qant_score",
        "sort_dir": -1,
        "max_products": 10,
        "sections": ["hero", "why-alternatives", "top-alternatives", "comparison-table", "how-to-choose", "faq"],
    },
    {
        "slug": "alternatives-github-copilot",
        "category": "intent-page",
        "intent_type": "alternatives",
        "title": "Аналоги GitHub Copilot: 10 лучших альтернатив в 2026",
        "subtitle": "Бесплатные и платные заменители Copilot с лучшей производительностью",
        "target_keyword": "аналоги GitHub Copilot",
        "secondary_keywords": ["GitHub Copilot alternatives", "замена Copilot", "бесплатный аналог Copilot", "Copilot vs Cursor", "Copilot vs Claude Code"],
        "base_product": "github-copilot",
        "exclude_slug": "github-copilot",
        "products_filter": {"product_type": {"$in": ["ide", "cli", "terminal-agent"]}},
        "sort_by": "qant_score",
        "sort_dir": -1,
        "max_products": 10,
        "sections": ["hero", "why-alternatives", "top-alternatives", "comparison-table", "how-to-choose", "faq"],
    },
    {
        "slug": "alternatives-claude-code",
        "category": "intent-page",
        "intent_type": "alternatives",
        "title": "Аналоги Claude Code: 10 лучших терминальных AI-агентов",
        "subtitle": "Альтернативы Claude Code для терминала — open-source, дешевле, быстрее",
        "target_keyword": "аналоги Claude Code",
        "secondary_keywords": ["Claude Code alternatives", "замена Claude Code", "terminal AI agents", "CLI coding agents", "Claude Code vs Codex CLI"],
        "base_product": "claude-code",
        "exclude_slug": "claude-code",
        "products_filter": {"product_type": {"$in": ["cli", "terminal-agent"]}},
        "sort_by": "qant_score",
        "sort_dir": -1,
        "max_products": 10,
        "sections": ["hero", "why-alternatives", "top-alternatives", "comparison-table", "how-to-choose", "faq"],
    },
    {
        "slug": "ai-agents-startup-stack",
        "category": "intent-page",
        "intent_type": "best",
        "title": "AI-стек для стартапа: какие агенты выбрать в 2026",
        "subtitle": "Минимальный бюджет, максимальная отдача — AI-инструменты для стартапов",
        "target_keyword": "AI агенты для стартапа",
        "secondary_keywords": ["AI stack startup", "AI инструменты для стартапа", "дешёвые AI агенты", "стартап AI стек 2026", "с чего начать AI"],
        "products_filter": {"pricing_model": {"$in": ["free", "freemium", "open-source"]}},
        "sort_by": "qant_score",
        "sort_dir": -1,
        "max_products": 12,
        "sections": ["hero", "recommended-stack", "top-picks", "comparison-table", "budget", "faq"],
    },
]

# ─── LLM Client ──────────────────────────────────────────────────
from agents.llm_client import LLMClient
llm = LLMClient()

def load_skill_context():
    """Load relevant skill context for the LLM prompt."""
    return """
You are an SEO content strategist at Qantcore — the leading Russian-language AI agents review platform.
You write for a technical B2B audience: CTOs, engineering leads, ML engineers, startup founders.

Platform facts:
- 62 AI agent products tracked and reviewed
- 200+ detailed comparison pages
- Proprietary QantScore™ rating system (0-100 composite score)
- Russian-language interface, English product names
- Design: dark Bloomberg-terminal aesthetic, serious and analytical

Your writing style:
- Russian language, professional tone
- Data-driven: cite specific metrics, scores, numbers
- Practical: developers should be able to make a decision after reading
- No fluff, no marketing BS — direct, actionable, technical
- Structure: short paragraphs, bullet points, comparison tables
- Use «вы» not «ты»
"""

def generate_with_llm(page_def, products, system_prompt):
    """Generate a full intent page body via LLM."""
    slug = page_def['slug']
    intent_type = page_def['intent_type']
    title = page_def['title']
    
    # Build product data summary
    product_summaries = []
    for p in products:
        ps = f"- {p.get('title', p.get('slug','?'))}"
        ps += f" | QantScore: {p.get('qant_score','?')}"
        ps += f" | Rating: {p.get('rating','?')}/5"
        ps += f" | Price: {p.get('pricing_model','?')}"
        ps += f" | Type: {p.get('product_type','?')}"
        if p.get('tagline'):
            ps += f" | {p.get('tagline')}"
        product_summaries.append(ps)
    
    products_text = "\n".join(product_summaries)
    
    prompt = f"""Generate a rich SEO-optimized HTML page for Qantcore.space.

Page: /{intent_type}/{slug}/
Title: {title}
Target keyword: {page_def['target_keyword']}
Type: {'Best-of list' if intent_type == 'best' else 'Alternatives page'}

Available products for this page ({len(products)} total):
{products_text}

Requirements:
1. Generate complete HTML body content (inside a <div class="detail"> wrapper)
2. Include ALL of these sections (use h2 for section headers, h3 for subsections):
   - Hero/intro with key statistics
   - Quick picks (top 3 with brief explanations why each is #1/#2/#3)
   - Full comparison table (products as rows, columns: Name, QantScore, Rating, Price, Type, Best For)
   - "How to choose" decision guide (decision tree or checklist)
   - FAQ section (4-5 questions with answers)
3. Use proper semantic HTML: h2, h3, p, ul/li, table, strong
4. Add data-driven insights: mention specific QantScore values, ratings, pricing models
5. Internal linking: link to /product/{slug}/ for each mentioned product
6. Every alt-text and link should be meaningful
7. Keep total output under 4000 words
8. DO NOT include <!DOCTYPE>, <html>, <head>, <body> tags — just the content div
9. Use Russian language throughout
10. Embed the CSS classes qantcore uses: table class="compare-table", product links with class="product-link"

IMPORTANT: Output ONLY the HTML body content. No markdown code fences. No explanations."""

    response = llm.chat(system_prompt, prompt, temperature=0.4, max_tokens=8192)
    return response

def generate_intent_pages(dry_run=False):
    """Generate all intent-money pages and save to MongoDB."""
    from agents.state_manager_mongo import MongoStateManager
    state = MongoStateManager()
    
    generated = []
    
    for page_def in INTENT_PAGES:
        slug = page_def['slug']
        
        # Check if already exists
        existing = DB.articles.find_one({"slug": slug, "category": "intent-page"})
        if existing:
            print(f"  SKIP {slug} — already exists")
            continue
        
        # Find matching products
        products = list(DB.articles.find(
            {"category": "product", **page_def['products_filter']}
        ).sort(page_def['sort_by'], page_def['sort_dir']).limit(page_def['max_products']))
        
        if len(products) < 3:
            print(f"  SKIP {slug} — only {len(products)} matching products (need 3+)")
            continue
        
        print(f"  Generating {slug} ({len(products)} products)...")
        
        if dry_run:
            print(f"    [DRY RUN] Would generate {page_def['title']}")
            continue
        
        # Generate content via LLM
        system_prompt = load_skill_context()
        
        try:
            body = generate_with_llm(page_def, products, system_prompt)
            
            # Save to MongoDB
            doc = {
                "slug": slug,
                "category": "intent-page",
                "intent_type": page_def['intent_type'],
                "title": page_def['title'],
                "tagline": page_def['subtitle'],
                "description": page_def['subtitle'],
                "target_keyword": page_def['target_keyword'],
                "secondary_keywords": page_def['secondary_keywords'],
                "body_html": body,
                "meta_title": f"{page_def['title']} — Qantcore",
                "meta_description": page_def['subtitle'],
                "product_ids": [p['_id'] for p in products],
                "product_count": len(products),
                "created_at": datetime.datetime.now().isoformat(),
                "status": "published",
            }
            
            state.save_article(doc)
            generated.append(slug)
            print(f"    ✓ Saved to MongoDB ({len(body)} chars)")
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
            continue
    
    return generated

if __name__ == "__main__":
    import datetime
    dry = "--dry-run" in sys.argv
    
    print(f"\n{'[DRY RUN] ' if dry else ''}Intent-Money Page Generator\n")
    print(f"Total pages defined: {len(INTENT_PAGES)}")
    
    # Check existing
    existing = DB.articles.count_documents({"category": "intent-page"})
    print(f"Already in DB: {existing}")
    print()
    
    result = generate_intent_pages(dry_run=dry)
    
    print(f"\nGenerated: {len(result)} pages")
    if result:
        for r in result:
            print(f"  ✓ {r}")
    
    print("\nNext: python3 generate_static.py  (to render HTML)")
