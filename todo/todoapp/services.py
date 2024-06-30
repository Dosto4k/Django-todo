def translate_title_to_slug(string):
    """Переводит строку string в Slug"""
    template = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh',
        'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r',
        'ю': 'yu', 'я': 'ya'
    }
    return ''.join(map(lambda x: template[x] if template.get(x, False) else x, string.lower()))
