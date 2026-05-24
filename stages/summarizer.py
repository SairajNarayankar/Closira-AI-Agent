"""
Stage 4: Conversation Summary
Generates structured summaries of customer conversations.
"""

import json
from typing import Dict, Any, List
from utils.openai_client import OpenAIClient
from prompts.system_prompts import get_system_prompt, SUMMARY_PROMPT


class ConversationSummarizer:
    """Generates structured conversation summaries."""
    
    def __init__(self, sop_data: Dict[str, Any], openai_client: OpenAIClient):
        """
        Initialize conversation summarizer.
        
        Args:
            sop_data: SOP data dictionary
            openai_client: OpenAI client instance
        """
        self.sop_data = sop_data
        self.client = openai_client
        self.system_prompt = get_system_prompt(json.dumps(sop_data, indent=2))
    
    def generate_summary(
        self,
        conversation_history: list,
        escalation_info: Dict[str, Any] = None,
        qualification_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive conversation summary.
        
        Args:
            conversation_history: Full conversation history
            escalation_info: Information about any escalations
            qualification_data: Data collected during lead qualification
        
        Returns:
            Dict with structured summary
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": SUMMARY_PROMPT}
        ]
        
        # Add full conversation history
        messages.extend(conversation_history)
        
        # Add context about escalations and qualification
        context = self._build_context(escalation_info, qualification_data)
        if context:
            messages.append({
                "role": "system",
                "content": f"Additional context: {json.dumps(context, indent=2)}"
            })
        
        # Get summary from OpenAI
        response = self.client.chat_completion(
            messages=messages,
            temperature=0.3,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )
        
        if "error" in response:
            return self._create_fallback_summary(conversation_history, escalation_info)
        
        try:
            result = response["content"]
            
            # Ensure summary structure is complete
            if "summary" not in result:
                result["summary"] = self._extract_basic_summary(conversation_history)
            
            # Add metadata
            result["metadata"] = {
                "total_messages": len(conversation_history),
                "user_messages": len([m for m in conversation_history if m["role"] == "user"]),
                "assistant_messages": len([m for m in conversation_history if m["role"] == "assistant"]),
                "escalated": escalation_info is not None if escalation_info else False
            }
            
            return result
            
        except (json.JSONDecodeError, KeyError) as e:
            return self._create_fallback_summary(conversation_history, escalation_info)
    
    def _build_context(
        self,
        escalation_info: Dict[str, Any] = None,
        qualification_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Build additional context for summary generation."""
        context = {}
        
        if escalation_info:
            context["escalation"] = {
                "occurred": True,
                "reasons": escalation_info.get("escalation_reasons", []),
                "primary_reason": escalation_info.get("primary_reason", "Unknown")
            }
        
        if qualification_data:
            context["qualification"] = {
                "completed": qualification_data.get("qualification_complete", False),
                "data_collected": qualification_data.get("data_collected", {})
            }
        
        return context
    
    def _extract_basic_summary(self, conversation_history: list) -> Dict[str, Any]:
        """Extract basic summary information from conversation history."""
        user_messages = [m for m in conversation_history if m["role"] == "user"]
        
        # Extract questions
        questions = [
            msg["content"] for msg in user_messages
            if "?" in msg["content"]
        ]
        
        # Identify intent from first message
        intent = "General inquiry"
        if user_messages:
            first_message = user_messages[0]["content"].lower()
            if any(word in first_message for word in ["price", "cost"]):
                intent = "Pricing inquiry"
            elif any(word in first_message for word in ["book", "appointment"]):
                intent = "Booking request"
            elif any(word in first_message for word in ["hour", "open"]):
                intent = "Business hours inquiry"
        
        return {
            "customer_intent": intent,
            "key_details": {},
            "questions_asked": questions[:5],  # First 5 questions
            "answers_provided": [],
            "sop_gaps": [],
            "escalation_status": "No escalation",
            "recommended_next_action": "Follow up if customer showed interest"
        }
    
    def _create_fallback_summary(
        self,
        conversation_history: list,
        escalation_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a fallback summary when AI generation fails."""
        basic_summary = self._extract_basic_summary(conversation_history)
        
        if escalation_info:
            basic_summary["escalation_status"] = f"Escalated: {escalation_info.get('primary_reason', 'Unknown reason')}"
        
        return {
            "response": "Thank you for contacting Bloom Aesthetics. A summary of our conversation has been recorded.",
            "confidence": 1.0,
            "stage": "summary",
            "escalation_needed": False,
            "summary": basic_summary,
            "metadata": {
                "total_messages": len(conversation_history),
                "generation_method": "fallback"
            }
        }
    
    def format_summary_for_display(self, summary: Dict[str, Any]) -> str:
        """
        Format summary for human-readable display.
        
        Args:
            summary: Summary dictionary
        
        Returns:
            Formatted string
        """
        if "summary" not in summary:
            return "Summary not available"
        
        s = summary["summary"]
        
        output = []
        output.append("=" * 60)
        output.append("CONVERSATION SUMMARY")
        output.append("=" * 60)
        output.append(f"\nCustomer Intent: {s.get('customer_intent', 'Unknown')}")
        
        if s.get("key_details"):
            output.append("\nKey Details Collected:")
            for key, value in s["key_details"].items():
                output.append(f"  - {key}: {value}")
        
        if s.get("questions_asked"):
            output.append("\nQuestions Asked:")
            for i, q in enumerate(s["questions_asked"][:5], 1):
                output.append(f"  {i}. {q}")
        
        if s.get("sop_gaps"):
            output.append("\nSOP Gaps Identified:")
            for gap in s["sop_gaps"]:
                output.append(f"  - {gap}")
        
        output.append(f"\nEscalation Status: {s.get('escalation_status', 'None')}")
        output.append(f"\nRecommended Next Action: {s.get('recommended_next_action', 'None')}")
        output.append("=" * 60)
        
        return "\n".join(output)

