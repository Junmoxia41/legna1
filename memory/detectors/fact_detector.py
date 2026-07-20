from memory.detectors.detector import Detector

from models.memory_evaluation import MemoryEvaluation

from memory.text_extractor import TextExtractor

from memory.language import FACT_PATTERNS


class FactDetector(Detector):

    def detect(self, segment):

        evaluations = []

        segment = segment.lower()

        for trigger in FACT_PATTERNS:

            if segment.startswith(trigger):

                content = segment[len(trigger):].strip()

                facts = TextExtractor.split_items(content)

                for fact in facts:

                    evaluations.append(

                        MemoryEvaluation(

                            should_save=True,

                            importance=3,

                            confidence=8,

                            persistence=4,

                            detector="fact",

                            memory_type="fact",

                            category="personal",

                            canonical_key=f"personal:{fact}",

                            content=fact,

                            reason="Posible hecho personal detectado."

                        )

                    )

        return evaluations