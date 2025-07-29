import os
import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = type('', (), {'completions': type('', (), {'create': self._create})()})()
    
    def _create(self, model, messages):
        # Convert messages to a proper prompt format
        prompt = ""
        for msg in messages:
            if msg['role'] == 'system':
                prompt += f"System: {msg['content']}\n"
            elif msg['role'] == 'user':
                prompt += f"User: {msg['content']}\n"
        prompt += "Assistant:"
        
        try:
            response = self.model.generate_content(prompt)
            return type('', (), {
                'choices': [
                    type('', (), {
                        'message': type('', (), {
                            'content': response.text
                        })()
                    })()
                ]
            })()
        except Exception as e:
            return type('', (), {
                'choices': [
                    type('', (), {
                        'message': type('', (), {
                            'content': f"Error: {e}"
                        })()
                    })()
                ]
            })()

# Test code - only runs when this file is executed directly, not when imported
if __name__ == "__main__":
    # Get API key from environment variable for security
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY environment variable")

    client = GeminiClient(api_key=api_key)

    completion = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant"},
            {"role": "user", "content": "what is coding"}
        ]
    )

    print(completion.choices[0].message.content)
