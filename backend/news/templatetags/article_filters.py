from django import template
import re

register = template.Library()

@register.filter(name='split_sentences')
def split_sentences(text):
    if not text:
        return []
    # Split by periods followed by space or end of string
    sentences = re.split(r'\.(?=\s|$)', text)
    # Remove empty sentences and strip whitespace
    return [s.strip() for s in sentences if s.strip()] 