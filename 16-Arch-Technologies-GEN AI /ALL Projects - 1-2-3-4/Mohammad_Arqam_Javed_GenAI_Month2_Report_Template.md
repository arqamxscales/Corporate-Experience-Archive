# ARCH TECHNOLOGIES - MONTH 2 INTERNSHIP REPORT

## Front Page

**Full Name:** MOHAMMAD ARQAM JAVED  
**Internship Domain:** Generative AI  
**Role:** GEN AI INTERN  
**Email:** arqamjaved873@gmail.com  
**Phone:** 03095069869  
**Month:** 2  

---

## Table of Contents
1. Introduction
2. Task 1
3. Task 2
4. Task 3 - RAG With Unsloth Dynamic 4-bit Quantization
5. Task 4 - Speech-to-Reasoning With Whisper & Quantized LLM
6. Challenges and Solutions
7. Conclusion
8. References

---

## 1) Introduction
This report summarizes my Month 2 internship work in Generative AI at Arch Technologies. The focus was on implementing practical AI pipelines, optimizing memory with quantized models, and demonstrating end-to-end solutions in Google Colab.

---

## 2) Task 1
> Add your official Task 1 problem statement here.

### Objective
- [Fill this section]

### Implementation
- [Fill this section]

### Results
- [Add outputs/screenshots]

---

## 3) Task 2
> Add your official Task 2 problem statement here.

### Objective
- [Fill this section]

### Implementation
- [Fill this section]

### Results
- [Add outputs/screenshots]

---

## 4) Task 3 - RAG With Unsloth Dynamic 4-bit Quantization

### Objective
Build a Retrieval-Augmented Generation pipeline using an Unsloth dynamic 4-bit model, with document indexing and retrieval for grounded responses.

### Environment
- Platform: Google Colab
- GPU: [Fill GPU type]
- Model: Unsloth dynamic 4-bit model (`unsloth-bnb-4bit` variant)

### Implementation Summary
1. Installed required libraries (`unsloth`, `transformers`, `bitsandbytes`, `sentence-transformers`, `faiss-cpu`).
2. Loaded a dynamic 4-bit quantized LLM using Unsloth.
3. Added domain documents and split them into chunks.
4. Created embeddings and stored them in a FAISS vector index.
5. Implemented retrieval (`top-k` chunks by semantic similarity).
6. Built a grounded prompt from retrieved context.
7. Generated final answers from the quantized LLM.

### Code File
- `Task3_RAG_Unsloth_4bit.ipynb`

### Key Output
- Show retrieval chunks and generated answer screenshots.

### Memory Optimization Notes
- 4-bit loading reduces VRAM significantly.
- Limited sequence length and controlled generation tokens.
- Used batch encoding and normalized embeddings.

---

## 5) Task 4 - Speech-to-Reasoning With Whisper & Quantized LLM

### Objective
Create an end-to-end speech pipeline that transcribes audio with Whisper and passes transcription to a quantized reasoning model.

### Environment
- Platform: Google Colab
- ASR Model: `openai/whisper-small`
- Reasoning Model: Unsloth dynamic 4-bit model

### Implementation Summary
1. Installed speech + LLM dependencies.
2. Initialized Whisper ASR pipeline with chunking and batching.
3. Transcribed sample audio to text.
4. Loaded Unsloth dynamic 4-bit reasoning model.
5. Passed transcript into reasoning prompt.
6. Generated final logical response.

### Code File
- `Task4_Speech_to_Reasoning_Whisper_Unsloth.ipynb`

### Key Output
- Show transcription screenshot.
- Show reasoning output screenshot.

### Efficiency Notes
- ASR chunking for stable transcription.
- Quantized 4-bit model to stay within Colab GPU memory.
- Controlled output length and sampling params.

---

## 6) Challenges and Solutions
- **Challenge:** Limited Colab VRAM for larger models.  
  **Solution:** Used Unsloth dynamic 4-bit quantization and smaller sequence lengths.
- **Challenge:** Hallucination risk in generation.  
  **Solution:** Added retrieval context and grounded prompt constraints.
- **Challenge:** Audio quality variations.  
  **Solution:** Used Whisper with chunk-based inference.

---

## 7) Conclusion
In Month 2, I implemented advanced Generative AI workflows covering both text-based retrieval generation and audio-to-reasoning pipelines. The projects demonstrate practical deployment patterns with memory-efficient quantized models suitable for constrained GPU environments.

---

## 8) References
- Unsloth documentation
- Hugging Face Transformers
- FAISS documentation
- OpenAI Whisper model card

---

## Submission Checklist
- [ ] Add Task 1 details
- [ ] Add Task 2 details
- [ ] Paste code snippets in report
- [ ] Insert project screenshots
- [ ] Export to PDF
- [ ] Rename as: `Mohammad_Arqam_Javed_GenerativeAI_Month2.pdf`
- [ ] Email to: submissions.archtech@gmail.com
- [ ] Upload on LinkedIn and mention @Arch Technologies
