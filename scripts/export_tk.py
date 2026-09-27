"""Create a complete TK export without changing article content or mathematics."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = str.maketrans({
    '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
    '\u2013': '-', '\u2014': '--', '\u00a0': ' ', '\u202f': ' ',
})


def normalize(text):
    text = text.translate(TRANSLATION)
    # Normalize emphasis delimiters without touching word-internal underscores
    # in mathematical subscripts, filenames, or URLs.
    return re.sub(r'(?<![\w\\])_([^\n]+?)_(?!\w)', r'*\1*', text)


if __name__ == '__main__':
    text = (ROOT / 'article.md').read_text(encoding='utf-8')
    (ROOT / 'article_tk.md').write_text(normalize(text), encoding='utf-8')
    print('Wrote complete article_tk.md')
