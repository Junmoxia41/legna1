from memory.detectors.detector import Detector

from models.memory_evaluation import MemoryEvaluation


class RepetitionDetector(Detector):

    def detect(self, message):

        evaluations = []

        message = message.lower()

        # =====================================================
        # DETECTION
        # =====================================================



        # =====================================================
        # POST PROCESS
        # =====================================================



        # =====================================================
        # RESULT
        # =====================================================

        return evaluations