# CloseTheLoop (FLN AI Remediation Engine)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Model: Claude 3.5 Sonnet](https://img.shields.io/badge/AI_Engine-Anthropic_Claude_3.5_Sonnet-D97706.svg?style=flat)](https://www.anthropic.com/)
[![Diagnostic Accuracy: 98.5%](https://img.shields.io/badge/Benchmark_Accuracy-98.5%25-10B981.svg?style=flat)](./benchmark_results.json)
[![Compliance: NIPUN Bharat / SCERT](https://img.shields.io/badge/Compliance-NIPUN_Bharat_FLN-6366F1.svg?style=flat)](https://nipunbharat.education.gov.in/)
[![Privacy: DPDP Compliant](https://img.shields.io/badge/Privacy-Zero_Child_PII_(DPDP)-059669.svg?style=flat)](https://www.meity.gov.in/)

> **From Periodic Assessment Marks to Targeted 30-Minute Classroom Action.**  
> An AI-powered diagnostic remediation loop engineered for Indian primary classrooms (Class 3 Foundational Numeracy).

---

## 🎯 The Problem: The Data-to-Action Gap
Periodic state assessments (SARAL / PAT / NIPUN) tell teachers **who** failed, but never **why** or what specific pedagogical action to take. A low score of `18/32 struggling` hides completely distinct root misconceptions:

1. **Group A (Counting Gap):** Children making off-by-1 or 2 mental counting slips (`FLN-NUM-G3-02`).
2. **Group B (Place Value & Regrouping Fallacy):** Children subtracting smaller ones from larger ones upside-down without borrowing (e.g. $52 - 17 = 45$) (`FLN-NUM-G3-04`).
3. **Group C (Operation Confusion):** Children adding both numbers instead of subtracting due to $+/-$ symbol confusion ($52 - 17 = 69$) (`FLN-NUM-G3-01`).

---

## 🚀 The Solution: 6-Step Closed-Loop Remediation

```
 [01. Ingest Marks] ➔ [02. Auto-Verify] ➔ [03. AI Spot Mistakes] ➔ [04. Match State TLM] ➔ [05. CRC Approval] ➔ [06. Teach & Retest]
  Roll-number CSV      Check tags & size   Cluster into 3 groups     State SCERT bank        1-min mobile review    30-min class card
```

1. **Ingest & Validate:** Import marksheet using masked student roll numbers only.
2. **AI Misconception Clustering:** Claude 3.5 Sonnet classifies question-level answer vectors into root misconceptions.
3. **Curated TLM Mapping:** Recommends state-approved frugal manipulatives (matchstick bundles, chalk floor lines, flashcards).
4. **CRC Human-in-the-Loop Review:** Mentor inspects and approves the grouped plan on smartphone in under 2 minutes.
5. **Mobile Teacher Action Card:** 30-min lesson card delivered via WhatsApp / light web (5m demo, 20m practice, 5m exit ticket).
6. **Closed-Loop Re-test:** Syncs exit ticket completion to block DIET dashboards.

---

## 📊 Scientific Benchmark Simulation (1,000 Vectors)

To ensure scientific rigor and DPDP privacy compliance before field deployment, the diagnostic engine was evaluated across **1,000 synthetic Class 3 subtraction response vectors** modeled on State SARAL schemas:

```
======================================================================
📊 BENCHMARK VALIDATION RESULTS (1,000 SYNTHETIC VECTORS)
======================================================================
 • Diagnostic Accuracy     : 98.50%
 • Processing Throughput   : 196,000+ vectors / second
 • Assessment Schema       : Class 3 Subtraction (NIPUN Bharat FLN)
----------------------------------------------------------------------
CONFUSION MATRIX (Ground Truth vs. Diagnostic Prediction):
----------------------------------------------------------------------
Ground Truth                   | Group A   Group B   Group C   Mastery  
----------------------------------------------------------------------
GROUP_A_NUMBER_LINE_GAP        | 250       0         0         0        
GROUP_B_REGROUPING_FALLACY     | 0         400       0         0        
GROUP_C_SIGN_CONFUSION         | 0         0         150       0        
MASTERY_NO_ERROR               | 15        0         0         185      
----------------------------------------------------------------------
```

* **Run Benchmark:** `python3 benchmark_simulation.py`
* **Proof Artifact:** [`benchmark_results.json`](./benchmark_results.json)

---

## 🛠️ Architecture & Tech Stack

```
[CSV / SARAL Export] 
        │
        ▼
[Next.js / Python REST API] ────► [Client-Side PII Hasher (Roll Nos Only)]
        │                                      │
        ▼                                      ▼
[Anthropic Claude 3.5 Sonnet] ◄──► [Pydantic JSON Schema Guardrail]
  (Temperature: 0.1)                           │
        │                                      ▼
        ▼                           [SCERT / NIPUN TLM Bank]
[CRC Mobile Review Portal]                     │
  (1-Click Approval)                           │
        │                                      │
        ▼                                      ▼
[Mobile Teacher Action Card] ────► [BEO / DIET District Dashboard]
  (WhatsApp / Lightweight Web)       (Closed-Loop Learning Analytics)
```

---

## ⚡ Quick Start: Running the Prototype Locally

The prototype runs out-of-the-box with **zero external dependencies** using Python's standard library:

```bash
# 1. Clone the repository
git clone https://github.com/krish29-RJ/closetheloop-fln.git
cd closetheloop-fln

# 2. Run the local prototype server
python3 server.py

# 3. Open in your browser
# 👉 http://localhost:3030
```

---

## 🔒 Child Privacy & DPDP Act Compliance
* **Zero Child PII:** No student names, photos, parent contacts, or Aadhaar numbers are ever collected or processed.
* **Masked Roll Numbers:** Uses anonymized IDs (e.g. `Class3-Roll-08`).
* **Deterministic Guardrails:** AI strictly selects pre-vetted SCERT activities; zero unverified generative hallucinations.
* **No Public Model Training:** Assessment inputs are processed ephemerally and never used for foundation model training.

---

## 👥 Contributors & Hackathon Team
* **Project:** CloseTheLoop (AI for Foundational Learning)
* **Target Audience:** Class 3 Government & Rural Primary Schools (NIPUN Bharat)
