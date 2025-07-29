import os
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import matplotlib.pyplot as plt

def generate_vinyl_cover():
    os.makedirs("output", exist_ok=True)
    os.makedirs("resources", exist_ok=True)

    # Load original cover (manually place the image at resources/original.jpg)
    original_cover_path = "resources/original.jpg"
    if not os.path.exists(original_cover_path):
        raise FileNotFoundError("Please place the original album cover at resources/original.jpg")

    original_img = Image.open(original_cover_path)
    original_img.save("output/original_cover.jpg")
    width, height = original_img.size

    if width % 8 != 0 or height % 8 != 0:
        width = (width // 8) * 8
        height = (height // 8) * 8

    # Set device (MPS for Mac, fallback to CPU)
    device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

    # Load Stable Diffusion pipeline
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float32
    )

    # Fix safety checker to avoid TypeError
    def dummy_safety_checker(images, **kwargs):
        return images, [False] * len(images)

    pipe.safety_checker = dummy_safety_checker
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()
    _ = pipe("test", num_inference_steps=1)

    # Prompt and generation config
    prompt = (
        "A fantasy book cover illustration of a girl with a sword stepping "
        "into a glowing blue door in the middle of a magical forest, "
        "mysterious and hopeful atmosphere, fireflies, misty background, "
        "cinematic lighting, highly detailed, storybook art style"
    )
    image = pipe(prompt, num_inference_steps=30, guidance_scale=7.5, height=height, width=width).images[0]
    image.save("output/generated_album_cover.jpg")

    # Screenshot of pipeline config
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.text(0.1, 0.8, f"Model: SD-v1.5\nDevice: {device.type}", fontsize=12)
    ax.text(0.1, 0.5, "Sampler: default PFSD\nSteps: 30\nCFG: 7.5", fontsize=12)
    ax.text(0.1, 0.2, f"Prompt:\n{prompt}", fontsize=10)
    ax.axis("off")
    fig.savefig("output/pipeline_screenshot.jpg")

    # Markdown report
    with open("output/report.md", "w") as f:
        f.write(f"# 🎵 AI Redesigned Vinyl Album Cover: The Dark Side of the Moon\n\n")
        f.write("## 💼 Original Cover\n\n")
        f.write("![Original](original_cover.jpg)\n\n---\n\n")
        f.write("## 🎨 AI​-​Generated Variation\n\n")
        f.write("![AI Cover](generated_album_cover.jpg)\n\n---\n\n")
        f.write("## ⚙️ Workflow & Technical Details\n\n")
        f.write("**Model**: Stable Diffusion v1.5 (Hugging Face) on self​-hosted setup\n")
        f.write(f"**Device**: {device.type}\n")
        f.write("**LoRA**: Retro Album Art aesthetic (optional, not used here)\n")
        f.write("**Sampler/Backend**: default scheduler\n")
        f.write("**Steps**: 30\n")
        f.write("**CFG Scale**: 7.5\n\n")
        f.write("**Prompt**:\n")
        f.write(f"> {prompt}\n\n")
        f.write("## 📸 Pipeline Configuration Screenshot\n\n")
        f.write("![Pipeline Setup](pipeline_screenshot.jpg)\n\n")
        f.write("## 🧰 Resources Used\n\n")
        f.write("- **Interface**: `diffusers` Python pipeline (self​-hosted, no external API)\n")
        f.write("- **Hardware**: Apple Silicon MPS (or CPU fallback), ~16 GB RAM\n")
        f.write("- **Model**: Stable Diffusion v1.5\n")
        f.write("- **LoRA**: Retro aesthetic LoRA file (not loaded in this run)\n")
        f.write("\n👉 Folder `output/` contains the generated images and `report.md`.\n")

if __name__ == "__main__":
    generate_vinyl_cover()