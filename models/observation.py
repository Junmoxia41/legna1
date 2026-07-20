from datetime import datetime


class Observation:

    def __init__(

        self,

        detector,

        memory_type,

        category,

        canonical_key,

        content,

        importance,

        confidence,

        polarity=None,

        persistence=0,

        timestamp=None,

        observation_id=None

    ):

        self.id = observation_id

        self.detector = detector

        self.memory_type = memory_type

        self.category = category

        self.canonical_key = canonical_key

        self.content = content

        self.importance = importance

        self.confidence = confidence

        self.polarity = polarity

        self.persistence = persistence

        self.timestamp = timestamp or datetime.now()

    @classmethod
    def from_evaluation(cls, evaluation):

        return cls(

            detector=evaluation.detector,

            memory_type=evaluation.memory_type,

            category=evaluation.category,

            canonical_key=evaluation.canonical_key,

            content=evaluation.content,

            importance=evaluation.importance,

            confidence=evaluation.confidence,

            polarity=evaluation.polarity,

            persistence=evaluation.persistence

        )