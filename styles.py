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
            
            /* Reduziere Abstände zwischen den Hauptelementen */
            .main .block-container {
                padding-top: 0.5rem !important;
                gap: 0.5rem !important;
            }
            
            /* Reduziere den Abstand nach dem Titel */
            .main .block-container > div:first-child {
                margin-bottom: 0.5rem !important;
            }
            
            /* Reduziere den Abstand der Überschriften */
            .main .block-container h1,
            .main .block-container h2,
            .main .block-container h3 {
                margin-top: 0.5rem !important;
                margin-bottom: 0.5rem !important;
                padding-top: 0 !important;
                padding-bottom: 0 !important;
            }
            
            /* Reduziere den Abstand des Trennstrichs */
            .main .block-container hr {
                margin-top: 0.5rem !important;
                margin-bottom: 0.5rem !important;
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
            
            /* Standard Button Style */
            .stButton button {
                background: white !important;
                color: black !important;
                border: 1px solid black !important;
                border-radius: 5px;
                padding: 0.5rem 1rem;
                font-weight: 600;
            }
            
            /* Button hover styles */
            div.stButton > button:hover {
                color: var(--text-color) !important;
                background-color: var(--primary-color) !important;
            }
            
            /* Button-Hover-Styles */
            button[data-testid="baseButton-secondary"]:hover,
            button[data-testid="baseButton-primary"]:hover {
                background-color: var(--primary-color) !important;
                color: white !important;
            }
            
            /* Tooltip-Button-Hover */
            div[class*="stTooltipIcon"] button[data-testid="baseButton-secondary"]:hover,
            div[class*="stTooltipIcon"] button[data-testid="baseButton-primary"]:hover {
                background-color: var(--primary-color) !important;
                color: white !important;
            }
            
            /* Streamlit Button Hover Fix */
            button[kind="secondary"]:hover {
                color: white !important;
            }
            
            /* Alternative Selektoren */
            .st-emotion-cache-upseer button:hover,
            .st-emotion-cache-6dnr6u button:hover {
                color: white !important;
                background-color: rgb(49, 51, 63) !important;
            }
            
            /* Sidebar spezifische Styles */
            [data-testid="stSidebar"] .stButton button {
                padding: 0.3rem !important;
            }
            
            /* Chat Title Button in Sidebar */
            [data-testid="stSidebar"] button[data-testid="baseButton-secondary"][class*="st-key-conv_"] {
                text-align: left !important;
                background: #f8f9fa !important;
                padding: 0.5rem 1rem !important;
            }
            
            /* Action Buttons in Sidebar (Edit & Delete) */
            [data-testid="stSidebar"] button[data-testid="baseButton-secondary"][class*="st-key-edit_"],
            [data-testid="stSidebar"] button[data-testid="baseButton-secondary"][class*="st-key-del_"] {
                padding: 0.2rem 0.5rem !important;
                min-width: 32px !important;
                height: 32px !important;
                line-height: 1 !important;
            }
            
            /* Header Icon Buttons */
            button[data-testid="baseButton-secondary"].st-key-new_chat_btn,
            button[data-testid="baseButton-secondary"].st-key-logout_btn {
                min-width: 34px !important;
                width: 34px !important;
                height: 34px !important;
                padding: 0 !important;
                font-size: 1.2rem !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }

            /* Header Columns */
            [data-testid="column"]:first-child > div,
            [data-testid="column"]:last-child > div {
                padding: 0 !important;
                display: flex !important;
                justify-content: center !important;
            }
            
            /* Neuer Chat Button */
            button[data-testid="baseButton-secondary"].st-key-new_chat_btn {
                background: #e6f3ff !important;
                border-color: #0066cc !important;
            }

            button[data-testid="baseButton-secondary"].st-key-new_chat_btn:hover {
                background: #cce5ff !important;
                border-color: #0066cc !important;
                color: white !important;
            }
            
            /* Logout Button */
            button[data-testid="baseButton-secondary"].st-key-logout_btn {
                background: #ffeeee !important;
                border-color: #cc0000 !important;
            }

            button[data-testid="baseButton-secondary"].st-key-logout_btn:hover {
                background: #ffdddd !important;
                border-color: #ff0000 !important;
                color: white !important;
            }
            
            /* Entferne doppelte Borders bei Dropdowns */
            .st-bj, .st-bk, .st-bm {
                border: none !important;
            }
            
            /* Chat Input Button */
            button[kind="primary"][data-testid="baseButton-primary"].st-key-send_button {
                background: #28a745 !important;
                color: white !important;
                border-color: #1e7e34 !important;
            }
            
            /* Template Selector */
            .stSelectbox div[data-baseweb="select"] {
                background: white;
                border-radius: 5px;
                border: 1px solid black !important;
            }
            
            /* Chat Container Styles */
            .chat-message {
                padding: 1.5rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                position: relative;
            }
            
            .user-message {
                background: #f8f9fa;
                border-left: 5px solid #0066cc;
            }
            
            .bot-message {
                background: #ffffff;
                border-left: 5px solid #28a745;
                border: 1px solid #e9ecef;
            }

            /* Chat Input Styles */
            textarea[aria-label="Ihre Nachricht..."] {
                min-height: 300px !important;
                caret-color: black !important;
            }

            /* Chat Input Styling */
            .stTextArea textarea {
                padding: 10px 15px !important;
                font-size: 16px !important;
                resize: none !important;
                background-color: white !important;
                border: 1px solid #e0e0e0 !important;
            }
            
            /* Send Button Styling */
            button[data-testid="baseButton-primary"] {
                border-radius: 50% !important;
                padding: 0.5rem !important;
                min-height: 40px !important;
                width: 40px !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            }
            
            button[data-testid="baseButton-primary"]:hover {
                transform: scale(1.05) !important;
                box-shadow: 0 3px 6px rgba(0,0,0,0.15) !important;
                color: white !important;
            }
            
            /* Fix black corners */
            .stTextArea div[data-baseweb="textarea"] {
                background-color: transparent !important;
                overflow: hidden !important;
            }
            
            /* Fix sidebar spacing */
            .stVerticalBlock {
                gap: 0.5rem !important;
            }
            
            /* Remove padding from columns */
            div[data-testid="column"] {
                padding: 0 !important;
            }
            
            /* Ensure full width for text area */
            .stTextArea {
                width: 100% !important;
            }
            
            /* Hover-Effekte für spezifische Buttons */
            button[kind="secondary"][data-testid="baseButton-secondary"].st-key-new_chat_btn:hover {
                background: #cce5ff !important;
                color: white !important;
            }
            
            button[data-testid="baseButton-secondary"][class*="st-key-conv_"]:hover {
                background: #e2e6ea !important;
                color: white !important;
            }
            
            button[data-testid="baseButton-secondary"][class*="st-key-del_"]:hover {
                background: #ffdddd !important;
                color: white !important;
            }
            
            button[kind="primary"][data-testid="baseButton-primary"].st-key-send_button:hover {
                background: #218838 !important;
                color: white !important;
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
            
            /* Reduziere den Abstand des Trennstrichs */
            .main .block-container hr {
                margin-top: 0.5rem !important;
                margin-bottom: 0.5rem !important;
            }
            
            /* Nur Tooltips ausblenden, Dropdowns beibehalten */
            .stTooltipIcon {
                display: none !important;
            }
            
            .stMarkdownContainer [data-testid="stTooltipHoverTarget"],
            .element-container [data-testid="stTooltipHoverTarget"] {
                visibility: hidden !important;
            }
            
            div[data-baseweb="tooltip"] {
                display: none !important;
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