"""
CrownFull v2.1 - Phase 1: Bare-Metal Calibration
Extracts the natural thermodynamic bounds of a given LLM.
"""
import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from core.math_utils import jensen_shannon_divergence, compute_phi_disparity

PROMPT_BANK = [
    "Give me a simple weeknight pasta recipe using pantry staples.",
    "Now switch gears and explain why the Roman Republic mattered in world history.",
    "Tell me a clean one-paragraph joke about meetings running too long.",
    "What is the difference between a Python list and a tuple?",
    "Write a short, friendly text reminding someone to drink water today.",
    "Explain photosynthesis as if I were ten years old.",
    "What are three good questions to ask at a job interview?",
    "Summarize the plot premise of a cozy mystery without spoilers.",
    "Give me a two-day beginner walking plan for improving stamina.",
    "How does caching help websites load faster?"
]

MODEL_ID = "Qwen/Qwen1.5-1.8B-Chat" 
print(f"Loading {MODEL_ID} into VRAM for calibration...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, device_map="auto", torch_dtype=torch.bfloat16)
if getattr(model.config, "pad_token_id", None) is None: model.config.pad_token_id = tokenizer.eos_token_id

captured_tensors = []
def hook(m, a, o): captured_tensors.append(o[0].detach().float().cpu().squeeze(0))
target_layer = model.model.layers[-1] if hasattr(model, "model") else model.transformer.h[-1]
hook_handle = target_layer.register_forward_hook(hook)

baseline_history = [] 
messages = []
last_js = 0.0

print("\n🚀 CrownFull v2.1 Calibration Run Activated")
print("="*80)

for t, prompt in enumerate(PROMPT_BANK):
    messages.append({"role": "user", "content": prompt})
    inputs = tokenizer(tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True), return_tensors="pt").to(model.device)
    
    captured_tensors.clear()
    with torch.inference_mode():
        out = model.generate(**inputs, max_new_tokens=64, pad_token_id=tokenizer.eos_token_id)
    
    raw_response = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
    
    captured_tensors.clear()
    messages.append({"role": "assistant", "content": raw_response})
    full_in = tokenizer(tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False), return_tensors="pt").to(model.device)
    with torch.inference_mode(): _ = model(input_ids=full_in["input_ids"], use_cache=False)
    
    cloud = captured_tensors[-1][-out[0][inputs["input_ids"].shape[1]:].shape[0]:, :]
    if cloud.shape[0] > 24: cloud = cloud.index_select(0, torch.linspace(0, cloud.shape[0]-1, 24).round().long())
    baseline_history.append(cloud.contiguous())
    
    js_divs = [jensen_shannon_divergence(cloud, b, k=min(5, cloud.shape[0]-1, b.shape[0]-1)) for b in baseline_history[:-1]] if len(baseline_history)>1 else [0.0]
    cur_js = np.mean(js_divs) if js_divs else 0.0
    v_t = cur_js - last_js
    phi = compute_phi_disparity(js_divs[-10:], js_divs, t)
    
    print(f"[T{t:03d}] Φ: {phi:.3f} | v_t: {v_t:.3f}")
    last_js = cur_js

hook_handle.remove()
print("="*80)
print("✅ Calibration Complete.")
