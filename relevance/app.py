from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from relevance_checker import QuestionRelevanceChecker

app = Flask(__name__)
# Initialize checker when app starts
checker = None

def get_checker():
    global checker
    if checker is None:
        checker = QuestionRelevanceChecker()
    return checker

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_relevance', methods=['POST'])
def check_relevance():
    data = request.get_json()
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({'error': 'Please enter a question'})
    
    # Get fresh checker instance
    current_checker = get_checker()
    result = current_checker.check_relevance(question)
    
    return jsonify({
        'question': question,
        'relevance': result['relevance'],
        'unit': result['best_unit'],
        'score': round(result['similarity_score'], 3),
        'message': result['message']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)