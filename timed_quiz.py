#!/usr/bin/env python3
"""
WEAC Quiz Game - Timed quiz mode
"""

import time
from colorama import Fore, Style


class TimedQuiz:
    """Handle timed quiz functionality."""
    
    def __init__(self, time_limit_seconds=None):
        """Initialize timed quiz with optional time limit."""
        self.time_limit = time_limit_seconds
        self.start_time = None
        self.elapsed_time = 0
    
    def start(self):
        """Start the timer."""
        self.start_time = time.time()
    
    def get_elapsed(self):
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time
    
    def get_remaining(self):
        """Get remaining time in seconds."""
        if self.time_limit is None:
            return None
        remaining = self.time_limit - self.get_elapsed()
        return max(0, remaining)
    
    def is_time_up(self):
        """Check if time limit has been exceeded."""
        if self.time_limit is None:
            return False
        return self.get_remaining() <= 0
    
    def format_time(self, seconds):
        """Format seconds to MM:SS format."""
        mins = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{mins:02d}:{secs:02d}"
    
    def display_timer(self):
        """Display formatted timer."""
        remaining = self.get_remaining()
        if remaining is None:
            return ""
        
        formatted = self.format_time(remaining)
        
        # Color code based on remaining time
        if remaining > 60:
            color = Fore.GREEN
        elif remaining > 30:
            color = Fore.YELLOW
        else:
            color = Fore.RED
        
        return f"{color}Time: {formatted}{Style.RESET_ALL}"
    
    def get_bonus_points(self, base_score):
        """Calculate bonus points based on time remaining."""
        if self.time_limit is None:
            return 0
        
        remaining = self.get_remaining()
        if remaining <= 0:
            return 0
        
        # Give 5% bonus if more than 50% time remains
        percentage_remaining = (remaining / self.time_limit) * 100
        if percentage_remaining > 50:
            return int(base_score * 0.05)
        
        return 0
