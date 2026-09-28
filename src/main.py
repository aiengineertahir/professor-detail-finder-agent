import os
from crewai import Crew
from dotenv import load_dotenv
from src.tasks import get_research_task, get_contact_task

load_dotenv()

def run():
    print("=========================================")
    print("   PROFESSOR DETAIL FINDER (FREE API)    ")
    print("=========================================\n")
    
    # User se Input lena
    professor_name = input("Enter Professor Name (e.g., Dr. Andrew Ng): ")
    university_name = input("Enter University Name (e.g., Stanford University): ")

    # Tasks initialize karna
    r_task = get_research_task(professor_name, university_name)
    c_task = get_contact_task(professor_name, university_name)

    # Crew banana
    professor_crew = Crew(
        agents=[r_task.agent, c_task.agent],
        tasks=[r_task, c_task],
        verbose=True
    )

    print("\n[INFO] AI Agent is searching the web using DuckDuckGo (Free Search)...\n")
    
    inputs = {
        'professor_name': professor_name,
        'university_name': university_name
    }

    # Agent ko run karna
    result = professor_crew.kickoff(inputs=inputs)

    print("\n\n=========================================")
    print("        FINAL PROFESSOR REPORT           ")
    print("=========================================\n")
    print(result)

    # Report ko output folder mein save karna
    os.makedirs("output", exist_ok=True)
    with open("output/professor_report.txt", "w", encoding="utf-8") as f:
        f.write(str(result))
    
    print("\n[SUCCESS] Report successfully saved to 'output/professor_report.txt'")

if __name__ == "__main__":
    run()