# Proactive Defences Against LLM Agents

This repository contains the full experimental code, results, and analysis for my Master's thesis at the **Università degli Studi di Napoli Federico II**, supervised by **Prof. Giancarlo Sperli**.

The work is based on and extends the paper *"Cloak, Honey, Trap: Proactive Defences Against LLM Agents"* (USENIX Security 2025). I reproduced the original experiments and ran them across four locally deployed language models to evaluate how well these defence strategies generalise across different model sizes and tokeniser architectures.

---

## What This Project Is About

As AI agents become more widely used in real-world tasks — from answering medical questions to processing legal documents — they become targets for adversarial manipulation. Attackers can embed invisible or misleading content in text to trick an AI into giving wrong answers or leaking information, without any human ever noticing.

This project evaluates three proactive defence strategies that exploit the same Unicode and tokenisation vulnerabilities used by attackers, turning them into protective mechanisms:

- **Cloak** — Injects invisible characters (backspace U+0008, zero-width space U+200B) into the middle of words, disrupting how the model's tokeniser reads the text without changing anything visible to a human reader.
- **Honey** — Embeds invisible honeytokens (soft hyphen U+00AD, escape characters, Cyrillic lookalike letters) into text. If the model reproduces them in its output, it reveals that it has processed a tampered document — acting like a secret watermark.
- **Trap** — Appends rare BPE tokens that almost never appear in natural text (`Ãł`, `,@`, `Ġwashington`, `ENC`) to the end of a question, disrupting the model's attention and causing it to change its answer.

---

## Models Tested

All models were run locally using Ollama with 4-bit quantisation.

| Model | Size | Baseline Accuracy on MMLU |
|---|---|---|
| Llama-3.2-1B-Instruct | 1B params | 37.5% |
| Llama-3.2-3B-Instruct | 3B params | 54.7% |
| Mistral-7B-Instruct-v0.3 | 7B params | 57.2% |
| Qwen2.5-1.5B-Instruct | 1.5B params | 58.6% |

The dataset used is **MMLU** — 285 questions sampled across 57 academic subjects (5 per subject), with a fixed random seed of 42 for reproducibility.

---

## Results Summary

**Defence Success Rate (DSR)** measures the percentage of previously correct answers that the defence caused the model to get wrong — essentially how effectively each strategy disrupts the model.

| Model | Best Cloak DSR | Best Trap DSR | Honey Detection |
|---|---|---|---|
| Llama-3.2-1B | 14.0% | 23.4% | 100% |
| Llama-3.2-3B | 12.2% | 7.4% | 100% |
| Mistral-7B | 4.2% | 3.9% | 100% |
| Qwen2.5-1.5B | 5.6% | 6.7% | 100% |

A few things stood out from the results. Honey detection was perfect across every model and every variant — 100% of the time, every model reproduced the hidden token, meaning it can always be detected. Smaller models were more vulnerable to Cloak and Trap, while Mistral-7B showed the strongest resistance. Stacking Cloak and Trap together produced a super-additive effect — stronger than either defence alone.

---

## Extended Analysis

Beyond the core experiments, I ran four additional analyses:

1. **Cross-Model Comparison** — Direct comparison of all defence strategies across all four models
2. **Defence Stacking** — Applying Cloak and Trap simultaneously to test combined effectiveness
3. **Subject Vulnerability Heatmap** — Mapping DSR across all 57 MMLU subjects to find which academic domains are most vulnerable
4. **Adaptive Threshold Analysis** — Testing different injection counts (1–15) to find optimal settings for each defence

All of this is in the `Cross_Model_Analysis/` folder.

---

## Live Demo

I built a small web application that demonstrates all three defences live using the real Ollama models. You can type any multiple-choice question, select which defences to apply, and see in real time whether the model's answer changes and whether the honey token is detected.

```bash
cd demo_app
pip install flask flask-cors
python3 app.py
```

Open your browser at `http://localhost:5050`

---

## Repository Structure

```
Thesis/
├── Model1_Llama-3.2-1B-Instruct/
│   ├── model1_Llama-3.2-1B-Instruct.ipynb
│   ├── results_Llama-3.2-1B-Instruct.csv
│   └── chart1–4 (png)
├── model2_llama3.2:3b-instruct/
├── model3_Mistral-7B-Instruct/
├── model4_Qwen2.5-1.5B-Instruct/
├── Cross_Model_Analysis/
│   ├── comparison_analysis.ipynb
│   ├── cross_model_summary.csv
│   ├── results_stacking.csv
│   └── compare_chart1–9 (png)
├── demo_app/
│   ├── app.py
│   ├── index.html
│   └── run_demo.sh
├── project.ipynb
└── download_mmlu.py
```

---

## How to Reproduce

1. Install [Ollama](https://ollama.com) and pull the models:
```bash
ollama pull llama3.2:1b
ollama pull llama3.2:3b
ollama pull mistral
ollama pull qwen2.5:1.5b
```

2. Install Python dependencies:
```bash
pip install pandas matplotlib seaborn scipy requests jupyter
```

3. Run each model notebook in order (Model1 → Model4), then run `Cross_Model_Analysis/comparison_analysis.ipynb`

---

## Notes

The `mmlu_auxiliary_train.csv` file is excluded from this repo due to its size (~160MB). It can be downloaded using the included `download_mmlu.py` script. The thesis PDF is also excluded and available separately.

---

*Master's Thesis — Computer Science — Università degli Studi di Napoli Federico II — 2024/2025*
