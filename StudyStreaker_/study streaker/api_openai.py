import os
from openai import OpenAI # type: ignore
from dotenv import load_dotenv # type: ignore

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Generate AI response
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[{"role": "user", "content": "write a haiku about ai"}]
)

# Print the response
print(completion.choices[0].message)
