from google import genai

def gen_lighting_prompt():
    input_caption_prompt = (
        "Please generate a short and descriptive prompt for lighting to change light in a given image using a text-to-image generative models."
        "The prompt should be short and precise, in one-line format, and does not exceed 77 tokens."
    )
    caption_model = genai.Client(
        api_key="AIzaSyAy9_fdp2beH_ylVDtejfnhgHTEDg0ya6s"
    )
    prompt = caption_model.models.generate_content(
        model='gemini-1.5-flash', contents=[input_caption_prompt]).text
    return prompt

