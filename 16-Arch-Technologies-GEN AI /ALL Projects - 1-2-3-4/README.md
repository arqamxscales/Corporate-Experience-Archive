# Task 2 — Medical Fine-Tuning with QLoRA (Unsloth + Colab)

This workspace contains a **ready-to-run Google Colab notebook** for QLoRA fine-tuning on a medical dataset.

## Files
- [medical_qlora_unsloth_colab.ipynb](medical_qlora_unsloth_colab.ipynb): Full training + evaluation workflow.
- [requirements_colab.txt](requirements_colab.txt): Reference dependency list.

## What this notebook does
1. Installs Unsloth + training dependencies in Colab.
2. Loads a 4-bit quantized base model (`unsloth/DeepSeek-R1-Distill-Llama-8B-bnb-4bit`).
3. Applies LoRA adapters with memory-efficient settings.
4. Loads and formats a domain-specific medical Q&A dataset (`medmcqa`) and prints dataset previews.
5. Runs epoch-based supervised fine-tuning with `SFTTrainer`.
6. Logs GPU memory usage before/after training.
7. Saves adapters/tokenizer to Colab and optional Google Drive path.
8. Provides an optional qualitative check on MedMCQA validation questions.
9. Exposes an `ask_medical(...)` helper and `interactive_chat()` loop for testing the tuned model.

## Run steps (Colab)
1. Upload/open `medical_qlora_unsloth_colab.ipynb` in Google Colab.
2. In `Training + generation configuration`, optionally edit:
   - `BASE_MODEL`
   - `MAX_STEPS` / `NUM_EPOCHS`
   - `DATASET_NAME`
   - generation settings (`GEN_MAX_NEW_TOKENS`, `GEN_TEMPERATURE`, `GEN_TOP_P`)
3. Run cells **top to bottom**.
4. Download adapter from `/content/medical_qlora_adapter` (or from Drive if enabled).
5. Use the last inference cell (or `interactive_chat()`) to test new medical questions.

## Safety
- The model and notebook are for **research and education only**.
- Do **not** use outputs for real patient care or clinical decisions.

## Notes
- Best run target: Colab GPU runtime (T4/L4/A100).
- If VRAM is limited, reduce `BATCH_SIZE`, increase `GRAD_ACCUM`, and keep `MAX_SEQ_LENGTH` moderate.
- The provided defaults are tuned for reliability over speed.
