from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name='notes', on_delete=models.CASCADE)


class SharedNote(models.Model):
    note = models.ForeignKey(
        Note, related_name='shared_notes', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='shared_notes', on_delete=models.CASCADE)


class NoteChange(models.Model):
    note = models.ForeignKey(
        Note, related_name='change_history', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    change_content = models.TextField()
