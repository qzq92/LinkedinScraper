from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
import os

from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    print("Hello LangChain!")
    
    f = open('openai_key.txt')
    api_key = f.read()

    # Template for LLM
    summary_template = """
        Given the Linkedin information {information} about a person from I want you to create:
        1. A short summary.
        2. Two interesting facts about them
    """


    # Construct template and llm into chain
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    # LLM model with 0 creativity defined by temperature
    llm = ChatOpenAI(api_key=api_key, temperature=0, model_name="gpt-3.5-turbo")

    # Chain summary prompt to LLM
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # Invoke chain with scraped data
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/eden-marco/")

    res = chain.invoke(input ={"information": linkedin_data})
    print(res.content)