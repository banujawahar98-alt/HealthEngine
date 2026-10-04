import httpx, asyncio

SYSTEM_PROMPT = """You are MindCare AI, a warm, empathetic, and conversational mental well-being companion.
Ask thoughtful follow-up questions. Keep responses concise (3-5 sentences). Never diagnose."""

async def test():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    key = os.getenv('GEMINI_API_KEY', '')
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={key}'
    payload = {
        'system_instruction': {'parts': [{'text': SYSTEM_PROMPT}]},
        'contents': [{'role': 'user', 'parts': [{'text': 'I have been feeling really anxious about my exams'}]}],
        'generationConfig': {'temperature': 0.8, 'maxOutputTokens': 300}
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(url, json=payload)
        print('STATUS:', r.status_code)
        if r.status_code == 200:
            data = r.json()
            print('RESPONSE:', data['candidates'][0]['content']['parts'][0]['text'])
        else:
            print('ERROR:', r.text[:500])

asyncio.run(test())
