import os
import requests
from PIL import Image
from io import BytesIO

# =============== 基本设置 ===============
api_key = os.getenv("ARK_API_KEY")
if not api_key:
    raise ValueError("Set the ARK_API_KEY environment variable before running.")
url = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# =============== Prompt ===============
prompt = (
    "Wide cinematic 16:9 illustration inspired by 'The Little Prince'. "
    "A small boy with golden hair, wearing a green coat and yellow scarf, sits on a tiny round planet "
    "at the bottom center of the frame, gazing toward a warm sunset sky in outer space. "
    "The background shows soft clouds of cosmic light, glowing stars and nebulae illuminated by the sunset. "
    "The light is gentle, warm and radiant — golden orange, rose pink and lilac tones fading gradually into soft twilight blue. "
    "The mood feels peaceful, wistful, and dreamy, like the last moment before nightfall. "
    "No other ground, no horizon line, only the small round planet beneath the boy. "
    "Soft watercolor brushstrokes, cinematic wide shot composition, painterly and picture-book aesthetic, "
    "no collage or multiple panels, consistent character design, open panoramic framing safe for 16:9 cropping."
)

# =============== 参数配置 ===============
data = {
    "model": "YOUR_ENDPOINT_ID",
    "prompt": prompt,
    "width": 2048,
    "height": 2048,
    "num_images": 1
}

# =============== 请求生成 ===============
resp = requests.post(url, json=data, headers=headers)
result = resp.json()
image_url = result["data"][0]["url"]
print("生成图片 URL:", image_url)

# =============== 下载与裁剪 ===============
img_data = requests.get(image_url).content
img = Image.open(BytesIO(img_data)).convert("RGBA")

target_w, target_h = 1920, 1080
w, h = img.size
target_ratio = target_w / target_h

if w / h >= target_ratio:
    new_h = h
    new_w = int(h * target_ratio)
else:
    new_w = w
    new_h = int(w / target_ratio)

left = (w - new_w) // 2
top = (h - new_h) // 2
top_offset = int(new_h * 0.10)  # 保留星球下方
top = max(0, top + top_offset)
if top + new_h > h:
    top = h - new_h
right = left + new_w
bottom = top + new_h

cropped = img.crop((left, top, right, bottom))
resized = cropped.resize((target_w, target_h), Image.LANCZOS)

os.makedirs("outputs", exist_ok=True)
out_path = os.path.join("outputs", "little_prince_sunset_frame.png")
resized.save(out_path)
print("✅ 已保存：", out_path)
