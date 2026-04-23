import base64
from openai import OpenAI
import os
with open("apikey.txt","r") as f:
    api_key=f.read().strip() 
client = OpenAI(api_key=api_key)
def chat_send_promt_with_image(STANDARD_PROMT, PHOTO_PATH):
        # leser bildefil og enkoder til base64
    with open(PHOTO_PATH, "rb") as f: #leser en fil som heter "trash.jpg"
        image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    print("image decoded")
    response = client.responses.create(
        model="gpt-4.1-mini",  # modell som klarer å lese bilder
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": STANDARD_PROMT},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}",
                    },
                ],
            }
        ],
    )

    return response.output_text
