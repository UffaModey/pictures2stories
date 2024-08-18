from django.urls import path
from . import views

urlpatterns = [
    path('', views.stories_list, name='stories_list'),
    path('create', views.create_story, name='create_story'),
    path('add', views.add_story, name='add_story'),
    path('story/<uuid:id>', views.story_details, name='story_details'),
    path('story/<uuid:pk>/delete', views.StoryDeleteView.as_view(), name='story_delete'),
    path('story-delete-success', views.story_delete_success, name='story_delete_success'),
    # More patterns to come later
]
