import os
import chromadb
from chromadb.config import Settings
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class RAGChatbot:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # ChromaDB 초기화
        self.chroma_client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            is_persistent=True,
            persist_directory="./chroma_db"
        ))
        
        # 컬렉션 생성 또는 가져오기
        try:
            self.collection = self.chroma_client.get_collection(name="scc_knowledge")
        except:
            self.collection = self.chroma_client.create_collection(
                name="scc_knowledge",
                metadata={"description": "Seoul Chess Club knowledge base"}
            )
            self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """지식 베이스 파일을 읽어서 ChromaDB에 저장"""
        try:
            with open("knowledge_base.txt", "r", encoding="utf-8") as f:
                content = f.read()
            
            # 섹션별로 분할
            sections = content.split("\n##")
            documents = []
            metadatas = []
            ids = []
            
            for i, section in enumerate(sections):
                if section.strip():
                    # Gemini로 임베딩 생성
                    documents.append(section.strip())
                    metadatas.append({"source": "knowledge_base.txt", "section": i})
                    ids.append(f"doc_{i}")
            
            # ChromaDB에 저장
            if documents:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"✅ Loaded {len(documents)} documents into knowledge base")
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
    
    def _search_knowledge(self, query: str, top_k: int = 3) -> List[str]:
        """쿼리와 관련된 문서 검색"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            if results and results['documents']:
                return results['documents'][0]
            return []
        except Exception as e:
            print(f"❌ Error searching knowledge: {e}")
            return []
    
    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """RAG 기반 챗봇 응답 생성"""
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
            
            # 4. 대화 히스토리 구성
            messages = []
            if conversation_history:
                for msg in conversation_history[-5:]:  # 최근 5개만
                    messages.append({"role": msg["role"], "parts": [msg["content"]]})
            
            # 5. Gemini API 호출
            chat = self.model.start_chat(history=messages)
            response = chat.send_message(f"{system_prompt}\n\n사용자 질문: {user_message}")
            
            return response.text
            
        except Exception as e:
            print(f"❌ Error in chat: {e}")
            return f"죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요. 오류: {str(e)}"
    
    def reset_knowledge_base(self):
        """지식 베이스 초기화 (관리자용)"""
        try:
            self.chroma_client.delete_collection(name="scc_knowledge")
            self.collection = self.chroma_client.create_collection(
                name="scc_knowledge",
                metadata={"description": "Seoul Chess Club knowledge base"}
            )
            self._load_knowledge_base()
            return True
        except Exception as e:
            print(f"❌ Error resetting knowledge base: {e}")
            return False


# 싱글톤 인스턴스
_chatbot_instance = None

def get_chatbot() -> RAGChatbot:
    """챗봇 인스턴스 가져오기 (싱글톤)"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = RAGChatbot()
    return _chatbot_instance

