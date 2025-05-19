from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

import os

MODEL = os.getenv('MODEL', 'ollama2')

def prompt(user_prompt):

    # Initialize TinyLlama via Ollama
    llm = Ollama(model=MODEL)

    # Create a prompt
    prompt = PromptTemplate.from_template("You are an agent integrated into system to do specifed tasks for its users. ```{text}``` is a user prompt from API.")
    chain = LLMChain(prompt=prompt, llm=llm)

    # Run it
    result = chain.run(user_prompt)
    return result

