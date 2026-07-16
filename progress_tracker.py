#!/usr/bin/env python3
"""
WEAC Quiz Game - Progress tracking and statistics module
"""

import json
import os
from datetime import datetime
from pathlib import Path


class ProgressTracker:
    """Track user progress and statistics across quiz sessions."""
    
    def __init__(self, progress_file="progress.json"):
        """Initialize progress tracker."""
        self.progress_file = progress_file
        self.data = self._load_progress()
    
    def _load_progress(self):
        """Load progress from file or create new."""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._create_new_progress()
        return self._create_new_progress()
    
    def _create_new_progress(self):
        """Create new progress structure."""
        return {
            "total_quizzes": 0,
            "total_questions": 0,
            "total_correct": 0,
            "sessions": [],
            "category_stats": {},
            "created_at": datetime.now().isoformat()
        }
    
    def _save_progress(self):
        """Save progress to file."""
        with open(self.progress_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def record_session(self, category, score, total, questions_data):
        """Record a quiz session."""
        session = {
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "score": score,
            "total": total,
            "percentage": round((score / total * 100) if total > 0 else 0, 2),
            "questions": [
                {
                    "id": q.get("id"),
                    "question": q.get("question", ""),
                    "correct": q.get("correct", False)
                }
                for q in questions_data
            ]
        }
        
        self.data["sessions"].append(session)
        self.data["total_quizzes"] += 1
        self.data["total_questions"] += total
        self.data["total_correct"] += score
        
        # Update category stats
        if category not in self.data["category_stats"]:
            self.data["category_stats"][category] = {
                "attempts": 0,
                "total_questions": 0,
                "correct": 0,
                "best_score": 0
            }
        
        cat_stats = self.data["category_stats"][category]
        cat_stats["attempts"] += 1
        cat_stats["total_questions"] += total
        cat_stats["correct"] += score
        cat_stats["best_score"] = max(cat_stats["best_score"], session["percentage"])
        
        self._save_progress()
        return session
    
    def get_statistics(self):
        """Get overall statistics."""
        total_q = self.data["total_questions"]
        total_c = self.data["total_correct"]
        overall_percentage = (total_c / total_q * 100) if total_q > 0 else 0
        
        return {
            "total_quizzes": self.data["total_quizzes"],
            "total_questions": total_q,
            "total_correct": total_c,
            "overall_percentage": round(overall_percentage, 2),
            "category_stats": self.data["category_stats"],
            "recent_sessions": self.data["sessions"][-5:] if self.data["sessions"] else []
        }
    
    def get_category_performance(self, category):
        """Get performance for specific category."""
        return self.data["category_stats"].get(category, None)
    
    def clear_progress(self):
        """Clear all progress data."""
        self.data = self._create_new_progress()
        self._save_progress()
