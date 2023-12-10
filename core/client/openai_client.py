import openai

from core.config.secrets import OPEN_AI_API_KEY

client = openai.OpenAI(api_key=OPEN_AI_API_KEY)
image_url = "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2F739fefcb-5610-40a5-ac12-af2b5bb112cd.jpg" # 치맥
image_url2 = "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg" # 삼겹살+소주
image_url3 = "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg" # 회+소주

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "이 그림에서 보이는 술과 안주를 술:뭐, 안주:뭐로 알려줘. 보이지 않으면 X라고 알려줘"
                },
                {
                    "type": "image_url",
                    "image_url": image_url3
                }
            ]
        }
    ],
    max_tokens=1000
)

print(response.choices[0].message.content)
