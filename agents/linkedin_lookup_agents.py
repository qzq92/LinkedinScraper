import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
# Hub containing many prompts
from langchain import hub

from tools.tools import get_profile_url_via_tavily

#Load env
load_dotenv()

# Update this to read from .env file if necessary
API_Key = os.getenv('OPENAI_API_KEY')

def lookup(name: str) -> str:
    """Function wich performs linkedin url lookup using Langchain ReaAct agent 
    """
    # LLM needed
    llm = ChatOpenAI(
        api_key = API_Key,
        temperature = 0,
        model_name = "gpt-3.5-turbo",
    )

    #Note: Sometimes results obtained may not be what you want due to same names adopted by different person. Sometimes results obtained may deviate from what is required which means more precise prompting is required.
    template = """Given a person's full name {name_of_person}, I want you to get me the link to their Linkedin profile page related to https://www.linkedin.com. Your answer should be URL link that is contains a starting string of https://www.linkedin.com/in
    """

    # Define prompt template with input variables
    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name_of_person"]
    )
    # List of tools
    tools_for_agent = [
        Tool(
            name = "Crawl Google for Linkedin profile page", # identifier of tool
            func = get_profile_url_via_tavily, # Function to run
            description="Useful when you need to get Linkedin profile page URL of a person" # LLM will use description to determine whether to need tool or not
        )
    ]

    # Prompt by harison chase, serving as reasoning engine for agent.
    react_prompt = hub.pull("hwchase17/react")

    # Create agent as recipe with react prompt to reason and act based on outputs obtained from tools used.
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )

    # Orchestrator for agent
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True
    )

    # Invoke inputs with function parameter into executor input
    result = agent_executor.invoke(
        input = {"input": prompt_template.format_prompt(name_of_person= name)}
    )

    # Extract and return the result's output key
    linkedin_profile_url = result["output"]
    return linkedin_profile_url

if __name__ == "__main__":
    # Testing purpose.
    linkedin_url = lookup(name="Hillary Clinton")
    print(linkedin_url)