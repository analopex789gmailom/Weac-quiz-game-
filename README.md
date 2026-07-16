# WEAC Quiz Game

A Python-based quiz game to help you prepare for the **Welder Entry Assessment & Certification (WEAC)** exam.

## Features

- 📚 Multiple quiz categories (Welding Fundamentals, Safety, Techniques, etc.)
- 🎮 Interactive command-line quiz interface
- 🎯 Instant feedback on answers with correct explanations
- 📊 Score tracking and performance analysis
- 🔀 Randomized questions each round
- 🎨 Colored terminal output for better readability

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/analopex789gmailom/Weac-quiz-game-.git
cd Weac-quiz-game-
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the quiz game:
```bash
python quiz_game.py
```

### How to Play

1. **Select a Category**: Choose from available quiz categories or "Random Mix" to test across all topics
2. **Answer Questions**: Read each question and select your answer (1-4)
3. **Get Feedback**: See immediately if your answer is correct with explanations
4. **View Results**: Get your final score and performance percentage
5. **Play Again**: Choose to take another quiz or exit

## Quiz Categories

- **Welding Fundamentals**: Core welding concepts and terminology
- **Safety**: Welding safety procedures and requirements
- **Techniques**: Different welding methods and processes

## Difficulty Levels

Questions are tagged with difficulty levels:
- 🟢 Easy: Basic concepts
- 🟡 Medium: Applied knowledge
- 🔴 Hard: Advanced topics (coming soon)

## Project Structure

```
Weac-quiz-game-/
├── quiz_game.py          # Main game implementation
├── questions.json        # Quiz questions database
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

## Adding More Questions

Edit `questions.json` to add more quiz questions. Format:

```json
{
  "category_name": [
    {
      "id": 1,
      "question": "Your question here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "difficulty": "easy"
    }
  ]
}
```

- `id`: Unique question identifier
- `question`: The question text
- `options`: Array of answer choices
- `correct_answer`: Index (0-based) of the correct option
- `difficulty`: "easy", "medium", or "hard"

## Performance Scoring

- **80-100%**: Excellent! Ready for the exam
- **60-79%**: Good effort, keep studying
- **Below 60%**: Focus on weak areas and practice more

## Future Enhancements

- [ ] Difficulty filtering (easy/medium/hard)
- [ ] Progress tracking and statistics
- [ ] Timed quizzes
- [ ] Web-based interface
- [ ] Mobile app version
- [ ] Question explanations
- [ ] Study mode with hints

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to:
- Add more welding questions
- Improve the UI
- Report bugs
- Suggest features

## Support

For issues or questions, please open an issue on GitHub.

---

**Good luck on your WEAC exam! 🔥⚒️**