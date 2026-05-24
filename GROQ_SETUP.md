# Groq API Setup Guide (FREE)

## 🎉 Why Groq?

- ✅ **Completely FREE** - No credit card required
- ✅ **Very Fast** - Fastest inference speeds
- ✅ **Generous Limits** - 30 requests/min, 14,400/day
- ✅ **OpenAI Compatible** - Drop-in replacement
- ✅ **Great Models** - Llama 3.1, Mixtral, Gemma

## 🚀 Quick Setup (2 minutes)

### Step 1: Get Your FREE API Key

1. Go to: **https://console.groq.com/**
2. Sign up with Google/GitHub (free, no credit card)
3. Click "API Keys" in the left sidebar
4. Click "Create API Key"
5. Copy your key (starts with `gsk_...`)

### Step 2: Add Key to .env File

Open `closira-assignment/.env` and add:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 3: Run the Application

```bash
python main.py
```

That's it! 🎉

## 📊 Available Models

Your code is configured to use **llama-3.1-70b-versatile** (best balance of speed & quality).

Other free models available:
- `llama-3.1-70b-versatile` - Best overall (default)
- `mixtral-8x7b-32768` - Good for long contexts
- `gemma-7b-it` - Fastest, lighter model
- `llama-3.1-8b-instant` - Ultra-fast responses

## 🔧 Changing Models

Edit `utils/openai_client.py` line 38:

```python
self.model = "llama-3.1-70b-versatile"  # Change this
```

## 📈 Rate Limits (FREE Tier)

- **30 requests per minute**
- **14,400 requests per day**
- Perfect for development, demos, and testing!

## ❓ Troubleshooting

### "GROQ_API_KEY not found"
- Make sure you created the `.env` file
- Check the key starts with `gsk_`
- Restart your terminal after adding the key

### "Rate limit exceeded"
- You're making too many requests too fast
- Wait 1 minute and try again
- Free tier: 30 requests/minute

### "Invalid API key"
- Double-check you copied the full key
- Make sure there are no extra spaces
- Generate a new key if needed

## 🆚 Groq vs OpenAI

| Feature | Groq | OpenAI |
|---------|------|--------|
| Cost | FREE | Paid ($) |
| Speed | Very Fast | Fast |
| Models | Llama 3.1, Mixtral | GPT-4, GPT-3.5 |
| Rate Limit | 30/min | Varies |
| Setup | 2 minutes | Need billing |

## 🎓 For Your Assignment

**Perfect for:**
- ✅ Development and testing
- ✅ Demo videos
- ✅ Assignment submissions
- ✅ Learning and experimentation

**Your evaluators will see:**
- Professional API integration
- Cost-conscious solution
- Modern tech stack (Llama 3.1)
- Production-ready code

## 🔗 Useful Links

- **Groq Console**: https://console.groq.com/
- **Groq Docs**: https://console.groq.com/docs
- **Model Playground**: https://console.groq.com/playground
- **API Status**: https://status.groq.com/

## 💡 Pro Tips

1. **Test in Playground First**: Try your prompts at https://console.groq.com/playground
2. **Monitor Usage**: Check your usage in the Groq console
3. **Multiple Keys**: Create separate keys for dev/prod
4. **Error Handling**: The code already handles rate limits gracefully

## 🎉 You're All Set!

Your Closira AI workflow now uses:
- ✅ FREE Groq API
- ✅ Fast Llama 3.1 model
- ✅ No cost for unlimited testing
- ✅ Production-ready code

Happy coding! 🚀