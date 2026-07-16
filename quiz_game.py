#!/usr/bin/env python3
"""
WEAC Quiz Game - A study tool for Welder Entry Assessment & Certification
"""

import json
import random
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)


class QuizGame:
    def __init__(self, questions_file="questions.json"):
        """Initialize the quiz game with questions from a JSON file."""
        self.questions_file = questions_file
        self.questions = self._load_questions()
        self.score = 0
        self.total_answered = 0
        self.category = None
        
    def _load_questions(self):
        """Load questions from JSON file."""
        try:
            with open(self.questions_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{Fore.RED}Error: {self.questions_file} not found!")
            return {}
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error: Invalid JSON format in {self.questions_file}")
            return {}
    
    def display_welcome(self):
        """Display welcome screen."""
        print(f"\n{Back.BLUE}{Fore.WHITE}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}  WEAC QUIZ GAME - Welder Certification Prep  {Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}{'=' * 50}{Style.RESET_ALL}\n")
        
    def show_categories(self):
        """Display available quiz categories."""
        print(f"{Fore.CYAN}Available Categories:{Style.RESET_ALL}")
        categories = list(self.questions.keys())
        
        if not categories:
            print(f"{Fore.RED}No categories available!{Style.RESET_ALL}")
            return None
        
        for i, category in enumerate(categories, 1):
            question_count = len(self.questions[category])
            print(f"  {i}. {category.replace('_', ' ').title()} ({question_count} questions)")
        
        print(f"  0. Random Mix (All categories)")
        
        choice = input(f"\n{Fore.YELLOW}Select category (0-{len(categories)}): {Style.RESET_ALL}")
        
        try:
            choice = int(choice)
            if choice == 0:
                return "random_mix"
            elif 1 <= choice <= len(categories):
                return categories[choice - 1]
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
                return self.show_categories()
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!{Style.RESET_ALL}")
            return self.show_categories()
    
    def get_quiz_questions(self, category):
        """Get questions for selected category."""
        if category == "random_mix":
            all_questions = []
            for cat_questions in self.questions.values():
                all_questions.extend(cat_questions)
            return all_questions
        else:
            return self.questions.get(category, [])
    
    def ask_question(self, question):
        """Ask a single question and return if answer is correct."""
        print(f"\n{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Question {self.total_answered + 1}:{Style.RESET_ALL}")
        print(f"\n{question['question']}\n")
        
        for i, option in enumerate(question['options'], 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                answer = int(input(f"\n{Fore.GREEN}Your answer (1-{len(question['options'])}): {Style.RESET_ALL}"))
                if 1 <= answer <= len(question['options']):
                    break
                else:
                    print(f"{Fore.RED}Please enter a valid option!{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a number!{Style.RESET_ALL}")
        
        # Convert to 0-based index
        is_correct = (answer - 1) == question['correct_answer']
        
        if is_correct:
            print(f"\n{Fore.GREEN}✓ Correct!{Style.RESET_ALL}")
            self.score += 1
        else:
            correct_option = question['options'][question['correct_answer']]
            print(f"\n{Fore.RED}✗ Incorrect!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}The correct answer is: {correct_option}{Style.RESET_ALL}")
        
        self.total_answered += 1
        return is_correct
    
    def display_results(self):
        """Display final quiz results."""
        percentage = (self.score / self.total_answered * 100) if self.total_answered > 0 else 0
        
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Quiz Complete!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Results:{Style.RESET_ALL}")
        print(f"  Score: {Fore.GREEN}{self.score}{Style.RESET_ALL}/{self.total_answered}")
        print(f"  Percentage: {Fore.GREEN}{percentage:.1f}%{Style.RESET_ALL}")
        
        if percentage >= 80:
            print(f"\n{Fore.GREEN}Excellent! You're well prepared for the exam!{Style.RESET_ALL}")
        elif percentage >= 60:
            print(f"\n{Fore.YELLOW}Good effort! Keep studying to improve your score.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}Keep practicing! Focus on the areas you struggled with.{Style.RESET_ALL}")
        
        print()
    
    def run(self):
        """Run the quiz game."""
        self.display_welcome()
        
        while True:
            self.score = 0
            self.total_answered = 0
            
            category = self.show_categories()
            if category is None:
                print(f"{Fore.RED}No category selected. Exiting...{Style.RESET_ALL}")
                break
            
            quiz_questions = self.get_quiz_questions(category)
            
            if not quiz_questions:
                print(f"{Fore.RED}No questions available for this category!{Style.RESET_ALL}")
                continue
            
            # Shuffle questions
            random.shuffle(quiz_questions)
            
            # Run quiz
            for question in quiz_questions:
                self.ask_question(question)
            
            self.display_results()
            
            # Ask if user wants to play again
            again = input(f"{Fore.YELLOW}Play again? (y/n): {Style.RESET_ALL}").lower()
            if again != 'y':
                print(f"\n{Fore.CYAN}Thanks for using WEAC Quiz Game! Good luck on your exam!{Style.RESET_ALL}\n")
                break


def main():
    """Main entry point."""
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
