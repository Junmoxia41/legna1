from memory.detectors.detector import Detector
from models.memory_evaluation import MemoryEvaluation
from memory.language import COMMAND_PATTERNS

class CommandDetector(Detector):
    def detect(self, segment):
        evaluations = []
        segment_lower = segment.lower().strip()

        for trigger in COMMAND_PATTERNS:
            if segment_lower.startswith(trigger):
                # Extraemos el resto del comando como contenido
                content = segment_lower[len(trigger):].strip()
                
                evaluations.append(
                    MemoryEvaluation(
                        should_save=False, # Los comandos usualmente no se guardan como recuerdos permanentes por defecto
                        importance=5,
                        confidence=10,
                        persistence=0,
                        detector="command",
                        memory_type="command",
                        category="action",
                        canonical_key=f"command:{trigger}",
                        content=content,
                        reason=f"Comando detectado: {trigger}"
                    )
                )
                # Una vez que detectamos un comando en este segmento, solemos parar
                break

        return evaluations
