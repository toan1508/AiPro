from flask import Flask, render_template, request, jsonify, url_for
import datetime
import os
from gtts import gTTS
import wikipedia

app = Flask(__name__)

language = "en"
wikipedia.set_lang(language)

def set_language(lang):
    global language
    language = lang
    wikipedia.set_lang(lang)
    return "Đã chuyển sang tiếng Việt." if lang == "vi" else "Language set to English."

def speak(text):
    tts = gTTS(text=text, lang=language)
    filename = "static/output.mp3"
    tts.save(filename)
    return filename

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return ("Theo Wikipedia..." if language == "vi" else "According to Wikipedia...") + " " + result
    except:
        return "Không tìm thấy thông tin." if language == "vi" else "Nothing found."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("query")
    global language

    if user_input.lower() == "switch to vie":
        msg = set_language("vi")
    elif user_input.lower() == "switch to en":
        msg = set_language("en")
    elif user_input.lower().startswith("wiki"):
        query = user_input[5:]
        msg = search_wikipedia(query)
    elif "time" in user_input.lower() or "giờ" in user_input.lower():
        now = datetime.datetime.now().strftime("%I:%M %p")
        msg = now
    else:
        msg = "Tôi chưa hiểu. Hãy thử lại." if language == "vi" else "I didn't understand. Please try again."

    audio_path = speak(msg)
        return jsonify({"text": msg, "audio": url_for('static', filename='output.mp3')})

if __name__ == "__main__":
    app.run(debug=True)
