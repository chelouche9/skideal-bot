"""Streamlit Chat Interface for Shlomo Sixt Car Sales Bot.

A beautiful Hebrew chat interface for demoing the car sales agent to clients.
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
    page_title="שלמה סיקסט - יועץ רכב AI",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for Hebrew RTL support and styling
st.markdown("""
<style>
    /* RTL support for Hebrew */
    .stChatMessage {
        direction: rtl;
        text-align: right;
    }
    
    /* Make the chat input RTL */
    .stChatInput > div > div > textarea {
        direction: rtl;
        text-align: right;
    }
    
    /* Style the title */
    h1 {
        text-align: center;
        color: #1f4788;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Style chat messages */
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    
    /* User message styling */
    [data-testid="stChatMessageContent"] {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Assistant avatar */
    .stChatMessage img {
        border-radius: 50%;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🚗 שלמה סיקסט - יועץ רכב AI")
st.markdown("""
<div style='text-align: center; direction: rtl;'>
    <p style='color: #666; font-size: 14px;'>
        שלום! אני היועץ הדיגיטלי של שלמה סיקסט. אני כאן כדי לעזור לך למצוא את הרכב המושלם עבורך.
        <br>
        שאל אותי על רכבים זמינים, מחירים, ומפרטים טכניים! 🚘
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
        "content": "שלום! אני סוכן המכירות הדיגיטלי של שלמה סיקסט. 😊\n\nאני כאן כדי לעזור לך למצוא את הרכב המתאים ביותר לצרכים שלך!\n\nספר לי, מה אתה מחפש? משפחתי? צעיר וחסכוני? יוקרה?"
    })

if "thread_id" not in st.session_state:
    # Generate a unique thread ID for this conversation
    import uuid
    st.session_state.thread_id = str(uuid.uuid4())

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🚗" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("הקלד את השאלה שלך כאן..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Display assistant response with streaming
    with st.chat_message("assistant", avatar="🚗"):
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
            with st.spinner("מחפש את המידע הטוב ביותר עבורך..."):
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

# Sidebar with info
with st.sidebar:
    st.markdown("## 📊 מידע על השיחה")
    st.markdown(f"**מספר הודעות:** {len(st.session_state.messages)}")
    st.markdown(f"**Thread ID:** `{st.session_state.thread_id[:8]}...`")
    
    st.markdown("---")
    
    st.markdown("## 🔧 הגדרות")
    if st.button("🗑️ נקה שיחה", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(__import__("uuid").uuid4())
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("## ℹ️ אודות")
    st.markdown("""
    **שלמה סיקסט AI Bot**
    
    יועץ רכב אינטליגנטי המופעל על ידי:
    - 🤖 Claude Sonnet 4.5
    - 🔗 LangChain v1
    - 🔄 LangGraph
    
    **יכולות:**
    - חיפוש רכבים זמינים
    - פרטים טכניים ומחירים
    - המלצות מותאמות אישית
    - תמיכה בעברית בלבד
    """)
    
    st.markdown("---")
    st.markdown("🏢 **שלמה סיקסט** - אחד מספקי הרכב המובילים בישראל")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px; direction: rtl;'>
    פותח עם ❤️ באמצעות Claude Sonnet 4.5 | © 2025 שלמה סיקסט
</div>
""", unsafe_allow_html=True)

