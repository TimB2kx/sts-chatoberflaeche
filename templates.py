import streamlit as st
import xml.etree.ElementTree as ET
from typing import List, TypedDict

class PromptTemplate(TypedDict):
    title: str
    description: str
    template: str

def load_prompt_templates() -> List[PromptTemplate]:
    """Lädt die Promptvorlagen aus der XML-Datei"""
    try:
        tree = ET.parse('prompt_templates.xml')
        root = tree.getroot()
        templates = []
        for prompt in root.findall('.//prompt'):
            template = PromptTemplate(
                title=prompt.find('title').text,
                description=prompt.find('description').text,
                template=prompt.find('template').text.strip()  # Strip whitespace from template
            )
            templates.append(template)
        return templates
    except Exception as e:
        st.error(f"Fehler beim Laden der Promptvorlagen: {str(e)}")
        return []

def render_template_selector(templates: List[PromptTemplate]) -> None:
    """Rendert die Vorlagenauswahl und Einfügen-Button"""
    if templates:
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                template_options = ["Vorlage auswählen..."] + [f"{t['title']}" for t in templates]
                selected_index = st.selectbox(
                    "",
                    range(len(template_options)),
                    format_func=lambda x: template_options[x],
                    key="template_selector",
                    label_visibility="collapsed"
                )
            
            with col2:
                insert_disabled = selected_index == 0
                if st.button("Einfügen", key="insert_template", disabled=insert_disabled):
                    # Strip any extra whitespace when inserting the template
                    st.session_state.current_message = templates[selected_index-1]['template'].strip()
                    st.rerun()
            
            if selected_index > 0:
                st.markdown(f"**Beschreibung:** {templates[selected_index-1]['description']}")