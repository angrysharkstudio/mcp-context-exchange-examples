"""
MCP Context Server Implementation
Manages context exchange between different AI models
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import asyncio
from dataclasses import dataclass, asdict, field


@dataclass
class ContextEntry:
    """Represents a single context entry from a model"""
    model: str
    timestamp: str
    content: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)


@dataclass
class SharedContext:
    """Manages shared context between models"""
    conversations: List[ContextEntry] = field(default_factory=list)
    tool_outputs: List[Dict[str, Any]] = field(default_factory=list)
    discovered_info: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "conversations": [c.to_dict() for c in self.conversations],
            "tool_outputs": self.tool_outputs,
            "discovered_info": self.discovered_info
        }


class ContextServer:
    """MCP server for managing context exchange between AI models"""
    
    def __init__(self):
        self.shared_context = SharedContext()
        self._lock = asyncio.Lock()
    
    async def store_context(self, model: str, context: Dict[str, Any]) -> None:
        """Store context from one model for others to use"""
        async with self._lock:
            entry = ContextEntry(
                model=model,
                timestamp=datetime.now().isoformat(),
                content=context
            )
            self.shared_context.conversations.append(entry)
            
            # Extract key information for quick access
            if "discoveries" in context:
                self.shared_context.discovered_info.update(context["discoveries"])
            
            # Store tool outputs if present
            if "tool_outputs" in context:
                self.shared_context.tool_outputs.extend(context["tool_outputs"])
    
    async def get_context(self, for_model: str, max_entries: int = 10) -> Dict[str, Any]:
        """Retrieve relevant context for a specific model"""
        async with self._lock:
            # Get recent conversations from other models
            other_conversations = [
                conv for conv in self.shared_context.conversations
                if conv.model != for_model
            ][-max_entries:]
            
            # Format context for consumption
            relevant_context = {
                "previous_analysis": self._format_previous_analysis(other_conversations),
                "key_findings": dict(self.shared_context.discovered_info),
                "recent_tool_outputs": self.shared_context.tool_outputs[-10:]
            }
            
            return relevant_context
    
    def _format_previous_analysis(self, conversations: List[ContextEntry]) -> List[Dict[str, Any]]:
        """Format previous analysis for easy consumption"""
        formatted = []
        for conv in conversations:
            formatted.append({
                "model": conv.model,
                "timestamp": conv.timestamp,
                "summary": conv.content.get("summary", ""),
                "findings": conv.content.get("findings", []),
                "suggestions": conv.content.get("suggestions", [])
            })
        return formatted
    
    async def clear_context(self) -> None:
        """Clear all stored context"""
        async with self._lock:
            self.shared_context = SharedContext()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the current context state"""
        return {
            "total_conversations": len(self.shared_context.conversations),
            "models_involved": list(set(c.model for c in self.shared_context.conversations)),
            "discoveries_count": len(self.shared_context.discovered_info),
            "tool_outputs_count": len(self.shared_context.tool_outputs)
        }
    
    async def export_context(self, filepath: str) -> None:
        """Export context to a JSON file for debugging or persistence"""
        async with self._lock:
            with open(filepath, 'w') as f:
                json.dump(self.shared_context.to_dict(), f, indent=2)
    
    async def import_context(self, filepath: str) -> None:
        """Import context from a JSON file"""
        async with self._lock:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Reconstruct context from data
            self.shared_context = SharedContext(
                conversations=[
                    ContextEntry(**conv) for conv in data.get("conversations", [])
                ],
                tool_outputs=data.get("tool_outputs", []),
                discovered_info=data.get("discovered_info", {})
            )