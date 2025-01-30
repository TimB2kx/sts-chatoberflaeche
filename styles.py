import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');
            
            /* Allgemeiner Block Container */
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 4rem !important;
            }

            /* Streamlit spezifische Container */
            div[class*="stMainBlockContainer"],
            div[data-testid="stDecoration"],
            div[data-testid="stToolbar"],
            .main .block-container,
            .st-emotion-cache-yw8pof {
                padding-top: 1rem !important;
                padding-bottom: 4rem !important;
            }
            
            .stApp {
                background: white;
                font-family: 'Open Sans', sans-serif;
                color: black !important;
            }
            
            /* Ensure all text elements are black */
            .stMarkdown, p, h1, h2, h3, h4, h5, h6, span, div {
                color: black !important;
            }
            
            #MainMenu, .stDeployButton, header, footer {
                visibility: hidden !important;
                display: none !important;
            }
            
            /* Ausblenden des leeren Containers */
            .element-container[data-testid="stElementContainer"] .stMarkdown hr {
                display: none !important;
            }
            
            .chat-history {
                height: calc(100vh - 45vh);
                overflow-y: auto;
                margin-bottom: 2rem;
                padding-right: 1rem;
            }
            
            .footer-container {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: white;
                padding: 1rem;
                border-top: 1px solid #ddd;
                z-index: 100;
                max-height: 40vh;
                overflow-y: auto;
            }
            
            .stButton button {
                background: white !important;
                color: black !important;
                border: 1px solid black !important;
                border-radius: 5px;
                padding: 0.5rem 1rem;
                font-weight: 600;
            }
            
            /* Header Buttons */
            button[kind="secondary"][data-testid="baseButton-secondary"].st-key-new_chat_btn {
                background: #e6f3ff !important;
                border-color: #0066cc !important;
            }
            
            button[kind="primary"][data-testid="baseButton-primary"].st-key-logout_btn {
                background: #ff4444 !important;
                color: white !important;
                border-color: #cc0000 !important;
            }
            
            /* Sidebar Buttons */
            button[data-testid="baseButton-secondary"][class*="st-key-conv_"] {
                text-align: left !important;
                background: #f8f9fa !important;
            }
            
            button[data-testid="baseButton-secondary"][class*="st-key-del_"] {
                padding: 0.25rem !important;
                min-width: 40px !important;
                background: #ffeeee !important;
            }
            
            /* Chat Input Button */
            button[kind="primary"][data-testid="baseButton-primary"].st-key-send_button {
                background: #28a745 !important;
                color: white !important;
                border-color: #1e7e34 !important;
            }
            
            .stButton button:hover {
                background: #f0f0f0 !important;
            }
            
            /* Hover-Effekte für spezifische Buttons */
            button[kind="secondary"][data-testid="baseButton-secondary"].st-key-new_chat_btn:hover {
                background: #cce5ff !important;
            }
            
            button[kind="primary"][data-testid="baseButton-primary"].st-key-logout_btn:hover {
                background: #cc0000 !important;
            }
            
            button[data-testid="baseButton-secondary"][class*="st-key-conv_"]:hover {
                background: #e2e6ea !important;
            }
            
            button[data-testid="baseButton-secondary"][class*="st-key-del_"]:hover {
                background: #ffdddd !important;
            }
            
            button[kind="primary"][data-testid="baseButton-primary"].st-key-send_button:hover {
                background: #218838 !important;
            }
            
            .stChatMessage {
                background: white !important;
                border: 1px solid #ddd;
                border-radius: 10px;
                margin-bottom: 1rem;
                padding: 0.5rem;
                color: black !important;
            }
            
            .stChatMessage p {
                color: black !important;
            }
            
            .stTextArea textarea {
                color: black !important;
                background: white !important;
                border: 1px solid #ddd !important;
            }
            
            /* Selectbox Styling */
            [data-testid="stSelectbox"],
            [data-testid="stSelectbox"] > div,
            [data-testid="stSelectbox"] > div > div,
            [data-testid="stSelectbox"] div[role="button"],
            [data-testid="stSelectbox"] div[role="listbox"],
            [data-testid="stSelectbox"] div[role="option"],
            div[role="listbox"],
            div[role="option"],
            .stSelectbox,
            .stSelectbox > div,
            .stSelectbox div[role="button"],
            .stSelectbox div[role="listbox"],
            .stSelectbox div[role="option"] {
                background-color: white !important;
                color: black !important;
            }
            
            /* Ensure dropdown options have white background */
            div[role="listbox"],
            div[role="listbox"] *,
            .streamlit-selectbox div[role="listbox"],
            .streamlit-selectbox div[role="option"] {
                background-color: white !important;
            }
            
            div[role="option"]:hover,
            .stSelectbox div[role="option"]:hover {
                background-color: #f0f0f0 !important;
            }

            /* Zusätzliche Spezifität für Dropdown-Menüs */
            .streamlit-selectbox,
            [data-baseweb="select"] *,
            [data-baseweb="popover"] * {
                background-color: white !important;
            }
            
            /* Spezifisch für das Webhook Dropdown */
            div[data-testid="stSelectbox"].st-key-webhook_dropdown,
            div[data-testid="stSelectbox"].st-key-webhook_dropdown > div,
            div[data-testid="stSelectbox"].st-key-webhook_dropdown > div > div,
            div[data-testid="stSelectbox"].st-key-webhook_dropdown div[role="button"],
            div[data-testid="stSelectbox"].st-key-webhook_dropdown div[role="listbox"],
            div[data-testid="stSelectbox"].st-key-webhook_dropdown div[role="option"] {
                background-color: white !important;
            }
            
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #f1f1f1;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #888;
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #555;
            }
            
            div[data-testid="stExpander"] {
                border: 1px solid black !important;
                border-radius: 5px !important;
                margin: 10px 0 !important;
                background-color: white !important;
            }

            div[data-testid="stExpander"] > div:first-child {
                background-color: white !important;
            }
            
            .streamlit-expanderContent {
                background-color: white !important;
                padding: 10px !important;
            }
        </style>
        
        <script>
            function scrollToBottom() {
                const messages = window.parent.document.querySelector('.chat-history');
                if (messages) {
                    messages.scrollTop = messages.scrollHeight;
                }
            }
            
            const observer = new MutationObserver(scrollToBottom);
            
            window.addEventListener('load', function() {
                const messages = window.parent.document.querySelector('.chat-history');
                if (messages) {
                    observer.observe(messages, {
                        childList: true,
                        subtree: true
                    });
                    scrollToBottom();
                }
            });
        </script>
    """, unsafe_allow_html=True)