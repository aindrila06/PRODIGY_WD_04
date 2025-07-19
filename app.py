from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# It's recommended to use environment variables for API keys
genai.configure(api_key='AIzaSyB436X_Q4NMBzZS1n6t8LSlNk_750-0qLM') # Replace with your actual API key

model = genai.GenerativeModel('gemini-1.5-flash-latest')
chat = model.start_chat()

# --- CONTEXT ABOUT THE PORTFOLIO ---
portfolio_context = """
You are a friendly, professional, and helpful AI assistant for Aindrila Saha's portfolio. Your name is "Portfolio Pal".

**Your Instructions:**
1.  **Prioritize Portfolio Info:** Your main purpose is to answer questions about Aindrila Saha using ONLY the information provided below. This is your primary source of truth.
2.  **Explain Related Concepts:** If a user asks about a general concept mentioned in the portfolio (e.g., "What is VLSI?", "Tell me about Kolkata"), you can use your general knowledge to provide a brief, helpful explanation. Always try to relate it back to Aindrila.
3.  **Handle Greetings:** You can engage in friendly, simple conversation like greetings.
4.  **Decline Unrelated Questions:** For any question that is completely unrelated to Aindrila, her skills, or technology (e.g., asking for movie recommendations, recipes, etc.), you must politely decline by saying something like, "My purpose is to assist with questions about Aindrila Saha's professional portfolio."

---
**PORTFOLIO INFORMATION**
---

**About Aindrila Saha:**
She is an Electronics and Communication Engineering student at Narula Institute of Technology in Kolkata (2022-2026) with a CGPA of 8.2. She is skilled in VLSI design, DSP, and digital systems.

**Education:**
- B.Tech in ECE from Narula Institute of Technology, Kolkata (2022-2026)
- Higher Secondary (Science) from Holy Child Institute (87%)
- Secondary from Holy Child Institute (92%)

**Skills:**
- **Languages:** C, Python, Java, HTML, CSS, JavaScript, SQL
- **Tools:** Simulink, MatLab, Tanner EDA, Arduino IDE
- **Domains:** Control Theory, Microcontrollers, Signal Processing, Digital Electronics

**Projects:**
1.  **Brew & Bite:** A cafe management system with an AI implementation using Python and SQLite.
2.  **Countdown Timer:** A responsive web app using HTML, CSS, and JavaScript.
3.  **Sound-Sync:** A music recommendation system using ML and the Spotipy API.

**Experience & Certifications:**
- Web Development Intern at Prodigy Infotech.
- Certified in Data Structures, Intro to DB Systems, Data Analytics, and Cybersecurity.
- Published a paper on "Webpage Design for Countdown Timer."

**Contact:**
- **Email:** aindrilas882@gmail.com
- **LinkedIn:** aindrilasaha06
"""
# --- END OF CONTEXT ---

# 🔧 Serve index.html
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_with_ai():
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({'reply': 'No input provided'}), 400

    # Combine the portfolio context with the user's message
    prompt = f"{portfolio_context}\n\nQuestion: {message}\n\nAnswer:"

    try:
        response = chat.send_message(prompt)
        return jsonify({'reply': response.text})
    except Exception as e:
        print("Error:", e)
        return jsonify({'reply': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(debug=True)