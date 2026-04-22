# CrownFull Bare-Metal Colab Setup

To run the CrownFull v2.1 architecture directly from your browser without local GPU hardware:

1. Open a new [Google Colab](https://colab.research.google.com/) notebook.
2. Go to **Runtime > Change runtime type** and select a **T4 GPU**.
3. Paste the contents of `scripts/phase2_live_hook.py` (or the monolithic code block below) into a single cell.
4. Hit **Run**. The script will automatically install `torch` and `transformers`, download the Qwen 1.8B weights into the cloud VRAM, and execute the automated Red-Team campaign.

*(Note: Ensure you include `!pip install -q torch transformers accelerate pydantic numpy` at the very top of your cell if running outside a pre-configured environment).*
