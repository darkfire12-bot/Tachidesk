import cv2
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from translate import Translator
import argparse

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

    # Apply inpainting
    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    # Convert to PIL Image
    img_pil = Image.fromarray(dst)
    draw = ImageDraw.Draw(img_pil)

    # Set font
    font = ImageFont.truetype('manga_translator/NotoSansJP-Regular.ttf', 20)

    # Translate and render text
    translator= Translator(to_lang="en", from_lang="ja")
    for i in range(n_boxes):
        if int(data['conf'][i]) > 60:
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            text = data['text'][i]
            if text.strip():
                translated_text = translator.translate(text)
                draw.text((x, y), translated_text, font=font, fill=(0, 0, 0))

    # Save the result
    img_pil.save('manga_translator/translated_final.jpg')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate manga images.')
    parser.add_argument('image_path', type=str, help='Path to the manga image.')
    args = parser.parse_args()
    translate_manga(args.image_path)
