from models.observation import Observation


class ShortTermMemory:

    def __init__(self, database):

        self.database = database

    # =========================================================
    # OBSERVATIONS
    # =========================================================

    def record(self, evaluations):

        for evaluation in evaluations:

            if not evaluation.should_save:
                continue

            observation = Observation.from_evaluation(
                evaluation
            )

            self.database.save_observation(
                observation
            )

    def load(self):

        return self.database.load_observations()

    def remove(self, observation_id):

        self.database.remove_observation(
            observation_id
        )

    def clear_expired(self):

        self.database.clear_expired_observations()