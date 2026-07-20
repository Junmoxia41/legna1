from memory.detectors.preference_detector import PreferenceDetector
from memory.detectors.fact_detector import FactDetector
from memory.detectors.goal_detector import GoalDetector
from memory.detectors.habit_detector import HabitDetector
from memory.detectors.contradiction_detector import ContradictionDetector
from memory.detectors.repetition_detector import RepetitionDetector


def load_detectors():

    return [

        PreferenceDetector(),

        FactDetector(),

        GoalDetector(),

        HabitDetector(),

        ContradictionDetector(),

        RepetitionDetector()

    ]