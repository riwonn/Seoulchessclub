import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class RAGChatbot:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.initialized = False
        self.knowledge_base = []
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
        
        if not self.gemini_api_key:
            print("⚠️  WARNING: GEMINI_API_KEY not found - chatbot will not work")
            return
        
        try:
            # 간단한 텍스트 기반 지식 베이스 로드
            self._load_knowledge_base()
            
            self.initialized = True
            print(f"✅ RAG Chatbot initialized successfully (using REST API)")
            print(f"📡 API URL: {self.api_url}")
            
        except Exception as e:
            print(f"❌ Failed to initialize RAG Chatbot: {e}")
            self.initialized = False
    
    def _load_knowledge_base(self):
        """Load knowledge base file into memory for simple text search"""
        try:
            with open("knowledge_base.txt", "r", encoding="utf-8") as f:
                content = f.read()

            # Split by sections
            sections = content.split("\n##")

            for i, section in enumerate(sections):
                if section.strip():
                    self.knowledge_base.append({
                        'id': i,
                        'content': section.strip(),
                        'content_lower': section.strip().lower()
                    })

            print(f"✅ Loaded {len(self.knowledge_base)} documents into knowledge base")
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
    
    def _search_knowledge(self, query: str, top_k: int = 3) -> List[str]:
        """Search for documents related to the query (simple keyword matching)"""
        try:
            query_lower = query.lower()
            query_words = set(query_lower.split())

            # Calculate matching score for each document
            scored_docs = []
            for doc in self.knowledge_base:
                doc_words = set(doc['content_lower'].split())

                # Count common words
                common_words = query_words.intersection(doc_words)
                score = len(common_words)

                # Partial keyword matching
                for word in query_words:
                    if word in doc['content_lower']:
                        score += 2  # Weight for partial matching

                if score > 0:
                    scored_docs.append((score, doc['content']))

            # Sort by score and return top_k
            scored_docs.sort(reverse=True, key=lambda x: x[0])
            return [doc for score, doc in scored_docs[:top_k]]

        except Exception as e:
            print(f"❌ Error searching knowledge: {e}")
            return []
    
    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Generate RAG-based chatbot response (direct REST API call)"""
        if not self.initialized:
            return "Sorry, the chatbot service is currently unavailable. Please contact the administrator."

        try:
            # 1. Search for relevant knowledge
            relevant_docs = self._search_knowledge(user_message)

            # 2. Build context
            context = "\n\n".join(relevant_docs) if relevant_docs else "No information available."

            # 3. Detect language and generate prompt
            # Simple language detection (check Korean character ratio)
            korean_chars = sum(1 for c in user_message if '\uac00' <= c <= '\ud7a3')
            total_chars = len(user_message.replace(' ', ''))
            is_korean = (korean_chars / total_chars > 0.3) if total_chars > 0 else False

            if is_korean:
                system_prompt = f"""You are a friendly customer support chatbot for Seoul Chess Club (SCC).
Please answer the user's question **in Korean** based on the knowledge base below.

Knowledge Base:
{context}

Response Guidelines:
- Use a friendly and warm tone in **Korean**
- Base your answer on the information from the knowledge base
- If you're unsure, start with "확실하지 않지만..." (I'm not entirely certain, but...)
- Use emojis appropriately (♟️, ✨, 🎉, etc.)
- Keep answers concise, 2-3 sentences
"""
                user_label = "User Question"
            else:
                system_prompt = f"""You are a friendly customer support chatbot for Seoul Chess Club (SCC).
Please answer the user's question **in English** based on the knowledge base below.

Knowledge Base:
{context}

Response Guidelines:
- Use a friendly and warm tone in **English**
- Base your answer on the information from the knowledge base
- If you're unsure, start with "I'm not entirely certain, but..."
- Use emojis appropriately (♟️, ✨, 🎉, etc.)
- Keep answers concise, 2-3 sentences
"""
                user_label = "User Question"

            # 4. Build REST API request
            full_prompt = f"{system_prompt}\n\n{user_label}: {user_message}"

            payload = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }

            # 5. Call Gemini REST API
            response = requests.post(
                f"{self.api_url}?key={self.gemini_api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        text = candidate['content']['parts'][0]['text']
                        return text.strip()
                    else:
                        print(f"❌ Unexpected response structure: {result}")
                        return "Sorry, I couldn't generate a response. Please try again."
                else:
                    print(f"❌ No candidates in response: {result}")
                    return "Sorry, I couldn't generate a response. Please try again."
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return f"Sorry, a temporary error occurred. (Error code: {response.status_code})"

        except requests.exceptions.Timeout:
            print(f"❌ Timeout error in chat")
            return "Sorry, the request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error in chat: {e}")
            return "Sorry, a network error occurred. Please check your connection and try again."
        except Exception as e:
            print(f"❌ Unexpected error in chat: {e}")
            return "Sorry, an unexpected error occurred. Please try again."


# Singleton instance
_chatbot_instance = None

def get_chatbot() -> RAGChatbot:
    """Get chatbot instance (singleton)"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = RAGChatbot()
    return _chatbot_instance

