# 🎸 Guitar to Piano Chord Converter

Веб-приложение для преобразования гитарных аккордов в фортепианные с визуализацией клавиш. Также умеет парсить аккорды с amdm.ru и показывать их на клавиатуре.

## Быстрый старт

### Локально (Python)

```bash
git clone <your-repo-url>
cd guitar_to_piano
pip install -r requirements.txt
python app.py

Через Docker
bash
docker build -t guitar-piano .
docker run -p 5000:5000 guitar-piano

Или с docker-compose:
bash
docker-compose up -d

Использование
Введите аккорд (например, Cmaj7) – получите ноты и картинку клавиатуры.

Вставьте URL песни с amdm.ru – получите таблицу всех уникальных аккордов с картинками клавиатур.

Структура
app.py – основной сервер

piano_drawer.py – генерация изображений клавиатуры

templates/ – HTML-шаблоны

static/ – CSS

Зависимости
Список в requirements.txt

text

## 5. `setup.py` (опционально, если хотите сделать пакет)

Для больших проектов можно добавить, но для вашего приложения достаточно `requirements.txt`.

## 6. Убедитесь, что в проекте нет лишних файлов

Перед коммитом проверьте, что не добавляете:
- `__pycache__`
- `*.pyc`
- виртуальное окружение `venv/`

## Итог

После добавления этих файлов любой разработчик (или вы сами на Debian) сможет развернуть проект одной командой:

```bash
git clone ...
cd project
pip install -r requirements.txt
python app.py
А если используете Docker – ещё проще.