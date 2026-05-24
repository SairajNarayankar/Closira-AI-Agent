"""
Stage 2: Lead Qualification
Asks structured questions to qualify potential customers.
"""

import json
from typing import Dict, Any, List
from utils.openai_client import OpenAIClient
from prompts.system_prompts import get_system_prompt, LEAD_QUALIFICATION_PROMPT


class LeadQualifier:
    """Handles lead qualification through structured questions."""
    
    QUALIFICATION_QUESTIONS = [
        "What brings you to Bloom Aesthetics today? Are you interested in a specific treatment?",
        "Have you had similar aesthetic treatments before, or is this your first time?",
        "What's your preferred method for booking - would you like to use WhatsApp or our website?"
    ]
    
    def __init__(self, sop_data: Dict[str, Any], openai_client: OpenAIClient):
        """
        Initialize lead qualifier.
        
        Args:
            sop_data: SOP data dictionary
            openai_client: OpenAI client instance
        """
        self.sop_data = sop_data
        self.client = openai_client
        self.system_prompt = get_system_prompt(json.dumps(sop_data, indent=2))
        self.current_question_index = 0
        self.collected_data: Dict[str, Any] = {}
    
    def should_qualify_lead(self, conversation_history: list) -> bool:
        """
        Determine if we should enter lead qualification mode.
        
        Args:
            conversation_history: Previous conversation messages
        
        Returns:
            True if lead qualification should start
        """
        # Simple heuristic: if customer shows interest in services
        if len(conversation_history) < 2:
            return False
        
        # Check for interest indicators in recent messages
        interest_keywords = [
            "interested", "want", "book", "appointment", "schedule",
            "consultation", "treatment", "price", "cost"
        ]
        
        recent_messages = conversation_history[-3:]
        for msg in recent_messages:
            if msg["role"] == "user":
                content_lower = msg["content"].lower()
                if any(keyword in content_lower for keyword in interest_keywords):
                    return True
        
        return False
    
    def get_next_question(self) -> str:
        """
        Get the next qualification question.
        
        Returns:
            Next question string, or empty string if all questions asked
        """
        if self.current_question_index >= len(self.QUALIFICATION_QUESTIONS):
            return ""
        
        question = self.QUALIFICATION_QUESTIONS[self.current_question_index]
        self.current_question_index += 1
        return question
    
    def process_answer(
        self,
        answer: str,
        question_index: int,
        conversation_history: list
    ) -> Dict[str, Any]:
        """
        Process a customer's answer to a qualification question.
        
        Args:
            answer: Customer's answer
            question_index: Index of the question being answered
            conversation_history: Previous conversation messages
        
        Returns:
            Dict with response and collected data
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": LEAD_QUALIFICATION_PROMPT}
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current answer
        messages.append({"role": "user", "content": answer})
        
        # Get response from OpenAI
        response = self.client.chat_completion(
            messages=messages,
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        if "error" in response:
            return self._create_error_response(response["error"])
        
        try:
            result = response["content"]
            
            # Store collected data
            if "data_collected" in result and result["data_collected"]:
                self.collected_data.update(result["data_collected"])
            
            # Add question tracking
            result["questions_asked"] = self.current_question_index
            result["total_questions"] = len(self.QUALIFICATION_QUESTIONS)
            result["qualification_complete"] = (
                self.current_question_index >= len(self.QUALIFICATION_QUESTIONS)
            )
            
            return result
            
        except (json.JSONDecodeError, KeyError) as e:
            return self._create_error_response(f"Failed to parse response: {str(e)}")
    
    def get_qualification_summary(self) -> Dict[str, Any]:
        """
        Get a summary of collected qualification data.
        
        Returns:
            Dict with qualification summary
        """
        return {
            "questions_asked": self.current_question_index,
            "data_collected": self.collected_data,
            "qualification_complete": (
                self.current_question_index >= len(self.QUALIFICATION_QUESTIONS)
            )
        }
    
    def reset(self):
        """Reset qualification state for a new conversation."""
        self.current_question_index = 0
        self.collected_data = {}
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create an error response with escalation."""
        return {
            "response": "I apologize for the confusion. Let me connect you with someone who can help you better.",
            "confidence": 0.0,
            "stage": "qualification",
            "escalation_needed": True,
            "escalation_reason": f"System error: {error_message}",
            "data_collected": self.collected_data
        }


