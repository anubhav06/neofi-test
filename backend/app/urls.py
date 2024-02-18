from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:id>/', views.note_detail, name='note_detail'),
    path('notes/share/', views.share_note, name='share_note'),
    path('notes/<int:id>/', views.note_detail,
         name='note_detail'),
    path('notes/version-history/<int:id>/',
         views.get_note_version_history, name='get_note_version_history'),

]
