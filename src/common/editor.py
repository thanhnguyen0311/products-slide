import moviepy.editor as mp
from moviepy.editor import AudioFileClip
import math
from PIL import Image
import numpy
from gtts import gTTS


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


def create_slide(product):
    image_files = product.images
    size = (1600, 1600)
    slides = []
    for n, url in enumerate(image_files):
        slides.append(
            mp.ImageClip(url).set_fps(24).set_duration(4).resize(size)
        )

        slides[n] = zoom_in_effect(slides[n], 0.04)

    video = mp.concatenate_videoclips(slides)

    # Background music

    try:
        tts = gTTS(text="The 3-piece modern dining table set effortlessly merges style, functionality, and comfort to "
                        "enhance The overall ambiance of your dining area. It comprises a conveniently designed round "
                        "wooden table with a pedestal base and is accompanied by 2 finely crafted parson dining room "
                        "chairs, elevating your dining experience. This design harmoniously combines traditional and "
                        "contemporary elements, showcasing a Linen White tabletop that beautifully matches its Linen "
                        "White wooden legs. Crafted from premium rubberwood, The dining chairs feature Willow Green "
                        "faux Leather upholstery, accentuated by coordinating Linen White wooden legs, "
                        "ensuring exceptional durability even with daily use. Moreover, These kitchen chairs offer "
                        "The added advantage of easy-to-maintain faux Leather seats and stylish chair backs, "
                        "making Them an excellent choice for households with families. Assembling and caring for "
                        "These pieces is a straightforward process, and regular cleaning will help maintain Their "
                        "pristine appearance. In summary, This dining room set consistently creates a welcoming and "
                        "modern atmosphere, making it a remarkable addition to your dining space.", lang="en",
                   slow=False)
        tts_audio_file = "output.mp3"
        tts.save(tts_audio_file)

        audio_clip = mp.AudioFileClip(tts_audio_file)

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
