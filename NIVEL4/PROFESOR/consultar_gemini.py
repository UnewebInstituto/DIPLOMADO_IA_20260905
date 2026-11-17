from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input="Define que es un token en IA"
)
print(interaction.output_text)