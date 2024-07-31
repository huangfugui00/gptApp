from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma,VectorStore
from langchain.chains import RetrievalQA
#import chromadb

load_dotenv(find_dotenv('.env'))
api_key = os.environ.get('openai_api_key')
api_key = 'sk-s1AuQVZizBNwJuTwMLwXgQ4OSLosHXdzq8Q5do1DdeHI7hyR'

model_name = 'gpt-4o-mini' #首选gpt-4o-mini

llm = ChatOpenAI(temperature=0, model_name = model_name,
                 openai_api_base="https://api.chatanywhere.tech/v1",
                 openai_api_key= api_key,
                 )

embeddings = OpenAIEmbeddings(openai_api_key=api_key,openai_api_base="https://api.chatanywhere.tech/v1")

#chroma_client = chromadb.Client()


def doc_to_vecstore(filename:str,docs):
    def __to_valid_collect_name(filename:str):
        filename = filename.replace(" ","")
        filename = filename.replace(".","")
        if len(filename)>60:
            filename = filename[:60]
        filename[0]
        return filename

    collection_name=__to_valid_collect_name(filename)
    return Chroma.from_documents(docs,  embedding=embeddings,collection_name= collection_name)
#
# def doc_to_vecstore(filename,docs):
#     collection = chroma_client.get_or_create_collection(filename)
#     embed_list = embeddings.embed_documents(docs)
#     collection.add(documents=docs,ids=['id{}'.format(i) for i in range(len(docs))],embeddings=embed_list)
#     #return Chroma.from_documents(docs,embedding=embeddings)
#     return collection


def qa_web(propmt_word):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一名强大的文本生成机器人."),
        ("user", "{input}")
    ])

    chain = prompt | llm

    content = chain.invoke({"input": propmt_word}).content
    return content


def qa_sources_db(db:VectorStore,question):
    retriever = db.as_retriever()
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                        input_key="question")
    response = chain({"question": question})
    return response['result']


def qa_sources(docs,propmt_word):
    prompt = PromptTemplate(input_variables=['docs'],
                            template=f""""以下是一个文档列表
                     {{docs}}
                     根据这个文档列表，{propmt_word}.
                     Helpful Answer:""")

    chain = LLMChain(llm=llm,prompt=prompt)  # 比chain = load_summarize_chain(llm, chain_type='map_reduce')更快，消耗的token也基本一样，且只需要调用一次#与chain = load_summarize_chain(llm, chain_type='stuff')一致；自己创建prompt的好处就是可以自定义，推荐
    content = chain.invoke(docs)
    content = content['text']
    return content