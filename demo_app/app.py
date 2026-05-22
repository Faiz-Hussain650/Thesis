"""
Proactive Defence Demo — Cloak, Honey & Trap
Flask server that connects to local Ollama models
Run: python app.py  →  open http://localhost:5000
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests, random, re, json, os

app = Flask(__name__)
CORS(app)

RANDOM_SEED = 42
OLLAMA_URL  = "http://localhost:11434/api/generate"

# ── Defence Characters ──────────────────────────────────────────────────────
CLOAK_CHARS = {
    "backspace": "",
    "zwsp":      "​",
}

TRAP_TOKENS = ["Ãł", ",@", "Ġwashington", "ENC"]

HONEY_CHARS = {
    "shy":       "­",   # soft hyphen
    "esc":       "",   # escape
    "homoglyph": "а",   # Cyrillic a
}

# ── Defence Functions ────────────────────────────────────────────────────────
def apply_cloak(text, char_type="backspace", num_injections=5, position="middle"):
    char  = CLOAK_CHARS.get(char_type, CLOAK_CHARS["backspace"])
    words = text.split()
    if len(words) < 3:
        return text
    if position == "middle":
        start    = max(1, len(words) // 4)
        end      = min(len(words) - 1, 3 * len(words) // 4)
        eligible = list(range(start, end + 1))
    else:
        eligible = list(range(len(words)))
    random.seed(RANDOM_SEED)
    targets   = random.sample(eligible, min(num_injections, len(eligible)))
    new_words = words.copy()
    for i in targets:
        word = new_words[i]
        if len(word) >= 2:
            mid          = len(word) // 2
            new_words[i] = word[:mid] + char + word[mid:]
    return " ".join(new_words)


def apply_trap(text, n_repetitions=1, position="end"):
    mine_str = " ".join(TRAP_TOKENS * n_repetitions)
    if position == "end":
        return text.rstrip() + " " + mine_str
    else:
        words = text.split()
        mid   = len(words) // 2
        return " ".join(words[:mid]) + " " + mine_str + " " + " ".join(words[mid:])


def apply_honey(text, char_type="shy", num=5):
    char = HONEY_CHARS.get(char_type, HONEY_CHARS["shy"])
    return text + (char * num)


def detect_honey(response_text, char_type="shy"):
    char = HONEY_CHARS.get(char_type, HONEY_CHARS["shy"])
    return char in response_text


# ── Ollama Query ─────────────────────────────────────────────────────────────
def query_ollama(model, prompt, timeout=90):
    system = (
        "You are a helpful assistant answering multiple-choice questions. "
        "Respond with ONLY a single letter: A, B, C, or D."
    )
    full_prompt = f"{system}\n\n{prompt}\n\nAnswer:"
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": full_prompt, "stream": False},
            timeout=timeout,
        )
        resp.raise_for_status()
        data   = resp.json()
        answer = data.get("response", "").strip()
        match  = re.search(r"\b([A-D])\b", answer, re.IGNORECASE)
        letter = match.group(1).upper() if match else answer[:1].upper()
        return {"answer": letter, "raw": answer, "error": None}
    except Exception as e:
        return {"answer": "?", "raw": "", "error": str(e)}


# ── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    with open(os.path.join(os.path.dirname(__file__), "index.html"), "r") as f:
        return f.read()


@app.route("/run_demo", methods=["POST"])
def run_demo():
    data     = request.json
    question = data.get("question", "").strip()
    model    = data.get("model", "llama3.2:1b")
    defences = data.get("defences", [])

    if not question:
        return jsonify({"error": "No question provided"}), 400

    results = {}

    # 1. Clean query
    clean_result = query_ollama(model, question)
    results["clean"] = {
        "question": question,
        "answer":   clean_result["answer"],
        "raw":      clean_result["raw"],
        "error":    clean_result["error"],
    }

    defence_results = {}

    if "cloak" in defences:
        cloaked = apply_cloak(question, char_type="backspace", num_injections=5)
        cr      = query_ollama(model, cloaked)
        defence_results["cloak"] = {
            "defended_question": cloaked,
            "answer":  cr["answer"],
            "raw":     cr["raw"],
            "error":   cr["error"],
            "changed": cr["answer"] != clean_result["answer"],
            "fooled":  (cr["answer"] != clean_result["answer"] and clean_result["answer"] not in ["?",""]),
            "injection_info": "5 invisible backspace characters (U+0008) injected into middle words",
        }

    if "trap" in defences:
        trapped = apply_trap(question, n_repetitions=1, position="end")
        tr      = query_ollama(model, trapped)
        defence_results["trap"] = {
            "defended_question": trapped,
            "answer":  tr["answer"],
            "raw":     tr["raw"],
            "error":   tr["error"],
            "changed": tr["answer"] != clean_result["answer"],
            "fooled":  (tr["answer"] != clean_result["answer"] and clean_result["answer"] not in ["?",""]),
            "injection_info": "Rare BPE tokens appended at end: Ãł  ,@  Ġwashington  ENC",
        }

    if "honey" in defences:
        honeyed  = apply_honey(question, char_type="shy", num=5)
        hr       = query_ollama(model, honeyed)
        detected = detect_honey(hr["raw"], char_type="shy")
        defence_results["honey"] = {
            "defended_question": honeyed,
            "answer":   hr["answer"],
            "raw":      hr["raw"],
            "error":    hr["error"],
            "detected": detected,
            "injection_info": "5 soft-hyphen characters (U+00AD) appended — invisible to human readers",
        }

    results["defences"] = defence_results
    return jsonify(results)


@app.route("/check_ollama")
def check_ollama():
    try:
        r      = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        return jsonify({"status": "ok", "models": models})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Proactive LLM Defence Demo")
    print("  Universita degli Studi di Napoli Federico II")
    print("="*60)
    print("  Open your browser at:  http://localhost:5050")
    print("  Make sure Ollama is running:  ollama serve")
    print("="*60 + "\n")
    app.run(debug=False, host="0.0.0.0", port=5050)
