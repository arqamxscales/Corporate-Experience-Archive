# ARCH TECHNOLOGIES - MONTH 2 REPORT (TASK 3 & TASK 4)

## Front Page

**Full Name:** MOHAMMAD ARQAM JAVED  
**Internship Domain:** Generative AI  
**Position:** GEN AI INTERN  
**Email:** arqamjaved873@gmail.com  
**Phone Number:** 03095069869  
**Month:** 2  

---

## Project Scope
This report covers only the following assigned Month 2 tasks:
1. Task 3: Implement RAG with Unsloth dynamic 4-bit quantization
2. Task 4: Build a Speech-to-Reasoning pipeline with Whisper and quantized LLM

---

## Task 3: Implement RAG With Unsloth Dynamic 4-bit Quantization

### Objective
Build a Retrieval-Augmented Generation (RAG) pipeline in Colab using an Unsloth dynamic 4-bit model, retrieve relevant chunks from domain documents, and generate grounded responses.

### Notebook
- Task3_RAG_Unsloth_4bit.ipynb

### Implementation Summary
- Installed required libraries (`unsloth`, `transformers`, `bitsandbytes`, `sentence-transformers`, `faiss-cpu`).
- Loaded dynamic 4-bit quantized model: `unsloth/Llama-3.2-3B-Instruct-unsloth-bnb-4bit`.
- Created document chunking pipeline for domain-specific text.
- Generated embeddings with `all-MiniLM-L6-v2`.
- Built FAISS vector index for semantic retrieval.
- Implemented top-k retrieval + context-grounded prompting.
- Generated responses from quantized LLM.

### VRAM / Efficiency Handling
- 4-bit quantized loading to reduce memory footprint.
- Controlled `max_seq_length` and `max_new_tokens`.
- Used embedding batch processing.

### Evidence to Attach
- Screenshot: package/model loading
- Screenshot: retrieved chunks
- Screenshot: final grounded answer

---

## Task 4: Speech-to-Reasoning Pipeline With Whisper & Quantized LLM

### Objective
Build one Colab notebook that transcribes audio using Whisper and feeds transcript into a quantized reasoning model for logical QA/summarization.

### Notebook
- Task4_Speech_to_Reasoning_Whisper_Unsloth.ipynb

### Implementation Summary
- Installed ASR and LLM dependencies.
- Loaded Whisper ASR model: `openai/whisper-small`.
- Performed audio transcription with chunking and batching.
- Loaded Unsloth dynamic 4-bit reasoning model.
- Prompted model with transcript for reasoning output.
- Demonstrated end-to-end pipeline using sample audio.

### VRAM / Efficiency Handling
- Whisper chunked inference (`chunk_length_s`) and batching.
- Quantized LLM in 4-bit mode for Colab GPU constraints.
- Controlled output length and sampling parameters.

### Evidence to Attach
- Screenshot: transcription output
- Screenshot: reasoning prompt/output
- Screenshot: end-to-end run success

---

## Code Section (for Word/PDF)
Copy selected code blocks from both notebooks:
- Model loading cell
- Retrieval/indexing cell (Task 3)
- ASR transcription cell (Task 4)
- Final generation/reasoning cell

---

## Final Submission Checklist
- [ ] Add screenshots from notebook runs
- [ ] Copy this report into Word document format
- [ ] Ensure front page includes personal details
- [ ] Convert to PDF
- [ ] File name format: `Mohammad_Arqam_Javed_GenerativeAI_Month2.pdf`
- [ ] Email to: submissions.archtech@gmail.com
- [ ] Upload LinkedIn post and mention @Arch Technologies
