from crewai import Task
from src.agents import get_researcher_agent, get_contact_extractor_agent

def get_research_task(professor_name, university_name):
    researcher = get_researcher_agent()
    return Task(
        description=f'Search across the web and university portal for Professor {professor_name} at {university_name}. '
                    f'Find their full name, official department, designation, research topics, and social links.',
        expected_output='A comprehensive summary report detailing the professor name, department, designation, research interests, and web profiles.',
        agent=researcher
    )

def get_contact_task(professor_name, university_name):
    extractor = get_contact_extractor_agent()
    return Task(
        description=f'Find the official university email address, office phone number, or professional contact details for Professor {professor_name} at {university_name}.',
        expected_output='A clean list containing official email, office phone number, and any public contact information available.',
        agent=extractor
    )