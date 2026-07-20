from memory.detector_registry import load_detectors
from memory.text_extractor import TextExtractor


class KnowledgeEngine:

    def __init__(self):

        self.detectors = load_detectors()

    def extract(self, message):

        evaluations = []

        segments = TextExtractor.split_segments(message)

        for segment in segments:

            for detector in self.detectors:

                evaluations.extend(

                    detector.detect(segment)

                )

        return evaluations