# Manga Translator

This script translates the text in manga images from Japanese to English.

## Installation

1.  **Install Tesseract OCR:**

    *   **Ubuntu/Debian:**
        ```bash
        sudo apt-get update
        sudo apt-get install tesseract-ocr tesseract-ocr-jpn
        ```
    *   **macOS:**
        ```bash
        brew install tesseract tesseract-lang
        ```
    *   **Windows:**
        Download and install Tesseract from the [official website](https://github.com/UB-Mannheim/tesseract/wiki). Make sure to include the Japanese language pack during installation.

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

```bash
python translate_manga.py /path/to/your/manga_image.jpg
```

The translated image will be saved as `translated_final.jpg` in the `manga_translator` directory.
