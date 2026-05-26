"""Fill empty review bodies with rich HTML content.
Usage: python3 scripts/fill_review_bodies.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from pymongo import MongoClient
from agents.llm_client import get_default_client

client = MongoClient('mongodb://localhost:27017/')
db = client['qantcore']
llm = get_default_client()

reviews = list(db.articles.find({'category': 'review', 'body': ''}))
print(f"Reviews with empty body: {len(reviews)}")

REVIEW_PROMPT = """Напиши глубокий технический обзор продукта на русском языке.

Продукт: {title}
Описание: {tagline}
Тип: {product_type}
Категория: {subcategory}

Структура (строго следуй, используй HTML-теги):

<h2>Что такое {name}</h2>
<p>2-3 абзаца: что это за инструмент, для кого, основная ценность.</p>

<h2>Ключевые возможности</h2>
<ul>
<li>5-7 пунктов с конкретными техническими деталями</li>
</ul>

<h2>Характеристики и тарифы</h2>
<p>Информация о модели распространения, ценах, уровнях доступа. Если open-source — указать.</p>

<h2>Плюсы и минусы</h2>
<h3>Сильные стороны</h3>
<ul><li>3-5 пунктов</li></ul>
<h3>Ограничения</h3>
<ul><li>2-3 пункта</li></ul>

<h2>Сравнение с аналогами</h2>
<p>2-3 ближайших конкурента, ключевые отличия. Без таблиц — текстом.</p>

<h2>Вердикт</h2>
<p>Для каких сценариев подходит лучше всего. Кому стоит выбрать, кому — посмотреть альтернативы.</p>

Требования:
— Аналитический стиль Habr, без маркетинговых штампов
— Конкретные технические детали, не общие слова
— HTML-разметка (h2, h3, ul, li, p, strong)
— 800-1200 слов
— Без h1 (заголовок уже есть на странице)
— Не используй markdown, только HTML
— Верни чистый HTML без обрамляющих ```html```
"""

for r in reviews:
    slug = r['slug']
    review_of = r.get('review_of', '')
    product = db.articles.find_one({'slug': review_of}) or {}
    
    title = r.get('title', '')
    name = title.replace('Обзор ', '').split(' 2026')[0].split(':')[0].strip()
    tagline = product.get('tagline', '') or r.get('tagline', '')
    product_type = product.get('product_type', '') or r.get('product_type', '')
    subcategory = product.get('subcategory', '') or r.get('subcategory', '')
    
    prompt = REVIEW_PROMPT.format(
        title=title, name=name, tagline=tagline,
        product_type=product_type, subcategory=subcategory
    )
    
    print(f"\nGenerating: {slug} ({name})...", flush=True)
    
    try:
        resp = llm.chat(
            "Ты — технический редактор платформы аналитики AI-агентов Qantcore (qantcore.space).",
            prompt,
            temperature=0.4,
            max_tokens=4096
        )
        body_html = resp.strip()
        if body_html.startswith('```html'):
            body_html = body_html[7:]
        if body_html.startswith('```'):
            body_html = body_html[3:]
        if body_html.endswith('```'):
            body_html = body_html[:-3]
        body_html = body_html.strip()
        
        word_count = len(body_html.split())
        
        db.articles.update_one(
            {'slug': slug},
            {'$set': {'body': body_html, 'body_html': body_html, 'word_count': word_count}}
        )
        print(f"  OK ({word_count} words)", flush=True)
    except Exception as e:
        print(f"  FAIL: {e}", flush=True)

print(f"\nDone. {len(reviews)} reviews.")
