import os
import uuid
from werkzeug.utils import secure_filename
from PIL import ImageDraw,Image,ImageFont

def allowed_file(filename, allowed_extensions):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in allowed_extensions
    )

def watermark(img, text="KAILANG"):
    img = img.convert("RGBA")

    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    font = ImageFont.truetype("arial.ttf", 72)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = img.width - text_width - 20
    y = img.height - text_height - 20

    shadow_offset = 3

    # Draw shadow
    draw.text(
        (x + shadow_offset, y + shadow_offset),
        text,
        fill=(0, 0, 0, 150),
        font=font
    )

    draw.text(
        (x, y),
        text,
        fill=(255, 0, 0, 255),
        font=font
    )

    return Image.alpha_composite(img,layer).convert("RGBA")

def save_image(
        file,
        upload_folder,
        allowed_extensions,
        resize_to=(800, 800),
        thumb_size=(100, 100)
):
    if not file or file.filename == '':
        return 'no file'

    if not allowed_file(file.filename, allowed_extensions):
        return 'invalid file'

    _, ext = os.path.splitext(file.filename)
    uuid_filename = f"{uuid.uuid4().hex}{ext}"
    name = secure_filename(uuid_filename)

    original_path = os.path.join(upload_folder, name)
    resized_path = os.path.join(upload_folder, f"resized_{name}")
    thumb_path = os.path.join(upload_folder, f"thumb_{name}")

    image = Image.open(file.stream)
    image = watermark(image)
    image.save(original_path,"PNG")

    resized = image.copy()
    resized.thumbnail(resize_to)
    resized.save(resized_path,"PNG")

    thumb = image.copy()
    thumb.thumbnail(thumb_size)
    thumb.save(thumb_path,"PNG")

    return {
        "original": name,
        "resized": f"resized_{name}",
        "thumbnail": f"thumb_{name}"
    }

