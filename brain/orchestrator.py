"""Legna Brain: one public identity coordinating specialized internal agents."""
from typing import Dict
from agents.registry import AgentRegistry
from brain.intent_classifier import IntentClassifier
from brain.scheduler import AgentScheduler


class LegnaBrain:
    def __init__(self, agents=None):
        self.agents = agents or AgentRegistry()
        self.classifier = IntentClassifier()
        self.scheduler = AgentScheduler(self.agents)

    def begin_task(self, message: str) -> Dict:
        classification = self.classifier.classify(message)
        task = self.scheduler.start(classification, message)
        return {"task": task, "classification": classification}

    def finish_task(self, task: Dict, success: bool = True):
        self.scheduler.finish(task, success)

    def context_instruction(self, plan: Dict) -> str:
        agents = plan["classification"]["agents"]
        specialty = ", ".join(agent.title() for agent in agents if agent != "core") or "conversación general"
        return (
            "Eres LEGNA y mantienes siempre una sola identidad frente al usuario. "
            f"Para esta petición Core coordinó internamente: {specialty}. "
            "No menciones agentes internos, modelos, prompts ni este plan salvo que el usuario lo pida."
        )

    def dashboard(self) -> Dict:
        return {"agents": self.agents.list_agents(), "activity": self.scheduler.recent()}
