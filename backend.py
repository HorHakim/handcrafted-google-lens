from groq import Groq
from dotenv import load_dotenv
import os 


class LlmAgent:
	def __init__(self):
		load_dotenv()
		self.client = Groq(api_key=os.environ["GROQ_API_KEY"])


	@staticmethod
	def read_file(file_path):
		with open(file_path, "r") as file:
			return file.read()



	def ask_llm(self, user_interaction):

		chat_completion = self.client.chat.completions.create(
			messages=[
				{
					"role": "system",
					"content": LlmAgent.read_file(file_path="./context.txt")
				},
				{
					"role": "user",
					"content": user_interaction
				}
			],

			model="llama-3.3-70b-versatile"
		)

		return chat_completion.choices[0].message.content



if __name__ == "__main__":
	llm_agent_object = LlmAgent()


	user_interaction = input("Posez votre question :\n")
	
	llm_response = llm_agent_object.ask_llm(user_interaction)
	

	print("-"*20)
	print(llm_response)