#!/usr/bin/env python3
"""
WEAC Quiz Game - Web Application (Flask)
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
from progress_tracker import ProgressTracker

app = Flask(__name__)
app.secret_key = 'weac-quiz-game-secret-key-2026'

# Load questions
with open('questions.json', 'r') as f:
    QUESTIONS = json.load(f)

PROGRESS = ProgressTracker()


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/api/categories')
def get_categories():
    """Get available quiz categories."""
    categories = [
        {
            'name': cat.replace('_', ' ').title(),
            'id': cat,
            'count': len(questions)
        }
        for cat, questions in QUESTIONS.items()
    ]
    return jsonify(categories)


@app.route('/api/quiz/start', methods=['POST'])
def start_quiz():
    """Start a new quiz session."""
    data = request.json
    category = data.get('category')
    difficulty = data.get('difficulty', 'all')
    
    # Get questions
    if category == 'random_mix':
        all_questions = []
        for questions_list in QUESTIONS.values():
            all_questions.extend(questions_list)
    else:
        all_questions = QUESTIONS.get(category, [])
    
    # Filter by difficulty
    if difficulty and difficulty != 'all':
        all_questions = [q for q in all_questions if q.get('difficulty') == difficulty]
    
    # Shuffle and limit questions
    import random
    random.shuffle(all_questions)
    
    # Store quiz session
    quiz_id = datetime.now().timestamp()
    session['quiz_id'] = quiz_id
    session['category'] = category
    session['questions'] = all_questions[:10]  # Limit to 10 questions
    session['current_question'] = 0
    session['score'] = 0
    session['answers'] = []
    
    return jsonify({
        'quiz_id': quiz_id,
        'total_questions': len(session['questions']),
        'first_question': get_question_data(session['questions'][0], 0)
    })


@app.route('/api/quiz/question/<int:question_num>')
def get_question(question_num):
    """Get a specific question."""
    if 'questions' not in session or question_num >= len(session['questions']):
        return jsonify({'error': 'Invalid question'}), 404
    
    question = session['questions'][question_num]
    return jsonify(get_question_data(question, question_num))


def get_question_data(question, index):
    """Format question data for API response."""
    return {
        'id': question.get('id'),
        'number': index + 1,
        'question': question.get('question'),
        'options': question.get('options'),
        'difficulty': question.get('difficulty')
    }


@app.route('/api/quiz/answer', methods=['POST'])
def submit_answer():
    """Submit an answer and get feedback."""
    data = request.json
    answer_index = data.get('answer')
    question_num = data.get('question_num')
    
    if 'questions' not in session:
        return jsonify({'error': 'No active quiz'}), 400
    
    question = session['questions'][question_num]
    is_correct = answer_index == question.get('correct_answer')
    
    if is_correct:
        session['score'] += 1
    
    # Record answer
    session['answers'].append({
        'question_id': question.get('id'),
        'answer': answer_index,
        'correct': is_correct
    })
    
    correct_answer = question.get('options')[question.get('correct_answer')]
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': correct_answer,
        'explanation': f"The correct answer is: {correct_answer}"
    })


@app.route('/api/quiz/results')
def get_results():
    """Get quiz results."""
    if 'questions' not in session:
        return jsonify({'error': 'No completed quiz'}), 400
    
    total = len(session['questions'])
    score = session['score']
    percentage = (score / total * 100) if total > 0 else 0
    
    # Record in progress tracker
    questions_data = [
        {
            'id': session['questions'][i].get('id'),
            'question': session['questions'][i].get('question'),
            'correct': session['answers'][i]['correct'] if i < len(session['answers']) else False
        }
        for i in range(len(session['questions']))
    ]
    
    PROGRESS.record_session(session.get('category', 'unknown'), score, total, questions_data)
    
    return jsonify({
        'score': score,
        'total': total,
        'percentage': round(percentage, 2),
        'performance': 'Excellent! You\'re ready for the exam!' if percentage >= 80 else
                       'Good effort! Keep studying.' if percentage >= 60 else
                       'Keep practicing and focus on weak areas.'
    })


@app.route('/api/stats')
def get_stats():
    """Get user statistics."""
    stats = PROGRESS.get_statistics()
    return jsonify(stats)


@app.route('/api/stats/reset', methods=['POST'])
def reset_stats():
    """Reset all statistics."""
    PROGRESS.clear_progress()
    return jsonify({'success': True, 'message': 'Progress reset successfully'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
