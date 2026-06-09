from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True)
    project_type = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.email}"

class ChatSession(models.Model):
    session_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_key}"

class ChatMessage(models.Model):
    ROLE_CHOICES = [('user', 'User'), ('assistant', 'Assistant')]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.role}] {self.content[:60]}"





# class CallLog(models.Model):
#     caller_number = models.CharField(max_length=20)
#     call_sid = models.CharField(max_length=100)
#     status = models.CharField(max_length=50, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.caller_number
    
class CallLog(models.Model):

    caller_number = models.CharField(max_length=30)
    call_sid = models.CharField(max_length=200)
    recording_url = models.URLField(blank=True, null=True)
    recording_sid = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)



class AgentSettings(models.Model):

    agent_name = models.CharField(max_length=100, default="Fari")

    voice = models.CharField(
        max_length=50,
        default="alice"
    )

    greeting_message = models.TextField(
        default="Hello. Welcome to Fari AI Receptionist. How can I help you today?"
    )

    personality = models.TextField(
        default="Friendly, professional and confident"
    )

    speaking_rate = models.FloatField(default=1.0)

    recording_enabled = models.BooleanField(default=True)

    transfer_enabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agent_name




# =========================================
# STRUCTURED MESSAGE
# =========================================

class StructuredMessage(models.Model):

    caller_name = models.CharField(
        max_length=255
    )

    reason = models.TextField()

    callback_number = models.CharField(
        max_length=20
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.caller_name