from django.urls import path
from . import views

urlpatterns = [
    path('', views.stories_list, name='stories_list'),
    path('create', views.create_story, name='create_story'),
    path('add', views.add_story, name='add_story'),
    path('story/<uuid:id>', views.story_details, name='story_details'),
    # More patterns to come later
]
