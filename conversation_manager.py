"""
Conversation Manager - Orchestrates the 4-stage AI workflow.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.openai_client import OpenAIClient
from utils.logger import ConversationLogger
from stages.faq_handler import FAQHandler
from stages.lead_qualifier import LeadQualifier
from stages.escalation import EscalationDetector
from stages.summarizer import ConversationSummarizer


class ConversationManager:
    """Manages the complete customer conversation workflow."""
    
    def __init__(self, sop_data_path: str, api_key: Optional[str] = None):
        """
        Initialize conversation manager.
        
        Args:
            sop_data_path: Path to SOP data JSON file
            api_key: OpenAI API key (optional, can use env var)
        """
        # Load SOP data
        with open(sop_data_path, 'r', encoding='utf-8') as f:
            self.sop_data = json.load(f)
        
        # Initialize OpenAI client
        self.client = OpenAIClient(api_key)
        
        # Initialize all stages
        self.faq_handler = FAQHandler(self.sop_data, self.client)
        self.lead_qualifier = LeadQualifier(self.sop_data, self.client)
        self.escalation_detector = EscalationDetector(self.sop_data, self.client)
        self.summarizer = ConversationSummarizer(self.sop_data, self.client)
        
        # Initialize logger
        self.logger = ConversationLogger()
        
        # Conversation state
        self.conversation_history: List[Dict[str, str]] = []
        self.current_stage = "faq"
        self.is_escalated = False
        self.escalation_info: Optional[Dict[str, Any]] = None
        self.last_confidence = 1.0
    
    def process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process a user message through the appropriate stage.
        
        Args:
            user_message: Customer's message
        
        Returns:
            Dict with response and metadata
        """
        # Log user message
        self.logger.log_message("user", user_message)
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Check for escalation first
        escalation_check = self.escalation_detector.check_escalation(
            user_message,
            self.conversation_history,
            self.last_confidence
        )
        
        if escalation_check["escalation_needed"]:
            return self._handle_escalation(escalation_check)
        
        # Route to appropriate stage
        if self.current_stage == "faq":
            response = self._handle_faq(user_message)
        elif self.current_stage == "qualification":
            response = self._handle_qualification(user_message)
        else:
            response = self._handle_faq(user_message)  # Default to FAQ
        
        # Check if we should transition to qualification
        if (self.current_stage == "faq" and 
            not response.get("escalation_needed", False) and
            self.lead_qualifier.should_qualify_lead(self.conversation_history)):
            self.current_stage = "qualification"
            # Add qualification prompt to next response
            next_question = self.lead_qualifier.get_next_question()
            if next_question:
                response["response"] += f"\n\n{next_question}"
        
        # Update last confidence
        self.last_confidence = response.get("confidence", 1.0)
        
        # Log assistant response
        self.logger.log_message(
            "assistant",
            response.get("response", ""),
            metadata={
                "stage": response.get("stage", self.current_stage),
                "confidence": response.get("confidence", 0.0),
                "escalation_needed": response.get("escalation_needed", False)
            }
        )
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response.get("response", "")
        })
        
        return response
    
    def _handle_faq(self, message: str) -> Dict[str, Any]:
        """Handle FAQ stage."""
        response = self.faq_handler.handle_question(
            message,
            self.conversation_history
        )
        
        if response.get("escalation_needed", False):
            return self._handle_escalation({
                "escalation_needed": True,
                "escalation_reasons": [response.get("escalation_reason", "Unknown")],
                "primary_reason": response.get("escalation_reason", "Unknown")
            })
        
        return response
    
    def _handle_qualification(self, message: str) -> Dict[str, Any]:
        """Handle lead qualification stage."""
        response = self.lead_qualifier.process_answer(
            message,
            self.lead_qualifier.current_question_index - 1,
            self.conversation_history
        )
        
        # If qualification is complete, get next question or finish
        if not response.get("qualification_complete", False):
            next_question = self.lead_qualifier.get_next_question()
            if next_question:
                response["response"] += f"\n\n{next_question}"
        else:
            # Qualification complete, return to FAQ mode
            self.current_stage = "faq"
            response["response"] += "\n\nThank you for that information! How else can I help you today?"
        
        return response
    
    def _handle_escalation(self, escalation_check: Dict[str, Any]) -> Dict[str, Any]:
        """Handle escalation to human agent."""
        self.is_escalated = True
        self.escalation_info = escalation_check
        self.current_stage = "escalation"
        
        # Log escalation
        self.logger.log_escalation(
            reason=escalation_check.get("primary_reason", "Unknown"),
            context=escalation_check
        )
        
        # Generate escalation message
        response = self.escalation_detector.generate_escalation_message(
            escalation_check.get("escalation_reasons", []),
            self.conversation_history
        )
        
        return response
    
    def end_conversation(self) -> Dict[str, Any]:
        """
        End the conversation and generate summary.
        
        Returns:
            Dict with conversation summary
        """
        # Generate summary
        qualification_data = self.lead_qualifier.get_qualification_summary()
        
        summary = self.summarizer.generate_summary(
            self.conversation_history,
            self.escalation_info,
            qualification_data
        )
        
        # Log summary
        self.logger.log_message(
            "system",
            "Conversation ended",
            metadata={"summary": summary}
        )
        
        # Save conversation log
        self.logger.save_conversation()
        
        # Print summary
        print("\n" + self.summarizer.format_summary_for_display(summary))
        self.logger.print_summary()
        
        return summary
    
    def get_conversation_state(self) -> Dict[str, Any]:
        """Get current conversation state."""
        return {
            "current_stage": self.current_stage,
            "is_escalated": self.is_escalated,
            "message_count": len(self.conversation_history),
            "last_confidence": self.last_confidence,
            "qualification_progress": self.lead_qualifier.get_qualification_summary()
        }


