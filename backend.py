from dotenv import load_dotenv
import os 


load_dotenv()
print(os.environ["GROQ_API_KEY"])