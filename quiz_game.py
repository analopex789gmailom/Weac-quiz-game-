#!/usr/bin/env python3
"""
WEAC Quiz Game - A study tool for Welder Entry Assessment & Certification
"""

import json
import random
import time
from colorama import Fore, Back, Style, init
from progress_tracker import ProgressTracker
from timed_quiz import TimedQuiz

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)


class QuizGame:
    def __init__(self, questions_file="questions.json"):
        """Initialize the quiz game with questions from a JSON file."""
        self.questions_file = questions_file
        self.questions = self._load_questions()
        self.progress = ProgressTracker()
        self.score = 0
        self.total_answered = 0
        self.category = None
        self.timed_quiz = None
        self.questions_answered = []
        
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
        print(f"\n{Back.BLUE}{Fore.WHITE}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}{'WEAC QUIZ GAME - Welder Certification Prep':^60}{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}{'=' * 60}{Style.RESET_ALL}\n")
    
    def show_main_menu(self):
        """Display main menu with options."""
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Main Menu:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}1{Style.RESET_ALL}. Start Quiz")
        print(f"  {Fore.GREEN}2{Style.RESET_ALL}. View Statistics")
        print(f"  {Fore.GREEN}3{Style.RESET_ALL}. Study Mode (Difficulty Filter)")
        print(f"  {Fore.GREEN}4{Style.RESET_ALL}. Timed Quiz")
        print(f"  {Fore.GREEN}5{Style.RESET_ALL}. Reset Progress")
        print(f"  {Fore.GREEN}0{Style.RESET_ALL}. Exit")
        print()
        
        choice = input(f"{Fore.YELLOW}Select option (0-5): {Style.RESET_ALL}")
        return choice
    
    def show_categories(self):
        """Display available quiz categories."""
        print(f"\n{Fore.CYAN}Available Categories:{Style.RESET_ALL}")
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
    
    def get_quiz_questions(self, category, difficulty_filter=None):
        """Get questions for selected category with optional difficulty filter."""
        if category == "random_mix":
            all_questions = []
            for cat_questions in self.questions.values():
                all_questions.extend(cat_questions)
        else:
            all_questions = self.questions.get(category, [])
        
        # Apply difficulty filter if specified
        if difficulty_filter and difficulty_filter != "all":
            all_questions = [q for q in all_questions if q.get("difficulty") == difficulty_filter]
        
        return all_questions
    
    def show_statistics(self):
        """Display user statistics."""
        stats = self.progress.get_statistics()
        
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Your Statistics:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
        
        print(f"  {Fore.GREEN}Total Quizzes Completed:{Style.RESET_ALL} {stats['total_quizzes']}")
        print(f"  {Fore.GREEN}Total Questions Answered:{Style.RESET_ALL} {stats['total_questions']}")
        print(f"  {Fore.GREEN}Total Correct:{Style.RESET_ALL} {stats['total_correct']}")
        print(f"  {Fore.GREEN}Overall Percentage:{Style.RESET_ALL} {Fore.CYAN}{stats['overall_percentage']:.1f}%{Style.RESET_ALL}")
        
        if stats['category_stats']:
            print(f"\n{Fore.YELLOW}Category Performance:{Style.RESET_ALL}")
            for category, cat_stats in stats['category_stats'].items():
                print(f"\n  {Fore.GREEN}{category.replace('_', ' ').title()}:{Style.RESET_ALL}")
                print(f"    Attempts: {cat_stats['attempts']}")
                print(f"    Questions: {cat_stats['total_questions']}")
                print(f"    Correct: {cat_stats['correct']}")
                print(f"    Best Score: {Fore.CYAN}{cat_stats['best_score']:.1f}%{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def ask_question(self, question, show_timer=None):
        """Ask a single question and return if answer is correct."""
        print(f"\n{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Question {self.total_answered + 1}:{Style.RESET_ALL}")
        
        if show_timer:
            timer_display = show_timer.display_timer()
            if timer_display:
                print(f"  {timer_display}")
        
        print(f"\n{question['question']}\n")
        
        for i, option in enumerate(question['options'], 1):
            print(f"  {i}. {option}")
        
        # Check if time is up before getting answer
        if show_timer and show_timer.is_time_up():
            print(f"\n{Fore.RED}Time is up! Quiz ended.{Style.RESET_ALL}")
            return None
        
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
        
        question_record = {
            "id": question.get("id"),
            "question": question.get("question", ""),
            "correct": is_correct
        }
        self.questions_answered.append(question_record)
        self.total_answered += 1
        
        return is_correct
    
    def display_results(self):
        """Display final quiz results."""
        percentage = (self.score / self.total_answered * 100) if self.total_answered > 0 else 0
        
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Quiz Complete!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Results:{Style.RESET_ALL}")
        print(f"  Score: {Fore.GREEN}{self.score}{Style.RESET_ALL}/{self.total_answered}")
        print(f"  Percentage: {Fore.GREEN}{percentage:.1f}%{Style.RESET_ALL}")
        
        if percentage >= 80:
            print(f"\n{Fore.GREEN}🎉 Excellent! You're well prepared for the exam!{Style.RESET_ALL}")
        elif percentage >= 60:
            print(f"\n{Fore.YELLOW}👍 Good effort! Keep studying to improve your score.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}📚 Keep practicing! Focus on the areas you struggled with.{Style.RESET_ALL}")
        
        # Record session in progress tracker
        self.progress.record_session(self.category, self.score, self.total_answered, self.questions_answered)
        
        print()
    
    def run_quiz(self, difficulty_filter=None, time_limit=None):
        """Run a quiz session."""
        self.score = 0
        self.total_answered = 0
        self.questions_answered = []
        
        category = self.show_categories()
        if category is None:
            print(f"{Fore.RED}No category selected.{Style.RESET_ALL}")
            return
        
        self.category = category
        
        quiz_questions = self.get_quiz_questions(category, difficulty_filter)
        
        if not quiz_questions:
            print(f"{Fore.RED}No questions available for this category!{Style.RESET_ALL}")
            return
        
        # Shuffle questions
        random.shuffle(quiz_questions)
        
        # Setup timed quiz if time limit specified
        timed_quiz = None
        if time_limit:
            timed_quiz = TimedQuiz(time_limit_seconds=time_limit)
            timed_quiz.start()
            print(f"\n{Fore.YELLOW}⏱️  Timed Quiz Started! You have {timed_quiz.format_time(time_limit)} to complete.{Style.RESET_ALL}\n")
        
        # Run quiz
        for question in quiz_questions:
            if timed_quiz and timed_quiz.is_time_up():
                print(f"\n{Fore.RED}⏰ Time is up! Quiz ended.{Style.RESET_ALL}")
                break
            
            self.ask_question(question, show_timer=timed_quiz)
        
        self.display_results()
    
    def run_study_mode(self):
        """Run study mode with difficulty filtering."""
        print(f"\n{Fore.CYAN}Study Mode - Select Difficulty:{Style.RESET_ALL}")
        print(f"  1. Easy Questions Only")
        print(f"  2. Medium Questions Only")
        print(f"  3. Hard Questions Only")
        print(f"  4. All Difficulties")
        
        choice = input(f"\n{Fore.YELLOW}Select difficulty (1-4): {Style.RESET_ALL}")
        
        difficulty_map = {
            "1": "easy",
            "2": "medium",
            "3": "hard",
            "4": "all"
        }
        
        difficulty = difficulty_map.get(choice, "all")
        self.run_quiz(difficulty_filter=difficulty)
    
    def run_timed_mode(self):
        """Run timed quiz mode."""
        print(f"\n{Fore.CYAN}Timed Quiz - Select Time Limit:{Style.RESET_ALL}")
        print(f"  1. 5 minutes (300 seconds)")
        print(f"  2. 10 minutes (600 seconds)")
        print(f"  3. 15 minutes (900 seconds)")
        print(f"  4. 20 minutes (1200 seconds)")
        print(f"  5. Custom (enter seconds)")
        
        choice = input(f"\n{Fore.YELLOW}Select time limit (1-5): {Style.RESET_ALL}")
        
        time_map = {
            "1": 300,
            "2": 600,
            "3": 900,
            "4": 1200
        }
        
        if choice in time_map:
            time_limit = time_map[choice]
        elif choice == "5":
            try:
                time_limit = int(input(f"{Fore.YELLOW}Enter time in seconds: {Style.RESET_ALL}"))
            except ValueError:
                print(f"{Fore.RED}Invalid input. Using 10 minutes.{Style.RESET_ALL}")
                time_limit = 600
        else:
            print(f"{Fore.RED}Invalid choice. Using 10 minutes.{Style.RESET_ALL}")
            time_limit = 600
        
        self.run_quiz(time_limit=time_limit)
    
    def reset_progress(self):
        """Reset all progress data."""
        confirm = input(f"{Fore.YELLOW}Are you sure you want to reset all progress? (y/n): {Style.RESET_ALL}").lower()
        if confirm == 'y':
            self.progress.clear_progress()
            print(f"{Fore.GREEN}Progress reset successfully!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Reset cancelled.{Style.RESET_ALL}")
    
    def run(self):
        """Run the main quiz game loop."""
        self.display_welcome()
        
        while True:
            choice = self.show_main_menu()
            
            if choice == "1":
                self.run_quiz()
            elif choice == "2":
                self.show_statistics()
            elif choice == "3":
                self.run_study_mode()
            elif choice == "4":
                self.run_timed_mode()
            elif choice == "5":
                self.reset_progress()
            elif choice == "0":
                print(f"\n{Fore.CYAN}Thanks for using WEAC Quiz Game! Good luck on your exam! 🔥⚒️{Style.RESET_ALL}\n")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")


def main():
    """Main entry point."""
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
