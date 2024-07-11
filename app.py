from flask import Flask, render_template_string, request
import speech_recognition as sr
from deep_translator import GoogleTranslator

app = Flask(__name__)

recognizer = sr.Recognizer()
recognized_text = ""
translated_text = ""
target_language = "es"  # Default target language (Spanish)

# Dictionary to map language codes to language names
LANGUAGES = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian', 'az': 'Azerbaijani',
    'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
    'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)',
    'co': 'Corsican', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
    'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'fy': 'Frisian',
    'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole',
    'ha': 'Hausa', 'haw': 'Hawaiian', 'he': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian',
    'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese',
    'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer', 'ko': 'Korean', 'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish',
    'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori',
    'mr': 'Marathi', 'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian',
    'or': 'Odia (Oriya)', 'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi',
    'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic', 'sr': 'Serbian', 'st': 'Sesotho',
    'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish',
    'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai',
    'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'ug': 'Uyghur', 'uz': 'Uzbek', 'vi': 'Vietnamese', 'cy': 'Welsh',
    'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    global recognized_text, translated_text, target_language
    if request.method == 'POST':
        if 'speak' in request.form:
            try:
                with sr.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)
                    recognized_text = recognizer.recognize_google(audio).lower()
                    translated_text = GoogleTranslator(source='auto', target=target_language).translate(recognized_text)
            except sr.UnknownValueError:
                recognized_text = "Could not understand audio"
                translated_text = ""
        elif 'language' in request.form:
            target_language = request.form['language']
    
    return render_template_string('''
        <!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Speech Recognition and Translation</title>
    <style>
      body {
        background-image: linear-gradient(to left, #0000FF, #0099cc);
        color: white;
      }
      button {
        background-image: linear-gradient(to right, #FF7F50, #FF4500);
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition: background-image 0.5s ease-in-out;
      }
      button:hover {
        background-image: linear-gradient(to right, #FF4500, #FF7F50);
      }
      select {
        background-image: linear-gradient(to right, #32CD32, #008000);
        border: none;
        color: white;
        padding: 10px;
        font-size: 16px;
        border-radius: 12px;
        transition: background-image 0.5s ease-in-out;
      }
      select:hover {
        background-image: linear-gradient(to right, #008000, #32CD32);
      }
      option {
        background-color: #008000;
        color: white;
      }
    </style>
  </head>
  <body>
    <center>
      <h1>Speech Recognition and Translation</h1>
      <form method="post">
        <button name="speak" type="submit">Speak</button><br><br><br>Translate To
        <select name="language" onchange="this.form.submit()">
          {% for lang_code, lang_name in languages.items() %}
            <option value="{{ lang_code }}" {% if lang_code == target_language %}selected{% endif %}>
              {{ lang_name }}
            </option>
          {% endfor %}
        </select>
      </form>
      <p>Your Speech: {{ recognized_text }}</p>
      <p>Translated Text: {{ translated_text }}</p>
    </center>
  </body>
</html>

    ''', recognized_text=recognized_text, translated_text=translated_text, languages=LANGUAGES, target_language=target_language)

if __name__ == '__main__':
    app.run(debug=True)
