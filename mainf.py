import os
import json
import re
import google.generativeai as genai

# ✅ Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def parse_jd_with_ai(jd):
    """Use Gemini AI to extract skills, tools, and topics from JD and clean output."""
    prompt = f"""
    Extract only the key skills, tools, and important topics from this Job Description.
    Return the result strictly as a JSON list of strings, like this:
    ["Python", "SQL", "Data Analysis"]

    Job Description:
    {jd}
    """
    model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")    
    response = model.generate_content(prompt)

    text = response.text.strip()
    # Remove ```json and ```
    text = re.sub(r"```(json)?", "", text).replace("```", "").strip()
    # Remove escape characters and newlines
    text = text.replace("\\n", "").replace("\n", "").replace("\\", "").strip()

    # Try to find a list pattern inside text
    match = re.search(r"\[.*\]", text)
    if match:
        text = match.group(0)

    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        else:
            return list(data.values())
    except Exception:
        # Fallback: split by commas if JSON fails
        return [item.strip() for item in text.split(",") if item.strip()]

def get_company_interview_process(company):
    company = company.lower()
    if "tcs" in company:
        rounds = ["Aptitude", "Technical", "HR"]
        difficulty = "Easy"
    elif "infosys" in company:
        rounds = ["Aptitude", "Coding", "HR"]
        difficulty = "Medium"
    elif "google" in company:
        rounds = ["MCQ", "Coding", "System Design", "HR"]
        difficulty = "Hard"
    else:
        rounds = ["Aptitude", "Technical", "HR"]
        difficulty = "Medium"
    return rounds, difficulty

def build_roadmap(company, role, jd):
    jd_data = parse_jd_with_ai(jd)
    rounds, difficulty = get_company_interview_process(company)
    roadmap = {
        "company": company,
        "role": role,
        "rounds": rounds,
        "topics": jd_data,
        "difficulty": difficulty,
        "recommended_order": rounds
    }
    return roadmap

if __name__ == "__main__":
    jd1 = "We need candidates with Python, SQL, and data analysis experience."
    jd2 = "Strong knowledge of Machine Learning, APIs, and Deep Learning preferred."

    roadmap1 = build_roadmap("TCS", "Data Analyst Intern", jd1)
    roadmap2 = build_roadmap("Google", "SDE Intern", jd2)

    results = [roadmap1, roadmap2]
    print(json.dumps(results, indent=2))

    with open("sample_output.json", "w") as f:
        json.dump(results, f, indent=2)
