import time
import moviepy.editor as mp
import requests
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.editor import AudioFileClip, vfx, afx
import math
from PIL import Image
import numpy
from gtts import gTTS
from moviepy.video.VideoClip import ImageClip


def create_slide(product):
    image_files = product.images
    size = (1920, 1080)
    slides = []
    for n, url in enumerate(image_files):
        if resize_image(url, size):
            time.sleep(1)
            slides.append(
                mp.ImageClip('image.jpg').set_fps(24).set_duration(5)
            )
            slides[n] = zoom_in_effect(slides[n], 0.03).fx(vfx.fadein, 1).fx(vfx.fadeout, 1)
        else:
            continue

    video = mp.concatenate_videoclips(slides)
    video_duration = video.duration

    # Background music
    text = "EAST WEST FURNITURE - 3-PIECE KITCHEN TABLE SET Enhance your kitchen's allure with a sophisticated 3-Piece kitchen set, comprising a rectangular dining table and 2 finely crafted dining chairs. This collection epitomizes contemporary elegance, featuring a sleek, high-gloss finish on both the table and chairs. Meticulously crafted with premium materials, it seamlessly harmonizes with various interior decors. The centerpiece, a modern dining table, combines a Cherry wood tabletop with a refined Buttermilk finish, ensuring both timeless aesthetics and enduring durability. Its versatile design effortlessly complements diverse decor styles, making it a perennial addition to your living space. The dining chairs' Buttermilk-finished wooden legs introduce a touch of modern sophistication, enhancing style and comfort. Constructed from top-grade Asian rubber wood, this dining set guarantees unmatched durability, free from heat-treated wood, plywood, veneer, or laminates. The set's versatile style effortlessly complements any decor, promising lasting appeal. The spacious wooden seats of the dining chairs elevate the kitchen's aesthetics and ensure exceptional comfort. Featuring a versatile backrest design suitable for various decor styles, from rustic to modern, these chairs offer a comfortable dining experience for all users. Assembly is straightforward with provided instructions, and our primary concern is your satisfaction. Buy with confidence and elevate your kitchen's allure professionally and stylishly."

    try:
        tts = gTTS(text=text, lang="en",
                   slow=False)
        tts_audio_file = "output.mp3"
        tts.save(tts_audio_file)

        overlay_music()
        audio_clip = mp.AudioFileClip('final.mp3')

        if audio_clip.duration > video_duration:
            # Trim audio if it's longer than the video
            audio_clip = audio_clip.subclip(0, video_duration).fx(afx.audio_fadeout, 5)

        video = video.set_audio(audio_clip)

    except Exception as e:
        print(f"An error occurred: {e}")

    video.write_videofile(f'{product.sku}.mp4')


# Add Text
# from moviepy.editor import TextClip, CompositeVideoClip
# Create an image clip
# image_clip = ImageClip("image1.jpg").set_duration(5)
#
# # Create a text clip
# text_clip = TextClip("Product Name", fontsize=70, color='white')
# text_clip = text_clip.set_position("center").set_duration(5)
#
# # Overlay the text clip on the image clip
# video = CompositeVideoClip([image_clip, text_clip])
#
# # Export to MP4
# video.write_videofile("video_with_text.mp4", fps=24)


def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)


def overlay_music():
    try:
        # Load the audio files
        audio1 = AudioFileClip('output.mp3')
        audio2 = AudioFileClip('background-music.mp3')

        # Composite the audio tracks
        # The first track will be used as the base duration
        final_audio = audio1.set_start(2)

        # Add the second track at the specified start time
        final_audio = final_audio.set_duration(audio1.duration).audio_fadeout(1).audio_fadein(1).volumex(0.9)
        overlay = audio2.set_start(0).volumex(1)

        # Combine the tracks
        combined = CompositeAudioClip([final_audio, overlay]).set_fps(44100)
        # Write the result
        combined.write_audiofile('final.mp3')

        # Close the clips to free up resources
        audio1.close()
        audio2.close()
        combined.close()

        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


def resize_image(image_url, target_size):
    target_height = int(target_size[1] * 0.8)

    response = requests.get(image_url, stream=True)

    if response.status_code == 200:
        with open('image.jpg', "wb") as file:
            for chunk in response.iter_content(1024):  # Download in chunks of 1 KB
                file.write(chunk)
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return False

    # Open the image
    img = Image.open('image.jpg')
    aspect_ratio = img.width / img.height
    target_width = int(target_height * aspect_ratio)
    resized_img = img.resize((target_width, target_height), Image.ANTIALIAS)

    # Create a new white image with the target size
    background = Image.new('RGB', target_size, (255, 255, 255))

    # Get the size of the original image
    img_width, img_height = resized_img.size

    # Center the image within the target size
    x_offset = (target_size[0] - img_width) // 2
    y_offset = (target_size[1] - img_height) // 2

    # Paste the original image onto the center of the white background
    background.paste(resized_img, (x_offset, y_offset))

    # Save the result
    background.save('image.jpg')
    return True
