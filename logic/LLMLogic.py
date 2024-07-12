from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'))
api_key = os.environ.get('openai_api_key')


model_name = 'gpt-3.5-turbo' #gpt-3.5-turbo-ca会消耗比较低,但响应时间会很长

llm = ChatOpenAI(temperature=0, model_name=model_name,
                 openai_api_base="https://api.chatanywhere.tech/v1",
                 openai_api_key=api_key
                 )


def qa(docs,propmt_word):
    prompt = PromptTemplate(input_variables=['docs'],
                            template=f""""以下是一个文档列表
                     {{docs}}
                     根据这个文档列表，{propmt_word}.
                     Helpful Answer:""")

    chain = LLMChain(llm=llm,prompt=prompt)  # 比chain = load_summarize_chain(llm, chain_type='map_reduce')更快，消耗的token也基本一样，且只需要调用一次#与chain = load_summarize_chain(llm, chain_type='stuff')一致；自己创建prompt的好处就是可以自定义，推荐
    content = chain.invoke(docs)
    return content