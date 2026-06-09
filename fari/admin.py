from django.contrib import admin
from .models import Lead, ChatSession, ChatMessage
from .models import AgentSettings,StructuredMessage


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'project_type', 'created_at']
    search_fields = ['name', 'email', 'company']
    list_filter = ['created_at']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'created_at', 'updated_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'content', 'created_at']
    list_filter = ['role']


admin.site.register(AgentSettings)
admin.site.register(StructuredMessage)