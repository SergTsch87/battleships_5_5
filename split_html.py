import json
import os
import re
import glob

#  Є кілька json-ф-лів, які містять діалоги.
# Вони мають однакову структуру, але різну кількість діалогів.
# Потрібно підставити ці json-ф-ли до шаблону html-файлу,
# який містить структуру сторінки та скрипт для відображення діалогів, - і т.ч.
# створити нові html-ф-ли для кожного json-ф-лу.  

# Додати '.json' до усіх файлів папки:
# for f in *; do mv "$f" "$f.json"; done

# var jsonData = []
# chat_min.html

CHAT_HTML = "../_chtgpt/chat.html"
CHAT_TEMPL_HTML = "./_chat/chat_min.html"
OUT_CHAT_FLDR = "../_chtgpt/htmls/"
JSON_FLDR = "../_chtgpt/jsons/"


def gen_html_from_json(json_file, template_file, output_file):
    with open(template_file, 'r', encoding='utf-8') as tmpl_html, \
         open(json_file, 'r', encoding='utf-8') as jsn_fl, \
         open(output_file, 'w', encoding='utf-8') as out_html:
            content = tmpl_html.read()
            
            try:
                json_data = json.load(jsn_fl)
            except json.JSONDecodeError as e:
                print(f"Помилка при десеріалізації JSON: {e}")
                print("Position:", e.pos)
                print("Around error:", repr(jsn_fl.read()[e.pos-10:e.pos+10]))
                return
            
            json_str = json.dumps(json_data, ensure_ascii=False)
            new_content = content.replace('var jsonData = []', f'var jsonData = [{json_str}]')
            out_html.write(new_content)


def split_chat_html(input_file, chunk_size=500):
    """
    input_file: шлях до вашого chat.html
    chunk_size: кількість діалогів у кожному новому файлі
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Створюємо шаблон: замінюємо JSON на порожній масив
    # Знаходимо рядок var jsonData = [...]
    json_match = re.search(r'var jsonData = (\[.*?\]);', content, re.DOTALL)

    if not json_match:
        raise ValueError("JSON data not found in the expected format")
    
    full_json_str = json_match.group(1)  # це [ ... ]
    template = content.replace(full_json_str, '[]')

    # 2. Десеріалізація повного JSON
    try:
        json_data = json.loads(full_json_str)
    except json.JSONDecodeError as e:
        print(f"Помилка при десеріалізації JSON: {e}")
        print("Position:", e.pos)
        print("Around error:", repr(full_json_str[e.pos-10:e.pos+10]))
        return
    
    # 3. Розбиття на чанки та запис файлів
    total_items = len(json_data)
    part_files = []
    for i in range(0, total_items, chunk_size):
        chunk = json_data[i : i + chunk_size]
        part_num = i // chunk_size + 1
        output_dir = os.path.dirname(input_file)
        output_filename = os.path.join(output_dir, f"chat_part_{part_num:03d}.html")
        
        # Формуємо вміст нового файлу: вставляємо chunk у шаблон
        chunk_json = json.dumps(chunk, ensure_ascii=False)
        new_content = template.replace('[]', chunk_json)
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Створено: {output_filename} ({len(chunk)} записів)")
        part_files.append(f"chat_part_{part_num:03d}.html")

    # 4. Створення index.html для навігації
    index_content = """<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Навігація по частинах чату</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 10px 0; }
        a { text-decoration: none; color: #007BFF; font-size: 18px; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Частини чату</h1>
    <ul>
"""
    for part_file in part_files:
        index_content += f'        <li><a href="{part_file}">{part_file}</a></li>\n'
    index_content += """    </ul>
</body>
</html>"""

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"Створено index файл: {index_path}")


def main():
    json_files = glob.glob(os.path.join(JSON_FLDR, '*.json'))
    for json_file in json_files:
        gen_html_from_json(json_file, CHAT_TEMPL_HTML, OUT_CHAT_FLDR + os.path.basename(json_file).replace('.json', '.html'))

    # split_chat_html('../_chtgpt/chat.html', chunk_size=100) # налаштуйте розмір чанка тут


if __name__ == "__main__":
    main()