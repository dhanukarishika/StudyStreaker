from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to StudyStreaker API!"})

# Load models
generator = pipeline("text-generation", model="bigscience/bloom-560m")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
question_generator = pipeline("text2text-generation", model="t5-small")

@app.route('/generate_notes', methods=['POST'])
def generate_notes():
    data = request.json
    topic = data.get("topic", "Explain Newton's Laws of Motion")

    # Generate Study Material
    generated_text = generator(topic, max_length=800, do_sample=True)
    study_material = generated_text[0]['generated_text']

    # Summarize into Flashcards
    flashcards = summarizer(study_material, max_length=50, min_length=10, do_sample=False)

    # Generate a Question
    question = question_generator("generate question: " + study_material, max_length=50)

    return jsonify({
        "study_material": study_material,
        "flashcard": flashcards[0]['summary_text'],
        "quiz_question": question[0]['generated_text']
    })
@app.route('/generate-flashcards', methods=['POST'])

def generate_flashcards(topic, num_cards=5):
    prompt = (
        f"Generate {num_cards} flashcards about the topic '{topic}'. "
        "Each flashcard should contain a question and an answer in this format:\n"
        "Q: [Question about the topic]\nA: [Answer to the question]\n"
        "Example:\n"
        "Q: What is the Sun made of?\nA: Mostly hydrogen and helium.\n\n"
        "Flashcards:\n"
    )
    
    # Generate the response using GPT-2
    response = generator(prompt, max_length=500, num_return_sequences=1, truncation=True)
    raw_text = response[0]['generated_text']
    
    # Split the generated text into lines and extract flashcards
    flashcards = []
    lines = raw_text.split("\n")
    
    # Collect pairs of question and answer (Q&A)
    for i in range(len(lines)):
        if lines[i].startswith("Q:") and i+1 < len(lines) and lines[i+1].startswith("A:"):
            flashcards.append((lines[i], lines[i+1]))
    
    # Return the desired number of flashcards
    if len(flashcards) < num_cards:
        print(f"Warning: Only {len(flashcards)} flashcards were generated.")
    return flashcards[:num_cards]

# Example usage
topic = "Sun"
flashcards = generate_flashcards(topic)

# Display the flashcards
if flashcards:
    for i, flashcard in enumerate(flashcards, 1):
        print(f"Flashcard {i}:")
        print(f"{flashcard[0]}\n{flashcard[1]}\n")
else:
    print("No valid flashcards were generated. Please refine the prompt or try again.")

if __name__ == '_main_':
    app.run(debug=True)