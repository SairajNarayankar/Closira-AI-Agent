# Video Walkthrough Guide (2-5 minutes)

This guide helps you create the required video walkthrough for the Closira assignment submission.

---

## 🎥 Video Structure (Recommended)

### Introduction (30 seconds)
- "Hi, I'm [Your Name], and this is my Closira AI Customer Support Workflow"
- "I've built a 4-stage AI system that handles customer conversations safely and intelligently"
- Show the project folder structure briefly

### Part 1: Architecture Overview (1 minute)
**Show:** `README.md` architecture diagram

**Explain:**
- "The system has 4 stages: FAQ Answering, Lead Qualification, Escalation Detection, and Summary Generation"
- "All stages work together through a Conversation Manager"
- "Everything is grounded in SOP data to prevent hallucinations"

### Part 2: Live Demo (2-3 minutes)
**Run:** `python main.py`

**Demonstrate 3 scenarios:**

1. **In-SOP Question (30 seconds)**
   - Type: "What are your Botox prices?"
   - Show: Accurate response from SOP
   - Point out: High confidence score

2. **Out-of-Scope Question (30 seconds)**
   - Type: "Do you offer laser hair removal?"
   - Show: AI doesn't hallucinate, escalates instead
   - Point out: Low confidence, escalation flag

3. **Escalation Trigger (30 seconds)**
   - Type: "This is ridiculous!"
   - Show: Immediate escalation on negative sentiment
   - Point out: Professional handoff message

4. **End Conversation (30 seconds)**
   - Type: "quit"
   - Show: Generated summary with all details
   - Point out: Structured output, SOP gaps identified

### Part 3: Key Features (1 minute)
**Show:** `prompt_design.md`

**Highlight:**
- "Multi-layer hallucination prevention"
- "5 different escalation triggers"
- "Confidence-based decision making"
- "Professional tone maintained throughout"

**Show:** Test transcripts folder
- "I've created 5 comprehensive test scenarios"
- "Each validates a different aspect of the system"

### Conclusion (30 seconds)
- "This system is production-ready for SMB customer support"
- "It prioritizes safety, never makes up information, and knows when to escalate"
- "All code is modular, well-documented, and follows best practices"
- "Thank you for watching!"

---

## 🎬 Recording Tips

### Setup
1. **Clean Desktop**: Close unnecessary windows
2. **Good Lighting**: Face a window or use a lamp
3. **Clear Audio**: Use headphones with mic or external mic
4. **Screen Resolution**: 1920x1080 recommended
5. **Recording Software**: 
   - Windows: OBS Studio (free)
   - Mac: QuickTime or OBS Studio
   - Online: Loom (easiest)

### During Recording
- **Speak Clearly**: Pace yourself, don't rush
- **Show, Don't Just Tell**: Demonstrate features live
- **Zoom In**: Make text readable (Ctrl/Cmd + for terminal)
- **Pause Between Sections**: Makes editing easier
- **Smile**: Enthusiasm shows competence!

### What to Show on Screen
1. **Project Structure**: Briefly show folder tree
2. **Key Files**: 
   - `main.py` (entry point)
   - `prompt_design.md` (design decisions)
   - `test_transcripts/` (validation)
3. **Live Demo**: Terminal running the CLI
4. **Code Snippets**: Show 1-2 key functions if time permits

---

## 📝 Script Template

```
[INTRO]
"Hi, I'm [Name]. This is my AI customer support workflow for Closira.
I've built a production-ready system that handles customer conversations
across 4 intelligent stages while preventing hallucinations and knowing
when to escalate to humans."

[ARCHITECTURE]
"The system has 4 stages working together..."
[Show README diagram]

[DEMO - FAQ]
"Let me show you how it works. First, an in-scope question..."
[Type and show response]
"Notice the high confidence and accurate SOP-based answer."

[DEMO - ESCALATION]
"Now watch what happens with an out-of-scope question..."
[Type and show escalation]
"The AI doesn't make up information. It acknowledges the gap and escalates."

[DEMO - SENTIMENT]
"And if a customer gets frustrated..."
[Type negative message]
"Immediate escalation with a professional handoff."

[DEMO - SUMMARY]
"At the end, we get a comprehensive summary..."
[Show summary output]
"Customer intent, collected data, SOP gaps, and recommended actions."

[KEY FEATURES]
"The system uses multi-layer hallucination prevention..."
[Show prompt_design.md sections]
"5 escalation triggers, confidence scoring, and professional tone throughout."

[CONCLUSION]
"This is production-ready, well-documented, and built with safety first.
Thank you for watching!"
```

---

## ✅ Checklist Before Recording

- [ ] Project runs without errors
- [ ] `.env` file configured with API key
- [ ] Terminal font size increased (readable on video)
- [ ] Desktop cleaned up
- [ ] Recording software tested
- [ ] Script practiced once
- [ ] Microphone tested
- [ ] Good lighting checked

---

## 🎯 What Evaluators Look For

1. **Understanding**: Do you understand what you built?
2. **Communication**: Can you explain it clearly?
3. **Demonstration**: Does it actually work?
4. **Design Decisions**: Can you justify your choices?
5. **Professionalism**: Is the presentation polished?

---

## 📤 Export Settings

- **Format**: MP4 (most compatible)
- **Resolution**: 1920x1080 or 1280x720
- **Frame Rate**: 30fps
- **Audio**: 128kbps or higher
- **File Size**: Under 100MB if possible

---

## 🚀 Quick Recording with Loom (Easiest)

1. Go to [loom.com](https://www.loom.com)
2. Sign up (free)
3. Install browser extension or desktop app
4. Click "Record" → "Screen + Camera"
5. Select your terminal window
6. Hit record and follow the script
7. Loom automatically uploads and gives you a shareable link

**Advantage**: No editing needed, instant sharing, automatic captions

---

## 💡 Pro Tips

1. **Practice Once**: Do a dry run to catch issues
2. **Keep It Simple**: Don't try to show everything
3. **Focus on Value**: Highlight what makes your solution good
4. **Be Confident**: You built something impressive!
5. **Time Management**: Aim for 3-4 minutes, max 5

---

## 🎓 What Makes a Great Walkthrough

✅ **Clear Introduction**: Who you are, what you built  
✅ **Live Demo**: Actually run the code  
✅ **Key Features**: Highlight 2-3 main strengths  
✅ **Design Decisions**: Explain one important choice  
✅ **Professional**: Good audio, clear screen, confident delivery  

❌ **Avoid**: Reading code line by line, going over time, poor audio, no demo

---

## 📧 Submission

After recording:
1. Upload to YouTube (unlisted) or Loom
2. Get shareable link
3. Test link in incognito/private window
4. Include link in your submission email/form

---
