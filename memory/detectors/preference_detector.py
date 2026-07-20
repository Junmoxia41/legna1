from models.memory_evaluation import MemoryEvaluation

from memory.detectors.detector import Detector

from memory.text_extractor import TextExtractor

from memory.language import PREFERENCE_KEYWORDS


class PreferenceDetector(Detector):

    def detect(self, segment):

        evaluations = []

        segment = segment.lower()

        negative_found = False

        # =====================================================
        # NEGATIVE PREFERENCES
        # =====================================================

        for keyword in PREFERENCE_KEYWORDS["negative"]:

            if segment.startswith(keyword):

                negative_found = True

                content = segment[len(keyword):].strip()

                preferences = TextExtractor.split_items(content)

                for preference in preferences:

                    evaluations.append(

                        MemoryEvaluation(

                            should_save=True,

                            importance=3,

                            confidence=8,

                            memory_type="preference",

                            detector="preference",

                            category="general",

                            canonical_key=f"general:{preference}",

                            polarity="negative",

                            content=preference,

                            reason="Posible preferencia negativa detectada."

                        )

                    )

        # =====================================================
        # POSITIVE PREFERENCES
        # =====================================================

        if not negative_found:

            for keyword in PREFERENCE_KEYWORDS["positive"]:

                if segment.startswith(keyword):

                    content = segment[len(keyword):].strip()

                    preferences = TextExtractor.split_items(content)

                    for preference in preferences:

                        evaluations.append(

                            MemoryEvaluation(

                                should_save=True,

                                importance=3,

                                confidence=8,

                                memory_type="preference",

                                detector="preference",

                                category="general",

                                canonical_key=f"general:{preference}",

                                polarity="positive",

                                content=preference,

                                reason="Posible preferencia detectada."

                            )

                        )

            

        return evaluations