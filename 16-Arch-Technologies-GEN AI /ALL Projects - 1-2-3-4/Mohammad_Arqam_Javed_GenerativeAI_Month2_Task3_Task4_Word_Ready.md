# ARCH TECHNOLOGIES INTERNSHIP REPORT
## Month 2 (Task 3 & Task 4)

### Front Page Details
- **Full Name:** MOHAMMAD ARQAM JAVED
- **Internship Domain:** Generative AI
- **Position:** GEN AI INTERN
- **Email:** arqamjaved873@gmail.com
- **Phone Number:** 03095069869
- **Month:** 2

---

## Table of Contents
1. Introduction
2. Task 3: RAG With Unsloth Dynamic 4-bit Quantization
3. Task 4: Speech-to-Reasoning With Whisper & Quantized LLM
4. Challenges and Solutions
5. Conclusion
6. References

---

## 1) Introduction
This report presents the implementation of two Generative AI projects completed in Month 2 of the internship:
- Task 3: Retrieval-Augmented Generation (RAG) using Unsloth dynamic 4-bit quantized LLM
- Task 4: Speech-to-Reasoning pipeline using Whisper ASR and quantized LLM

The work was executed in Google Colab with focus on accurate outputs and efficient GPU memory usage.

---

## 2) Task 3: Implement RAG With Unsloth Dynamic 4-bit Quantization

### 2.1 Objective
Build a RAG system that retrieves relevant knowledge from indexed documents and generates grounded responses using an Unsloth dynamic 4-bit quantized model.

### 2.2 Tools and Libraries
- Python, Google Colab
- Unsloth
- Transformers + BitsAndBytes
- Sentence-Transformers
- FAISS

### 2.3 Implementation Steps
1. Installed dependencies for quantized inference and retrieval.
2. Loaded `unsloth/Llama-3.2-3B-Instruct-unsloth-bnb-4bit`.
3. Prepared domain-specific text documents.
4. Chunked documents into smaller semantic blocks.
5. Generated embeddings with `all-MiniLM-L6-v2`.
6. Indexed vectors with FAISS.
7. Implemented `top-k` retrieval for query context.
8. Built grounded prompt with retrieved chunks.
9. Generated final response using quantized LLM.

### 2.4 Memory Optimization Notes
- Dynamic 4-bit quantization lowers VRAM usage while preserving critical precision.
- Limited sequence length and output tokens.
- Batched embedding generation for stable performance.

### 2.5 Results
- Relevant chunks were retrieved for user queries.
- Final responses remained grounded in retrieved context.
- Pipeline executed within Colab GPU constraints.

### 2.6 Screenshot Placeholders
- **Figure 1:** [Insert screenshot of package installation + model loading]
- **Figure 2:** [Insert screenshot of FAISS index creation]
- **Figure 3:** [Insert screenshot of retrieved top-k chunks]
- **Figure 4:** [Insert screenshot of final grounded answer]

### 2.7 Code File
- Task3_RAG_Unsloth_4bit.ipynb

---

## 3) Task 4: Build a Speech-to-Reasoning Pipeline With Whisper & Quantized LLM

### 3.1 Objective
Create a complete pipeline where speech audio is transcribed using Whisper and then passed to a quantized reasoning model for logical answer generation.

### 3.2 Tools and Libraries
- Python, Google Colab
- OpenAI Whisper (`openai/whisper-small`)
- Unsloth dynamic 4-bit model
- Transformers

### 3.3 Implementation Steps
1. Installed ASR + quantized LLM dependencies.
2. Initialized Whisper ASR pipeline.
3. Processed sample audio and generated transcript text.
4. Loaded `unsloth/Llama-3.2-3B-Instruct-unsloth-bnb-4bit` for reasoning.
5. Designed reasoning prompt from transcript.
6. Generated final response from quantized model.
7. Verified complete end-to-end flow.

### 3.4 Efficiency Notes
- ASR chunking and batching for stable transcription.
- 4-bit quantized LLM for efficient GPU usage.
- Controlled generation settings for faster inference.

### 3.5 Results
- Audio input was successfully transcribed.
- Transcript was correctly passed to reasoning model.
- Final answer was generated in a single integrated pipeline.

### 3.6 Screenshot Placeholders
- **Figure 5:** [Insert screenshot of Whisper model initialization]
- **Figure 6:** [Insert screenshot of transcription output]
- **Figure 7:** [Insert screenshot of quantized reasoning model loading]
- **Figure 8:** [Insert screenshot of final reasoning output]

### 3.7 Code File
- Task4_Speech_to_Reasoning_Whisper_Unsloth.ipynb

---

## 4) Challenges and Solutions

### Challenge 1: Colab VRAM limitations
**Solution:** Used Unsloth dynamic 4-bit quantized model and tuned token lengths.

### Challenge 2: Maintaining grounded generation
**Solution:** Applied retrieval-first prompting in Task 3.

### Challenge 3: Audio inference stability
**Solution:** Enabled ASR chunking and batching for Whisper.

---

## 5) Conclusion
Both tasks were completed successfully with practical, efficient GenAI pipelines:
- A grounded RAG system using retrieval + dynamic 4-bit inference.
- A full speech-to-reasoning pipeline combining Whisper transcription with quantized LLM reasoning.

These implementations demonstrate production-relevant skills in memory-efficient model usage, retrieval integration, and multimodal workflow design.

---

## 6) References
- Unsloth Documentation
- Hugging Face Transformers Documentation
- FAISS Documentation
- OpenAI Whisper Model Documentation

---

## Final Submission Checklist
- [ ] Add all screenshots at figure placeholders
- [ ] Copy this report into Microsoft Word
- [ ] Apply professional formatting (title page, heading styles, spacing)
- [ ] Export to PDF
- [ ] Use file name: **Mohammad_Arqam_Javed_GenerativeAI_Month2.pdf**
- [ ] Email PDF to **submissions.archtech@gmail.com**
- [ ] Upload LinkedIn post and mention **@Arch Technologies**
