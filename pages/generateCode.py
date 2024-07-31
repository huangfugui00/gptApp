import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from PIL import Image
from io import BytesIO
load_dotenv()
api_key = os.environ.get('openai_api_key')
api_key = 'sk-s1AuQVZizBNwJuTwMLwXgQ4OSLosHXdzq8Q5do1DdeHI7hyR'

MODEL ="gpt-4o-mini"

client = OpenAI( base_url="https://api.chatanywhere.tech/v1",
                 api_key=api_key,)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def show_code_image(content):
    idx = content.find('```')
    content = content[idx+3:]
    idx = content.find('```')
    content = content[:idx]
    content = content+"plt.savefig('new.png')"
    exec(content[6:])
    image = Image.open('new.png')
    st.image(image, caption='使用gpt代码生成的图片', use_column_width=True)


def main():
    st.header("📄生成图片绘制代码🤗")

    # upload a your pdf file
    img = st.file_uploader("Upload your image", type=['png','jpg','jpeg'])
    if img is not None:
        image = Image.open(img)
        st.image(image, caption='上传的图片', use_column_width=True)
        buffered = BytesIO()

        image.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue())
        base64_image = base64_image.decode("utf-8")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that responds in Markdown. Help me with my math homework!"},
                {"role": "user", "content": [
                    {"type": "text", "text": "生成绘制图片代码;代码为:{}"},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"}
                     }
                ]}
            ],
            temperature=0.0,
        )
        content = response.choices[0].message.content
        col1, col2 = st.columns(2)
        with col1:
            st.write(content)
        with col2:
            show_code_image(content)
main()