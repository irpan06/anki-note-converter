# Anki Note Converter

A Python tool to automatically convert personal notes (Markdown format)
into Anki flashcards using AI (Groq API) and AnkiConnect.

---

## 💡 Motivation

Taking notes is common when reading books, doing research, or learning new skills.  
However, reviewing those notes effectively is often challenging.  
Anki, a popular spaced repetition software, is a powerful way to retain knowledge,  
but manually creating flashcards can be time-consuming.

This project solves that problem by **automatically converting Markdown notes into flashcards**  
using **AI (Groq API)** and importing them directly into Anki with **AnkiConnect**.

---

## 🚀 Features

- Convert Markdown notes into **Q&A flashcards**
- AI-powered card generation (Groq API)
- Auto-import into Anki via AnkiConnect
- Supports processing multiple notes in a folder
- Duplicate checking to prevent adding the same card twice

---

## 📂 Project Structure

```
anki-note-converter/
│
├── src/
│   ├── main.py             # main script
│   └── anki_client.py      # for AnkiConnect
│
├── examples/
│   └── deep_work_notes.md  # example note
│
├── requirements.txt        # python dependencies
└── README.md               # project documentation
```

---

## ⚡ How It Works

1. **Prepare notes**  
   Place your Markdown notes in a folder (default: `literature_notes/`).  
   
   You can change the folder path in the script if needed..  
   
   Notes can be free-form; the AI model will parse and structure them into flashcards.

2. **Run the script**  
   ```bash
   python src/main.py
   ```

3. **AI Processing**  
   - The script sends your notes to the Groq API.
   - The AI generates flashcards in structured JSON format.

4. **Import to Anki**  
   - The script calls AnkiConnect.
   - Flashcards are added into the specified deck (default: `Obsidian Notes`).

5. **Review in Anki**  
   - Open Anki, sync if needed, and start reviewing your newly created cards.

---

## 🔧 Requirements

- Python 3.10+
- [Anki](https://apps.ankiweb.net/) with [AnkiConnect](https://foosoft.net/projects/anki-connect/) plugin installed
- Groq API key
- Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

   `requirements.txt` includes:
   ```
   requests==2.32.3
   groq==0.9.0
   ```

---

## 📌 Example

Input (`deep_work_notes.md`):

```markdown
# Deep Work: Rules for Focused Success in a Distracted World

## What is Deep Work?
- Deep Work is the ability to focus without distraction on a cognitively demanding task.
- It allows you to produce high-quality output in less time.

## Why is Deep Work Important?
- In the modern knowledge economy, the ability to learn quickly and produce at an elite level is a critical skill.
- Shallow work (emails, quick meetings, social media) does not create much value.
- Deep work helps to build rare and valuable skills.

## Principles of Deep Work
1. **Work Deeply**  
   Structure your day to minimize distractions. Ritualize your habits and environment to promote focus.

2. **Embrace Boredom**  
   Allow your mind to rest and build tolerance for boredom.

...
```

Output (in Anki):

- **Q:** What is Deep Work?  
  **A:** The ability to focus without distraction on a cognitively demanding task.

- **Q:** Why is Deep Work valuable?  
  **A:** It helps produce high-quality output in less time.

- **Q:** One principle of Deep Work is "Work Deeply." What does it mean?  
  **A:** Structure your day to minimize distractions.

- **Q:** What does "Embrace Boredom" mean in the context of Deep Work?  
  **A:** Allow your mind to rest and build tolerance for boredom.

---

## 🛠 Tech Stack

- **Python** → main programming language
- **Groq API** → AI-powered flashcard generation
- **Requests** → HTTP client to communicate with APIs
- **AnkiConnect** → bridge to import flashcards into Anki

---
## ⚙️ Configuration

- **Notes folder path** → by default the script processes all `.md` files in `literature_notes/`.  
  You can change this path inside `src/main.py` to point to any folder you want.
- **Deck name** → default is `"Obsidian Notes"`.  
  Change the deck name variable in `src/main.py` if you want your cards to go into a different deck.
- **Processed files tracking** → the script automatically creates a file called `processed.json`.  
  This file keeps track of which notes have already been converted and added to Anki.  

  - If you add new notes, only the new files will be processed.  
  - If you want to re-import all notes (e.g., after editing old ones), simply delete `processed.json` and rerun the script.
- **API Key** → this project uses Groq API.  
  Open `src/main.py` and replace the placeholder string with your own API key:
  ```python
  api_key = "your_api_key_here"