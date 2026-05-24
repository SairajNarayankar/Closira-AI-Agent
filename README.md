# Closira AI Customer Support Workflow

A production-ready AI-powered customer support system demonstrating intelligent conversation handling, lead qualification, escalation detection, and conversation summarization for SMB customer service.

## 🎯 Project Overview

This project implements a 4-stage AI workflow for **Bloom Aesthetics Clinic** that:
- Answers customer questions using only verified SOP data (no hallucinations)
- Qualifies leads through structured questions
- Detects when to escalate to human agents
- Generates actionable conversation summaries

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Customer Input                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Conversation Manager                          │
│  (Orchestrates all stages + escalation detection)       │
└─────┬──────────┬──────────┬──────────┬─────────────────┘
      │          │          │          │
      ▼          ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Stage 1 │ │ Stage 2 │ │ Stage 3 │ │ Stage 4 │
│   FAQ   │ │  Lead   │ │Escalate │ │ Summary │
│Answering│ │Qualify  │ │Detection│ │Generate │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
      │          │          │          │
      └──────────┴──────────┴──────────┘
                     │
                     ▼
              ┌─────────────┐
              │  SOP Data   │
              │   (JSON)    │
              └─────────────┘
```

### Stage Flow

1. **Stage 1: FAQ Answering** - Answers questions using only SOP data
2. **Stage 2: Lead Qualification** - Collects structured customer information
3. **Stage 3: Escalation Detection** - Identifies when human intervention needed
4. **Stage 4: Conversation Summary** - Generates actionable summary at end

---

## 📁 Project Structure

```
closira-assignment/
├── main.py                      # CLI entry point
├── conversation_manager.py      # Orchestrates workflow
├── stages/
│   ├── faq_handler.py          # Stage 1: FAQ answering
│   ├── lead_qualifier.py       # Stage 2: Lead qualification
│   ├── escalation.py           # Stage 3: Escalation detection
│   └── summarizer.py           # Stage 4: Summary generation
├── prompts/
│   └── system_prompts.py       # All prompt templates
├── utils/
│   ├── openai_client.py        # OpenAI API wrapper
│   └── logger.py               # Conversation logging
├── data/
│   └── sop_data.json           # Bloom Aesthetics SOP
├── test_transcripts/           # 5 test scenarios
│   ├── 01_in_sop_question.md
│   ├── 02_out_of_scope_question.md
│   ├── 03_escalation_trigger.md
│   ├── 04_lead_qualification.md
│   └── 05_conversation_summary.md
├── logs/                        # Generated conversation logs
├── prompt_design.md            # Prompt engineering documentation
├── README.md                   # This file
├── requirements.txt            # Python dependencies
└── .env.example                # Environment variable template
```

---

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.13+** (or 3.10+)
- **OpenAI API Key** (GPT-4 access recommended)
- **Git** (for cloning)

### Installation

1. **Clone or download the project**
   ```bash
   cd closira-assignment
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=sk-your-key-here
   ```

---

## 💻 Usage

### Running the CLI

```bash
python main.py
```

### Interactive Commands

Once running, you can:
- **Chat normally** - Type your message and press Enter
- **`help`** - Show help information
- **`state`** - View current conversation state
- **`quit`** or **`exit`** - End conversation and generate summary

### Example Interaction

```
You: What are your Botox prices?

AI Assistant:
Stage: FAQ | Confidence: 0.95
┌─────────────────────────────────────────────────────────┐
│ Our Botox treatments start from £200. We also offer    │
│ free consultations if you'd like to discuss your        │
│ specific needs. Would you like to book a consultation?  │
└─────────────────────────────────────────────────────────┘

You: quit

Ending conversation and generating summary...
```

---

## 🧪 Testing

### Test Scenarios

Five comprehensive test transcripts are provided in `test_transcripts/`:

1. **In-SOP Question** - Verifies accurate SOP-based responses
2. **Out-of-Scope Question** - Verifies escalation on unknown topics
3. **Escalation Trigger** - Verifies sentiment detection
4. **Lead Qualification** - Verifies structured data collection
5. **Conversation Summary** - Verifies complete summary generation

### Running Tests

Review the test transcripts to understand expected behaviors:

```bash
# View test scenarios
cat test_transcripts/01_in_sop_question.md
cat test_transcripts/02_out_of_scope_question.md
# ... etc
```

### Manual Testing

Test each scenario by running `main.py` and following the conversation patterns in the test transcripts.

---

## 🎨 Key Features

### 1. Hallucination Prevention

**Multi-layer approach:**
- ✅ Explicit prompt instructions ("ONLY answer from SOP")
- ✅ SOP data embedded in system prompt
- ✅ Confidence scoring with 0.7 threshold
- ✅ Response validation and auto-escalation
- ✅ Stage-specific reinforcement

**Result:** AI never invents prices, services, or policies.

### 2. Escalation Detection

**Triggers:**
- 🔴 Low confidence (<0.7)
- 🔴 Negative sentiment (anger, frustration)
- 🔴 Explicit request for human
- 🔴 Out-of-scope questions
- 🔴 Multiple unanswered questions (>2)

**Result:** Safe handoff to humans when needed.

### 3. Lead Qualification

**Structured questions:**
1. What brings you here? (intent)
2. Previous experience? (qualification)
3. Booking preference? (action)

**Result:** Actionable customer data for follow-up.

### 4. Conversation Summary

**Includes:**
- Customer intent
- Key details collected
- Questions asked/answered
- SOP gaps identified
- Escalation status
- Recommended next action

**Result:** Complete context for human agents.

---

## 📊 Prompt Design

See [`prompt_design.md`](prompt_design.md) for comprehensive documentation on:
- System prompt architecture
- Hallucination prevention strategy
- Escalation logic
- Tone and persona design
- Temperature settings
- Known limitations and trade-offs

---

## 🔧 Configuration

### SOP Data

Edit `data/sop_data.json` to customize:
- Business information
- Services and pricing
- Business hours
- Policies
- Escalation triggers

### Prompts

Modify `prompts/system_prompts.py` to adjust:
- System prompt
- Stage-specific prompts
- Tone and style
- Response format

### API Settings

In `utils/openai_client.py`:
- Model selection (default: `gpt-4-turbo-preview`)
- Temperature settings
- Max tokens
- Response format

---

## 📝 Logging

Conversations are automatically logged to `logs/` directory:

```json
{
  "session_id": "20240115_143022",
  "conversation_history": [...],
  "escalations": [...],
  "total_messages": 14,
  "total_escalations": 2
}
```

---

## 🎯 Assignment Requirements Checklist

### ✅ Core Functionality
- [x] Stage 1: FAQ Answering with SOP-only responses
- [x] Stage 2: Lead Qualification with structured questions
- [x] Stage 3: Escalation Detection with multiple triggers
- [x] Stage 4: Conversation Summary with structured output

### ✅ Safety & Reliability
- [x] Hallucination prevention (multi-layer)
- [x] Confidence-based escalation
- [x] Sentiment detection
- [x] Out-of-scope handling
- [x] Graceful error handling

### ✅ Documentation
- [x] `prompt_design.md` - Complete prompt documentation
- [x] `README.md` - Setup and usage instructions
- [x] Test transcripts - 5 scenarios covered
- [x] Code comments - Comprehensive inline documentation

### ✅ Code Quality
- [x] Modular architecture (separate stages)
- [x] Clean separation of concerns
- [x] Error handling and fallbacks
- [x] Logging and audit trail
- [x] Type hints and docstrings

---

## 🚨 Known Limitations

1. **Keyword-Based Sentiment**: May miss subtle negativity
2. **English Only**: No multilingual support
3. **Static SOP**: Requires manual updates
4. **API Dependency**: Requires OpenAI API access

See `prompt_design.md` Section 8 for detailed trade-offs and mitigation strategies.

---

## 🔮 Future Improvements

- [ ] Semantic search using embeddings for better SOP matching
- [ ] Multi-turn context handling for complex conversations
- [ ] Dedicated sentiment analysis model
- [ ] Database-backed SOP with real-time updates
- [ ] A/B testing framework for prompt optimization
- [ ] Multilingual support
- [ ] Voice integration for phone conversations
- [ ] Analytics dashboard for conversation insights

---

## 📚 Dependencies

```
openai>=1.12.0          # OpenAI API client
python-dotenv>=1.0.0    # Environment variable management
pydantic>=2.6.0         # Data validation
rich>=13.7.0            # CLI formatting
```

Install all with: `pip install -r requirements.txt`

---

## 🤝 Assignment Context

**Built for:** Closira AI Engineering Internship  
**Objective:** Demonstrate AI workflow design, prompt engineering, and safety-first implementation  
**Focus Areas:**
- Prompt quality and reasoning
- Hallucination prevention
- Escalation logic
- Production-ready code
- Clear documentation

---

## 📧 Support

For questions about this implementation:
1. Review `prompt_design.md` for design decisions
2. Check test transcripts for expected behaviors
3. Review inline code comments for technical details

---

## 📄 License

This is an assignment submission. All rights reserved.

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Advanced prompt engineering
- ✅ Multi-stage AI workflow design
- ✅ Safety-first AI implementation
- ✅ Production-ready code architecture
- ✅ Comprehensive documentation
- ✅ Real-world SMB customer service understanding

---

**Built with ❤️ for Closira**