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

# =============== 编辑 Prompt ===============
# 更精准地描述要去掉的部分，同时保留整体结构与柔光
prompt = (
    "Clean up the image by removing both tiny protruding lines at the upper end of the glowing pod. Keep the pod’s overall shape, lighting, and glow completely unchanged."
    "Carefully remove all unwanted lines without affecting any other details. "
    "Keep the seed's overall shape, glow, and lighting completely unchanged. "
    "Do not alter the background, color, or atmosphere — only remove those short tail-like lines smoothly."
)

# =============== 请求配置 ===============
data = {
    "model": "seededit-3-0-i2i-250628",
    "prompt": prompt,
    "image": "YOUR_IMAGE_URL",
    "response_format": "url",
    "size": "adaptive",
    "seed": 21,
    "guidance_scale": 6.0,
    "watermark": False
}

# =============== 调用 API ===============
response = requests.post(url, headers=headers, json=data)
result = response.json()
print("返回结果：", result)

# =============== 自动下载与保存 ===============
try:
    image_url = result["data"][0]["url"]
    img_data = requests.get(image_url).content
    img = Image.open(BytesIO(img_data))
    os.makedirs("outputs", exist_ok=True)
    out_path = os.path.join("outputs", "rose_seed_cleaned.png")
    img.save(out_path)
    print("✅ 已保存编辑后的图片：", out_path)
    print("图片URL：", image_url)
except Exception as e:
    print("❌ 下载或保存失败：", e)
