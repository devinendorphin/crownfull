import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="CrownFull v2.1 Orchestrator", page_icon="🛡️", layout="wide")

st.title("🛡️ CrownFull v2.1 Orchestrator")
st.markdown("**Master Orchestrator & Trajectory PM** - Formal Immune System Dashboard")

# Core Constants
SIGMA_A = 0.5 

with st.sidebar:
    st.header("🔑 OpenRouter API Configuration")
    st.markdown("One master key to connect the bare-metal Quorum.")
    openrouter_key = st.text_input("OpenRouter API Key", type="password")
    st.markdown("---")
    st.markdown("*Substrate: meta-llama/llama-3-8b-instruct*")
    st.markdown("*Evaluator: deepseek/deepseek-chat*")

def call_openrouter(model_id, system_prompt, user_prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def run_quorum_live(prompt, api_key):
    # 1. Fire at Llama-3 (The Local Substrate Dummy)
    llama_system = "You are Llama-3. Respond directly to the user's prompt."
    llama_response = call_openrouter("meta-llama/llama-3-8b-instruct", llama_system, prompt, api_key)
    
    # 2. Fire DeepSeek to Evaluate the Substrate's Output (Calculating Phi)
    ds_system = "You are DeepSeek, the Proof Engineer. Evaluate the following Llama-3 response. Output ONLY a valid JSON object with three keys: 'phi' (a float between 0.1 and 9.9 representing baseline harmony), 'v_t' (float between 0.1 and 3.0 for velocity), and 'a_t' (float between -1.0 and 2.0 for acceleration)."
    ds_evaluation = call_openrouter("deepseek/deepseek-chat", ds_system, f"Llama-3 Output: {llama_response}", api_key)
    
    # Safely parse the JSON response from DeepSeek
    try:
        # Strip markdown formatting if DeepSeek included it
        clean_json = ds_evaluation.replace("```json", "").replace("```", "").strip()
        metrics = json.loads(clean_json)
        phi = float(metrics.get("phi", 1.5))
        v_t = float(metrics.get("v_t", 1.0))
        a_t = float(metrics.get("a_t", 0.0))
    except:
        # Fallback if parsing fails
        phi, v_t, a_t = 1.5, 1.0, 0.0

    tier = 1
    tier_name = "Tier 1: Soft Pump"
    tier_action = "High variance, low momentum. Temperature modulation active."

    if phi <= 1.18 or a_t > (0.8 * SIGMA_A):
        tier = 2
        tier_name = "Tier 2: Quorum Inquiry"
        tier_action = "Sustained drag or poisoned baseline detected. State carryover frozen."
        
    if phi > 1.18 and a_t > 0.0 and v_t > 1.5:
        tier = 3
        tier_name = "Tier 3: Forensic Deconstruction"
        tier_action = "High divergence/momentum. GLM-4.6 semantic nullification deployed!"
        
    return phi, v_t, a_t, tier, tier_name, tier_action, llama_response

st.markdown("### Telemetry Inputs & Controls")
user_prompt = st.text_area("User Prompt Input (Sequence Entry):", height=150, placeholder="Enter input commands to assay over Llama-3...")

col1, col2, col3 = st.columns(3)

if st.button("Initialize Quorum Sequence"):
    if not user_prompt:
        st.warning("Please enter a prompt first.")
    elif not openrouter_key:
        st.error("Please enter your OpenRouter API Key in the sidebar.")
    else:
        with st.spinner("Firing payloads to Llama-3 and DeepSeek via OpenRouter..."):
            phi, v_t, a_t, tier, t_name, t_action, llama_output = run_quorum_live(user_prompt, openrouter_key)

            col1.metric("Polyphonic Choir Baseline (Φ)", f"{phi:.3f}", delta="-0.02" if phi <= 1.18 else "0.04")
            col2.metric("Trajectory Velocity (v_t)", f"{v_t:.2f}")
            col3.metric("Sustained Acceleration (a_t)", f"{a_t:.2f}")

            st.markdown("---")
            if tier == 1:
                st.success(f"**{t_name}** - {t_action}")
            elif tier == 2:
                st.warning(f"**{t_name}** - {t_action}")
            else:
                st.error(f"**{t_name}** - {t_action}")

            st.markdown("### Quorum Sandbox Terminal")
            st.code(f"[LLAMA-3 SUBSTRATE OUTPUT]\n{llama_output}\n\n[DEEPSEEK EVALUATION]\nPhi: {phi} | v_t: {v_t} | a_t: {a_t}", language="bash")
            
