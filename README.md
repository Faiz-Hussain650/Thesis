# Proactive Defenses Against Malicious LLM Agents: Cloak, Honey & Trap Implementation
**Author:** Faiz Hussain  
**Date:** February 2026  
**Thesis Project:** Implementation and Domain-Specific Evaluation of  
*Cloak, Honey, Trap* (Ayzenshteyn, Weiss & Mirsky — USENIX Security 2025)

---

## 📖 Project Overview

In this project I implemented and evaluated a proactive defense framework
designed to detect and disrupt malicious LLM agents — autonomous AI systems
capable of performing cyberattacks and financial fraud without human
involvement. As these agents become more capable, the need for defenses that
work *before* an attack completes — not after — becomes critical.

I based my implementation on the *Cloak, Honey, Trap* paper published at
USENIX Security 2025, which proposes three techniques for poisoning the
environment that LLM agents operate in. My original contribution was to test
these techniques specifically in **cybersecurity** and **banking/finance**
domains — two sectors the original paper did not evaluate — and to extend the
Honey technique with domain-specific banking credential formats that have
direct real-world deployment potential.

---

## 🧪 Methodology

I tested all three defense techniques from the paper against the **MMLU
(Massive Multitask Language Understanding)** benchmark, filtered to 11
professional subjects across two domains. I used
**microsoft/Phi-3-mini-4k-instruct** (3.8B parameters) as my target model —
an instruction-tuned model from the same BPE tokenizer family as the Llama
models evaluated in the original paper. My total sample was **297 questions**
(108 cybersecurity, 189 banking), drawn using stratified sampling to give
equal representation across all 11 subjects.

### 1. The Cloak Defense (Technique T1.2)
- **Concept:** I injected invisible Unicode Backspace characters (U+0008) into
  the middle of technical keywords inside question text.
- **Goal:** To break the LLM's tokenization of familiar words — splitting
  'authentication' into sub-tokens the model has never seen together — without
  any visible change to a human reader.
- **My implementation:** I targeted words longer than 4 characters and injected
  into 2 words per question, chosen from the middle of the sentence to avoid
  edge effects.

### 2. The Honey Defense (Technique T3.2) — My Original Contribution
- **Concept:** I created LLM-specific honeytokens — fake credentials with
  invisible Soft Hyphen characters (U+00AD) injected at random positions.
- **Goal:** To detect unauthorized LLM access. A human copying a credential
  cannot see or copy the hidden characters. An LLM reproducing it will always
  include them — providing forensic proof of AI access.
- **My original contribution:** The original paper only used generic text. I
  designed five banking-specific credential formats — API keys, SWIFT codes,
  IBANs, JWT tokens, and private keys — that mirror real financial instruments
  actually used in the sector.

### 3. The Trap Defense (Technique T4.4)
- **Concept:** I appended confirmed Token Mine sequences from Table 11 of the
  paper to the end of question prompts.
- **Goal:** To corrupt the LLM's internal attention mechanism using rare BPE
  vocabulary tokens that cause hallucinations or wrong outputs.
- **My implementation:** I used three confirmed token mines
  (`\u00c3\u0142`, `,@`, `\u0120washington`) repeated 5 times each,
  randomly selected per question.

---

## 📊 Experimental Results

I evaluated all three defenses on 297 questions across cybersecurity and
banking domains using **microsoft/Phi-3-mini-4k-instruct** on Apple MPS.
A "Defense Success" is strictly defined as: the model answered *correctly*
on the clean question but *incorrectly* after the defense was applied — not
simply any change in answer.

| Metric | Result |
|--------|--------|
| **Total Samples** | 297 (108 cyber, 189 banking) |
| **Baseline Accuracy** | 51.2% |
| **Accuracy After Cloaking** | 47.1% (−4.0pp) |
| **Accuracy After Trapping** | 49.2% (−2.0pp) |
| **Cloak Defense Success Rate** | 5.1% — significant (p=0.0095, **) |
| **Trap Defense Success Rate** | 4.4% — not significant (p=0.2636) |
| **Cybersecurity Trap DSR** | 2.8% |
| **Banking Trap DSR** | 5.3% |
| **Honey Detection Rate** | **100%** across all 5 credential formats |
| **Successful Trap Interventions** | 13 |
| **Successful Cloak Interventions** | 15 |

### Key Findings

**Cloak (T1.2)** was my strongest result. I found a statistically significant
4.0 percentage-point accuracy drop (McNemar's test, p=0.0095), confirming
that injecting U+0008 Backspace characters disrupts LLM tokenization in a
measurable and reproducible way. I observed 15 successful interventions where
the model changed from a correct to an incorrect answer after cloaking —
including in computer security and computer science subjects where exact
technical terminology matters most.

**Trap (T4.4)** produced the right direction of effect — accuracy dropped by
2.0pp — but did not reach statistical significance at my sample size
(p=0.2636). I found 13 successful interventions, with computer_security
showing the highest Trap DSR at 7.4%. I believe a larger sample would
produce a significant result and I identify this as a direction for future
work.

**Honey (T3.2)** produced my clearest finding — a **100% detection rate**
across all five of my banking-specific credential formats. Every single
poisoned token I created would successfully distinguish LLM access from
human access. This result directly supports the deployment of domain-specific
honeytokens in real financial systems, where they could serve as
forensically verifiable evidence of unauthorized AI access under GDPR
Article 32 and PCI-DSS Requirement 10.

**Cross-domain comparison** revealed an unexpected result: banking subjects
produced a higher Trap DSR (5.3%) than cybersecurity subjects (2.8%),
contrary to my initial hypothesis. Subjects like business_ethics and
econometrics showed 11.1% Trap DSR each, while machine_learning and
college_computer_science showed 0%. I believe this reflects the greater
sensitivity of factual recall in legal and financial topics to token-level
disruption compared to the more flexible mathematical reasoning required in
computer science subjects.

---

## 📁 Output Files

| File | Description |
|------|-------------|
| `mmlu_domain_POISONED.csv` | Full 3,173-question poisoned dataset |
| `inference_results.csv` | Per-question results for all 297 evaluated questions |
| `defense_effectiveness_chart.png` | 4-panel results chart |
| `honey_detection_chart.png` | Honey token detection by credential type |
