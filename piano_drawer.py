from PIL import Image, ImageDraw, ImageFont

# Размеры клавиш (подобраны под одну октаву)
WHITE_KEY_W = 40
WHITE_KEY_H = 130
BLACK_KEY_W = 26
BLACK_KEY_H = 80

WHITE_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
WHITE_SEMITONES = [0, 2, 4, 5, 7, 9, 11]

# Позиции чёрных клавиш (полутон -> индекс белой клавиши, смещение)
BLACK_POSITIONS = {
    1: (0, 0.65),   # C# / Db
    3: (1, 0.65),   # D# / Eb
    6: (3, 0.65),   # F# / Gb
    8: (4, 0.65),   # G# / Ab
    10: (5, 0.65)   # A# / Bb
}

def draw_piano(start_octave=3, num_octaves=1, pressed_notes=None):
    """
    Рисует одну октаву клавиатуры (по умолчанию 3-я).
    pressed_notes: список названий нот (например ['C','E','G']), 
                   могут быть с диезами или бемолями (бемоль преобразуется).
    """
    if pressed_notes is None:
        pressed_notes = []

    # Нормализация бемолей -> диезы
    def normalize(n):
        return {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#'}.get(n, n)
    pressed = [normalize(n) for n in pressed_notes]

    total_white_keys = num_octaves * 7  # 7
    width = total_white_keys * WHITE_KEY_W
    height = WHITE_KEY_H
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # 1. Рисуем белые клавиши
    white_rects = []
    for octave in range(start_octave, start_octave + num_octaves):
        for wi, note in enumerate(WHITE_NOTES):
            x = (octave - start_octave) * 7 * WHITE_KEY_W + wi * WHITE_KEY_W
            rect = (x, 0, x + WHITE_KEY_W, WHITE_KEY_H)
            fill = (255, 255, 200) if note in pressed else (255, 255, 255)
            draw.rectangle(rect, fill=fill, outline='#888')
            white_rects.append((rect, note, octave))

    # 2. Рисуем чёрные клавиши
    for octave in range(start_octave, start_octave + num_octaves):
        for semi, (white_index, offset_ratio) in BLACK_POSITIONS.items():
            note_name = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][semi]
            white_x = (octave - start_octave) * 7 * WHITE_KEY_W + white_index * WHITE_KEY_W
            black_x = white_x + WHITE_KEY_W * offset_ratio - BLACK_KEY_W // 2
            rect = (black_x, 0, black_x + BLACK_KEY_W, BLACK_KEY_H)
            fill = (255, 240, 150) if note_name in pressed else (20, 20, 20)
            draw.rectangle(rect, fill=fill, outline='#444')

    # 3. Подписи нот (только на белых клавишах)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()
    for rect, note, octave in white_rects:
        x_center = (rect[0] + rect[2]) // 2
        y_text = rect[3] - 22
        draw.text((x_center - 8, y_text), f"{note}{octave}", fill='#222', font=font)

    return img