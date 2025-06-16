from core.utils.texts import get_text, DEFAULT_LANGUAGE

def test_get_existing_key_en():
    text = get_text("start_message", "en")
    assert isinstance(text, str)
    assert "Choose" in text or "Welcome" in text 

def test_get_existing_key_de():
    text = get_text("start_message", "de")
    assert isinstance(text, str)
    assert text != "[missing: start_message]"

def test_fallback_to_default_language():
    text = get_text("start_message", "fr")
    assert isinstance(text, str)
    assert "missing" not in text.lower()

def test_missing_key():
    text = get_text("nonexistent_key", "en")
    assert text == "[missing: nonexistent_key]"
