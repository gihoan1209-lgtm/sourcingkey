from deep_translator import GoogleTranslator

def translate_to_ko(text: str) -> str:
    """
    Translates text to Korean using deep-translator (auto-detects source language).
    """
    if not text or len(text.strip()) == 0:
        return text
    try:
        translated = GoogleTranslator(source='auto', target='ko').translate(text)
        return translated
    except Exception as e:
        print(f"Translation Error: {e}")
        return text

