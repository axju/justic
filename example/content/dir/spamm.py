from lorem_text import lorem

TITLE = 'Spamm'

CONTENT = [item for item in lorem.paragraphs(1).split('\n') if len(item) > 4]
