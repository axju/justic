from lorem_text import lorem

template = 'index.html'

title = 'Lorem Example'

content_list = [item for item in lorem.paragraphs(200).split('\n') if len(item) > 4]
