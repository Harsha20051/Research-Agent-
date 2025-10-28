# Research-Agent-

👨‍💻 Developed by: Harshal Sonawane

🎓 B.Tech (AIML) | Director – STEM Sage Techword LLP | AI & IoT Innovator

📘 Project Overview

This AI Agent automatically analyzes Job Descriptions (JDs) using Google Gemini API and generates a personalized interview roadmap in JSON format.
It extracts skills, tools, and responsibilities, predicts the interview process, and combines everything into a structured roadmap.

⚙️ How the Agent Works
🧩 Step 1 – JD Parser Agent

Input: Job Description text

Process: Sends the JD to Gemini 2.5 Flash model for semantic analysis

Output: JSON with extracted skills, tools, and responsibilities

🧩 Step 2 – Interview Process Agent

Input: Company name

Process: Maps company to known interview patterns

Output: rounds and difficulty level

🧩 Step 3 – Roadmap Builder Agent

Combines data from both agents

Builds a final AI-generated roadmap for preparation

🧠 Reasoning & Skill Extraction

The agent uses Gemini’s multi-step reasoning to analyze natural language text.
It identifies technical terms, key responsibilities, and tool names using semantic understanding.
The output is structured into JSON format for further processing or visualization.

Features

Multi-Agent Reasoning
Gemini API Integration
JSON-formatted output
Customizable interview process
Ready for further extension with LangChain







It identifies technical terms, key responsibilities, and tool names using semantic understanding.

The output is structured into JSON format for further processing or visualization.
