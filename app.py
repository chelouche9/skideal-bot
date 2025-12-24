"""Streamlit Chat Interface for SkiDeal Bot.

A beautiful chat interface for demoing the ski trip sales agent.
"""

import sys
import logging
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# Now import the graph
from agent.graph import graph

# Load environment variables
load_dotenv()
logger.info("Environment loaded")

# Page configuration
st.set_page_config(
    page_title="SkiDeal - יועץ חופשות סקי",
    page_icon="⛷️",
    layout="centered",
    initial_sidebar_state="collapsed",  # No sidebar used
)

# Custom CSS for styling with full Hebrew RTL support
st.markdown("""
<style>
    /* Import fonts - Hebrew-friendly */
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Global RTL and Hebrew font */
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Heebo', 'Poppins', sans-serif;
    }
    
    /* Main background - snowy gradient */
    .stApp {
        background: linear-gradient(135deg, #1a2a6c 0%, #2d4a9c 50%, #4a6baf 100%);
    }
    
    /* RTL support for chat messages */
    .stChatMessage {
        direction: rtl;
        text-align: right;
    }
    
    /* Chat message content RTL */
    [data-testid="stChatMessage"] {
        direction: rtl;
    }
    
    [data-testid="stChatMessageContent"] {
        direction: rtl;
        text-align: right;
        font-size: 16px;
        line-height: 1.8;
        font-family: 'Heebo', sans-serif;
    }
    
    /* Chat message content paragraphs */
    [data-testid="stChatMessageContent"] p {
        direction: rtl;
        text-align: right;
    }
    
    /* Make the chat input RTL */
    .stChatInput > div > div > textarea,
    .stChatInput textarea,
    [data-testid="stChatInput"] textarea {
        direction: rtl;
        text-align: right;
        font-family: 'Heebo', sans-serif;
    }
    
    /* Chat input placeholder */
    .stChatInput textarea::placeholder {
        direction: rtl;
        text-align: right;
    }
    
    /* Style the title */
    h1, h2, h3 {
        text-align: center;
        color: #ffffff;
        font-family: 'Heebo', sans-serif;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Chat container styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 12px;
        margin: 8px 0;
        backdrop-filter: blur(10px);
    }
    
    /* Assistant avatar - keep on right for RTL */
    .stChatMessage img {
        border-radius: 50%;
    }
    
    /* Markdown text color and RTL */
    .stMarkdown {
        color: #e0e0e0;
        direction: rtl;
        text-align: right;
    }
    
    .stMarkdown p, .stMarkdown li, .stMarkdown ul, .stMarkdown ol {
        direction: rtl;
        text-align: right;
    }
    
    /* Lists should be RTL */
    ul, ol {
        direction: rtl;
        padding-right: 20px;
        padding-left: 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #00b4d8 0%, #0077b6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-family: 'Heebo', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #00d4f8 0%, #0097d6 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 180, 216, 0.4);
    }
    
    /* Spinner text */
    .stSpinner > div {
        color: #90e0ef !important;
        direction: rtl;
    }
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("⛷️ SkiDeal - יועץ חופשות סקי")
st.markdown("""
<div style='text-align: center; direction: rtl;'>
    <p style='color: #b8d4e8; font-size: 15px; font-family: Heebo, sans-serif;'>
        שלום! אני היועץ הדיגיטלי של SkiDeal. אני כאן כדי לעזור לך למצוא את חופשת הסקי המושלמת.
        <br>
        שאל אותי על מלונות סקי, קייטנות לילדים, ואתרי סקי מובילים באירופה! 🏔️
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": """שלום וברוכים הבאים ל-SkiDeal! ❄️🎿

אני כאן כדי לעזור לך לתכנן את חופשת הסקי המושלמת!

יש לנו מלונות נפלאים באתרי הסקי הטובים ביותר באירופה:
🇦🇩 **אנדורה** - פאס דה לה קאסה, סולדאו, וואל נורד
🇧🇬 **בולגריה** - בנסקו
🇬🇪 **גיאורגיה** - גודאורי
🇮🇹 **איטליה** - פאסו טונלה, סלה רונדה, צרביניה
🇫🇷 **צרפת** - ואל טורנס, לז-ארק, אבוריאז
🇦🇹 **אוסטריה** - אישגיל, זולדן, סאן אנטון

ספר לי, מה אתה מחפש? 
- 👨‍👩‍👧‍👦 חופשה משפחתית עם ילדים?
- 💑 בריחה רומנטית לזוג?
- ⛷️ אקשן לגולשים מנוסים?
- 🎉 חופשה עם חברים?"""
    })

if "thread_id" not in st.session_state:
    # Generate a unique thread ID for this conversation
    import uuid
    st.session_state.thread_id = str(uuid.uuid4())

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="⛷️" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("הקלד את השאלה שלך כאן..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Display assistant response with streaming
    with st.chat_message("assistant", avatar="⛷️"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Prepare input for the agent
            config = {
                "configurable": {
                    "thread_id": st.session_state.thread_id
                }
            }
            
            logger.info(f"🚀 Starting agent with prompt: {prompt[:50]}...")
            logger.debug(f"Config: {config}")
            
            # Stream the response from the agent
            with st.spinner("מחפש את חופשת הסקי המושלמת עבורך... 🏔️"):
                # Prepare all messages for the agent (entire conversation history)
                all_messages = []
                for msg in st.session_state.messages:
                    all_messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Invoke the agent with streaming - use dict format per LangChain docs
                event_count = 0
                for event in graph.stream(
                    {"messages": all_messages},
                    config=config,
                    stream_mode="values"
                ):
                    event_count += 1
                    logger.debug(f"📦 Event {event_count}: {type(event)}")
                    logger.debug(f"   Keys: {event.keys() if isinstance(event, dict) else 'N/A'}")
                    
                    # Get the last message from the agent
                    if "messages" in event and len(event["messages"]) > 0:
                        last_message = event["messages"][-1]
                        logger.debug(f"   Last message type: {type(last_message)}")
                        logger.debug(f"   Has content attr: {hasattr(last_message, 'content')}")
                        
                        # Check if it's an AI message
                        if hasattr(last_message, "content"):
                            content = last_message.content
                            logger.debug(f"   Content type: {type(content)}")
                            logger.debug(f"   Content value: {str(content)[:100]}")
                            
                            if content:
                                full_response = str(content)
                                message_placeholder.markdown(full_response + "▌")
                
                logger.info(f"✅ Streaming completed after {event_count} events")
                
                # Remove cursor
                if full_response:
                    message_placeholder.markdown(full_response)
                else:
                    logger.warning("⚠️ No response generated")
                    full_response = "מצטער, לא קיבלתי תשובה. נסה שוב."
                    message_placeholder.markdown(full_response)
                
        except Exception as e:
            logger.error(f"❌ Error occurred: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            
            error_message = f"מצטער, נתקלתי בבעיה: {str(e)}\n\nבבקשה נסה שוב או שאל שאלה אחרת."
            full_response = error_message
            message_placeholder.markdown(error_message)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #90caf9; font-size: 12px; direction: rtl; font-family: Heebo, sans-serif;'>
    פותח עם ❄️ באמצעות Claude Sonnet 4.5 | © 2025 SkiDeal
</div>
""", unsafe_allow_html=True)
