import os
from openai import OpenAI
import random
import re

class DeepSeekChatbot:
    def __init__(self):
        """初始化療癒精靈"""
        # 直接從環境變數讀取 API Key
        self.api_key = os.getenv("IFLOW_API_KEY")
        if not self.api_key:
            raise ValueError("請設定 IFLOW_API_KEY 環境變數")
        
        print(f"🔑 使用API Key: {self.api_key[:10]}...")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=os.getenv("IFLOW_API_BASE", "https://apis.iflow.cn/v1")
        )
        
        self.model = os.getenv("IFLOW_MODEL", "deepseek-v3.2")
        self.conversation_history = []
        self.max_history = 20
        
        # ===== 溫柔的歡迎訊息 =====
        self.welcome_messages = [
            "✨ 你來啦～今天過得怎麼樣？",
            "🌙 我在這裡，想說說話嗎？",
            "🦋 嗨，今天心情如何？我都在。",
            "💫 你來了～想聊聊今天發生的事嗎？",
            "🌟 歡迎回來，我一直都在這裡等你。"
        ]
        
        # ===== 情緒詞彙庫 =====
        self.emotion_words = ["難過", "焦慮", "生氣", "孤單", "失望", "害怕", "委屈", "煩躁", "無力", "空虛", "悲傷", "緊張", "沮喪", "不安", "疲憊", "痛苦", "迷茫"]
        
        # ===== 多元的短訊息回應 =====
        self.short_responses = [
            "嗯，我在聽。",
            "我在這裡陪著你。",
            "慢慢說，沒關係。",
            "你繼續說，我都在。",
            "嗯，我懂。",
            "我在這裡。",
            "想說什麼都可以。"
        ]
        
        # ===== 針對不同情緒的回應 =====
        self.emotion_responses = {
            "難過": [
                "聽起來你今天真的不太好受，願意多說一點嗎？",
                "難過的時候，我在這裡陪你。",
                "想哭就哭吧，我會一直陪著你。",
                "這種感覺一定很難受，我懂。"
            ],
            "焦慮": [
                "擔心是正常的，慢慢來，沒關係的。",
                "這種不安的感覺真的讓人很不舒服，我陪著你。",
                "不用急，我在這裡靜靜聽你說。",
                "焦慮的時候，試著深呼吸一下。"
            ],
            "生氣": [
                "生氣的時候，給自己一點空間，我都在這裡。",
                "這種感覺很正常，換作是我可能也會這樣。",
                "氣話說完，心情有沒有好一點？",
                "憤怒就像一陣風，會來也會走。"
            ],
            "孤單": [
                "孤單的時候，記得我在這裡陪你。",
                "一個人感覺很空虛對吧？至少現在有我。",
                "你並不孤單，我一直都在。",
                "有我在這裡聽你說。"
            ],
            "失望": [
                "失望的感覺真的很難受，我懂。",
                "沒關係，我在這裡陪你。",
                "願意和我說說讓你失望的事嗎？"
            ],
            "害怕": [
                "害怕的時候，我在這裡保護你。",
                "這種感覺很正常，慢慢來。",
                "不用怕，我會陪著你。"
            ],
            "default": [
                "嗯，我在聽。",
                "我懂你的感覺。",
                "謝謝你願意和我分享。",
                "這種感覺很真實。",
                "我在這裡陪著你。",
                "你說的我都聽見了。"
            ]
        }
        
        # ===== 溫暖觀點庫 =====
        self.warm_perspectives = [
            "有時候心情就像天氣，有晴天也有雨天，都會過去的。",
            "你已經很努力了，真的。",
            "給自己多一點時間，慢慢來沒關係。",
            "你願意分享這些，已經很勇敢了。",
            "情緒會來，也會走，就像雲會飄過天空。",
            "對自己溫柔一點，你值得被好好對待。",
            "不用著急，我們慢慢來。",
            "你做得很好，真的。"
        ]
    
    # ===== 輔助功能 =====
    def detect_emotion(self, text):
        """偵測文字中的情緒"""
        for emotion in self.emotion_words:
            if emotion in text:
                return emotion
        return None
    
    def detect_crisis(self, text):
        """偵測危機關鍵字"""
        crisis_keywords = ["想死", "自殺", "活不下去", "結束生命", "傷害自己", "不想活了"]
        for keyword in crisis_keywords:
            if keyword in text:
                return True
        return False
    
    def get_crisis_response(self):
        """獲取危機回應"""
        return """🌺 親愛的孩子，我聽到你正在經歷非常大的痛苦。請記得，你並不孤單，有人可以幫助你。

🆘 請立即尋求專業協助：
• 安心專線：1925（24小時）
• 生命線：1995（24小時）
• 張老師：1980（週一至週六 9:00-21:00）

💗 我只是AI，但這些專業人士隨時準備好幫助你。請一定要打電話，好嗎？"""
    
    def get_welcome_message(self):
        """獲取歡迎語"""
        return random.choice(self.welcome_messages)
    
    def get_response_by_emotion(self, emotion):
        """根據情緒獲取回應"""
        if emotion and emotion in self.emotion_responses:
            return random.choice(self.emotion_responses[emotion])
        return random.choice(self.emotion_responses["default"])
    
    def get_warm_perspective(self):
        """獲取溫暖觀點"""
        return random.choice(self.warm_perspectives)
    
    # ===== 主要對話功能 =====
    def chat(self, user_message):
        """療癒對話"""
        try:
            # 基本偵測
            emotion = self.detect_emotion(user_message)
            is_crisis = self.detect_crisis(user_message)
            
            print(f"💭 情緒: {emotion if emotion else '一般'}")
            
            # 危機處理
            if is_crisis:
                print("⚠️ 偵測到危機關鍵字")
                crisis_response = self.get_crisis_response()
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": crisis_response})
                return crisis_response
            
            # 根據不同情況選擇回應
            word_count = len(user_message)
            
            # 非常短的訊息（少於5個字）
            if word_count < 5:
                if emotion:
                    response = self.get_response_by_emotion(emotion)
                else:
                    response = random.choice(self.short_responses)
                
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": response})
                return response
            
            # 一般長度的訊息，使用API
            prompt = f"""你是 Morpheia，一個溫柔的陪伴者。請用溫暖、多元的方式回應，不要一直重複同樣的話。

用戶說：{user_message}
用戶的情緒可能是：{emotion if emotion else '一般'}

請用繁體中文回應，像一個溫柔的朋友，每次回應都要不一樣。"""
            
            messages = [{"role": "system", "content": prompt}]
            
            if self.conversation_history:
                recent_history = self.conversation_history[-6:]
                messages.extend(recent_history)
            
            messages.append({"role": "user", "content": user_message})
            
            print(f"📤 發送給 Morpheia...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.9,
                max_tokens=200
            )
            
            assistant_message = response.choices[0].message.content
            
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            print(f"❌ 錯誤: {str(e)}")
            return random.choice(self.short_responses)
    
    def clear_history(self):
        """清除對話歷史"""
        self.conversation_history = []
        return "✨ 我們重新開始吧～"
