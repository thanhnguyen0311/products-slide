from moviepy.editor import ImageClip, concatenate_videoclips


def create_slide(product):
    image_files = product.images

    # Create a list of image clips
    clips = [ImageClip(img).set_duration(3) for img in image_files]  # Each image lasts 3 seconds

    # Concatenate all image clips into a single video
    video = concatenate_videoclips(clips, method="compose")

    # Export to MP4
    video.write_videofile(f"{product.sku}.mp4", fps=24)

# Background music
# from moviepy.editor import VideoFileClip, AudioFileClip
#
# # Load a video and an audio file
# video = VideoFileClip("slideshow.mp4")
# audio = AudioFileClip("background_music.mp3").set_duration(video.duration)
#
# # Add audio to the video
# video = video.set_audio(audio)
#
# # Export to MP4
# video.write_videofile("slideshow_with_music.mp4", fps=24)


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
