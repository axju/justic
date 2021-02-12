from lorem_text import lorem

META = {
    'template': 'index.html'
}

TITLE = 'Lorem Example'

CONTENT = [item for item in lorem.paragraphs(200).split('\n') if len(item) > 4]
