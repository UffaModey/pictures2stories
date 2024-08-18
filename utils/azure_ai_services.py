from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI
import os
from django.shortcuts import render
from dotenv import load_dotenv
from azureai.models import Image, Story

# Initialize the Azure and OpenAI clients
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
cl = ImageAnalysisClient(
    endpoint=os.getenv("VISION_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("VISION_KEY"))
)


def generate_story_from_pictures(image_one, image_two, image_three):
    # Analyze images using Azure Vision API
    image_data_one = image_one.read()
    image_data_two = image_two.read()
    image_data_three = image_three.read()

    result_one = cl.analyze(
        image_data=image_data_one,
        visual_features=["CAPTION", "READ"],
        gender_neutral_caption=True,
    )
    result_two = cl.analyze(
        image_data=image_data_two,
        visual_features=["CAPTION", "READ"],
        gender_neutral_caption=True,
    )
    result_three = cl.analyze(
        image_data=image_data_three,
        visual_features=["CAPTION", "READ"],
        gender_neutral_caption=True,
    )

    # Prepare the prompt using captions from all images
    prompt = f"Write a short story of 50 words that includes these elements: {result_one.caption.text}, " \
             f"{result_two.caption.text}, and {result_three.caption.text}. Generate a title for the story " \
             f"in 5 words or less."

    try:
        # Generate the story using OpenAI API
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a children's book author skilled in adventure and "
                                              "fiction novels set in 1980."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_story = completion.choices[0].message.content

        # Splitting the response into story and title
        story_parts = generated_story.split("\n\n")

        if len(story_parts) == 2:
            title_text = story_parts[0]
            if title_text.lower().startswith("title:"):
                title_text = title_text[7:].strip()
            story_text = story_parts[1]
        else:
            title_text = "Untitled Story"
            story_text = generated_story

    except Exception as e:
        return render(request, 'pictures_2_stories/create_story.html', {
            'error_message': f"Error generating story: {e}",
        })

    # Save the story and images to the database
    story = Story(generated_story=story_text,
                  title=title_text)
    story.save()

    Image.objects.create(image=image_one, caption=result_one.caption.text, caption_confidence=result_one.caption.confidence, story=story)
    Image.objects.create(image=image_two, caption=result_two.caption.text, caption_confidence=result_two.caption.confidence, story=story)
    Image.objects.create(image=image_three, caption=result_three.caption.text, caption_confidence=result_three.caption.confidence, story=story)

    return story
        
        