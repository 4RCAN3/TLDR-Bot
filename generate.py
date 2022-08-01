from transformers import T5Tokenizer, TFT5ForConditionalGeneration

from PIL import Image, ImageDraw, ImageFont
from string import ascii_letters
import textwrap

def generate_summary_t5(sample_text) -> str:
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    model = TFT5ForConditionalGeneration.from_pretrained("t5-small")

    inputs = tokenizer("summarize: " + sample_text, return_tensors="tf", truncation = True).input_ids  # Batch size 1
    outputs = model.generate(inputs, min_length = 0, max_length = 254)
    
    summary_text = tokenizer.decode(outputs[0], skip_special_tokens = True)
    return summary_text

def write_to_image(summary):
    img = Image.open('assets/background.jpg')
    im = ImageDraw.Draw(img)
    font = ImageFont.truetype(font='arial.ttf', size=30)

    avg_char_width = sum(font.getbbox(char)[-2] for char in ascii_letters) / len(ascii_letters)
    max_char_count = int(img.size[0] * .618 / avg_char_width)
    text = textwrap.fill(text=summary, width=max_char_count)
    im.text(xy=(img.size[0]/2, img.size[1] / 2), text=text, font=font, fill='#ffffff', anchor='mm')

    img.save("assets/summary_image.jpg")