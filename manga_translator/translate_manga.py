import cv2
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from translate import Translator
import argparse

def wrap_text(text, font, max_width):
    lines = []
    if font.getbbox(text)[2] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and font.getbbox(line + words[i])[2] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines

def translate_manga(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Get bounding box data
    data = pytesseract.image_to_data(thresh, lang='jpn', output_type=pytesseract.Output.DICT)

    # Create a mask for inpainting
    mask = np.zeros(img.shape[:2], dtype="uint8")

    n_boxes = len(data['level'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 60:
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)

    # Dilate the mask
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.dilate(mask, kernel, iterations = 1)

    # Apply inpainting with the Navier-Stokes algorithm
    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)

    # Convert to PIL Image
    img_pil = Image.fromarray(dst)
    draw = ImageDraw.Draw(img_pil)

    # Set font
    font_path = 'manga_translator/NotoSansJP-Regular.ttf'

    # Translate and render text
    translator= Translator(to_lang="en", from_lang="ja")
    for i in range(n_boxes):
        if int(data['conf'][i]) > 60:
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            text = data['text'][i]
            if text.strip():
                translated_text = translator.translate(text)

                # Dynamically adjust font size
                font_size = int(h * 0.8)
                font = ImageFont.truetype(font_path, font_size)

                # Wrap text
                wrapped_text = wrap_text(translated_text, font, w)

                # Render wrapped text
                for j, line in enumerate(wrapped_text):
                    draw.text((x, y + (j * font_size)), line, font=font, fill=(0, 0, 0))

    # Save the result
    img_pil.save('manga_translator/translated_final.jpg')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate manga images.')
    parser.add_argument('image_path', type=str, help='Path to the manga image.')
    args = parser.parse_args()
    translate_manga(args.image_path)
