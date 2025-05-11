
⸻

🔍 Clippy – Your Cross-Platform Smart Search Butler

Clippy is your personal AI-powered assistant, beautifully blending a lightning-fast search interface with intelligent agent capabilities. Inspired by the minimalism of macOS Spotlight and enhanced by the power of the Agno Agent Framework, ClippyAI helps you:
	•	✨ Search files instantly
	•	📁 Summarize files by dragging and dropping them
	•	💬 Get concise answers, quick code snippets, or word definitions
	•	🤖 Use agent-powered lightweight utilities with precision
	•	🎯 All wrapped in a stunning native UI using only Python!

⸻

🧠 Features

Feature	Description
🔎 Smart Search	Type anything to trigger intelligent file search with instant result sorting.
🧠 Agent Assistant	Get AI-powered summaries, quick definitions, or code in seconds.
📂 File Drop	Drag and drop a file to get instant AI summarization and indexing.
🖥️ Native UI	Fully native desktop UI using Flet — beautiful, frameless, and minimal.
🔁 Debounced Input	Performance-optimized search using a custom debouncer utility.
🪄 Precise Results	Responses are short, focused, and designed for quick utility.
🔌 Cross Platform	Runs seamlessly on Windows, macOS, and soon Linux.
🎨 Animations Coming Soon	Eye-candy animations and transitions planned with Flet’s animation support.



⸻

🚀 Getting Started

1. Clone this Repo

git clone https://github.com/smil-thakur/Clippy.git
cd Clippy

2. Install Requirements

We recommend using a virtual environment:

python -m venv clippyENV
source clippyENV/bin/activate  # or clippyENV\Scripts\activate on Windows
pip install -r requirements.txt

3. Setup .env

Create a .env file and add your Gemini API Key:

GEMINI_API_KEY=your_api_key_here

4. Run the App

python src/main.py



⸻

📁 Project Structure

<ul>
  <li><strong>clippyai/</strong>
    <ul>
      <li><strong>agentTool/</strong> – Agno agent integration (WIP)</li>
      <li><strong>components/</strong> – UI components like result section</li>
      <li><strong>utilities/</strong> – Debouncer, File & Search utils</li>
      <li><strong>src/</strong>
        <ul>
          <li><strong>main.py</strong> – Main entry point of the app</li>
        </ul>
      </li>
      <li><strong>.env</strong> – Environment file for keys</li>
      <li><strong>requirements.txt</strong> – Python dependencies</li>
      <li><strong>README.md</strong> – You are here!</li>
    </ul>
  </li>
</ul>


⸻

🧩 Tech Stack
	•	🐍 Python
	•	💻 Flet – Native cross-platform UI framework
	•	🧠 Agno Agent https://www.agno.com/
	•	🪄 Gemini API (via Agno Models)
	•	⚙️ Asyncio, Debouncing, File system search, and more

⸻

🎯 Vision

We’re building the next-gen AI-powered Spotlight for your desktop – a hybrid between a blazing-fast search tool and a context-aware assistant. This is just the beginning. In the future, ClippyAI will include:
	•	🔄 Intelligent multi-agent workflows
	•	🔊 TTS summarization of documents
	•	🧠 Local memory for smarter interactions
	•	📦 Plugin architecture

⸻

🤝 Contributing

Got an idea? PRs welcome!
Open an issue or drop your suggestions.

⸻

🏆 Hackathon Participation
https://github.com/global-agent-hackathon/global-agent-hackathon-may-2025

This project is being developed as part of the Global Agent Hackathon – May 2025. Let’s build the future of intelligent agents, one utility at a time.

⸻

📸 Sneak Peek



https://github.com/user-attachments/assets/b2fc8fe4-195c-4656-bd5d-356ba2d9e1b6


⸻

📬 Contact

Feel free to reach out or connect on GitHub if you’d like to collaborate or contribute!

⸻
