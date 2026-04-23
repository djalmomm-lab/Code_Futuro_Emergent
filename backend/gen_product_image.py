"""Generate CodeFuturo Pro product image for Stripe checkout."""
import asyncio
import os
import base64
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()

PROMPT = (
    "Clean professional product image for an online coding learning platform. "
    "Dark deep-navy background (#0A0F1E) with subtle tech grid pattern. "
    "Center: a friendly modern robot mascot in lime-green accents (#A3E635), "
    "wearing a subtle golden crown indicating PRO tier. "
    "Mascot is cube-headed with glowing lime eyes, smiling. "
    "Floating around the robot: small geometric icons representing code (</>, "
    "Python logo, JavaScript braces, hexagonal lesson nodes). "
    "At the top, stylized text 'CodeFuturo PRO' in bold modern sans-serif, "
    "lime-green color, clean and readable. "
    "Subtitle below: 'Do zero ao deploy' smaller, muted text. "
    "Soft green glow radiating from the mascot. "
    "Square 1:1 aspect ratio, polished marketing style, high contrast, "
    "premium feel, no clutter. The image must look professional for a paid product "
    "on Stripe checkout."
)


async def main():
    api_key = os.getenv("EMERGENT_LLM_KEY")
    chat = LlmChat(
        api_key=api_key,
        session_id="cf-pro-product-image",
        system_message="You generate polished product/marketing images for tech brands.",
    )
    chat.with_model("gemini", "gemini-3.1-flash-image-preview").with_params(modalities=["image", "text"])

    text, images = await chat.send_message_multimodal_response(UserMessage(text=PROMPT))
    print(f"Text response (truncated): {text[:200] if text else ''}")
    if not images:
        print("No images returned")
        return
    for i, img in enumerate(images):
        out = f"/app/codefuturo_pro_{i}.png"
        with open(out, "wb") as f:
            f.write(base64.b64decode(img["data"]))
        print(f"Saved: {out}  ({img['mime_type']})")


if __name__ == "__main__":
    asyncio.run(main())
