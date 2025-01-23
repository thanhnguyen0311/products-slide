import math

import numpy
import numpy as np
from PIL import Image


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


def swipe_in_effect(clip, direction="left"):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size  # Original size of the frame
        width, height = base_size

        # Progress of the swipe (0.0 to 1.0)
        progress = t / clip.duration
        if progress > 1.0:
            progress = 1.0

        # Create a blank (white) canvas
        canvas = Image.new("RGB", base_size, "white")

        # Calculate the visible area based on the progress
        if direction == "left":
            visible_width = math.ceil(width * progress)
            box = (width - visible_width, 0, width, height)
        elif direction == "right":
            visible_width = math.ceil(width * progress)
            box = (0, 0, visible_width, height)
        elif direction == "up":
            visible_height = math.ceil(height * progress)
            box = (0, height - visible_height, width, height)
        elif direction == "down":
            visible_height = math.ceil(height * progress)
            box = (0, 0, width, visible_height)
        else:
            raise ValueError("Invalid direction. Choose from 'left', 'right', 'up', or 'down'.")

        # Crop and paste the visible portion of the image onto the canvas
        visible_part = img.crop(box)
        paste_position = box[:2]
        canvas.paste(visible_part, paste_position)

        result = np.array(canvas)
        img.close()

        return result

    return clip.fl(effect)