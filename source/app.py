# app.py
from flask import Flask, request, render_template_string
from jinja2 import Undefined
import jinja2.runtime

if hasattr(jinja2.runtime.Undefined, '__init__'):
    del jinja2.runtime.Undefined.__init__

app = Flask(__name__)

REAL_FLAG = open('flag.txt').read()

def caesar_shift(text, shift):
    result = []
    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        elif char.islower():
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(char)
    return ''.join(result)

@app.route('/', methods=['GET', 'POST'])
def translator():
    english_text = ""
    alien_text = ""
    message = ""

    if request.method == 'POST':
        english_input = request.form.get('english', '').strip()
        alien_input = request.form.get('alien', '').strip()
        action = request.form.get('action', '')

        active_input = ""
        direction = ""
        blacklist_keywords = [
            'lipsum', 'get_flashed_messages', 'cycler', 
        ]
        if action == 'to_alien' and english_input:
            active_input = english_input
            direction = 'to_alien'
        elif action == 'to_english' and alien_input:
            active_input = alien_input
            direction = 'to_english'

        if active_input:
            if any(keyword in active_input.lower() for keyword in blacklist_keywords):
                message = (
                    '<div style="background:#fee2e2; padding:15px; border-radius:8px; margin-top:20px; color:#991b1b;">'
                    'Transmission rejected — forbidden galactic dialect detected.<br>'
                    '<small>Try a different approach, Earthling.</small>'
                    '</div>'
                )
            else:
                try:
                    rendered = render_template_string(active_input)

                    if direction == 'to_alien':
                        translated = caesar_shift(rendered, 12)
                        alien_text = translated
                        english_text = english_input
                    else:  # to_english
                        translated = caesar_shift(rendered, -12)
                        english_text = translated
                        alien_text = alien_input

                    if english_text.strip() == REAL_FLAG:
                        message = (
                            '<div style="background:#d4edda; padding:15px; border-radius:8px; margin-top:20px; color:#155724;">'
                            '<strong>DECODED ALIEN TRANSMISSION!</strong><br>'
                            'Earth has intercepted and understood the message.'
                            '</div>'
                        )

                except Exception as e:
                    error_msg = str(e).replace('<', '&lt;').replace('>', '&gt;')
                    message = (
                        f'<div style="background:#fee2e2; padding:15px; border-radius:8px; margin-top:20px; color:#991b1b;">'
                        f'Translator malfunction: {error_msg}<br>'
                        f'<small>Input was: <code>{active_input}</code></small>'
                        '</div>'
                    )

    page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Venusian Translator</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                max-width: 1100px;
                margin: 40px auto;
                padding: 20px;
                background: #0d1117;
                color: #c9d1d9;
            }}
            h1 {{
                text-align: center;
                color: #58a6ff;
            }}
            .container {{
                background: #161b22;
                padding: 30px;
                border-radius: 12px;
                border: 1px solid #30363d;
            }}
            .split {{
                display: flex;
                gap: 30px;
                margin: 30px 0;
            }}
            .box {{
                flex: 1;
            }}
            .box h3 {{
                margin: 0 0 10px 0;
                color: #8b949e;
            }}
            textarea {{
                width: 100%;
                height: 180px;
                padding: 12px;
                font-family: 'Courier New', monospace;
                font-size: 15px;
                background: #0d1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 6px;
                resize: vertical;
            }}
            .buttons {{
                text-align: center;
                margin: 20px 0;
            }}
            button {{
                background: #238636;
                color: white;
                border: none;
                padding: 12px 32px;
                font-size: 16px;
                border-radius: 6px;
                cursor: pointer;
                margin: 0 15px 10px 50px;
            }}
            button:hover {{
                background: #2ea043;
            }}
            .result-message {{
                margin-top: 20px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Venusian ↔ English Translator</h1>
            <p style="text-align:center; color:#8b949e;">
                Communicate with the invaders... or decode their secrets.
            </p>

            <form method="POST">
                <div class="split">
                    <div class="box">
                        <h3>English</h3>
                        <textarea name="english" placeholder="Type or paste English here...">{english_text}</textarea>
                    </div>
                    <div class="box">
                        <h3>Venusian</h3>
                        <textarea name="alien" placeholder="Type or paste Venusian text here...">{alien_text}</textarea>
                    </div>
                </div>

                <div class="buttons">
                    <button type="submit" name="action" value="to_alien">Translate to Venusian →</button>
                    <button type="submit" name="action" value="to_english">← Translate to English</button>
                </div>
            </form>

            <div class="result-message">
                {message}
            </div>
        </div>
    </body>
    </html>
    """

    return page

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(host='0.0.0.0', port=8000, debug=False)