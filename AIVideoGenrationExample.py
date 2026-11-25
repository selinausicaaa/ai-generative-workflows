import os
import requests
import time

# 1️⃣ Ark API Key
api_key = os.getenv("ARK_API_KEY")
if not api_key:
    raise ValueError("Set the ARK_API_KEY environment variable before running.")

# 2️⃣ 首尾帧 URL
first_frame_url = "YOUR_FIRST_FRAME_IMAGE_URL"
last_frame_url = "YOUR_LAST_FRAME_IMAGE_URL"

# 3️⃣ Seedance Lite i2v 模型 ID
model_id = "YOUR_ENDPOINT_ID"

# 4️⃣ 文本描述
text_prompt = (
    "The Little Prince sits on his tiny planet, watching the sun slowly set,"
    "wearing a green coat and a single yellow scarf, gently draped over one shoulder, fluttering lightly in the wind"
    "The warm orange and pink sunset light softly illuminates his golden hair and green coat,"
    "creating gentle highlights on the small planet's surface."
    "As the sky gradually darkens, sparkling stars and a faint galaxy appear in the background."
    "Wide cinematic shot, dreamy watercolor illustration style, soft light, magical and whimsical atmosphere,"
    "smooth and natural transition from sunset to deep night sky, picture book quality, highly detailed,"
    "consistent character design, 16:9 composition, cinematic storytelling tone. "
    "transition to a sparkling night sky. --rs 720p --dur 10 --cf false --wide --fps 25"
)

# 5️⃣ 请求体
data = {
    "model": model_id,
    "content": [
        {"type": "text", "text": text_prompt},
        {"type": "image_url", "image_url": {"url": first_frame_url}, "role": "first_frame"},
        {"type": "image_url", "image_url": {"url": last_frame_url}, "role": "last_frame"}
    ]
}

# 6️⃣ 发送 POST 请求创建视频生成任务
url = "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)
if response.status_code != 200:
    print(f"⚠️ 请求失败: {response.status_code} {response.text}")
    exit()

task_info = response.json()
task_id = task_info.get("id")
if not task_id:
    print("⚠️ 未返回任务 ID:", task_info)
    exit()

print("✅ 视频生成任务已创建，任务 ID:", task_id)

# 7️⃣ 轮询任务状态直到完成
status_url = f"{url}/{task_id}"
while True:
    status_response = requests.get(status_url, headers=headers)
    status_data = status_response.json()
    task_status = status_data.get("status")
    
    if task_status == "succeeded":
        video_url = status_data.get("content", {}).get("video_url")
        if video_url:
            print("✅ 视频生成完成:", video_url)
            # 下载视频
            video_data = requests.get(video_url).content
            output_path = os.path.join("outputs", "little_prince_animation.mp4")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(video_data)
            print(f"🎬 视频已保存为 {output_path}")
        else:
            print("⚠️ 视频 URL 未找到，请检查返回数据:", status_data)
        break
    elif task_status in ["failed", "error"]:
        print("⚠️ 视频生成失败:", status_data)
        break
    else:
        print(f"⏳ 当前状态: {task_status}, 5 秒后继续检查...")
        time.sleep(5)
