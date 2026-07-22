"""Declarative agent registry. Agents share Legna's identity and memory."""
from copy import deepcopy

AGENT_DEFINITIONS = (
    {"id": "core", "name": "Core", "role": "Orquestación y respuesta final", "preferred_model": "general", "tools": ["chat", "memory"], "priority": 100},
    {"id": "planner", "name": "Planner", "role": "Planificación, objetivos y seguimiento", "preferred_model": "general", "tools": ["memory", "projects"], "priority": 70},
    {"id": "code", "name": "Code", "role": "Código, revisión y depuración", "preferred_model": "code", "tools": ["workspace"], "priority": 80},
    {"id": "memory", "name": "Memory", "role": "Memoria, contexto y aprendizaje", "preferred_model": "local", "tools": ["memory"], "priority": 90},
    {"id": "research", "name": "Research", "role": "Documentos y síntesis de información", "preferred_model": "general", "tools": ["documents"], "priority": 60},
    {"id": "system", "name": "System", "role": "Telemetría y diagnóstico local", "preferred_model": "local", "tools": ["system_read"], "priority": 50},
    {"id": "vision", "name": "Vision", "role": "Análisis de imágenes cuando haya modelo compatible", "preferred_model": "vision", "tools": ["images"], "priority": 40},
    {"id": "documents", "name": "Documents", "role": "Extracción, resumen y clasificación documental", "preferred_model": "general", "tools": ["documents"], "priority": 65},
    {"id": "data", "name": "Data", "role": "Tablas, datos y análisis estructurado", "preferred_model": "general", "tools": ["data_read"], "priority": 55},
    {"id": "quality", "name": "Quality", "role": "Validación de resultados y recuperación ante fallos", "preferred_model": "general", "tools": ["validation"], "priority": 85},
    {"id": "security", "name": "Security", "role": "Revisión de riesgos y permisos", "preferred_model": "general", "tools": ["policy"], "priority": 75},
)


class AgentRegistry:
    def __init__(self):
        self._states = {agent["id"]: "idle" for agent in AGENT_DEFINITIONS}

    def list_agents(self):
        agents = []
        for definition in AGENT_DEFINITIONS:
            agent = deepcopy(definition)
            agent["state"] = self._states[agent["id"]]
            agents.append(agent)
        return agents

    def set_state(self, agent_id: str, state: str):
        if agent_id not in self._states:
            raise ValueError("Agente no encontrado")
        if state not in {"idle", "thinking", "waiting", "switching", "error", "offline"}:
            raise ValueError("Estado de agente inválido")
        self._states[agent_id] = state
