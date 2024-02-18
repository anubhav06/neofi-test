from django.contrib import admin
from django.contrib.auth.models import User
from .models import Note, SharedNote, NoteChange

# Register your models here.
admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Note)
admin.site.register(SharedNote)
admin.site.register(NoteChange)
