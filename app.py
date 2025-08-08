import os
import re
from flask import Flask, render_template, request
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBobob3QNfQntqTuZspp5fNfJi5-KefKNU")
client = genai.Client(api_key=API_KEY)

# --- Markdown "cleaner" and formatter ---
def markdown_to_html(text):
    if not text:
        return ""
    text = text.replace("@", "")
    text = re.sub(r'``````', '', text, flags=re.DOTALL)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'^###\s*(.+)$', r'<div class="ai-heading">\1</div>', text, flags=re.MULTILINE)
    text = re.sub(r'^##\s*(.+)$', r'<div class="ai-heading">\1</div>', text, flags=re.MULTILINE)
    text = re.sub(r'^#\s*(.+)$', r'<div class="ai-heading">\1</div>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)

    def list_replacer(match):
        items = [f"<li>{item.strip()[1:].strip()}</li>" for item in match.group(0).strip().split('\n')]
        return "<ul>" + "".join(items) + "</ul>"

    text = re.sub(r'(^(\*|\-)\s.+(\n(\*|\-)\s.+)*)', list_replacer, text, flags=re.MULTILINE)

    def numlist_replacer(match):
        items = [f"<li>{re.sub(r'^\d+\.\s*', '', item.strip())}</li>" for item in match.group(0).strip().split('\n')]
        return "<ol>" + "".join(items) + "</ol>"

    text = re.sub(r'(^\d+\..+(\n\d+\..+)*)', numlist_replacer, text, flags=re.MULTILINE)
    text = re.sub(r'^\-\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'(\n\s*){2,}', '\n', text)
    text = text.replace('\n', '<br>')
    text = text.replace('_', '')
    return text.strip()

def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return response.text

def get_diet_plan(age, gender, weight, height):
    prompt = (
        f"Suggest a personalized, healthy one-day diet plan for a {age}-year-old {gender}, "
        f"weighing {weight} kg, height {height} cm. Include meals, calorie estimate, "
        f"macronutrient ratios, and hydration advice in markdown with headings and bullet points."
    )
    return ask_gemini(prompt)

def get_health_advice(symptom_or_goal):
    prompt = (
        f"You are an AI healthcare coach. Provide safe, evidence-based advice for: {symptom_or_goal}."
        "Format key points as bullet points and section headings. Use markdown; avoid diagnosis/prescription."
    )
    return ask_gemini(prompt)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    diet_plan = ""
    health_advice = ""
    if request.method == "POST":
        age = request.form.get("age")
        gender = request.form.get("gender")
        weight = request.form.get("weight")
        height = request.form.get("height")
        symptom = request.form.get("symptom", "").strip()
        plan_raw = get_diet_plan(age, gender, weight, height)
        diet_plan = markdown_to_html(plan_raw)
        if symptom:
            advice_raw = get_health_advice(symptom)
            health_advice = markdown_to_html(advice_raw)
    return render_template("index.html", diet_plan=diet_plan, health_advice=health_advice)

if __name__ == "__main__":
    app.run(debug=True)
