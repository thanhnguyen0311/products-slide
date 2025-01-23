import time
import moviepy.editor as mp
import requests
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.editor import AudioFileClip, vfx, afx
from PIL import Image
from gtts import gTTS

from src.Enum.FilePath import FilePath
from src.common.effects import zoom_in_effect, swipe_in_effect


def create_slide(product):
    image_files = product.images
    size = (1920, 1080)
    slides = []
    for n, url in enumerate(image_files):
        if resize_image(url, size):
            time.sleep(1)
            slides.append(
                mp.ImageClip(FilePath.IMAGE_OUTPUT.value).set_fps(24).set_duration(5)
            )
            if n > 1:
                slides[n] = swipe_in_effect(slides[n], 'left').subclip(1, 5)
                break
            slides[n] = zoom_in_effect(slides[n], 0.03).fx(vfx.fadein, 1).fx(vfx.fadeout, 1)
        else:
            continue

    video = mp.concatenate_videoclips(slides)
    video_duration = video.duration

    # Background music
    text = "EAST WEST FURNITURE - 3-PIECE KITCHEN TABLE SET Enhance your kitchen's allure with a sophisticated 3-Piece kitchen set, comprising a rectangular dining table and 2 finely crafted dining chairs. This collection epitomizes contemporary elegance, featuring a sleek, high-gloss finish on both the table and chairs. Meticulously crafted with premium materials, it seamlessly harmonizes with various interior decors. The centerpiece, a modern dining table, combines a Cherry wood tabletop with a refined Buttermilk finish, ensuring both timeless aesthetics and enduring durability. Its versatile design effortlessly complements diverse decor styles, making it a perennial addition to your living space. The dining chairs' Buttermilk-finished wooden legs introduce a touch of modern sophistication, enhancing style and comfort. Constructed from top-grade Asian rubber wood, this dining set guarantees unmatched durability, free from heat-treated wood, plywood, veneer, or laminates. The set's versatile style effortlessly complements any decor, promising lasting appeal. The spacious wooden seats of the dining chairs elevate the kitchen's aesthetics and ensure exceptional comfort. Featuring a versatile backrest design suitable for various decor styles, from rustic to modern, these chairs offer a comfortable dining experience for all users. Assembly is straightforward with provided instructions, and our primary concern is your satisfaction. Buy with confidence and elevate your kitchen's allure professionally and stylishly."

    voice_generator(text)
    
    overlay_music()
    audio_clip = mp.AudioFileClip(FilePath.FINAL_AUDIO.value)

    if audio_clip.duration > video_duration:
        # Trim audio if it's longer than the video
        audio_clip = audio_clip.subclip(0, video_duration).fx(afx.audio_fadeout, 5)

    video = video.set_audio(audio_clip)

    video.write_videofile(f'{product.sku}.mp4')


def overlay_music():
    try:
        # Load the audio files
        audio1 = AudioFileClip(FilePath.VOICE_OUTPUT.value)
        audio2 = AudioFileClip(FilePath.BACKGROUND_MUSIC.value)

        # Composite the audio tracks
        # The first track will be used as the base duration
        final_audio = audio1.set_start(2)

        # Add the second track at the specified start time
        final_audio = final_audio.set_duration(audio1.duration).audio_fadeout(1).audio_fadein(1).volumex(0.9)
        overlay = audio2.set_start(0).volumex(1)

        # Combine the tracks
        combined = CompositeAudioClip([final_audio, overlay]).set_fps(44100)
        # Write the result
        combined.write_audiofile(FilePath.FINAL_AUDIO.value)

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
        with open(FilePath.IMAGE_OUTPUT.value, "wb") as file:
            for chunk in response.iter_content(1024):  # Download in chunks of 1 KB
                file.write(chunk)
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return False

    # Open the image
    img = Image.open(FilePath.IMAGE_OUTPUT.value)
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
    background.save(FilePath.IMAGE_OUTPUT.value)
    return True


def voice_generator(text):
    try:
        tts = gTTS(text=text,
                   lang="en",
                   tld="co.uk",
                   slow=False)
        tts_audio_file = FilePath.VOICE_OUTPUT.value
        tts.save(tts_audio_file)

    except Exception as e:
        print(f"An error occurred: {e}")
