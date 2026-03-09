from flask import Flask, render_template, request, jsonify
from chatbot import DeepSeekChatbot
import logging
import traceback
import os  # 新增：需要讀取環境變數

# 設置日誌
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# 初始化聊天機器人
try:
    # 從環境變數讀取 API Key（Streamlit Cloud 會透過 Secrets 設定）
    api_key = os.getenv("IFLOW_API_KEY")
    if not api_key:
        logging.error("❌ 沒有設定 IFLOW_API_KEY 環境變數")
        bot = None
        welcome_message = "✨ 你來啦～今天過得怎麼樣？"
    else:
        # 可以在這裡傳入 API key，或者讓 chatbot.py 自己讀取環境變數
        # 如果你的 chatbot.py 會自己讀 .env，這行就不需要改
        bot = DeepSeekChatbot()
        welcome_message = bot.get_welcome_message()
        logging.info("✅ 療癒精靈初始化成功")
        
except Exception as e:
    logging.error(f"❌ 初始化失敗：{e}")
    logging.error(traceback.format_exc())
    bot = None
    welcome_message = "✨ 你來啦～今天過得怎麼樣？"

@app.route('/')
def home():
    return render_template('index.html', welcome_message=welcome_message)

@app.route('/chat', methods=['POST'])
def chat():
    if not bot:
        return jsonify({
            'response': '✨ 對不起，我現在有點累，等等再來找我好嗎？',
            'status': 'error'
        })
    
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'response': '🌙 我在這裡，你想說什麼呢？',
                'status': 'error'
            })
        
        response = bot.chat(user_message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f"聊天錯誤：{e}")
        return jsonify({
            'response': '✨ 可以再說一次嗎？我剛剛沒聽清楚。',
            'status': 'error'
        })

@app.route('/clear', methods=['POST'])
def clear_history():
    if bot:
        result = bot.clear_history()
        return jsonify({'message': result, 'status': 'success'})
    return jsonify({'message': '✨ 我們重新開始吧～', 'status': 'success'})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'bot_initialized': bot is not None,
        'model': bot.model if bot else None
    })

if __name__ == '__main__':
    # 雲端部署需要從環境變數讀取 port，預設 5000
    port = int(os.getenv("PORT", 5000))
    # 生產環境關閉 debug 模式
    app.run(host='0.0.0.0', port=port, debug=False)