import os
import json
import time
import requests
from pathlib import Path
from groq import Groq

FOLDER = Path("D:\Obsidian\PKM\Literature Notes")
META_FILE = "processed.json"
DECK_NAME = "Obsidian Notes"
ANKI_CONNECT_URL = "http://localhost:8765"

# === Setup Groq API ===
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# === Helper Metadata ===
def load_meta():
    if os.path.exists(META_FILE):
        with open(META_FILE, "r") as f:
            return json.load(f)
    return {}

def save_meta(meta):
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)

def get_modified_time(file):
    return os.path.getmtime(file)

# === Kirim catatan ke Anki ===
def add_note_to_anki(deck, front, back):
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "options": {
                    "allowDuplicate": True
                },
                "tags": ["obsidian", "auto"]
            }
        }
    }
    r = requests.post(ANKI_CONNECT_URL, json=payload).json()
    return r

# === Panggil Groq untuk ubah catatan jadi flashcard JSON ===
def extract_flashcards(text):
    prompt = f"""
    Dari teks Markdown berikut, buatkan flashcard untuk Anki.
    Jawab hanya dalam format JSON array, setiap item punya field:
    - question
    - answer

    Teks:
    {text}
    """
    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Anda adalah asisten yang membuat flashcard untuk Anki."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    output = chat.choices[0].message.content


    # Ambil JSON array dari output
    start = output.find("[")
    end = output.rfind("]") + 1
    if start == -1 or end == -1:
        raise ValueError("Tidak ditemukan JSON array di output")
    json_text = output[start:end]
    flashcards = json.loads(json_text)

    return flashcards

# === Proses file markdown lewat Groq ===
def process_file(file):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    flashcards = extract_flashcards(content)
    print(f"Selesai menghasilkan {len(flashcards)} kartu.")

    added = 0
    for card in flashcards:
        q, a = card["question"], card["answer"]
        res = add_note_to_anki(DECK_NAME, q, a)
        if "error" not in res or res["error"] is None:
            added += 1
    return added

# === Scan folder ===
def scan_folder():
    meta = load_meta()
    updates = []

    for file in FOLDER.glob("*.md"):
        mtime = get_modified_time(file)
        recorded = meta.get(file.name)
        if not recorded or mtime > recorded:
            updates.append(file)
            meta[file.name] = mtime

    save_meta(meta)
    return updates

if __name__ == "__main__":
    updated_files = scan_folder()
    if not updated_files:
        print("Tidak ada file baru/terupdate.")
    else:
        total_cards = 0
        for file in updated_files:
            print(f"Memproses {file.name}...")
            added = process_file(file)
            total_cards += added
            print(f"  Ditambahkan {added} kartu.")
        print(f"Selesai. Total kartu ditambahkan: {total_cards}")
