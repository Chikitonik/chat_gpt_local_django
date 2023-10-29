from django import template

register = template.Library()


@register.filter
def read_file(file_path, encoding='utf-8', num_rows=5):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            lines = file.readlines()
            return ''.join(lines[:num_rows])
    except Exception as e:
        return f"File not found or an error occurred: {str(e)}"
