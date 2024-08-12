from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI
import os
from dotenv import load_dotenv

from azureai.models import Image, Story

# Initialize the Azure and OpenAI clients
# load_dotenv()
#
# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )
# cl = ImageAnalysisClient(
#     endpoint=os.getenv("VISION_ENDPOINT"),
#     credential=AzureKeyCredential(os.getenv("VISION_KEY"))
# )

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

        # # Analyze images using Azure Vision API
        # image_data_one = image_one.read()
        # image_data_two = image_two.read()
        # image_data_three = image_three.read()

        # result_one = cl.analyze(
        #     image_data=image_data_one,
        #     visual_features=["CAPTION", "READ"],
        #     gender_neutral_caption=True,
        # )
        # result_two = cl.analyze(
        #     image_data=image_data_two,
        #     visual_features=["CAPTION", "READ"],
        #     gender_neutral_caption=True,
        # )
        # result_three = cl.analyze(
        #     image_data=image_data_three,
        #     visual_features=["CAPTION", "READ"],
        #     gender_neutral_caption=True,
        # )
        #
        # # Prepare the prompt using captions from all images
        # prompt = f"Write a short story of 50 words that includes these elements: {result_one.caption.text}, {result_two.caption.text}, and {result_three.caption.text}."
        #
        # try:
        #     # Generate the story using OpenAI API
        #     completion = client.chat.completions.create(
        #         model="gpt-3.5-turbo",
        #         messages=[
        #             {"role": "system", "content": "You are a children's book author skilled in adventure and fiction novels set in 1980."},
        #             {"role": "user", "content": prompt}
        #         ]
        #     )
        #     generated_story = completion.choices[0].message['content']
        # except Exception as e:
        #     return render(request, 'create_story.html/add_story.html', {
        #         'error_message': f"Error generating story: {e}",
        #     })

        # Save the story and images to the database
        # story = Story(generated_story=generated_story)
        story = Story(generated_story="new story content",
                      title="new story")
        story.save()

        Image.objects.create(image=image_one, caption="test caption", caption_confidence=9, story=story)
        Image.objects.create(image=image_two, caption="test caption", caption_confidence=9, story=story)
        Image.objects.create(image=image_three, caption="test caption", caption_confidence=9, story=story)

        return HttpResponseRedirect(reverse('story_details', args=(story.id,)))

    else:
        return render(request, 'pictures_2_stories/add_story.html')
