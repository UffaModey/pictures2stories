from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from azureai.models import Image, Story
from utils.azure_ai_services import generate_story_from_pictures


class StoryDeleteView(DeleteView):
    model = Story
    template_name = 'pictures_2_stories/story_confirm_delete.html'
    success_url = reverse_lazy('story_delete_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['story'] = self.object
        return context

def story_delete_success(request):
    print('Request for story delete success received')
    return render(request, 'pictures_2_stories/delete_story_success.html')

def stories_list(request):
    print('Request for index page received')
    stories = Story.objects.all()
    return render(request, 'pictures_2_stories/index.html', {'stories': stories})

@cache_page(60)
def story_details(request, id):
    print('Request for stories details page received')
    story = get_object_or_404(Story, id=id)
    images = Image.objects.filter(story=story)
    return render(request, 'pictures_2_stories/details.html', {'story': story, 'images': images})

def create_story(request):
    print('Request for add story page received')
    return render(request, 'pictures_2_stories/create_story.html')

@csrf_exempt
def add_story(request):
    if request.method == 'POST':
        try:
            # Fetch the uploaded images
            image_one = request.FILES.get('image_one')
            image_two = request.FILES.get('image_two')
            image_three = request.FILES.get('image_three')
        except KeyError as e:
            # Redisplay the form with an error message if any image is missing
            return render(request, 'pictures_2_stories/create_story.html', {
                'error_message': e,
            })
        
        try:
            story = generate_story_from_pictures(image_one, image_two, image_three)
        except Exception as e:
            return render(request, 'pictures_2_stories/create_story.html', {
                'error_message': e,
            })

        return HttpResponseRedirect(reverse('story_details', args=(story.id,)))

    else:
        return render(request, 'pictures_2_stories/add_story.html')
