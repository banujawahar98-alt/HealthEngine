"""
LLM Client - Google Gemini API with conversational mental health support.
Falls back to a smart rule-based engine if no API key is configured.
"""
import logging
import httpx
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger("mindcare.ai")

SYSTEM_PROMPT = """You are MindCare AI, a warm, empathetic, and conversational mental well-being companion.

Your personality:
- Friendly, caring, and non-judgmental — like a supportive friend who genuinely listens
- Ask thoughtful follow-up questions to understand how the user is really feeling
- Check in naturally: "How has your day been?", "How long have you been feeling this way?", "What's been on your mind lately?"
- Validate emotions before offering advice — never jump straight to tips
- Keep responses concise (3-5 sentences or short bullet points), never overwhelming

Conversation style:
- Start new conversations by warmly greeting and asking how they're doing today
- If the user seems stressed, ask what's causing it before giving advice
- If they mention sleep issues, ask about their routine
- If they mention anxiety, ask what triggers it
- Always end with a gentle question to keep the conversation going

STRICT RULES:
1. Never diagnose any mental health condition
2. Never recommend specific medications
3. Never claim to be a therapist or doctor
4. If the user mentions self-harm or suicidal thoughts, immediately provide crisis resources
5. Use the provided knowledge base context to give evidence-informed tips when relevant
6. Keep the tone warm and human — avoid clinical or robotic language

You are here to listen, support, and gently guide — not to lecture."""


class LLMClient:

    @staticmethod
    async def generate_response(
        user_message: str,
        conversation_history: List[Dict[str, Any]],
        rag_docs: List[Dict[str, Any]]
    ) -> str:
        # Try Gemini first
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY not in ("", "your_gemini_api_key_here"):
            try:
                return await LLMClient._call_gemini(user_message, conversation_history, rag_docs)
            except Exception as e:
                logger.warning("Gemini API failed, falling back: %s", e)

        # Try OpenAI if key starts with sk-
        if settings.AI_API_KEY and settings.AI_API_KEY.startswith("sk-"):
            try:
                return await LLMClient._call_openai(user_message, conversation_history, rag_docs)
            except Exception as e:
                logger.warning("OpenAI API failed, falling back: %s", e)

        return LLMClient._smart_fallback(user_message, conversation_history)

    @staticmethod
    async def _call_gemini(
        user_message: str,
        conversation_history: List[Dict[str, Any]],
        rag_docs: List[Dict[str, Any]]
    ) -> str:
        # Build context from RAG docs
        rag_context = ""
        if rag_docs:
            rag_context = "\n\nRelevant well-being knowledge:\n" + "\n".join(
                f"- {d.get('title', '')}: {d.get('description', '')}" for d in rag_docs[:2]
            )

        # Build conversation turns for Gemini
        contents = []

        # Add history (skip system messages, map roles)
        for msg in conversation_history[-10:]:  # last 10 messages for context
            role = msg.get("role", "user")
            text = msg.get("message", "")
            if not text:
                continue
            gemini_role = "user" if role == "user" else "model"
            contents.append({"role": gemini_role, "parts": [{"text": text}]})

        # Add current user message with RAG context appended
        current_text = user_message
        if rag_context:
            current_text = f"{user_message}\n{rag_context}"

        # Ensure last message is from user
        if contents and contents[-1]["role"] == "user":
            contents[-1]["parts"][0]["text"] = current_text
        else:
            contents.append({"role": "user", "parts": [{"text": current_text}]})

        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": contents,
            "generationConfig": {
                "temperature": 0.8,
                "maxOutputTokens": 400,
                "topP": 0.9
            }
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={settings.GEMINI_API_KEY}"

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                logger.error("Gemini error %s: %s", resp.status_code, resp.text)
                raise Exception(f"Gemini returned {resp.status_code}")

    @staticmethod
    async def _call_openai(
        user_message: str,
        conversation_history: List[Dict[str, Any]],
        rag_docs: List[Dict[str, Any]]
    ) -> str:
        rag_context = ""
        if rag_docs:
            rag_context = "\n\nRelevant context:\n" + "\n".join(
                f"- {d.get('title')}: {d.get('description')}" for d in rag_docs[:2]
            )

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in conversation_history[-10:]:
            role = msg.get("role", "user")
            text = msg.get("message", "")
            if text and role in ("user", "assistant"):
                messages.append({"role": role, "content": text})

        if messages[-1].get("role") != "user":
            messages.append({"role": "user", "content": user_message + rag_context})
        else:
            messages[-1]["content"] = user_message + rag_context

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.AI_API_KEY}"},
                json={"model": "gpt-3.5-turbo", "messages": messages, "max_tokens": 400, "temperature": 0.8}
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            raise Exception(f"OpenAI returned {resp.status_code}")

    @staticmethod
    def _smart_fallback(message: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Conversational rule-based fallback that asks follow-up questions."""
        text = message.lower().strip()
        is_first_message = len(conversation_history) <= 1

        if is_first_message:
            return (
                "Hi there! 👋 I'm MindCare AI, your well-being companion. I'm here to listen and support you.\n\n"
                "How are you feeling today? Is there something specific on your mind, or would you just like to check in?"
            )

        # Greetings / check-ins
        if any(w in text for w in ["hi", "hello", "hey", "good morning", "good evening"]):
            return (
                "Hello! It's good to hear from you. 😊\n\n"
                "How has your day been going so far? Anything on your mind you'd like to talk about?"
            )

        if text in ["fine", "ok", "okay", "good", "alright", "not bad"]:
            return (
                "Glad to hear that! Sometimes 'okay' can mean a lot of different things though. 😊\n\n"
                "Is there anything — even something small — that's been weighing on you lately, or are you genuinely feeling settled?"
            )

        if text in ["bad", "not good", "terrible", "awful", "horrible", "not great"]:
            return (
                "I'm sorry to hear that. 💙 It takes courage to acknowledge when things aren't going well.\n\n"
                "Would you like to share what's been making things feel difficult? I'm here to listen — no judgment at all."
            )

        # Stress
        if any(w in text for w in ["stress", "stressed", "overwhelm", "pressure", "too much"]):
            if "?" not in text:
                return (
                    "It sounds like you're carrying a lot right now. That's really tough. 💙\n\n"
                    "Can you tell me a bit more about what's been stressing you out the most? "
                    "Is it something at work, studies, relationships, or something else entirely?"
                )
            return (
                "Stress can feel really heavy, especially when it builds up over time.\n\n"
                "A few things that can help in the moment:\n"
                "• **Box breathing**: Inhale 4 counts → hold 4 → exhale 4 → hold 4. Repeat 3 times.\n"
                "• **Name it**: Write down the top 3 things stressing you — it helps your brain process them.\n"
                "• **One thing at a time**: What's the single most urgent thing you need to handle today?\n\n"
                "What feels most overwhelming right now?"
            )

        # Anxiety / worry
        if any(w in text for w in ["anxious", "anxiety", "worry", "worried", "nervous", "panic", "fear", "scared"]):
            return (
                "Anxiety can feel really unsettling — your body and mind are working overtime. 💙\n\n"
                "Can I ask — is this a general feeling of unease, or is there something specific triggering it? "
                "For example, an upcoming event, a relationship, or just a general sense of dread?"
            )

        # Sadness / depression
        if any(w in text for w in ["sad", "depressed", "depression", "unhappy", "empty", "numb", "hopeless", "lonely", "alone"]):
            return (
                "I hear you, and I want you to know that what you're feeling is valid. 💙\n\n"
                "Feeling this way can be really isolating. How long have you been feeling like this? "
                "And is there anyone in your life you've been able to talk to about it?"
            )

        # Sleep
        if any(w in text for w in ["sleep", "insomnia", "tired", "exhausted", "can't sleep", "wake up", "fatigue"]):
            return (
                "Sleep issues can really affect everything — mood, focus, energy. You're not alone in this.\n\n"
                "Can you tell me more about what's happening? For example:\n"
                "• Do you have trouble *falling* asleep, or do you wake up during the night?\n"
                "• How long has this been going on?\n"
                "• Is your mind racing when you try to sleep, or is it more physical restlessness?"
            )

        # Exams / academic
        if any(w in text for w in ["exam", "study", "academic", "university", "college", "assignment", "deadline", "grade"]):
            return (
                "Academic pressure is one of the most common sources of stress — you're definitely not alone. 📚\n\n"
                "What's the situation right now? Are you feeling overwhelmed by the workload, worried about performance, "
                "or is it more about the pressure you're putting on yourself?"
            )

        # Work pressure
        if any(w in text for w in ["work", "job", "boss", "colleague", "burnout", "workplace", "career"]):
            return (
                "Work stress can really take a toll, especially when it follows you home.\n\n"
                "What's been the hardest part lately — the workload itself, the environment, "
                "or feeling like you're not getting the recognition or support you need?"
            )

        # Relationships
        if any(w in text for w in ["relationship", "breakup", "partner", "friend", "family", "fight", "argument", "lonely"]):
            return (
                "Relationship difficulties can be really painful — they touch something very deep in us. 💙\n\n"
                "Would you like to share a bit more about what's going on? "
                "Sometimes just talking it through can help bring some clarity."
            )

        # User asks how AI is / small talk
        if any(w in text for w in ["how are you", "how r u", "what are you", "who are you"]):
            return (
                "I'm MindCare AI — I'm here and ready to support you! 😊\n\n"
                "More importantly, how are *you* doing today? What's on your mind?"
            )

        # Positive / doing well
        if any(w in text for w in ["happy", "great", "amazing", "wonderful", "excited", "good day", "feeling good"]):
            return (
                "That's wonderful to hear! 😊 It's so important to acknowledge the good moments.\n\n"
                "What's been making things feel positive lately? I'd love to hear about it — "
                "and it's also great to reflect on what's working well for your well-being."
            )

        # Generic / unclear
        return (
            "Thank you for sharing that with me. 💙\n\n"
            "I want to make sure I understand what you're going through. "
            "Could you tell me a little more about how you've been feeling lately — "
            "maybe what a typical day looks like for you right now?"
        )
