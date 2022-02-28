from django.contrib import admin
from .models import Tag, Conversation, Goal ,userProfile



admin.site.register(Tag)
admin.site.register(Conversation)
admin.site.register(Goal)
admin.site.register(userProfile)