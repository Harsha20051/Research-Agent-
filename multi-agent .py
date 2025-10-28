import os
import json
import re
import google.generativeai as genai
from datetime import datetime

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# -----------------------
# JD Parser Agent
# -----------------------
def jd_parser_agent(jd_text):
    prompt = f"""
Analyze the following Job Description and return a JSON object with these fields:
- skills
- tools
- topics
- responsibilities

Return only valid JSON. Example:
{{"skills":["Python","SQL"],"tools":["Excel"],"topics":["Data Analysis"],"responsibilities":["Build reports"]}}

Job Description:
{jd_text}
    """

    model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Clean text
    text = re.sub(r"```(json)?", "", text)
    text = text.replace("```", "").replace("\\n", " ").replace("\n", " ").replace("\\", "").strip()

    try:
        parsed = json.loads(text)
        for k in ["skills", "tools", "topics", "responsibilities"]:
            if k not in parsed:
                parsed[k] = []
        return parsed
    except Exception:
        return {"skills": [], "tools": [], "topics": [], "responsibilities": []}

# -----------------------
# Interview Process Agent
# -----------------------
def interview_process_agent(company_name, role):
    c = company_name.lower()
    if "google" in c:
        return {"rounds": ["MCQ", "Coding", "System Design", "HR"], "difficulty": "Hard"}
    elif "infosys" in c:
        return {"rounds": ["Aptitude", "Coding", "HR"], "difficulty": "Medium"}
    elif "tcs" in c:
        return {"rounds": ["Aptitude", "Technical", "HR"], "difficulty": "Easy"}
    else:
        return {"rounds": ["Aptitude", "Technical", "HR"], "difficulty": "Medium"}

# -----------------------
# Roadmap Builder Agent
# -----------------------
def roadmap_builder_agent(company, role, jd_data, interview_info):
    topics = jd_data.get("topics", []) + jd_data.get("skills", [])
    tools = jd_data.get("tools", [])
    responsibilities = jd_data.get("responsibilities", [])

    roadmap = {
        "company": company,
        "role": role,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "rounds": interview_info["rounds"],
        "difficulty": interview_info["difficulty"],
        "topics": topics,
        "tools": tools,
        "responsibilities": responsibilities,
        "recommended_order": interview_info["rounds"] + topics + tools,
    }
    return roadmap

# -----------------------
# Pipeline
# -----------------------
def run_pipeline(company, role, jd_text):
    jd_data = jd_parser_agent(jd_text)
    interview_info = interview_process_agent(company, role)
    roadmap = roadmap_builder_agent(company, role, jd_data, interview_info)

    with open("final_roadmap.json", "w", encoding="utf-8") as f:
        json.dump(roadmap, f, indent=2, ensure_ascii=False)
    return roadmap

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    company = "TCS"
    role = "Data Analyst Intern"
    jd_text = "We need candidates with Python, SQL, and data visualization experience. Should perform data analysis and build reports."

    roadmap = run_pipeline(company, role, jd_text)
    print(json.dumps(roadmap, indent=2))
    print("\nSaved output to final_roadmap.json",flush=True)
    

