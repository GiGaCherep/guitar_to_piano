from flask import Flask, render_template, request
import re
import base64
from io import BytesIO
from piano_drawer import draw_piano

app = Flask(__name__)

NOTE_TO_SEMITONE = {
    'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,
    'F#':6,'Gb':6,'G':7,'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11
}
SEMITONE_TO_NOTE = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def normalize_note_name(note):
    mapping = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#'}
    return mapping.get(note, note)

def parse_chord(chord_str):
    chord_str = chord_str.strip().lower()
    match = re.match(r'^([a-g](?:b|#)?)(.*)$', chord_str)
    if not match:
        return None, None, None
    root_raw = match.group(1).upper()
    rest = match.group(2).lower()
    root = normalize_note_name(root_raw)
    chord_type = 'maj'
    if rest.startswith('maj7'): chord_type='maj7'
    elif rest.startswith('m7'): chord_type='m7'
    elif rest.startswith('m'): chord_type='min'
    elif rest.startswith('7'): chord_type='7'
    elif rest.startswith('6'): chord_type='6'
    elif rest.startswith('sus2'): chord_type='sus2'
    elif rest.startswith('sus4'): chord_type='sus4'
    elif rest.startswith('dim'): chord_type='dim'
    elif rest.startswith('aug'): chord_type='aug'
    return root, chord_type, None

def get_chord_notes(root, chord_type):
    intervals = {
        'maj':[0,4,7], 'min':[0,3,7], '7':[0,4,7,10],
        'maj7':[0,4,7,11], 'm7':[0,3,7,10], '6':[0,4,7,9],
        'sus2':[0,2,7], 'sus4':[0,5,7], 'dim':[0,3,6], 'aug':[0,4,8]
    }
    if chord_type not in intervals:
        chord_type = 'maj'
    root_semi = NOTE_TO_SEMITONE.get(root, 0)
    notes = []
    for interval in intervals[chord_type]:
        semi = (root_semi + interval) % 12
        notes.append(SEMITONE_TO_NOTE[semi])
    unique = []
    for n in notes:
        if n not in unique:
            unique.append(n)
    return unique

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    chord_notes = []
    img_data = None
    if request.method == 'POST':
        chord_input = request.form.get('chord_input', '').strip()
        if chord_input:
            chord_str = chord_input
        else:
            note = request.form.get('note', 'C')
            acc = request.form.get('accidental', '')
            ctype = request.form.get('chord_type', 'maj')
            ext = request.form.get('extension', '')
            chord_str = note + ('b' if acc=='b' else '#' if acc=='#' else '')
            if ctype == 'maj':
                chord_str += ext
            elif ctype == 'min':
                chord_str += 'm' + ext
            elif ctype == '7':
                chord_str += '7'
            else:
                chord_str += ctype + ext
        root, ctype, _ = parse_chord(chord_str)
        if root is None:
            error = f"Не удалось распознать аккорд '{chord_str}'"
        else:
            chord_notes = get_chord_notes(root, ctype)
            if chord_notes:
                img = draw_piano(start_octave=3, num_octaves=1, pressed_notes=chord_notes)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                img_data = f"data:image/png;base64,{img_base64}"
            else:
                error = f"Не удалось построить ноты для {root} {ctype}"
    return render_template('index.html', error=error, chord_notes=chord_notes, img_data=img_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)