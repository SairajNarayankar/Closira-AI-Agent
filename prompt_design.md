# Prompt Design Documentation

## Overview
This document details the prompt engineering decisions, hallucination prevention strategies, escalation logic, and tone design for the Closira AI customer support workflow.

---

## 1. System Prompt Architecture

### Main System Prompt
The core system prompt establishes the AI's role, constraints, and behavior guidelines:

```
You are a professional customer service AI assistant for Bloom Aesthetics Clinic.
```

**Key Design Decisions:**

1. **Clear Role Definition**: Explicitly states the AI is a customer service assistant, not a medical professional
2. **Business Context**: Grounds the AI in the specific business (Bloom Aesthetics Clinic)
3. **Structured Output**: Requires JSON responses for consistent parsing and validation

### Critical Rules Section
The prompt includes a "CRITICAL RULES" section that MUST be followed:

```
1. ONLY answer questions using information from the provided SOP data
2. If information is NOT in the SOP, say "I don't have that information" and escalate
3. NEVER make up prices, services, policies, or medical advice
4. NEVER guess or hallucinate information
5. If you're uncertain (confidence < 70%), acknowledge it and escalate
```

**Reasoning:**
- **Explicit Constraints**: Using "NEVER" and "ONLY" creates strong boundaries
- **Specific Examples**: Mentions prices, services, policies, and medical advice to prevent common hallucinations
- **Confidence Threshold**: Quantifies uncertainty with a 70% threshold for objective escalation decisions

---

## 2. Hallucination Prevention Strategy

### Multi-Layer Approach

#### Layer 1: Prompt-Level Instructions
- **Explicit Prohibition**: "NEVER make up" and "ONLY answer from SOP"
- **Repetition**: Rules stated multiple times in different sections
- **Consequences**: Clear instruction to escalate when uncertain

#### Layer 2: SOP Data Injection
```python
system_prompt = SYSTEM_PROMPT.format(sop_data=json.dumps(sop_data, indent=2))
```
- **Direct Inclusion**: SOP data embedded directly in system prompt
- **Structured Format**: JSON format makes data boundaries clear
- **Single Source of Truth**: All answers must reference this data

#### Layer 3: Confidence Scoring
```json
{
  "confidence": 0.0-1.0,
  "escalation_needed": true|false
}
```
- **Self-Assessment**: AI must rate its own confidence
- **Automatic Escalation**: Confidence < 0.7 triggers escalation
- **Transparency**: Confidence score logged for audit

#### Layer 4: Response Validation
```python
# Validate response structure
required_fields = ["response", "confidence", "stage", "escalation_needed"]
if not all(field in result for field in required_fields):
    return self._create_error_response("Invalid response structure")

# Auto-escalate if confidence is too low
if result["confidence"] < 0.7:
    result["escalation_needed"] = True
```
- **Schema Validation**: Ensures all required fields present
- **Confidence Enforcement**: Code-level check overrides AI if needed
- **Graceful Degradation**: Error responses trigger escalation

#### Layer 5: Stage-Specific Prompts
Each stage has additional instructions:

**FAQ Prompt:**
```
RULES:
1. Check if the answer exists in the SOP
2. If YES: Provide a clear, accurate answer
3. If NO: Say "I don't have that specific information" and escalate
4. Never invent or assume information
```

**Why This Works:**
- **Contextual Reinforcement**: Rules repeated in stage-specific context
- **Decision Tree**: Clear if-then logic for the AI to follow
- **Explicit Fallback**: Exact phrase to use when information is missing

---

## 3. Escalation Logic

### Trigger Categories

#### 1. Confidence-Based Escalation
```python
if last_confidence < 0.7:
    escalation_reasons.append(f"Low confidence score: {last_confidence:.2f}")
```
- **Threshold**: 70% confidence minimum
- **Reasoning**: Below 70% indicates significant uncertainty
- **Automatic**: No human judgment required

#### 2. Sentiment-Based Escalation
```python
NEGATIVE_KEYWORDS = [
    "angry", "frustrated", "ridiculous", "terrible", "awful",
    "horrible", "worst", "useless", "disappointed", "upset",
    "complaint", "complain", "unacceptable", "disgusted"
]
```
- **Keyword Detection**: Simple but effective for common negative expressions
- **Immediate Trigger**: Any negative keyword causes escalation
- **Customer Satisfaction**: Prevents AI from handling upset customers

#### 3. Explicit Request Escalation
```python
EXPLICIT_ESCALATION_PHRASES = [
    "speak to human", "talk to person", "real person",
    "human agent", "manager", "supervisor", "someone else"
]
```
- **Customer Choice**: Respects explicit requests for human assistance
- **Phrase Matching**: Covers common ways customers ask for humans
- **Immediate Handoff**: No attempt to convince customer otherwise

#### 4. Out-of-Scope Escalation
```python
def _check_out_of_scope(self, message: str) -> bool:
    sop_keywords = ["botox", "filler", "consultation", "price", ...]
    has_sop_keyword = any(keyword in message_lower for keyword in sop_keywords)
    if not has_sop_keyword and "?" in message:
        return True
```
- **Keyword Heuristic**: Checks if question relates to known services
- **Question Detection**: Only triggers for actual questions
- **Conservative**: Prefers escalation over guessing

#### 5. Multiple Unanswered Questions
```python
def _check_unanswered_questions(self, conversation_history: list) -> bool:
    question_count = sum(1 for msg in recent_user_messages if "?" in msg["content"])
    return question_count > 2
```
- **Threshold**: More than 2 questions in recent history
- **Pattern Recognition**: Indicates AI is struggling to help
- **Proactive**: Escalates before customer gets frustrated

### Escalation Message Generation
```python
def generate_escalation_message(self, reasons: List[str]) -> Dict[str, Any]:
    # Uses AI to craft professional handoff message
    # Falls back to default if AI fails
```
- **Professional Tone**: AI generates empathetic handoff message
- **Context-Aware**: Considers escalation reasons
- **Reliable Fallback**: Default message if generation fails

---

## 4. Tone and Persona

### Persona Definition
**Role**: Professional customer service representative for an aesthetics clinic

**Characteristics:**
- **Professional**: Uses proper grammar, complete sentences
- **Warm**: Friendly and approachable, not robotic
- **Empathetic**: Acknowledges customer needs and concerns
- **Concise**: Clear and direct, respects customer's time
- **Respectful**: Addresses customers politely

### Tone Guidelines in Prompt
```
# TONE & STYLE
- Professional yet warm and friendly
- Concise and clear
- Empathetic to customer needs
- Use proper grammar and punctuation
- Address customers respectfully
```

### Example Responses

**Good (Professional + Warm):**
> "Our Botox treatments start from £200. We also offer free consultations if you'd like to discuss your specific needs. Would you like to book a consultation?"

**Bad (Too Casual):**
> "Botox is £200+. Want to book?"

**Bad (Too Formal):**
> "I am pleased to inform you that our establishment offers Botox treatments commencing at the price point of £200 sterling."

### SMB Context Considerations
- **Accessibility**: Language should be clear for all education levels
- **Efficiency**: Small businesses value quick, helpful responses
- **Personal Touch**: Warmer than corporate, but still professional
- **Trust Building**: Transparency about limitations builds credibility

---

## 5. Stage-Specific Design

### Stage 1: FAQ Answering
**Goal**: Answer questions accurately from SOP only

**Prompt Strategy:**
- Lower temperature (0.3) for consistency
- Explicit SOP boundary enforcement
- Confidence scoring mandatory
- JSON mode for structured output

**Key Instruction:**
> "Check if the answer exists in the SOP. If YES: Provide a clear, accurate answer. If NO: Say 'I don't have that specific information' and escalate."

### Stage 2: Lead Qualification
**Goal**: Collect structured information through natural conversation

**Prompt Strategy:**
- Predefined question sequence
- One question at a time
- Store responses in structured format
- Detect disinterest and escalate

**Questions:**
1. "What brings you to Bloom Aesthetics today?"
2. "Have you had similar treatments before?"
3. "What's your preferred booking method?"

**Design Rationale:**
- **Progressive Disclosure**: Start broad, get specific
- **Natural Flow**: Questions feel conversational, not interrogative
- **Actionable Data**: Responses inform follow-up strategy

### Stage 3: Escalation Detection
**Goal**: Identify when human intervention is needed

**Prompt Strategy:**
- Multiple trigger checks (confidence, sentiment, scope)
- Immediate detection, no delays
- Clear reason logging
- Professional handoff message

**Design Rationale:**
- **Safety First**: Better to escalate unnecessarily than mishandle
- **Transparency**: Always log why escalation occurred
- **Customer Experience**: Smooth handoff maintains trust

### Stage 4: Conversation Summary
**Goal**: Generate actionable summary for human review

**Prompt Strategy:**
- Structured output format
- Identify customer intent
- List SOP gaps
- Recommend next action

**Summary Structure:**
```json
{
  "customer_intent": "...",
  "key_details": {},
  "questions_asked": [],
  "answers_provided": [],
  "sop_gaps": [],
  "escalation_status": "...",
  "recommended_next_action": "..."
}
```

**Design Rationale:**
- **Actionable**: Human agent knows exactly what to do next
- **Complete**: All relevant information captured
- **Improvement**: SOP gaps inform business process updates

---

## 6. JSON Response Format

### Standard Response Schema
```json
{
  "response": "Message to customer",
  "confidence": 0.0-1.0,
  "stage": "faq|qualification|escalation|summary",
  "escalation_needed": true|false,
  "escalation_reason": "reason if escalated",
  "data_collected": {}
}
```

**Benefits:**
- **Parseable**: Easy to extract and validate
- **Consistent**: Same structure across all stages
- **Extensible**: Can add fields without breaking existing code
- **Debuggable**: Clear visibility into AI decisions

---

## 7. Temperature Settings

### By Stage
- **FAQ**: 0.3 (low) - Consistency and accuracy prioritized
- **Qualification**: 0.5 (medium) - Balance between natural and consistent
- **Escalation**: 0.5 (medium) - Professional but empathetic
- **Summary**: 0.3 (low) - Factual and structured

**Reasoning:**
- Lower temperature for factual responses
- Medium temperature for conversational flow
- Never high temperature (prevents creativity/hallucination)

---

## 8. Known Limitations and Trade-offs

### Limitations
1. **Keyword-Based Sentiment**: May miss subtle negativity
2. **English Only**: No multilingual support
3. **Static SOP**: Requires manual updates
4. **API Dependency**: Fails if OpenAI is down

### Trade-offs
1. **Conservative Escalation**: May escalate unnecessarily (chosen for safety)
2. **Structured Questions**: Less flexible than free-form (chosen for data quality)
3. **JSON Responses**: Adds parsing overhead (chosen for reliability)

### Mitigation Strategies
- Fallback responses for all error cases
- Logging for debugging and improvement
- Clear error messages to users
- Graceful degradation when possible

---

## 9. Testing and Validation

### Test Scenarios Covered
1. **In-SOP Question**: Verifies accurate SOP-based responses
2. **Out-of-Scope Question**: Verifies escalation on unknown topics
3. **Negative Sentiment**: Verifies sentiment detection and escalation
4. **Lead Qualification**: Verifies structured data collection
5. **Conversation Summary**: Verifies complete summary generation

### Validation Checks
- Response structure validation
- Confidence threshold enforcement
- Escalation trigger verification
- Data collection completeness
- Summary format validation

---

## 10. Future Improvements

### Potential Enhancements
1. **Semantic Search**: Use embeddings for better SOP matching
2. **Multi-turn Context**: Better handling of follow-up questions
3. **Sentiment Analysis**: Use dedicated model instead of keywords
4. **Dynamic SOP**: Database-backed, real-time updates
5. **A/B Testing**: Compare prompt variations
6. **Multilingual**: Support multiple languages
7. **Voice Integration**: Handle phone conversations

### Prompt Evolution
- Collect real conversation data
- Analyze escalation patterns
- Refine confidence thresholds
- Update keyword lists
- Improve tone based on feedback

---

## Conclusion

This prompt design prioritizes **safety, reliability, and customer satisfaction** over flexibility. The multi-layer hallucination prevention, clear escalation triggers, and professional tone ensure the AI behaves appropriately in real customer interactions while maintaining the ability to gracefully hand off to humans when needed.

The design is production-ready for SMB customer support with clear documentation for maintenance and improvement.