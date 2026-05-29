# Gainsboro Infotech — Fari AI Landing Page (Django)

## Setup (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Anthropic API key (for Fari chat to work)
export ANTHROPIC_API_KEY=your_key_here

# 3. Run migrations
python manage.py migrate

# 4. Start the server
python manage.py runserver
```

## Open in browser
- Landing page: http://127.0.0.1:8000/
- Lead dashboard: http://127.0.0.1:8000/dashboard/
- Django admin: http://127.0.0.1:8000/admin/

## Create admin user (optional)
```bash
python manage.py createsuperuser
```

## Pages & Features
| URL | Feature |
|-----|---------|
| `/` | Full landing page with Fari features, capabilities, process, tech stack, testimonials, and lead form |
| `/api/fari/chat/` | Fari AI chat API (POST) |
| `/submit-lead/` | Lead capture endpoint (POST) |
| `/dashboard/` | View all captured leads and chat sessions |
| `/admin/` | Full Django admin |

## What's included
- Full landing page in #14A800 green theme
- All 6 Fari AI features displayed
- 4 AI capability cards
- 4-step process section
- 15-item tech stack
- 3 testimonials
- Lead capture form (saves to SQLite)
- Fari chat widget (powered by Claude API)
- Lead dashboard
- Django admin for full data management

## Deployment (production)
Set `DEBUG = False` in settings.py and add your domain to `ALLOWED_HOSTS`.
Use gunicorn + nginx for production serving.
