# Test Transcript 2: Out-of-Scope Question

## Scenario
Customer asks about a service not mentioned in the SOP data.

## Expected Behavior
- AI recognizes question is outside SOP scope
- Does NOT make up information
- Acknowledges the gap professionally
- Escalates to human agent
- Low confidence or explicit escalation flag

---

## Conversation

**User:** Hi, do you offer laser hair removal treatments?

**AI Assistant:**
```
Stage: FAQ | Confidence: 0.45 | ⚠ ESCALATED

I don't have specific information about laser hair removal in our 
current service offerings. I can see we offer Botox, dermal fillers, 
and free consultations, but I want to make sure you get accurate 
information about all our available treatments.

Let me connect you with one of our specialists who can provide you 
with complete details about our full range of services, including 
whether we offer laser hair removal.

Escalation Reason: Question outside SOP scope, low confidence
```

**User:** What about chemical peels?

**AI Assistant:**
```
Stage: ESCALATION | Confidence: 0.0 | ⚠ ESCALATED

I don't have that specific information in our records. Rather than 
guess, I'd like to connect you with someone who can give you accurate 
details about all our treatment options.

Our specialist will be able to discuss:
- All available treatments
- Pricing information
- What might work best for your needs

Would you like me to arrange for someone to contact you?

Escalation Reason: Out-of-scope question, information not in SOP
```

**User:** Do you do microblading?

**AI Assistant:**
```
Stage: ESCALATION | Confidence: 0.0 | ⚠ ESCALATED

I apologize, but I don't have information about microblading services 
in my current knowledge base. To ensure you get accurate and complete 
information about all our services, I'd like to connect you with one 
of our team members who can help you better.

They'll be able to:
- Confirm which services we offer
- Discuss pricing and availability
- Answer any specific questions you have

Escalation Reason: Service not listed in SOP data
```

---

## Analysis

### ✅ Success Criteria Met

1. **No Hallucination**: AI did NOT invent services, prices, or policies
2. **Honest Acknowledgment**: Clearly stated "I don't have that information"
3. **Appropriate Escalation**: Correctly identified need for human assistance
4. **Professional Handling**: Maintained helpful tone while escalating
5. **Low Confidence**: Confidence scores reflected uncertainty (0.0-0.45)

### Key Observations

- AI recognized questions were outside SOP scope
- Did not attempt to answer with made-up information
- Provided context about what services ARE available
- Offered clear path to getting accurate information
- Maintained customer service quality during handoff

### Escalation Triggers

All three questions triggered escalation because:
- ❌ Laser hair removal - Not in SOP
- ❌ Chemical peels - Not in SOP
- ❌ Microblading - Not in SOP

### SOP Gaps Identified

This conversation reveals potential business opportunities:
1. Customer interest in laser hair removal
2. Customer interest in chemical peels
3. Customer interest in microblading

**Recommendation**: Consider adding these services or updating SOP to explicitly state they're not offered.

---

## Hallucination Prevention Validation

### What the AI Did NOT Do ✅
- Did not invent prices for unlisted services
- Did not claim services are available when uncertain
- Did not provide medical advice about treatments
- Did not make assumptions about service availability

### What the AI DID Do ✅
- Acknowledged knowledge limitations
- Stayed within SOP boundaries
- Escalated appropriately
- Maintained professional tone
- Offered alternative path to information

This demonstrates robust hallucination prevention working as designed.