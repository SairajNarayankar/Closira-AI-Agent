"""
Conversation logging utilities for audit and debugging.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


class ConversationLogger:
    """Logs conversation history and escalations for audit purposes."""
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize logger.
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.conversation_history: List[Dict[str, Any]] = []
        self.escalations: List[Dict[str, Any]] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def log_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """
        Log a conversation message.
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
            metadata: Additional metadata (stage, confidence, etc.)
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        self.conversation_history.append(entry)
    
    def log_escalation(self, reason: str, context: Dict[str, Any] = None):
        """
        Log an escalation event.
        
        Args:
            reason: Reason for escalation
            context: Additional context about the escalation
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "context": context or {},
            "conversation_length": len(self.conversation_history)
        }
        self.escalations.append(entry)
        print(f"\n🚨 ESCALATION LOGGED: {reason}")
    
    def save_conversation(self, filename: str = None):
        """
        Save conversation history to file.
        
        Args:
            filename: Optional custom filename
        """
        if filename is None:
            filename = f"conversation_{self.session_id}.json"
        
        filepath = self.log_dir / filename
        
        data = {
            "session_id": self.session_id,
            "conversation_history": self.conversation_history,
            "escalations": self.escalations,
            "total_messages": len(self.conversation_history),
            "total_escalations": len(self.escalations)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Conversation saved to: {filepath}")
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the conversation.
        
        Returns:
            Dict with conversation statistics
        """
        user_messages = [m for m in self.conversation_history if m["role"] == "user"]
        assistant_messages = [m for m in self.conversation_history if m["role"] == "assistant"]
        
        return {
            "session_id": self.session_id,
            "total_messages": len(self.conversation_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "escalations": len(self.escalations),
            "duration": self._calculate_duration()
        }
    
    def _calculate_duration(self) -> str:
        """Calculate conversation duration."""
        if len(self.conversation_history) < 2:
            return "0 seconds"
        
        start = datetime.fromisoformat(self.conversation_history[0]["timestamp"])
        end = datetime.fromisoformat(self.conversation_history[-1]["timestamp"])
        duration = (end - start).total_seconds()
        
        if duration < 60:
            return f"{int(duration)} seconds"
        else:
            return f"{int(duration / 60)} minutes {int(duration % 60)} seconds"
    
    def print_summary(self):
        """Print conversation summary to console."""
        summary = self.get_conversation_summary()
        print("\n" + "="*50)
        print("CONVERSATION SUMMARY")
        print("="*50)
        print(f"Session ID: {summary['session_id']}")
        print(f"Total Messages: {summary['total_messages']}")
        print(f"User Messages: {summary['user_messages']}")
        print(f"Assistant Messages: {summary['assistant_messages']}")
        print(f"Escalations: {summary['escalations']}")
        print(f"Duration: {summary['duration']}")
        print("="*50 + "\n")


