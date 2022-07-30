from transformers import BartTokenizer, TFBartForConditionalGeneration

def generate_summary(sample_text) -> str:
    model = TFBartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

    inputs = tokenizer([sample_text], max_length=1024, return_tensors="tf", truncation=True)
    summary_ids = model.generate(inputs["input_ids"], num_beams=3)
    summary_text = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return summary_text