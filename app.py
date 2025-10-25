import streamlit as st
import time
from chatbot import CNTTChatbot
from config import CHATBOT_NAME, CHATBOT_DESCRIPTION
import os

# Cấu hình trang
st.set_page_config(
    page_title=CHATBOT_NAME,    
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS theme tối như ChatGPT
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global dark theme */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #0f0f0f;
        color: #ffffff;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
        background: #0f0f0f;
    }
    
    
    /* Chat messages styling */
    .stChatMessage {
        margin: 1rem 0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* User message */
    .stChatMessage[data-testid="user-message"] {
        background: #1a1a1a;
        color: white;
        margin-left: 10%;
        border: 1px solid #333;
    }
    
    /* Assistant message */
    .stChatMessage[data-testid="assistant-message"] {
        background: #1a1a1a;
        color: white;
        margin-right: 10%;
        border: 1px solid #333;
    }
    
    /* Chat input area - FIX cho input */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #333;
        background: #1a1a1a !important;
        color: white !important;
        font-size: 1rem;
        padding: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .stTextArea textarea:focus {
        border-color: #4a9eff;
        box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.2);
        background: #1a1a1a !important;
        color: white !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #888 !important;
    }
    
    /* Buttons styling */
    .stButton > button {
        border-radius: 12px;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4a9eff 0%, #0066cc 100%);
        color: white;
    }
    
    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: #2d2d2d;
        color: white;
        border: 1px solid #444;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #1a1a1a;
        border-radius: 15px;
        margin: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid #333;
    }
    
    /* Sidebar text color fix */
    .css-1d391kg h1, 
    .css-1d391kg h2, 
    .css-1d391kg h3, 
    .css-1d391kg p, 
    .css-1d391kg div,
    .css-1d391kg span,
    .css-1d391kg label {
        color: white !important;
    }
    
    .sidebar-info {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid #333;
    }
    
    .sidebar-info h3 {
        color: white;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .sidebar-info ul {
        list-style: none;
        padding: 0;
    }
    
    .sidebar-info li {
        padding: 0.5rem 0;
        border-bottom: 1px solid #333;
        font-size: 0.9rem;
        color: #cccccc;
    }
    
    /* Suggested questions */
    .suggested-question {
        background: #2d2d2d;
        border: 1px solid #444;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
        font-size: 0.9rem;
        text-align: left;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .suggested-question:hover {
        background: #4a9eff;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(74, 158, 255, 0.3);
        border-color: #4a9eff;
    }
    
    /* Metrics styling */
    .metric-container {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Loading spinner */
    .stSpinner {
        color: #4a9eff;
    }
    
    /* Form styling */
    .stForm {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #666;
    }
    
    /* Animation keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stChatMessage {
        animation: fadeInUp 0.5s ease-out;
    }
    
    
    /* Welcome message styling */
    .welcome-message {
        text-align: center;
        padding: 3rem 2rem;
        color: #cccccc;
        background: #1a1a1a;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid #333;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Fix cho tất cả text elements */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: white !important;
    }
    
    /* Fix cho metrics */
    .metric-container .metric-value {
        color: white !important;
    }
    
    /* Fix cho labels */
    .stTextArea label {
        color: white !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .stChatMessage[data-testid="user-message"],
        .stChatMessage[data-testid="assistant-message"] {
            margin-left: 0;
            margin-right: 0;
        }
        
        .chat-container {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .main-header {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Khởi tạo chatbot"""
    if 'chatbot' not in st.session_state:
        try:
            st.session_state.chatbot = CNTTChatbot()
        except ValueError as e:
            st.error(f"Lỗi khởi tạo chatbot: {e}")
            st.error("Vui lòng kiểm tra file .env và đảm bảo GEMINI_API_KEY được cấu hình đúng.")
            st.stop()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'chat_sessions' not in st.session_state:
        st.session_state.chat_sessions = []


def main():
    # Khởi tạo chatbot
    initialize_chatbot()
    
    # Sidebar với lịch sử chat
    with st.sidebar:
        # Header cho sidebar
        st.markdown("### 💬 Lịch sử chat")
        
        # Hiển thị lịch sử chat cũ (luôn hiển thị từ chatbot history)
        import datetime
        
        # Lấy tất cả tin nhắn từ chatbot history
        all_messages = st.session_state.chatbot.get_chat_history()
        
        if all_messages:
            # Nhóm tin nhắn theo session (mỗi session là một cuộc trò chuyện hoàn chỉnh)
            sessions = []
            
            for msg in all_messages:
                if 'user_message' in msg and 'bot_response' in msg:
                    # Tạo session mới cho mỗi cặp user-bot
                    session = {
                        'user': msg['user_message'],
                        'bot': msg['bot_response'],
                        'timestamp': msg.get('timestamp', ''),
                        'id': len(sessions)
                    }
                    sessions.append(session)
            
            # Hiển thị các session chat
            for session in sessions[-10:]:  # Chỉ hiển thị 10 session gần nhất
                user_msg = session['user']
                # Rút gọn tin nhắn nếu quá dài
                display_msg = user_msg[:40] + "..." if len(user_msg) > 40 else user_msg
                
                # Format thời gian
                time_str = ""
                if session['timestamp']:
                    try:
                        dt = datetime.datetime.fromisoformat(session['timestamp'].replace('Z', '+00:00'))
                        time_str = dt.strftime("%H:%M")
                    except:
                        time_str = ""
                
                if st.button(
                    f"💭 {display_msg}" + (f" ({time_str})" if time_str else ""),
                    key=f"load_session_{session['id']}",
                    use_container_width=True,
                    help=f"Click để xem cuộc trò chuyện: {user_msg}"
                ):
                    # Load lại session này
                    st.session_state.messages = [
                        {"role": "user", "content": session['user']},
                        {"role": "assistant", "content": session['bot']}
                    ]
                    st.rerun()
        else:
            st.info("Chưa có cuộc trò chuyện nào")
        
        st.markdown("---")
        
        # Nút tạo cuộc trò chuyện mới
        if st.button("➕ Cuộc trò chuyện mới", type="primary", use_container_width=True):
            # Chỉ xóa tin nhắn hiện tại, không xóa lịch sử
            st.session_state.messages = []
            st.success("✅ Đã tạo cuộc trò chuyện mới!")
            st.rerun()
        
        # Nút xóa lịch sử
        if st.button("🗑️ Xóa lịch sử chat", type="secondary", use_container_width=True):
            st.session_state.chatbot.clear_history()
            st.session_state.messages = []
            st.success("✅ Đã xóa lịch sử chat!")
            st.rerun()
    
    # Hiển thị lịch sử chat hoặc welcome message
    if st.session_state.messages:
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(f"**👤 Bạn:** {message['content']}")
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"**🤖 {CHATBOT_NAME}:** {message['content']}")
    else:
        # Welcome message khi chưa có tin nhắn
        st.markdown("""
        <div class="welcome-message">
            <h3>👋 Chào mừng bạn đến với CNTT Chatbot!</h3>
            <p>Hãy bắt đầu cuộc trò chuyện bằng cách nhập câu hỏi bên dưới hoặc chọn một câu hỏi gợi ý.</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Sidebar với suggested questions
    with st.sidebar:
        # Câu hỏi gợi ý với design tối
        st.markdown("### 💡 Câu hỏi gợi ý")
        st.markdown("Chọn một câu hỏi để bắt đầu cuộc trò chuyện:")
        
        suggested_questions = st.session_state.chatbot.get_suggested_questions()
        
        for i, question in enumerate(suggested_questions):
            if st.button(
                f"💭 {question}", 
                key=f"suggest_{i}", 
                use_container_width=True,
                help="Nhấp để sử dụng câu hỏi này"
            ):
                st.session_state.suggested_question = question
                st.rerun()
        
    
    # Xử lý tin nhắn
    # THÊM KHỐI MỚI NÀY VÀO CUỐI HÀM MAIN()

    # Xử lý input (hoặc từ chat_input hoặc từ câu hỏi gợi ý)
    
    # Kiểm tra xem có câu hỏi gợi ý nào được click không (set trong sidebar)
    if hasattr(st.session_state, 'suggested_question'):
        user_input = st.session_state.suggested_question
        del st.session_state.suggested_question # Xóa đi để không bị lặp lại
    else:
        user_input = None
        
    # Lấy input từ st.chat_input (thanh nhập liệu ở dưới cùng)
    if prompt := st.chat_input("Ví dụ: Tôi nên học ngôn ngữ lập trình nào trước?"):
        user_input = prompt # Ghi đè user_input nếu người dùng gõ

    # Nếu có user_input (từ 1 trong 2 nguồn)
    if user_input:
        # Thêm tin nhắn người dùng
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Hiển thị tin nhắn người dùng ngay lập tức
        with st.chat_message("user"):
            st.markdown(f"**👤 Bạn:** {user_input}")
        
        # Hiển thị typing indicator và loading
        with st.chat_message("assistant"):
            with st.spinner("🤖 Đang suy nghĩ..."):
                response = st.session_state.chatbot.get_response(user_input)
        
        # Thêm phản hồi bot
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun để hiển thị tin nhắn mới của bot từ history
        st.rerun()

if __name__ == "__main__":
    main()
