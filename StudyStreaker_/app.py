import requests
import random
import html
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_category_id(topic):
    """Fetch available categories and find the matching category ID."""
    url = "https://opentdb.com/api_category.php"
    response = requests.get(url)

    if response.status_code == 200:
        categories = response.json().get("trivia_categories", [])
        for category in categories:
            if topic.lower() in category["name"].lower():
                return category["id"]  # Return category ID if found
        return None
    else:
        return None

def get_trivia_questions(topic, amount=10, difficulty="easy"):
    """Fetch trivia questions for a given topic."""
    category_id = get_category_id(topic)
    url = f"https://opentdb.com/api.php?amount={amount}&category=17&difficulty={difficulty}&type=multiple"
    if category_id:
        url += f"&category={category_id}"
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        questions = data.get("results", [])
        formatted_questions = []

        for idx, q in enumerate(questions, 1):
            question = html.unescape(q["question"])
            correct_answer = html.unescape(q["correct_answer"])
            incorrect_answers = [html.unescape(ans) for ans in q["incorrect_answers"]]
            
            options = incorrect_answers + [correct_answer]
            random.shuffle(options)

            formatted_questions.append({
                "question": question,
                "options": options,
                "correct_answer": correct_answer
            })
        return formatted_questions
    else:
        return []

@app.route('/')
def index():
    return render_template('flashcard.html')  # Serve the frontend HTML page

@app.route('/get_trivia', methods=['POST'])
def get_trivia():
    topic = request.json.get('topic')
    questions = get_trivia_questions(topic)
    return jsonify(questions)

if __name__ == '__main__':
    app.run(debug=True) 