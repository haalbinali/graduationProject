import streamlit as st
from datetime import datetime
import time

class CloudJapanTourismChatbot:
    def __init__(self):
        self.conversation_history = []
        
        # Japan tourism knowledge base - same as original
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
        
        # Pre-built responses for demo (since we can't use real AI without API key)
        self.demo_responses = {
            "plan a 7-day tokyo itinerary": """
            🗼 **7-Day Tokyo Itinerary**
            
            **Day 1: Traditional Tokyo**
            - Morning: Senso-ji Temple in Asakusa
            - Afternoon: Imperial Palace East Gardens
            - Evening: Dinner in Ginza district
            
            **Day 2: Modern Tokyo**
            - Morning: Tokyo Skytree and surrounding area
            - Afternoon: Harajuku and Takeshita Street
            - Evening: Shibuya crossing and nightlife
            
            **Day 3: Otaku Culture**
            - Morning: Akihabara electronics district
            - Afternoon: Anime/manga shopping
            - Evening: Themed café experience
            
            **Day 4: Parks and Museums**
            - Morning: Ueno Park and museums
            - Afternoon: Ameya-Yokocho market
            - Evening: Traditional izakaya dinner
            
            **Day 5: Day Trip**
            - Full day: Nikko (temples and nature)
            - OR: Kamakura (Great Buddha and beaches)
            
            **Day 6: Food and Shopping**
            - Morning: Tsukiji Outer Market
            - Afternoon: Shopping in Shinjuku
            - Evening: Golden Gai bar hopping
            
            **Day 7: Relaxation**
            - Morning: Meiji Shrine
            - Afternoon: Roppongi Hills
            - Evening: Tokyo Bay sunset
            
            **Budget:** ¥8,000-15,000 per day including accommodation
            **Transportation:** Get a 7-day Tokyo Metro pass (¥1,590)
            """,
            
            "best time to visit japan": """
            🌸 **Best Times to Visit Japan**
            
            **Spring (March-May) - MOST POPULAR**
            - Cherry blossoms (sakura) season
            - Mild weather, perfect for sightseeing
            - Peak season: Higher prices, crowds
            - Best for: First-time visitors, nature lovers
            
            **Summer (June-August)**
            - Hot and humid, especially July-August
            - Rainy season in June-July
            - Festivals and fireworks
            - Best for: Festival enthusiasts, beach activities
            
            **Autumn (September-November) - HIGHLY RECOMMENDED**
            - Beautiful fall foliage (koyo)
            - Comfortable temperatures
            - Less crowded than spring
            - Best for: Photography, hiking, comfortable travel
            
            **Winter (December-February)**
            - Cold but clear skies
            - Snow in northern regions
            - Fewer tourists, lower prices
            - Best for: Skiing, hot springs, budget travelers
            
            **My Recommendation:** 
            - **First visit:** Late March-April or October-November
            - **Budget travel:** January-February
            - **Festivals:** July-August
            - **Photography:** November or April
            """,
            
            "how to use jr pass": """
            🚅 **JR Pass Complete Guide**
            
            **What is JR Pass?**
            - Unlimited travel on JR trains including most Shinkansen
            - Must be purchased before arriving in Japan
            - Only for tourists with temporary visitor status
            
            **Types & Prices (2024):**
            - 7 days: ¥29,650 (≈$200)
            - 14 days: ¥47,250 (≈$320)
            - 21 days: ¥60,450 (≈$410)
            
            **How to Use:**
            1. **Before Japan:** Buy exchange voucher online
            2. **In Japan:** Exchange voucher at major stations
            3. **Activation:** Choose start date (within 3 months)
            4. **Travel:** Show pass at JR gates, don't use IC card readers
            
            **Covered Trains:**
            ✅ All JR local trains
            ✅ Most Shinkansen (except Nozomi and Mizuho)
            ✅ JR buses
            ✅ JR ferry to Miyajima
            
            **NOT Covered:**
            ❌ Private railways (Tokyo Metro, Keihan, etc.)
            ❌ Nozomi/Mizuho Shinkansen (fastest trains)
            ❌ Non-JR buses and subways
            
            **Money-Saving Tip:**
            Break-even point is about 2-3 long-distance trips
            Example: Tokyo-Kyoto return (¥26,000) almost pays for 7-day pass
            
            **Reservations:**
            - Free seat reservations at JR offices
            - Show your pass + passport
            - Recommended for long-distance travel
            """,
            
            "traditional japanese food to try": """
            🍜 **Must-Try Traditional Japanese Foods**
            
            **Sushi & Sashimi**
            - Fresh raw fish over seasoned rice
            - Try: Tuna, salmon, sea urchin, eel
            - Where: Tsukiji, conveyor belt sushi shops
            - Cost: ¥2,000-10,000+ depending on quality
            
            **Ramen**
            - Rich noodle soup, regional varieties
            - Types: Tonkotsu, miso, shoyu, shio
            - Must-try: Ichiran, Ippudo chains
            - Cost: ¥600-1,200 per bowl
            
            **Tempura**
            - Lightly battered and fried seafood/vegetables
            - Best: Shrimp, sweet potato, eggplant
            - Where: Specialized tempura restaurants
            - Cost: ¥1,500-5,000 for a set
            
            **Kaiseki**
            - Multi-course traditional haute cuisine
            - Seasonal ingredients, artistic presentation
            - Where: High-end restaurants, ryokan
            - Cost: ¥8,000-30,000+ per person
            
            **Yakitori**
            - Grilled chicken skewers
            - Try: Different cuts, not just breast meat
            - Where: Yakitori-ya under train tracks
            - Cost: ¥150-300 per skewer
            
            **Regional Specialties:**
            - **Osaka:** Takoyaki (octopus balls), okonomiyaki
            - **Kyoto:** Tofu cuisine, matcha sweets
            - **Hiroshima:** Hiroshima-style okonomiyaki
            - **Hokkaido:** Fresh seafood, Sapporo beer
            
            **Etiquette Tips:**
            - Say "itadakimasu" before eating
            - Don't stick chopsticks upright in rice
            - Slurping noodles is acceptable
            - Say "gochisousama" after finishing
            """
        }
    
    def generate_response(self, user_input):
        """Generate response using pre-built responses or general guidance"""
        user_input_lower = user_input.lower()
        
        # Check for matching demo responses
        for key, response in self.demo_responses.items():
            if key in user_input_lower:
                return response
        
        # General responses for common topics
        if any(word in user_input_lower for word in ["budget", "money", "cost", "expensive"]):
            return """
            💰 **Japan Budget Guide**
            
            **Daily Budget Estimates:**
            - **Budget:** ¥5,000-8,000 ($35-55) - Hostels, convenience store meals
            - **Mid-range:** ¥10,000-15,000 ($70-105) - Business hotels, restaurant meals  
            - **Luxury:** ¥20,000+ ($140+) - High-end hotels, fine dining
            
            **Major Expenses:**
            - **Accommodation:** ¥2,000-15,000+ per night
            - **Meals:** ¥500-3,000 per meal
            - **Transportation:** JR Pass ¥29,650 for 7 days
            - **Attractions:** ¥300-2,000 per site
            
            **Money-Saving Tips:**
            - Eat at convenience stores (surprisingly good!)
            - Use business hotels instead of Western chains
            - Buy JR Pass for long-distance travel
            - Visit free temples and parks
            - Shop at 100-yen stores
            """
        
        elif any(word in user_input_lower for word in ["etiquette", "manners", "culture", "customs"]):
            return """
            🙏 **Japanese Cultural Etiquette**
            
            **General Manners:**
            - Bow when greeting (slight nod is fine for tourists)
            - Remove shoes when entering homes, some restaurants
            - Don't eat while walking
            - Keep voices low on public transport
            - Don't blow your nose in public
            
            **Dining Etiquette:**
            - Say "itadakimasu" before eating
            - Don't stick chopsticks upright in rice
            - It's OK to slurp noodles
            - Don't tip - it's not expected
            - Pour drinks for others, not yourself
            
            **Temple/Shrine Etiquette:**
            - Bow before entering shrine gates
            - Purify hands and mouth at water basins
            - Clap twice, bow once at shrines
            - Don't take photos of people praying
            - Dress modestly
            
            **Public Transport:**
            - Queue orderly for trains
            - Give priority seats to elderly/pregnant
            - Don't talk on phone
            - Remove backpack in crowded trains
            - Let people exit before boarding
            
            **Gift-Giving:**
            - Bring omiyage (souvenirs) from your country
            - Present with both hands
            - Gifts are opened later, not immediately
            """
        
        elif any(word in user_input_lower for word in ["cherry blossom", "sakura", "spring"]):
            return """
            🌸 **Cherry Blossom Guide**
            
            **Best Viewing Spots:**
            
            **Tokyo:**
            - Ueno Park - Popular, crowded, great atmosphere
            - Chidorigafuchi - Beautiful at night, boat rentals
            - Shinjuku Gyoen - Multiple sakura varieties
            - Meguro River - Scenic riverside walk
            
            **Kyoto:**
            - Maruyama Park - Traditional hanami parties
            - Philosopher's Path - Romantic canal-side walk
            - Daigo-ji Temple - UNESCO site with stunning views
            - Arashiyama - Mountain backdrop
            
            **Osaka:**
            - Osaka Castle Park - Castle + sakura combo
            - Kema Sakuranomiya Park - Riverside picnics
            
            **Timing (varies yearly):**
            - Late March: Southern Japan (Kyushu)
            - Early April: Tokyo, Kyoto, Osaka
            - Late April: Northern areas
            - Peak viewing lasts only 1-2 weeks!
            
            **Hanami Culture:**
            - Traditional flower viewing parties
            - Bring blue tarps, food, drinks
            - Popular spots get crowded early
            - Evening illumination at many parks
            
            **Pro Tips:**
            - Check sakura forecasts before booking
            - Book accommodation early (peak season)
            - Bring portable charger for photos
            - Try sakura-flavored foods and drinks
            """
        
        else:
            # Default response for other questions
            return f"""
            Thank you for your question about "{user_input}"!
            
            This is a demo version showing the interface design. In the full version with Ollama, I would provide detailed information about:
            
            🗾 **Japan Tourism Topics I Can Help With:**
            - Destination planning and itineraries
            - Transportation (JR Pass, trains, buses)
            - Accommodation recommendations  
            - Food and restaurant guidance
            - Cultural etiquette and customs
            - Budget planning and money tips
            - Seasonal travel advice
            - Activity and attraction suggestions
            
            **Try asking about:**
            - "Plan a Tokyo itinerary"
            - "How to use JR Pass"
            - "Best time to visit Japan"
            - "Traditional Japanese food"
            - "Cherry blossom viewing"
            - "Cultural etiquette tips"
            
            The full application runs locally with Ollama for complete AI-powered responses!
            """

def main():
    st.set_page_config(
        page_title="Japan Tourism Assistant - Demo", 
        page_icon="🗾",
        layout="wide"
    )
    
    st.title("🗾 Japan Tourism Assistant")
    st.subheader("Academic Project - Live Demo Version")
    
    # Demo notice
    st.info("🎓 **Academic Project Demo** - This demonstrates the interface and features. The full version uses Ollama for complete AI responses.")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = CloudJapanTourismChatbot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Demo Information")
        st.success("✅ Demo Mode Active")
        st.info("💡 Full version uses Ollama locally for complete AI functionality")
        
        st.markdown("---")
        st.header("🎌 Try These Topics")
        
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
                    time.sleep(1)  # Simulate thinking time
                    response = st.session_state.chatbot.generate_response(user_input)
                st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
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
            st.rerun()
        
        st.markdown("---")
        st.header("🎓 Project Info")
        st.write("**Technology Stack:**")
        st.write("- Frontend: Streamlit")
        st.write("- AI: Ollama (local)")
        st.write("- Language: Python")
        st.write("- Deployment: Cloud demo")

if __name__ == "__main__":
    main()