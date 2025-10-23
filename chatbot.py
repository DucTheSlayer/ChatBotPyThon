import google.generativeai as genai
import json
import os
import random
from datetime import datetime
from config import GEMINI_API_KEY, SYSTEM_PROMPT, CHAT_HISTORY_FILE

class CNTTChatbot:
    def __init__(self):
        """Khởi tạo chatbot với Gemini API"""
        if not GEMINI_API_KEY:
            raise ValueError("Vui lòng cung cấp GEMINI_API_KEY trong file .env")
        
        # Cấu hình Gemini API
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Khởi tạo chat session
        self.chat = self.model.start_chat(history=[])
        
        # Load chat history
        self.chat_history = self.load_chat_history()
    
    def load_chat_history(self):
        """Load lịch sử chat từ file"""
        if os.path.exists(CHAT_HISTORY_FILE):
            try:
                with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_chat_history(self):
        """Lưu lịch sử chat vào file"""
        try:
            with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu lịch sử chat: {e}")
    
    def get_response(self, user_message):
        """Nhận phản hồi từ chatbot"""
        try:
            # Thêm system prompt vào đầu tin nhắn
            full_message = f"{SYSTEM_PROMPT}\n\nCâu hỏi của sinh viên: {user_message}"
            
            # Gửi tin nhắn đến Gemini
            response = self.chat.send_message(full_message)
            
            # Lưu vào lịch sử chat
            chat_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "bot_response": response.text
            }
            self.chat_history.append(chat_entry)
            self.save_chat_history()
            
            return response.text
            
        except Exception as e:
            error_message = f"Xin lỗi, đã có lỗi xảy ra: {str(e)}"
            return error_message
    
    def get_chat_history(self):
        """Lấy lịch sử chat"""
        return self.chat_history
    
    def clear_history(self):
        """Xóa lịch sử chat"""
        self.chat_history = []
        self.save_chat_history()
        # Reset chat session
        self.chat = self.model.start_chat(history=[])
    
    def get_suggested_questions(self):
        """Trả về danh sách câu hỏi gợi ý"""
        questions = [
            "Tôi nên học ngôn ngữ lập trình nào trước?",
            "Lộ trình học lập trình web như thế nào?",
            "Cơ hội nghề nghiệp trong lĩnh vực AI/ML?",
            "Làm thế nào để chuẩn bị cho kỳ thực tập?",
            "Nên chọn chuyên ngành nào trong CNTT?",
            "Kỹ năng nào quan trọng nhất cho sinh viên CNTT?",
            "Làm sao để xây dựng portfolio dự án?",
            "Tư vấn về việc học thêm chứng chỉ IT?",
            "Sinh viên an toàn thông tin có việc làm không?",
            "Làm sao để cải thiện kỹ năng giải thuật?",
            "Back-end và Front-end khác nhau thế nào?",
            "Hỏi Data Science thì cần gì?",
            "DevOps làm những công việc gì?",
            "Làm sao để luyện phỏng vấn IT?"
        ]    
        return random.sample(questions, 5)