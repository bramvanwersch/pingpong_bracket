from io import BytesIO

from PIL import Image

ALLOWED_IMAGE_FORMATS = {"jpg", "png", "gif", "webp", "svg"}
MAX_HEIGHT = 200


def verify_image(file):
    if file.size > 2 * 1024 * 1024:
        raise RuntimeError("Max image size is 2MB")
    try:
        extension = file.name.rsplit(".", 1)[1]
    except IndexError:
        raise RuntimeError("Unsupported image format")
    if extension not in ALLOWED_IMAGE_FORMATS:
        raise RuntimeError("Unsupported image format")
    img = Image.open(file.file)
    width, height = img.size
    if height < MAX_HEIGHT:
        return
    new_height = MAX_HEIGHT
    new_width = int((new_height / float(height)) * width)
    if extension in {"gif", "webp"}:
        scale_gif(img, (new_width, new_height), file)
    else:
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        if isinstance(file.file, BytesIO):
            buffer = BytesIO()
            img.save(buffer, file.content_type.replace("image/", ""))
            file.file = buffer
        else:
            img.save(file.file.name)


def scale_gif(img, scale, file):
    old_gif_information = {
        "loop": bool(img.info.get("loop", 1)),
        "duration": img.info.get("duration", 40),
        "background": img.info.get("background", 223),
        "transparency": img.info.get("transparency", 223),
    }
    new_frames = get_new_frames(img, scale)
    save_new_gif(new_frames, old_gif_information, file)


def get_new_frames(gif, scale):
    new_frames = []
    actual_frames = gif.n_frames
    for frame in range(actual_frames):
        gif.seek(frame)
        new_frame = Image.new("RGBA", gif.size)
        new_frame.paste(gif)
        new_frame.thumbnail(scale, Image.Resampling.LANCZOS)
        new_frames.append(new_frame)
    return new_frames


def save_new_gif(new_frames, old_gif_information, file):
    if isinstance(file.file, BytesIO):
        buffer = BytesIO()
        new_frames[0].save(
            buffer,
            format=file.content_type.replace("image/", ""),
            save_all=True,
            append_images=new_frames[1:],
            duration=old_gif_information["duration"],
            loop=old_gif_information["loop"],
            background=old_gif_information["background"],
            transparency=old_gif_information["transparency"],
        )
        file.file = buffer
    else:
        new_frames[0].save(
            file.file.name,
            save_all=True,
            append_images=new_frames[1:],
            duration=old_gif_information["duration"],
            loop=old_gif_information["loop"],
            background=old_gif_information["background"],
            transparency=old_gif_information["transparency"],
        )
