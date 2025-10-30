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
        """지식 베이스 파일을 읽어서 메모리에 저장 (간단한 텍스트 검색용)"""
        try:
            with open("knowledge_base.txt", "r", encoding="utf-8") as f:
                content = f.read()
            
            # 섹션별로 분할
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
        """쿼리와 관련된 문서 검색 (간단한 키워드 매칭)"""
        try:
            query_lower = query.lower()
            query_words = set(query_lower.split())
            
            # 각 문서에 대해 매칭 점수 계산
            scored_docs = []
            for doc in self.knowledge_base:
                doc_words = set(doc['content_lower'].split())
                
                # 공통 단어 수 계산
                common_words = query_words.intersection(doc_words)
                score = len(common_words)
                
                # 키워드 부분 매칭
                for word in query_words:
                    if word in doc['content_lower']:
                        score += 2  # 부분 매칭에 가중치
                
                if score > 0:
                    scored_docs.append((score, doc['content']))
            
            # 점수 순으로 정렬하고 상위 top_k 반환
            scored_docs.sort(reverse=True, key=lambda x: x[0])
            return [doc for score, doc in scored_docs[:top_k]]
            
        except Exception as e:
            print(f"❌ Error searching knowledge: {e}")
            return []
    
    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """RAG 기반 챗봇 응답 생성 (REST API 직접 호출)"""
        if not self.initialized:
            return "죄송합니다. 챗봇 서비스가 현재 이용 불가능합니다. 관리자에게 문의해주세요."
        
        try:
            # 1. 관련 지식 검색
            relevant_docs = self._search_knowledge(user_message)
            
            # 2. 컨텍스트 구성
            context = "\n\n".join(relevant_docs) if relevant_docs else "정보가 없습니다."
            
            # 3. 프롬프트 생성
            system_prompt = f"""당신은 Seoul Chess Club (SCC)의 친절한 고객 지원 챗봇입니다.
아래의 지식 베이스를 참고하여 사용자의 질문에 답변해주세요.

지식 베이스:
{context}

답변 가이드라인:
- 친근하고 따뜻한 톤으로 답변하세요
- 지식 베이스에 있는 정보를 바탕으로 답변하세요
- 모르는 정보는 솔직하게 "확실하지 않지만..." 이라고 시작하세요
- 이모지를 적절히 사용하세요 (♟️, ✨, 🎉 등)
- 간결하게 2-3문장으로 답변하세요
"""
            
            # 4. REST API 요청 구성
            full_prompt = f"{system_prompt}\n\n사용자 질문: {user_message}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }]
            }
            
            # 5. Gemini REST API 호출
            response = requests.post(
                f"{self.api_url}?key={self.gemini_api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    return text
                else:
                    return "죄송합니다. 응답을 생성할 수 없습니다."
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return f"죄송합니다. 일시적인 오류가 발생했습니다. (오류 코드: {response.status_code})"
            
        except Exception as e:
            print(f"❌ Error in chat: {e}")
            return f"죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요."


# 싱글톤 인스턴스
_chatbot_instance = None

def get_chatbot() -> RAGChatbot:
    """챗봇 인스턴스 가져오기 (싱글톤)"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = RAGChatbot()
    return _chatbot_instance

