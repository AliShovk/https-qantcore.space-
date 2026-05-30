# Доступы к поисковым инструментам qantcore.space
# Обновлено: 30.05.2026

## Google Search Console
Тип: Service Account
Email: hermes-gsc@my-project-1719928012658.iam.gserviceaccount.com
Проект: my-project-1719928012658 (числовой: 49340658033)
Ключ: skills/seo/google-search-console/references/hermes-gsc-key.json
Верификация: FILE (google01948badb315ae03.html на /var/www/qantcore/)
Статус: siteOwner, sitemap 560 URL, 0 indexed (ждём краулинг)

## Bing Webmaster
Тип: API Key
Ключ: db231b7e28394c9c82889f8027fff23f
Импортирован из GSC: да
Верифицирован: да (IsVerified: true)
Статус: 60/560 URL отправлено, квота 100/день

## IndexNow (Bing + Яндекс + Seznam + Yep)
Ключ: af6b31b1d07db24583da448b09758613
Файл: https://qantcore.space/indexnow-af6b31b1d07db24583da448b09758613.txt
Статус: Яндекс принял 560 URL, Bing ждёт верификации

## Яндекс.Метрика
Counter ID: 109327472
Статус: активен

## Яндекс.Вебмастер
User ID: 124439551
Токен: УТЕРЯН (был /tmp/ytoken.json)
Нужно: получить новый OAuth-токен

## Cron-задачи
- GSC Monitor: ежедневно 10:00 (job: 1744c2e85c69)
- IndexNow: ежедневно 2:00 (job: b15a3d5124d8)
- Bing Submit: ежедневно 3:00 (job: d53a04cb1247)

## Скрипты
- /opt/data/scripts/gsc_monitor.py — мониторинг индексации Google
- /opt/data/scripts/indexnow_submit.py — отправка URL через IndexNow
- /opt/data/scripts/bing_submit.py — отправка URL в Bing (100/день)
- /opt/data/skills/seo/google-search-console/references/hermes-gsc-key.json — ключ GSC

## SSH Host
IP: 186.246.14.234
User: root
Пароль: mid-?A-kL96-UD
Файлы сайта: /var/www/qantcore/
