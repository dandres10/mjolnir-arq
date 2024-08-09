

def snake_to_pascal(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)

def convert_to_kebab_case(snake_str):
    return snake_str.replace('_', '-')