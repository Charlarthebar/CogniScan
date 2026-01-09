"""
Dementia Diagnosis Assessment Application

A cognitive screening tool based on established neuropsychological tests including
elements from the Mini-Mental State Examination (MMSE) and Montreal Cognitive
Assessment (MoCA). This application provides a structured assessment across
multiple cognitive domains.

DISCLAIMER: This is NOT a medical diagnostic tool. Results should be interpreted
by qualified healthcare professionals only.
"""

import random
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window


# ============================================================================
# SCREEN DEFINITIONS
# ============================================================================

class TitleScreen(Screen):
    """Landing screen with app title and start button."""
    pass


class DescriptionScreen(Screen):
    """Introduction and disclaimer screen."""
    pass


class OrientationIntroScreen(Screen):
    """Introduction to orientation questions."""
    pass


class OrientationScreen(Screen):
    """Orientation questions testing awareness of time."""
    current_question = StringProperty("")
    question_number = NumericProperty(0)
    pass


class OrientationScoreScreen(Screen):
    """Display orientation test score."""
    orientation_score = StringProperty("0/5")
    pass


class FiveWordsIntroScreen(Screen):
    """Introduction to immediate word recall test."""
    pass


class FiveWordsScreen(Screen):
    """Display 5 words for memorization."""
    countdown = StringProperty("10")
    pass


class ImmediateRecallScreen(Screen):
    """User enters words they remember immediately."""
    pass


class ImmediateRecallScoreScreen(Screen):
    """Display immediate recall score."""
    immediate_score = StringProperty("0/5")
    pass


class Serial7sIntroScreen(Screen):
    """Introduction to Serial 7s test."""
    pass


class Serial7sScreen(Screen):
    """Serial 7s subtraction test."""
    pass


class Serial7sScoreScreen(Screen):
    """Display Serial 7s score."""
    serial7s_score = StringProperty("0/5")
    pass


class DigitSpanIntroScreen(Screen):
    """Introduction to digit span test."""
    pass


class DigitSpanForwardScreen(Screen):
    """Forward digit span test."""
    digits_to_remember = StringProperty("")
    current_level = NumericProperty(3)
    pass


class DigitSpanBackwardScreen(Screen):
    """Backward digit span test."""
    digits_to_remember = StringProperty("")
    current_level = NumericProperty(2)
    pass


class DigitSpanScoreScreen(Screen):
    """Display digit span score."""
    digit_span_score = StringProperty("0/4")
    pass


class CategoryFluencyIntroScreen(Screen):
    """Introduction to category fluency test."""
    pass


class CategoryFluencyScreen(Screen):
    """Category fluency test - name animals."""
    timer = StringProperty("60")
    pass


class CategoryFluencyScoreScreen(Screen):
    """Display category fluency score."""
    fluency_score = StringProperty("0/3")
    animals_count = StringProperty("0")
    pass


class StroopTestIntroScreen(Screen):
    """Introduction to Stroop test."""
    pass


class StroopTestScreen(Screen):
    """Stroop color-word test."""
    word_text = StringProperty("RED")
    word_color = ListProperty([1, 0, 0, 1])
    trial_number = NumericProperty(1)
    timer = StringProperty("30")
    pass


class StroopScoreScreen(Screen):
    """Display Stroop test score."""
    stroop_score = StringProperty("0/5")
    pass


class DelayedRecallIntroScreen(Screen):
    """Introduction to delayed recall test."""
    pass


class DelayedRecallScreen(Screen):
    """User tries to recall the 5 words from earlier."""
    pass


class DelayedRecallScoreScreen(Screen):
    """Display delayed recall score."""
    delayed_score = StringProperty("0/5")
    pass


class ResultsScreen(Screen):
    """Final results and interpretation screen."""
    total_score = StringProperty("0/30")
    score_category = StringProperty("")
    interpretation = StringProperty("")
    pass


class WindowManager(ScreenManager):
    """Manages transitions between screens."""
    pass


# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================

class DementiaDiagnosisApp(App):
    """
    Main application class implementing a comprehensive cognitive assessment.

    The assessment includes:
    - Orientation (5 points): Awareness of current date/time
    - Immediate Word Recall (5 points): Remember 5 words immediately
    - Serial 7s (5 points): Subtract 7 from 100 repeatedly
    - Digit Span (4 points): Forward and backward digit recall
    - Category Fluency (3 points): Name animals in 60 seconds
    - Stroop Test (5 points): Color-word interference
    - Delayed Word Recall (5 points): Recall words from earlier

    Total: 32 points (normalized to 30 for interpretation)
    """

    # ========================================================================
    # SCORE TRACKING
    # ========================================================================

    # Individual test scores
    orientation_score = NumericProperty(0)
    immediate_recall_score = NumericProperty(0)
    serial7s_score = NumericProperty(0)
    digit_span_forward_score = NumericProperty(0)
    digit_span_backward_score = NumericProperty(0)
    fluency_score = NumericProperty(0)
    stroop_score = NumericProperty(0)
    delayed_recall_score = NumericProperty(0)

    # Display properties
    recent_animals_text = StringProperty("None yet")
    animals_count_text = StringProperty("0")

    # ========================================================================
    # TEST STATE VARIABLES
    # ========================================================================

    # Word memorization
    words = ListProperty([])
    checked_words_immediate = ListProperty([])
    checked_words_delayed = ListProperty([])

    # Serial 7s
    serial7_correct = ["93", "86", "79", "72", "65"]
    checked_numbers = ListProperty([])

    # Orientation
    orientation_questions = ListProperty([])
    orientation_answers = ListProperty([])
    current_orientation_index = NumericProperty(0)

    # Digit span
    forward_digits = ListProperty([])
    backward_digits = ListProperty([])
    digit_forward_passed = BooleanProperty(False)
    digit_backward_passed = BooleanProperty(False)

    # Category fluency
    animals_entered = ListProperty([])
    fluency_timer_event = None

    # Stroop test
    stroop_trials = ListProperty([])
    stroop_current_trial = NumericProperty(0)
    stroop_correct = NumericProperty(0)
    stroop_timer_event = None

    # Timers
    word_display_timer = None

    # ========================================================================
    # APPLICATION LIFECYCLE
    # ========================================================================

    def build(self):
        """Initialize the application."""
        self.title = "Cognitive Assessment Tool"
        self.initialize_tests()
        return Builder.load_file('dementiadiagnosis.kv')

    def initialize_tests(self):
        """Set up all test data."""
        # Generate words for memorization
        self.words = self.generate_random_words()

        # Set up orientation questions
        self.setup_orientation_questions()

        # Set up digit span sequences
        self.setup_digit_span()

        # Set up Stroop test trials
        self.setup_stroop_test()

    def on_start(self):
        """Called when the app starts - set up initial screen data."""
        # Set up the five words display
        screen = self.root.get_screen('fivewords')
        for i, word in enumerate(self.words, 1):
            word_label = screen.ids.get(f'word{i}')
            if word_label:
                word_label.text = word.upper()

    # ========================================================================
    # WORD GENERATION
    # ========================================================================

    def generate_random_words(self):
        """Generate 5 random words from the word bank."""
        try:
            # Get the directory where main.py is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            words_path = os.path.join(script_dir, "words.txt")

            with open(words_path, "r") as file:
                word_list = [w.strip() for w in file.read().splitlines() if w.strip()]

            # Filter for good memorization words (4-8 letters, concrete nouns preferred)
            good_words = [w for w in word_list if 4 <= len(w) <= 8 and w.isalpha()]

            if len(good_words) < 5:
                good_words = word_list

            random.shuffle(good_words)
            return good_words[:5]
        except FileNotFoundError:
            # Fallback words if file not found
            return ["apple", "table", "penny", "garden", "finger"]

    # ========================================================================
    # ORIENTATION TEST
    # ========================================================================

    def setup_orientation_questions(self):
        """Set up orientation questions based on current date."""
        now = datetime.now()

        # Season calculation
        month = now.month
        if month in [12, 1, 2]:
            season = "winter"
        elif month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        else:
            season = "fall"

        # Day of week
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day_of_week = days[now.weekday()]

        # Month name
        months = ["january", "february", "march", "april", "may", "june",
                  "july", "august", "september", "october", "november", "december"]
        month_name = months[now.month - 1]

        self.orientation_questions = [
            "What year is it?",
            "What month is it?",
            "What day of the week is it?",
            "What is today's date (day number)?",
            "What season is it?"
        ]

        self.orientation_answers = [
            str(now.year),
            month_name,
            day_of_week,
            str(now.day),
            season
        ]

        self.current_orientation_index = 0

    def get_current_orientation_question(self):
        """Get the current orientation question."""
        if self.current_orientation_index < len(self.orientation_questions):
            return self.orientation_questions[self.current_orientation_index]
        return ""

    def check_orientation_answer(self, user_answer):
        """Check if the orientation answer is correct."""
        if self.current_orientation_index >= len(self.orientation_answers):
            return False

        correct = self.orientation_answers[self.current_orientation_index].lower()
        answer = user_answer.strip().lower()

        # Allow some flexibility in answers
        is_correct = (answer == correct or
                      answer in correct or
                      correct in answer or
                      (answer.isdigit() and correct.isdigit() and int(answer) == int(correct)))

        if is_correct:
            self.orientation_score += 1

        self.current_orientation_index += 1

        # Update the screen
        screen = self.root.get_screen('orientation')
        if self.current_orientation_index < len(self.orientation_questions):
            screen.current_question = self.orientation_questions[self.current_orientation_index]
            screen.question_number = self.current_orientation_index + 1
            return True  # More questions
        else:
            return False  # All questions done

    def finish_orientation(self):
        """Finish orientation test and display score."""
        screen = self.root.get_screen('orientationscore')
        screen.orientation_score = f"{self.orientation_score}/5"

    # ========================================================================
    # IMMEDIATE WORD RECALL
    # ========================================================================

    def start_word_display_timer(self, duration=10):
        """Start countdown timer for word display."""
        screen = self.root.get_screen('fivewords')
        screen.countdown = str(duration)

        def update_countdown(dt):
            current = int(screen.countdown)
            if current > 0:
                screen.countdown = str(current - 1)
            else:
                # Auto-advance to recall screen
                self.word_display_timer.cancel()
                self.root.current = 'immediaterecall'

        self.word_display_timer = Clock.schedule_interval(update_countdown, 1)

    def cancel_word_timer(self):
        """Cancel the word display timer if active."""
        if self.word_display_timer:
            self.word_display_timer.cancel()
            self.word_display_timer = None

    def calculate_immediate_recall(self, input_words):
        """Calculate score for immediate word recall."""
        words_list = input_words.lower().replace(',', ' ').split()

        for word in words_list:
            word = word.strip()
            if word in [w.lower() for w in self.words] and word not in self.checked_words_immediate:
                self.immediate_recall_score += 1
                self.checked_words_immediate.append(word)

        return f"{self.immediate_recall_score}/5"

    def finish_immediate_recall(self):
        """Display immediate recall score."""
        screen = self.root.get_screen('immediaterecallscore')
        screen.immediate_score = f"{self.immediate_recall_score}/5"

    # ========================================================================
    # SERIAL 7s TEST
    # ========================================================================

    def calculate_serial7s(self, input_nums):
        """Calculate Serial 7s score."""
        nums_list = input_nums.replace(',', ' ').split()

        for num in nums_list:
            num = num.strip()
            if num in self.serial7_correct and num not in self.checked_numbers:
                self.serial7s_score += 1
                self.checked_numbers.append(num)

        return f"{self.serial7s_score}/5"

    def finish_serial7s(self):
        """Display Serial 7s score."""
        screen = self.root.get_screen('serial7sscore')
        screen.serial7s_score = f"{self.serial7s_score}/5"

    # ========================================================================
    # DIGIT SPAN TEST
    # ========================================================================

    def setup_digit_span(self):
        """Generate digit sequences for digit span test."""
        # Forward digits - start with 3 digits
        self.forward_digits = [random.randint(1, 9) for _ in range(5)]
        # Backward digits - start with 2 digits
        self.backward_digits = [random.randint(1, 9) for _ in range(4)]

    def get_forward_digits(self, level):
        """Get forward digit sequence for given level."""
        return ' - '.join(str(d) for d in self.forward_digits[:level])

    def get_backward_digits(self, level):
        """Get backward digit sequence for given level."""
        return ' - '.join(str(d) for d in self.backward_digits[:level])

    def check_forward_digits(self, user_input, level):
        """Check forward digit recall."""
        user_digits = [d.strip() for d in user_input.replace('-', ' ').replace(',', ' ').split() if d.strip().isdigit()]
        correct_digits = [str(d) for d in self.forward_digits[:level]]

        if user_digits == correct_digits:
            self.digit_span_forward_score += 1
            return True
        return False

    def check_backward_digits(self, user_input, level):
        """Check backward digit recall."""
        user_digits = [d.strip() for d in user_input.replace('-', ' ').replace(',', ' ').split() if d.strip().isdigit()]
        correct_digits = [str(d) for d in reversed(self.backward_digits[:level])]

        if user_digits == correct_digits:
            self.digit_span_backward_score += 1
            return True
        return False

    def handle_forward_submit(self, user_input):
        """Handle forward digit span submission."""
        screen = self.root.get_screen('digitspanforward')
        level = screen.current_level
        passed = self.check_forward_digits(user_input, level)

        if passed and level < 4:
            screen.current_level = level + 1
            screen.digits_to_remember = self.get_forward_digits(screen.current_level)
        else:
            backward_screen = self.root.get_screen('digitspanbackward')
            backward_screen.digits_to_remember = self.get_backward_digits(2)
            backward_screen.current_level = 2
            self.root.current = "digitspanbackward"

    def handle_backward_submit(self, user_input):
        """Handle backward digit span submission."""
        screen = self.root.get_screen('digitspanbackward')
        level = screen.current_level
        passed = self.check_backward_digits(user_input, level)

        if passed and level < 3:
            screen.current_level = level + 1
            screen.digits_to_remember = self.get_backward_digits(screen.current_level)
        else:
            self.finish_digit_span()
            self.root.current = "digitspanscore"

    def handle_stroop_button(self, color):
        """Handle Stroop test button press."""
        has_more = self.check_stroop_answer(color)
        if not has_more:
            self.finish_stroop()
            self.root.current = "stroopscore"

    def handle_orientation_submit(self, answer):
        """Handle orientation answer submission."""
        has_more = self.check_orientation_answer(answer)
        if not has_more:
            self.finish_orientation()
            self.root.current = "orientationscore"

    def finish_digit_span(self):
        """Calculate and display digit span score."""
        total = self.digit_span_forward_score + self.digit_span_backward_score
        # Max 2 points for forward (levels 3,4), 2 points for backward (levels 2,3)
        screen = self.root.get_screen('digitspanscore')
        screen.digit_span_score = f"{min(total, 4)}/4"

    # ========================================================================
    # CATEGORY FLUENCY TEST
    # ========================================================================

    def start_fluency_timer(self, duration=60):
        """Start the 60-second fluency timer."""
        screen = self.root.get_screen('categoryfluency')
        screen.timer = str(duration)

        def update_timer(dt):
            current = int(screen.timer)
            if current > 0:
                screen.timer = str(current - 1)
            else:
                self.fluency_timer_event.cancel()
                self.finish_fluency()
                self.root.current = 'fluencyscore'

        self.fluency_timer_event = Clock.schedule_interval(update_timer, 1)

    def cancel_fluency_timer(self):
        """Cancel fluency timer."""
        if self.fluency_timer_event:
            self.fluency_timer_event.cancel()
            self.fluency_timer_event = None

    def add_animal(self, animal):
        """Add an animal to the list."""
        animal = animal.strip().lower()
        if animal and animal not in self.animals_entered and len(animal) > 1:
            self.animals_entered.append(animal)
            # Update display properties
            self.animals_count_text = str(len(self.animals_entered))
            self.recent_animals_text = ", ".join(self.animals_entered[-5:])

    def finish_fluency(self):
        """Calculate and display fluency score."""
        count = len(self.animals_entered)

        # Scoring based on normative data:
        # 15+ animals = 3 points
        # 10-14 animals = 2 points
        # 5-9 animals = 1 point
        # <5 animals = 0 points
        if count >= 15:
            self.fluency_score = 3
        elif count >= 10:
            self.fluency_score = 2
        elif count >= 5:
            self.fluency_score = 1
        else:
            self.fluency_score = 0

        screen = self.root.get_screen('fluencyscore')
        screen.fluency_score = f"{self.fluency_score}/3"
        screen.animals_count = str(count)

    # ========================================================================
    # STROOP TEST
    # ========================================================================

    def setup_stroop_test(self):
        """Set up Stroop test trials."""
        colors = {
            'red': [1, 0.2, 0.2, 1],
            'blue': [0.2, 0.4, 1, 1],
            'green': [0.2, 0.8, 0.2, 1],
            'yellow': [0.9, 0.9, 0.2, 1]
        }

        color_names = list(colors.keys())

        # Create 10 trials - mix of congruent and incongruent
        self.stroop_trials = []
        for i in range(10):
            word = random.choice(color_names)
            # 70% incongruent trials (word doesn't match ink color)
            if random.random() < 0.7:
                ink_color = random.choice([c for c in color_names if c != word])
            else:
                ink_color = word

            self.stroop_trials.append({
                'word': word.upper(),
                'ink_color': ink_color,
                'color_rgba': colors[ink_color]
            })

        self.stroop_current_trial = 0
        self.stroop_correct = 0

    def get_current_stroop_trial(self):
        """Get current Stroop trial data."""
        if self.stroop_current_trial < len(self.stroop_trials):
            return self.stroop_trials[self.stroop_current_trial]
        return None

    def start_stroop_timer(self, duration=30):
        """Start Stroop test timer."""
        screen = self.root.get_screen('strooptest')
        screen.timer = str(duration)

        def update_timer(dt):
            current = int(screen.timer)
            if current > 0:
                screen.timer = str(current - 1)
            else:
                self.stroop_timer_event.cancel()
                self.finish_stroop()
                self.root.current = 'stroopscore'

        self.stroop_timer_event = Clock.schedule_interval(update_timer, 1)

    def cancel_stroop_timer(self):
        """Cancel Stroop timer."""
        if self.stroop_timer_event:
            self.stroop_timer_event.cancel()
            self.stroop_timer_event = None

    def check_stroop_answer(self, user_answer):
        """Check Stroop test answer and advance to next trial."""
        trial = self.get_current_stroop_trial()
        if trial:
            correct_color = trial['ink_color'].lower()
            if user_answer.strip().lower() == correct_color:
                self.stroop_correct += 1

        self.stroop_current_trial += 1

        # Update display for next trial
        screen = self.root.get_screen('strooptest')
        next_trial = self.get_current_stroop_trial()

        if next_trial:
            screen.word_text = next_trial['word']
            screen.word_color = next_trial['color_rgba']
            screen.trial_number = self.stroop_current_trial + 1
            return True  # More trials
        else:
            # All trials complete
            self.cancel_stroop_timer()
            return False

    def finish_stroop(self):
        """Calculate and display Stroop score."""
        # Score based on correct answers out of 10 trials
        # 9-10 correct = 5 points
        # 7-8 correct = 4 points
        # 5-6 correct = 3 points
        # 3-4 correct = 2 points
        # 1-2 correct = 1 point
        # 0 correct = 0 points

        if self.stroop_correct >= 9:
            self.stroop_score = 5
        elif self.stroop_correct >= 7:
            self.stroop_score = 4
        elif self.stroop_correct >= 5:
            self.stroop_score = 3
        elif self.stroop_correct >= 3:
            self.stroop_score = 2
        elif self.stroop_correct >= 1:
            self.stroop_score = 1
        else:
            self.stroop_score = 0

        screen = self.root.get_screen('stroopscore')
        screen.stroop_score = f"{self.stroop_score}/5"

    # ========================================================================
    # DELAYED WORD RECALL
    # ========================================================================

    def calculate_delayed_recall(self, input_words):
        """Calculate score for delayed word recall."""
        words_list = input_words.lower().replace(',', ' ').split()

        for word in words_list:
            word = word.strip()
            if word in [w.lower() for w in self.words] and word not in self.checked_words_delayed:
                self.delayed_recall_score += 1
                self.checked_words_delayed.append(word)

        return f"{self.delayed_recall_score}/5"

    def finish_delayed_recall(self):
        """Display delayed recall score."""
        screen = self.root.get_screen('delayedrecallscore')
        screen.delayed_score = f"{self.delayed_recall_score}/5"

    # ========================================================================
    # FINAL RESULTS
    # ========================================================================

    def calculate_final_results(self):
        """Calculate and display final assessment results."""
        # Calculate total raw score (out of 32)
        raw_total = (
            self.orientation_score +           # 0-5
            self.immediate_recall_score +      # 0-5
            self.serial7s_score +              # 0-5
            min(self.digit_span_forward_score + self.digit_span_backward_score, 4) +  # 0-4
            self.fluency_score +               # 0-3
            self.stroop_score +                # 0-5
            self.delayed_recall_score          # 0-5
        )

        # Normalize to 30-point scale (similar to MoCA)
        normalized_score = round((raw_total / 32) * 30)

        # Determine category and interpretation
        if normalized_score >= 26:
            category = "Normal Cognition"
            interpretation = (
                "Your cognitive assessment results fall within the normal range. "
                "This suggests that your cognitive functions, including memory, attention, "
                "and executive function, are performing as expected for a healthy individual. "
                "Continue maintaining a healthy lifestyle with regular physical activity, "
                "mental stimulation, social engagement, and adequate sleep."
            )
        elif normalized_score >= 18:
            category = "Mild Cognitive Impairment"
            interpretation = (
                "Your results suggest possible mild cognitive impairment (MCI). "
                "MCI represents a stage between normal age-related cognitive changes and "
                "more serious decline. Not everyone with MCI develops dementia. "
                "We strongly recommend consulting with a healthcare provider for a "
                "comprehensive clinical evaluation. Early intervention and lifestyle "
                "modifications may help maintain cognitive function."
            )
        elif normalized_score >= 10:
            category = "Moderate Cognitive Impairment"
            interpretation = (
                "Your results indicate moderate cognitive difficulties across several domains. "
                "This level of impairment typically affects daily functioning and independence. "
                "It is important to seek medical evaluation promptly. A healthcare professional "
                "can conduct additional testing, identify potential causes, and discuss "
                "treatment options and support services."
            )
        else:
            category = "Severe Cognitive Impairment"
            interpretation = (
                "Your results suggest significant cognitive impairment. "
                "This level of difficulty typically has substantial impact on daily activities "
                "and may require assistance with various tasks. "
                "Please seek immediate medical evaluation. A healthcare team can provide "
                "comprehensive assessment, determine underlying causes, and develop an "
                "appropriate care plan."
            )

        # Update results screen
        screen = self.root.get_screen('results')
        screen.total_score = f"{normalized_score}/30"
        screen.score_category = category
        screen.interpretation = interpretation

        # Store for reference
        self.final_score = normalized_score
        self.final_category = category

    def get_score_breakdown(self):
        """Get detailed score breakdown string."""
        return (
            f"Orientation: {self.orientation_score}/5\n"
            f"Immediate Recall: {self.immediate_recall_score}/5\n"
            f"Serial 7s: {self.serial7s_score}/5\n"
            f"Digit Span: {min(self.digit_span_forward_score + self.digit_span_backward_score, 4)}/4\n"
            f"Category Fluency: {self.fluency_score}/3\n"
            f"Stroop Test: {self.stroop_score}/5\n"
            f"Delayed Recall: {self.delayed_recall_score}/5"
        )

    def restart_assessment(self):
        """Reset all scores and restart the assessment."""
        # Reset all scores
        self.orientation_score = 0
        self.immediate_recall_score = 0
        self.serial7s_score = 0
        self.digit_span_forward_score = 0
        self.digit_span_backward_score = 0
        self.fluency_score = 0
        self.stroop_score = 0
        self.delayed_recall_score = 0

        # Reset state variables
        self.checked_words_immediate = []
        self.checked_words_delayed = []
        self.checked_numbers = []
        self.current_orientation_index = 0
        self.animals_entered = []
        self.stroop_current_trial = 0
        self.stroop_correct = 0

        # Reset display properties
        self.recent_animals_text = "None yet"
        self.animals_count_text = "0"

        # Reinitialize tests with new data
        self.initialize_tests()

        # Update word display
        self.on_start()

        # Go back to title screen
        self.root.current = 'title'


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    DementiaDiagnosisApp().run()
