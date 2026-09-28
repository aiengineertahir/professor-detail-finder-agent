import os
import sys
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, LLM
from src.tools import search_tool

# --- FIX for CrewAI + Groq/LiteLLM compatibility ---
try:
    import crewai.llms.cache as _crewai_cache
    _crewai_cache.mark_cache_breakpoint = lambda msg: msg
except Exception:
    pass

try:
    import litellm
    litellm.drop_params = True
    litellm.set_verbose = False
except Exception:
    pass
# -----------------------------------------------------------

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Professor Finder AI - Local Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Gradient Header */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
    }
    
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60A5FA, #A78BFA, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    /* Result Box */
    .report-box {
        background: #0B1120;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'Outfit', sans-serif;
        color: #E2E8F0;
        line-height: 1.7;
    }

    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-right: 0.5rem;
    }

    .badge-gemini {
        background: rgba(59, 130, 246, 0.2);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.4);
    }

    .badge-groq {
        background: rgba(249, 115, 22, 0.2);
        color: #FB923C;
        border: 1px solid rgba(249, 115, 22, 0.4);
    }

    .badge-ddg {
        background: rgba(34, 197, 94, 0.2);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Settings & Model Provider Switcher
with st.sidebar:
    st.markdown("### ⚙️ AI Engine Settings")
    
    # Provider Selection
    provider = st.radio(
        "Select AI Provider:",
        options=["Google Gemini", "Groq", "OpenAI"],
        index=0,
        help="Google Gemini ya Groq select karein."
    )
    
    if provider == "Google Gemini":
        st.markdown("#### 🌟 Google Gemini Models")
        gemini_models = [
            "gemini/gemini-2.0-flash",
            "gemini/gemini-1.5-flash",
            "gemini/gemini-1.5-pro",
            "gemini/gemini-2.5-flash",
            "Custom Model..."
        ]
        
        selected_model_option = st.selectbox(
            "Select Gemini Model",
            options=gemini_models,
            index=0,
            help="Gemini 2.0 Flash is super fast, accurate, and free on Google AI Studio."
        )
        
        if selected_model_option == "Custom Model...":
            chosen_model = st.text_input("Enter Model Name:", value="gemini/gemini-2.0-flash")
        else:
            chosen_model = selected_model_option
            
        saved_key = os.getenv("GEMINI_API_KEY", "")
        api_key_input = st.text_input(
            "Gemini API Key",
            value=saved_key,
            type="password",
            help="Google AI Studio (aistudio.google.com) se free Gemini API key milti hai."
        )
        # Set to env for LiteLLM
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input

    elif provider == "Groq":
        st.markdown("#### ⚡ Groq Models (Active)")
        groq_models = [
            "groq/openai/gpt-oss-120b",
            "groq/openai/gpt-oss-20b",
            "groq/llama-3.3-70b-versatile",
            "groq/llama-3.1-8b-instant",
            "groq/deepseek-r1-distill-llama-70b",
            "groq/mixtral-8x7b-32768",
            "groq/qwen-2.5-32b",
            "Custom Model..."
        ]
        
        selected_model_option = st.selectbox(
            "Select Groq Model",
            options=groq_models,
            index=0,
            help="Groq ka active model select karein (decommissioned models remove kar diye gaye hain)."
        )
        
        if selected_model_option == "Custom Model...":
            chosen_model = st.text_input("Enter Model Name:", value="groq/llama-3.3-70b-versatile")
        else:
            chosen_model = selected_model_option
            
        saved_key = os.getenv("GROQ_API_KEY", "")
        api_key_input = st.text_input(
            "Groq API Key",
            value=saved_key,
            type="password",
            help="Groq API key console.groq.com se free milti hai."
        )
        # Set to env for LiteLLM
        if api_key_input:
            os.environ["GROQ_API_KEY"] = api_key_input

    else:  # OpenAI
        st.markdown("#### 🤖 OpenAI Models")
        openai_models = ["openai/gpt-4o-mini", "openai/gpt-4o", "Custom Model..."]
        selected_model_option = st.selectbox("Select OpenAI Model", options=openai_models, index=0)
        if selected_model_option == "Custom Model...":
            chosen_model = st.text_input("Enter Model Name:", value="openai/gpt-4o-mini")
        else:
            chosen_model = selected_model_option
            
        saved_key = os.getenv("OPENAI_API_KEY", "")
        api_key_input = st.text_input("OpenAI API Key", value=saved_key, type="password")
        if api_key_input:
            os.environ["OPENAI_API_KEY"] = api_key_input

    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; font-size: 0.85rem; margin-top: 10px;">
            <b>Selected Engine:</b> <code>{chosen_model}</code>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # App Info & Badges
    st.markdown("""
        <div>
            <span class="badge badge-gemini">Gemini</span>
            <span class="badge badge-groq">Groq</span>
            <span class="badge badge-ddg">Free Search</span>
        </div>
        <p style="margin-top: 1rem; font-size: 0.85rem; color: #94A3B8;">
            Yeh AI agent DuckDuckGo ke zariye internet aur university portals search karta hai aur professor ke research interests, contact info aur web profiles extract karta hai.
        </p>
    """, unsafe_allow_html=True)

# Main Hero Header
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🎓 Professor Detail Finder AI</h1>
        <p class="hero-subtitle">Automated Multi-Agent Academic & Contact Discovery Platform</p>
    </div>
""", unsafe_allow_html=True)

# Main Layout: 2 Columns
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 🔍 Search Parameters")
    
    with st.form("search_form"):
        professor_name = st.text_input(
            "Professor Name *",
            placeholder="e.g., Dr. Andrew Ng, Prof. Geoffrey Hinton",
            help="Jis professor ki details chahiye unka naam likhein."
        )
        
        university_name = st.text_input(
            "University / Institution *",
            placeholder="e.g., Stanford University, University of Toronto",
            help="University ya Organization ka naam likhein."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Start Finding Details", use_container_width=True)

    # Saved Reports / Output Explorer
    st.markdown("---")
    st.markdown("### 📁 Saved Reports History")
    output_dir = "output"
    if os.path.exists(output_dir):
        files = [f for f in os.listdir(output_dir) if f.endswith(('.txt', '.md'))]
        if files:
            selected_file = st.selectbox("View previous reports:", files)
            if selected_file:
                file_path = os.path.join(output_dir, selected_file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.download_button(
                    label=f"📥 Download {selected_file}",
                    data=content,
                    file_name=selected_file,
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.info("No saved reports yet.")

with col2:
    st.markdown("### 📊 Agent Results & Report")
    
    if submitted:
        if not professor_name or not university_name:
            st.error("⚠️ Please provide both Professor Name and University Name.")
        elif not api_key_input:
            st.error(f"⚠️ {provider} API Key required! Please enter your API Key in the sidebar or set it in your .env file.")
        else:
            status_box = st.status(f"🤖 AI Agents at work (using {chosen_model})...", expanded=True)
            
            with status_box:
                st.write(f"⚙️ Initializing LLM (`{chosen_model}`)...")
                
                try:
                    # Sync API key to os.environ for native SDK & LiteLLM
                    if provider == "Google Gemini":
                        os.environ["GEMINI_API_KEY"] = api_key_input
                    elif provider == "Groq":
                        os.environ["GROQ_API_KEY"] = api_key_input
                    elif provider == "OpenAI":
                        os.environ["OPENAI_API_KEY"] = api_key_input

                    # Initialize dynamic LLM
                    active_llm = LLM(
                        model=chosen_model,
                        api_key=api_key_input
                    )
                    
                    st.write("🔍 Creating Academic Researcher Agent...")
                    researcher = Agent(
                        role='Academic Researcher',
                        goal='Find detailed background, official department, research interests, and web profiles for {professor_name} at {university_name}.',
                        backstory='An expert academic internet researcher skilled at navigating university websites and search engines to gather professional profiles.',
                        tools=[search_tool],
                        llm=active_llm,
                        verbose=True,
                        memory=False,
                        max_iter=3
                    )

                    st.write("📞 Creating Contact Detail Extractor Agent...")
                    extractor = Agent(
                        role='Contact Detail Extractor',
                        goal='Extract official university email addresses, office phone numbers, and professional contact methods for {professor_name}.',
                        backstory='A meticulous data extractor specialized in finding verified official emails and university contact pages.',
                        tools=[search_tool],
                        llm=active_llm,
                        verbose=True,
                        memory=False,
                        max_iter=3
                    )

                    st.write("📋 Assigning tasks...")
                    r_task = Task(
                        description=f'Search across the web and university portal for Professor {professor_name} at {university_name}. '
                                    f'Find their full name, official department, designation, research topics, and web profiles.',
                        expected_output='A comprehensive summary report detailing the professor name, department, designation, research interests, and web profiles.',
                        agent=researcher
                    )

                    c_task = Task(
                        description=f'Find the official university email address, office phone number, or professional contact details for Professor {professor_name} at {university_name}.',
                        expected_output='A clean list containing official email, office phone number, and any public contact information available.',
                        agent=extractor
                    )

                    st.write("🌐 Agents are searching DuckDuckGo and analyzing university data...")
                    
                    crew = Crew(
                        agents=[researcher, extractor],
                        tasks=[r_task, c_task],
                        verbose=True
                    )

                    inputs = {
                        'professor_name': professor_name,
                        'university_name': university_name
                    }

                    result = crew.kickoff(inputs=inputs)
                    result_text = str(result)

                    # Save to output folder
                    os.makedirs("output", exist_ok=True)
                    safe_name = professor_name.replace(" ", "_").replace(".", "").lower()
                    report_filename = f"output/{safe_name}_report.txt"
                    
                    with open(report_filename, "w", encoding="utf-8") as f:
                        f.write(result_text)
                    
                    # Also write default professor_report.txt
                    with open("output/professor_report.txt", "w", encoding="utf-8") as f:
                        f.write(result_text)

                    status_box.update(label="✅ Search & Analysis Completed Successfully!", state="complete", expanded=False)
                    st.success("🎉 Professor details successfully gathered and saved!")

                    # Render Result Tabs
                    tab_report, tab_raw = st.tabs(["📄 Formatted Report", "📝 Raw Text"])
                    
                    with tab_report:
                        st.markdown(f"""
                        <div class="report-box">
                            {result_text}
                        </div>
                        """, unsafe_allow_html=True)

                    with tab_raw:
                        st.text_area("Raw Output:", value=result_text, height=350)

                    # Download Options
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.download_button(
                            label="📥 Download Report (.txt)",
                            data=result_text,
                            file_name=f"{safe_name}_report.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col_d2:
                        st.download_button(
                            label="📥 Download Markdown (.md)",
                            data=result_text,
                            file_name=f"{safe_name}_report.md",
                            mime="text/markdown",
                            use_container_width=True
                        )

                except Exception as e:
                    status_box.update(label="❌ An error occurred during search", state="error", expanded=True)
                    st.error(f"Error details: {str(e)}")
                    st.info(f"Tip: Check if your {provider} API key is valid and you have an active internet connection.")
    else:
        st.info("👈 Left side par Professor aur University ka naam likhein aur **Start Finding Details** dabayein.")
