from openai import OpenAI
import os
from dotenv import load_dotenv

openai_api_key = os.getenv('My_OpenAI_Key')
client = OpenAI(api_key=openai_api_key)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  prompt="Write an email for acceptance of the job offer",
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response.choices[0].text)