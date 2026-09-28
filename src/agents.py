from crewai import Agent, LLM
from src.tools import search_tool
import os

# --- FIX for CrewAI + Groq cache_breakpoint bug & LiteLLM compatibility ---
import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

try:
    import litellm
    litellm.drop_params = True
    litellm.set_verbose = False
except Exception:
    pass
# ----------------------------------------------------------------------------

# Groq LLM setup
groq_llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

def get_researcher_agent():
    return Agent(
        role='Academic Researcher',
        goal='Find detailed background, official department, research interests, and social/web profiles for {professor_name} at {university_name}.',
        backstory='An expert academic internet researcher skilled at navigating university websites and search engines to gather professional profiles.',
        tools=[search_tool],
        llm=groq_llm,
        verbose=True,
        memory=False,
        max_iter=3
    )

def get_contact_extractor_agent():
    return Agent(
        role='Contact Detail Extractor',
        goal='Extract official university email addresses, office phone numbers, and professional contact methods for {professor_name}.',
        backstory='A meticulous data extractor specialized in finding verified official emails and university contact pages.',
        tools=[search_tool],
        llm=groq_llm,
        verbose=True,
        memory=False,
        max_iter=3
    )
    