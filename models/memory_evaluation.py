class MemoryEvaluation:

    def __init__(

        self,

        should_save=False,

        importance=0,

        confidence=10,

        persistence=0,

        memory_type=None,

        detector=None,

        category=None,

        canonical_key=None,

        polarity=None,

        content=None,

        reason="No se detectó información relevante."

    ):

        self.should_save = should_save

        self.importance = importance

        self.confidence = confidence

        self.persistence = persistence

        self.memory_type = memory_type

        self.detector = detector

        self.category = category

        self.canonical_key = canonical_key

        self.polarity = polarity

        self.content = content

        self.reason = reason