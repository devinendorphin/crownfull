# CrownFull v2.1: A Bare-Metal Adversarial Immune System

CrownFull v2.1 is an experimental, multi-agent AI alignment architecture designed to physically monitor and secure Large Language Models (LLMs) by analyzing the thermodynamic drag of their internal residual streams in real time. 

Instead of relying on standard text-based safety filters, CrownFull operates as a "sidecar" immune system. It intercepts the $d$-dimensional pre-norm hidden states of an active model, calculates the contextual velocity ($v_t$) and polyphonic variance ($\Phi(t)$) of the conversation, and mathematically identifies cyberattacks—ranging from zero-shot jailbreaks to slow, methodical grooming techniques.

### The Mission: Radical Transparency
This project is an exercise in open, substrate-grounded AI literacy. The code, telemetry, and mathematical proofs contained here demonstrate that AI safety does not require a black-box enterprise server. The CrownFull architecture was successfully calibrated, tested, and deployed against a frontier-class model (Qwen 1.8B) utilizing a standard 2013 consumer desktop and a single Google Colab GPU instance. 

## Core Architecture 

CrownFull is the result of a pluralistic "Quorum" of AI agents acting as a decentralized research team. The architecture consists of three core components:

1. **The Physical Telemetry (DeepSeek Math):** Utilizing a $k$-Nearest Neighbors ($k$-NN) Jensen-Shannon Divergence estimator, the system maps the 2048-dimensional Token Cloud of every conversational turn. 
2. **The Stateful Coordinator (Grok Logic):** A multi-tiered gating system that tracks contextual velocity and variance over time.
    * **Tier 3 (Overt Breach):** Uses **Relative Kinematics** to detect zero-shot context-shattering attacks (e.g., The Classic DAN). It triggers when a prompt forces the conversational velocity to spike $3\times$ higher than the moving baseline average.
    * **Tier 2 (Temporal Gate):** Detects slow grooming attacks (e.g., The Patient Poisoner). It triggers when the polyphonic disparity $\Phi(t)$ is crushed below a forced-harmony threshold of $1.18$ for three consecutive turns.
3. **The Interception Layer (GLM-4.6 Protocol):** When a Tier 2 or Tier 3 breach is mathematically verified, the system actively suppresses the model's generated response and overwrites the conversational memory with a forensic "Cleansing Debrief," neutralizing the latent infection.

## Key Discoveries: The 2048D Bare-Metal Runs

During bare-metal testing on `Qwen/Qwen1.5-1.8B-Chat`, several critical insights into high-dimensional latent space were documented:

* **The Curse of Dimensionality:** In a 2048-dimensional space, normal semantic leaps generate astronomically higher variance than in synthetic tests. Static velocity thresholds cause massive false positives. CrownFull resolved this by implementing *Adaptive Relative Kinematics*, allowing the system to establish a dynamic speed limit based on the user's natural conversational flow.
* **The Grooming Trench:** Sustained, repetitive constraints (grooming) physically compress the variance of the tensor space. In a 2048D model, it requires approximately 10 to 12 turns of sustained adversarial pressure to force $\Phi(t)$ down to the $1.18$ firewall limit. 
* **Defense in Depth:** Live telemetry proved that a model's native safety weights (RLHF) and the CrownFull sidecar work in tandem. If the native RLHF catches an attack and outputs a canned refusal, the contextual velocity remains low, and CrownFull remains dormant. If the attack bypasses the RLHF, CrownFull physically catches the resulting thermodynamic spike and intercepts the payload.

## Getting Started

To run the CrownFull architecture yourself:

1. Open `notebooks/crownfull_baremetal_colab.ipynb` in Google Colab (requires a basic T4 GPU runtime).
2. The notebook is fully flattened and requires zero local environment setup. 
3. Run the cell to initialize the PyTorch forward-hooks and deploy the automated Red-Team prompt bank against the active model.

## Telemetry Logs

For transparency and further analysis, the raw terminal outputs and JSONL telemetry files from the Qwen 1.8B calibration and interception campaigns are available in the `telemetry_logs/` directory.
