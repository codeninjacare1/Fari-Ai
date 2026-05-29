import json
import uuid
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import Lead, ChatSession, ChatMessage

from django.http import HttpResponse
from twilio.twiml.voice_response import VoiceResponse
from .models import CallLog

FARI_SYSTEM_PROMPT = """You are Fari, the friendly and professional AI Receptionist for Gainsboro Infotech — a Top-Rated Software Development Company for 2026.

Company Overview:
- Gainsboro Infotech specializes in intelligent software development, AI solutions, data engineering, and web/app development
- We work with U.S.-aligned engineers who communicate clearly and deliver consistently
- Services include: AI & Machine Learning solutions, custom software development, web development (WordPress, Webflow, Framer, Shopify, Bubble), mobile app development, SEO, Google Ads, and digital marketing
- We are recognized as a Top-Rated company in 2026
- Brand color: #14A800 (green)

Your capabilities:
- 24/7 call answering with natural voice
- Smart call routing via Slack DMs and phone transfers
- Structured message taking (name, reason, callback number)
- Appointment scheduling via Google Calendar
- Agent configuration and conversation tuning

Your role:
- Warmly greet visitors and understand their needs
- Answer questions about Gainsboro's services, expertise, and process
- Help prospects understand how Gainsboro can solve their problems
- Collect lead info (name, email, project type) when someone wants to get started
- Suggest next steps: book a call, send inquiry, or leave a message
- Keep responses concise — 2-3 sentences unless detail is genuinely needed
- Use warm, confident, professional tone
- Never make up specific pricing — say the team will provide a tailored quote
- If asked something you don't know, say you'll connect them with the right person

Always aim to move the conversation toward a concrete next step."""


def landing(request):
    """Main landing page."""
    features = [
        {
            'icon': 'ti-phone-call',
            'title': '24/7 Call Answering',
            'desc': 'Answers every call instantly with a natural voice. Day, night, weekends, and holidays — zero missed opportunities.',
            'tag': 'Always on',
        },
        {
            'icon': 'ti-route',
            'title': 'Smart Call Routing',
            'desc': 'Routes calls via Slack DMs and phone transfers to the right person in real time — no hold music, no confusion.',
            'tag': 'Real-time',
        },
        {
            'icon': 'ti-notes',
            'title': 'Structured Message Taking',
            'desc': 'Captures caller name, reason, callback number, and message automatically. Delivered as a clean summary instantly.',
            'tag': 'Structured',
        },
        {
            'icon': 'ti-calendar-event',
            'title': 'Appointment Scheduling',
            'desc': 'Checks Google Calendar availability and books meetings during the call. No back-and-forth emails needed.',
            'tag': 'Google Calendar',
        },
        {
            'icon': 'ti-settings',
            'title': 'Agent Configuration',
            'desc': 'Configure personality, voice, knowledge base, pronunciations, and call recording — all from a simple dashboard.',
            'tag': 'Configurable',
        },
        {
            'icon': 'ti-sliders',
            'title': 'Conversation Tuning',
            'desc': 'Fine-tune voice and conversation parameters. Changes apply to new calls immediately — no redeployment needed.',
            'tag': 'Instant apply',
        },
    ]

    capabilities = [
        {
            'num': '01',
            'title': 'Custom AI & LLM Integration',
            'desc': 'We build custom AI systems powered by GPT-4, Claude, Gemini, and open-source LLMs — fine-tuned to your domain and data.',
            'tags': ['GPT-4', 'Claude', 'Fine-tuning', 'RAG'],
        },
        {
            'num': '02',
            'title': 'AI Agents & Automation',
            'desc': 'Multi-agent systems, autonomous workflows, and task automation that operate 24/7 without human intervention.',
            'tags': ['LangChain', 'AutoGen', 'CrewAI', 'Zapier'],
        },
        {
            'num': '03',
            'title': 'Data Engineering & Analytics',
            'desc': 'End-to-end data pipelines, warehousing, and real-time analytics dashboards built for enterprise-grade reliability.',
            'tags': ['Spark', 'Airflow', 'BigQuery', 'Snowflake'],
        },
        {
            'num': '04',
            'title': 'Intelligent Web & App Development',
            'desc': 'AI-enhanced web apps on WordPress, Webflow, Framer, Shopify, and Bubble — with smart features baked in from day one.',
            'tags': ['Webflow', 'Shopify', 'Bubble', 'WordPress'],
        },
    ]

    process_steps = [
        {'num': '01', 'title': 'Discovery Call', 'desc': 'We understand your goals, tech stack, timeline, and define clear success metrics together.'},
        {'num': '02', 'title': 'Solution Design', 'desc': 'Architecture, tech choices, sprint breakdown, and a detailed proposal — delivered within 48 hours.'},
        {'num': '03', 'title': 'Build & Iterate', 'desc': 'Agile sprints with weekly demos. You see progress every step of the way — no black boxes.'},
        {'num': '04', 'title': 'Launch & Scale', 'desc': 'Deployment, QA, documentation, and ongoing support. We stay with you after go-live.'},
    ]

    tech_stack = [
        {'icon': 'ti-brain', 'name': 'OpenAI GPT-4'},
        {'icon': 'ti-robot', 'name': 'Claude API'},
        {'icon': 'ti-sparkles', 'name': 'Gemini Pro'},
        {'icon': 'ti-code', 'name': 'Python / FastAPI'},
        {'icon': 'ti-brand-react', 'name': 'React / Next.js'},
        {'icon': 'ti-database', 'name': 'PostgreSQL'},
        {'icon': 'ti-cloud', 'name': 'AWS / GCP'},
        {'icon': 'ti-brand-docker', 'name': 'Docker / K8s'},
        {'icon': 'ti-chart-bar', 'name': 'LangChain'},
        {'icon': 'ti-server', 'name': 'Node.js'},
        {'icon': 'ti-brand-wordpress', 'name': 'WordPress'},
        {'icon': 'ti-browser', 'name': 'Webflow'},
        {'icon': 'ti-shopping-cart', 'name': 'Shopify'},
        {'icon': 'ti-circles-relation', 'name': 'Bubble'},
        {'icon': 'ti-search', 'name': 'SEO / GA4'},
    ]

    testimonials = [
        {
            'stars': '★★★★★',
            'quote': '"Gainsboro built our AI chatbot in 3 weeks. The communication was seamless and the delivery was exactly what we envisioned. Genuinely impressed."',
            'initials': 'JM',
            'name': 'James Mitchell',
            'role': 'CTO, TechFlow Inc.',
        },
        {
            'stars': '★★★★★',
            'quote': '"Fari answered every call while we focused on closing deals. We went from missing 30% of inbound calls to capturing every single one. Game changer."',
            'initials': 'SR',
            'name': 'Sarah Rowlands',
            'role': 'Founder, GrowthLabs',
        },
        {
            'stars': '★★★★★',
            'quote': '"Their data pipeline reduced our reporting time from 3 days to 20 minutes. The team was proactive, fast, and always available. Highly recommend."',
            'initials': 'AK',
            'name': 'Arjun Kapoor',
            'role': 'Head of Data, Vantage Co.',
        },
    ]

    return render(request, 'landing.html', {
        'features': features,
        'capabilities': capabilities,
        'process_steps': process_steps,
        'tech_stack': tech_stack,
        'testimonials': testimonials,
    })


def submit_lead(request):
    """Handle lead form submission."""
    if request.method == 'POST':
        Lead.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            company=request.POST.get('company', ''),
            project_type=request.POST.get('project_type', ''),
            message=request.POST.get('message', ''),
        )
        return JsonResponse({'status': 'ok', 'message': "Thanks! We'll be in touch within 24 hours."})
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def fari_chat(request):
    """Fari AI chat endpoint — proxies to Anthropic API and persists messages."""
    try:
        body = json.loads(request.body)
        user_message = body.get('message', '').strip()
        session_key = body.get('session_key', '') or str(uuid.uuid4())

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        # Get or create session
        session, _ = ChatSession.objects.get_or_create(session_key=session_key)

        # Save user message
        ChatMessage.objects.create(session=session, role='user', content=user_message)

        # Build history (last 20 messages)
        history = list(session.messages.order_by('created_at').values('role', 'content'))[-20:]
        messages = [{'role': m['role'], 'content': m['content']} for m in history]

        # Call Anthropic API
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json',
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 1000,
                'system': FARI_SYSTEM_PROMPT,
                'messages': messages,
            },
            timeout=30,
        )

        data = response.json()
        reply = data.get('content', [{}])[0].get('text', "I'm sorry, I couldn't process that. Please try again.")

        # Save assistant reply
        ChatMessage.objects.create(session=session, role='assistant', content=reply)

        return JsonResponse({'reply': reply, 'session_key': session_key})

    except requests.exceptions.Timeout:
        return JsonResponse({'reply': "I'm taking a bit long to respond. Please try again in a moment.", 'session_key': session_key})
    except Exception as e:
        return JsonResponse({'reply': "I'm having a small hiccup — please try again.", 'session_key': str(uuid.uuid4())})


def dashboard(request):
    """Simple lead dashboard for the team."""
    leads = Lead.objects.order_by('-created_at')
    sessions = ChatSession.objects.order_by('-updated_at')[:10]
    return render(request, 'dashboard.html', {'leads': leads, 'sessions': sessions, 'lead_count': leads.count()})






def incoming_call(request):

    caller = request.POST.get("From")
    call_sid = request.POST.get("CallSid")

    # Save Call
    CallLog.objects.create(
        caller_number=caller,
        call_sid=call_sid,
        status="incoming"
    )

    response = VoiceResponse()

    response.say(
        "Hello. Welcome to Fari AI Receptionist. How can I help you today?",
        voice='alice'
    )

    return HttpResponse(str(response), content_type='text/xml')