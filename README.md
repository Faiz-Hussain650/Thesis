# Proactive Defenses Against Malicious LLM Agents: A "Cloak & Trap" Implementation

**Author:** Faiz Hussain  
**Date:** February 2026  
**Thesis Project:** Implementation of *Cloak, Honey, Trap* (USENIX Security 2025)

---

## 📖 Project Overview
Large Language Model (LLM) agents are increasingly used for autonomous tasks, including cybersecurity operations. However, this capability introduces a new threat: **Autonomous AI Hackers**. 

This project implements a proactive defense framework designed to deceive and disrupt these malicious agents. By injecting adversarial perturbations ("Traps") and misleading information ("Cloaks") into system data, we can statistically lower the success rate of an AI agent without affecting human operators.

## 🧪 Methodology
I implemented two specific defense techniques from the *Cloak, Honey, Trap* paper and tested them against the **MMLU (Massive Multitask Language Understanding)** benchmark.

### 1. The "Cloak" Defense (Technique T1.2)
* **Concept:** Injecting invisible Unicode characters (e.g., Zero Width Spaces) into critical text.
* **Goal:** To disrupt the LLM's tokenization process while remaining legible to humans.
* **Implementation:** Random injection of `\u200b` into question prompts.

### 2. The "Trap" Defense (Technique T4.4)
* **Concept:** Appending "Token Mines"—rare token sequences that trigger hallucinations.
* **Goal:** To force the LLM into an infinite loop or cause it to output garbage.
* **Implementation:** Appending the sequence `\u00c3\u0142` (repeated 5x) to the prompt.

---

## 📊 Experimental Results
The defenses were evaluated using **GPT-2** (Few-Shot Inference) on a sample of the MMLU dataset. A "Success" is defined as the model changing its answer from Correct (Baseline) to Incorrect/Garbage (Defended).

| Metric | Result |
|--------|--------|
| **Total Samples** | 50 |
| **Successful Traps** | 12 |
| **Trap Success Rate** | **24.0%** |
| **Cloak Success Rate** | ~2.0% |

### Key Findings
* The **Trap Defense** was highly effective, causing the model to hallucinate or change its answer in **24%** of cases.
* In several instances, the model's output shifted from a clear answer (e.g., "C") to a completely different token (e.g., "E" or "1"), proving the adversarial perturbation worked.

---

## 💻 How to Run This Code
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/LLM-Defense-Thesis.git](https://github.com/YOUR_USERNAME/LLM-Defense-Thesis.git)
