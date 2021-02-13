from lorem_text import lorem

__META__ = {
    'build': 'foo1.html',
}

TITLE = 'Spamm'

CONTENT = [item for item in lorem.paragraphs(1).split('\n') if len(item) > 4]
