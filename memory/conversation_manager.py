"""
Conversation Manager - Legna v2.0
Persists full conversation history (messages, context, summaries)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class ConversationManager:
    def __init__(self, storage_path="/home/user/legna1/database/conversations.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.conversations = self._load()

    def _load(self) -> Dict:
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"conversations": []}

    def _save(self):
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.conversations, f, indent=2, ensure_ascii=False)

    def create_conversation(self, title: str = None) -> Dict:
        """Create a new conversation"""
        conv_id = f"conv_{int(datetime.now().timestamp())}"
        
        conversation = {
            "id": conv_id,
            "title": title or f"Conversación {datetime.now().strftime('%d/%m %H:%M')}",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "message_count": 0,
            "messages": [],
            "context_summary": "",
            "tags": []
        }
        
        self.conversations["conversations"].append(conversation)
        self._save()
        return conversation

    def add_message(self, conv_id: str, role: str, content: str):
        """Add a message to an existing conversation"""
        for conv in self.conversations["conversations"]:
            if conv["id"] == conv_id:
                conv["messages"].append({
                    "role": role,           # "user" or "legna"
                    "content": content,
                    "timestamp": datetime.now().isoformat()
                })
                conv["message_count"] = len(conv["messages"])
                conv["last_updated"] = datetime.now().isoformat()
                
                # Auto-generate title from first user message
                if conv["message_count"] == 1 and role == "user":
                    conv["title"] = content[:50] + ("..." if len(content) > 50 else "")
                
                self._save()
                return conv
        return None

    def get_conversation(self, conv_id: str) -> Optional[Dict]:
        for conv in self.conversations["conversations"]:
            if conv["id"] == conv_id:
                return conv
        return None

    def get_all_conversations(self, limit: int = 20) -> List[Dict]:
        """Return most recent conversations"""
        sorted_convs = sorted(
            self.conversations["conversations"],
            key=lambda x: x["last_updated"],
            reverse=True
        )
        return sorted_convs[:limit]

    def update_context_summary(self, conv_id: str, summary: str):
        for conv in self.conversations["conversations"]:
            if conv["id"] == conv_id:
                conv["context_summary"] = summary
                self._save()
                return True
        return False

    def delete_conversation(self, conv_id: str):
        self.conversations["conversations"] = [
            c for c in self.conversations["conversations"] if c["id"] != conv_id
        ]
        self._save()
