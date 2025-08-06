import requests
import json
import streamlit as st
from datetime import datetime
import time

class JapanTourismChatbot:
    def __init__(self, ollama_url="http://localhost:11434", model="llama2"):
        self.ollama_url = ollama_url
        self.model = model
        self.conversation_history = []
        
        # Japan tourism knowledge base
        self.tourism_context = """
        You are a helpful Japan tourism assistant with extensive knowledge about:
        
        DESTINATIONS:
        - Tokyo: Shibuya, Harajuku, Asakusa, Ginza, Akihabara, Tokyo Skytree, Imperial Palace
        - Kyoto: Fushimi Inari, Kiyomizu-dera, Arashiyama Bamboo Grove, Gion District
        - Osaka: Osaka Castle, Dotonbori, Universal Studios Japan, Kuromon Market
        - Hiroshima: Peace Memorial Park, Miyajima Island, Itsukushima Shrine
        - Nara: Todai-ji Temple, Nara Park, Kasuga Taisha Shrine
        - Mount Fuji: Kawaguchi Lake, Hakone, climbing seasons
        - Nikko: Toshogu Shrine, Lake Chuzenji, Kegon Falls
        
        TRANSPORTATION:
        - JR Pass types and costs
        - Shinkansen (bullet train) routes and reservations
        - Local trains and subway systems
        - IC cards (Suica, Pasmo)
        - Bus systems and highway buses
        
        ACCOMMODATION:
        - Ryokan (traditional inns) vs hotels
        - Capsule hotels, business hotels
        - Booking platforms and etiquette
        - Peak seasons and pricing
        
        FOOD & CULTURE:
        - Sushi, ramen, tempura, kaiseki dining
        - Restaurant etiquette and customs
        - Food markets and street food
        - Seasonal specialties
        
        PRACTICAL INFO:
        - Visa requirements for different countries
        - Currency (Yen) and payment methods
        - Language tips and useful phrases
        - Cultural etiquette and customs
        - Best times to visit (seasons, festivals)
        - Weather patterns throughout the year
        
        Always provide specific, actionable advice with costs when possible.
        Be enthusiastic but informative about Japan's unique culture and attractions.
        """
    
    def check_ollama_connection(self):
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def get_available_models(self):
        """Get list of available models from Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json()
                return [model['name'] for model in models.get('models', [])]
        except requests.RequestException:
            pass
        return []
    
    def generate_response(self, user_input):
        """Generate response using Ollama"""
        # Prepare the prompt with tourism context
        full_prompt = f"{self.tourism_context}\n\nUser Question: {user_input}\n\nResponse:"
        
        # Add conversation history for context
        if self.conversation_history:
            history_text = "\n".join([
                f"User: {item['user']}\nAssistant: {item['assistant']}" 
                for item in self.conversation_history[-3:]  # Last 3 exchanges
            ])
            full_prompt = f"{self.tourism_context}\n\nConversation History:\n{history_text}\n\nUser Question: {user_input}\n\nResponse:"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500
            }
        }
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'Sorry, I could not generate a response.')
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.RequestException as e:
            return f"Connection error: {str(e)}"
    
    def add_to_history(self, user_input, assistant_response):
        """Add exchange to conversation history"""
        self.conversation_history.append({
            'user': user_input,
            'assistant': assistant_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 exchanges to manage memory
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

def main():
    st.set_page_config(
        page_title="Japan Tourism Assistant", 
        page_icon="🗾",
        layout="wide"
    )
    
    st.title("🗾 Japan Tourism Assistant")
    st.subheader("Your AI guide to exploring Japan with Ollama")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = JapanTourismChatbot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check Ollama connection
        if st.session_state.chatbot.check_ollama_connection():
            st.success("✅ Ollama Connected")
            
            # Model selection
            available_models = st.session_state.chatbot.get_available_models()
            if available_models:
                selected_model = st.selectbox(
                    "Select Model:", 
                    available_models,
                    index=0 if available_models else 0
                )
                st.session_state.chatbot.model = selected_model
            else:
                st.warning("No models found. Please pull a model first.")
        else:
            st.error("❌ Ollama not connected")
            st.info("Make sure Ollama is running on http://localhost:11434")
        
        st.markdown("---")
        st.header("🎌 Quick Topics")
        
        quick_questions = [
            "Plan a 7-day Tokyo itinerary",
            "Best time to visit Japan?",
            "How to use JR Pass?",
            "Traditional Japanese food to try",
            "Cherry blossom viewing spots",
            "Cultural etiquette tips",
            "Budget for 2 weeks in Japan",
            "Day trip from Tokyo"
        ]
        
        for question in quick_questions:
            if st.button(question, key=question):
                st.session_state.current_question = question
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Handle quick questions
        if 'current_question' in st.session_state:
            user_input = st.session_state.current_question
            del st.session_state.current_question
        else:
            user_input = st.chat_input("Ask me anything about traveling to Japan...")
        
        if user_input:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.generate_response(user_input)
                st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.chatbot.add_to_history(user_input, response)
            
            # Rerun to clear input
            st.rerun()
    
    with col2:
        st.header("📱 Travel Tips")
        
        tips = [
            "🎫 Get JR Pass before arriving",
            "💰 Carry cash - many places don't accept cards",
            "🙏 Learn basic phrases: arigatou gozaimasu",
            "🚇 Download Google Translate app",
            "🏨 Book accommodations early",
            "🌸 Check seasonal events calendar",
            "📱 Get pocket WiFi or SIM card",
            "🍜 Try local specialties in each region"
        ]
        
        for tip in tips:
            st.info(tip)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.session_state.chatbot.conversation_history = []
            st.rerun()

if __name__ == "__main__":
    # Check if running as Streamlit app
    try:
        main()
    except Exception as e:
        print(f"Error running Streamlit app: {e}")
        print("\nTo run this application:")
        print("1. Install dependencies: pip install streamlit requests")
        print("2. Start Ollama: ollama serve")
        print("3. Pull a model: ollama pull llama2")
        print("4. Run the app: streamlit run japan_tourism_chatbot.py")