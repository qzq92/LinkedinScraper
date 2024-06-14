from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
import os
from typing import Tuple
from dotenv import load_dotenv
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agents import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary
# Update this to read from .env file if necessary
API_Key = os.getenv('OPENAI_API_KEY')

def get_summary_and_interesting_facts(name: str)-> Tuple[Summary, str, str, str]:
    """Function which scrapes information from linkedin profiles.

    Args:
        name (str): Name of person.

    Returns:
        Tuple[Summary, str, str, str]: Includes a LLM summary of the person based on input person name of interest, the corresponding profile_pic_url for frontend display, the person's occupation, country
    """
    # Get the linkedin lookup url with agentic call and scrape the information using nubela api
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)

    # Template for LLM to generate short summary and two interesting facts
    summary_template = """
        Given the Linkedin information {information} about a person from I want you to create:
        1. A short summary.
        2. Three interesting facts about them

        Use the information provided from Linkedin
        \n {format_instructions}
    """
    if linkedin_data:
        # Construct prompt template with summary template and defined input variable + the partial variable to indicate required formatting
        summary_prompt_template = PromptTemplate(
            input_variables=["information"],
            template=summary_template,
            partial_variables={"format_instructions": summary_parser.get_format_instructions()} # Format instruction for prompt templates into defined structured data. Since we have the value, declare as partial variable
        )

        # Defined LLM model using ChatOpenAI GPT3.5 with 0 creativity defined by temperature
        llm = ChatOpenAI(api_key=API_Key, temperature=0, model_name="gpt-3.5-turbo")

        # Chain the components via LCEL structure: prompt template > llm > summary parser and invoke with inputs to get summary
        chain = summary_prompt_template | llm | summary_parser
        res: Summary = chain.invoke(input ={"information": linkedin_data}) # input must match prompt template input variables

        # Retrieve other linkedin artefacts provided from Proxycurl API
        profile_pic_url = linkedin_data.get("profile_pic_url")
        occupation = linkedin_data.get("occupation")
        country = linkedin_data.get("country")

        if occupation == "":
            occupation = "Unknown"
        if country == "":
            country = "Unknown"
    # Case when invalid link is provided
    else:
        print("Unable to scrape linkedin data due to invalid link provided")
        res = None
        profile_pic_url = "https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png"
        occupation = "Undefined"
        country = "Undefined"
    
    return res, profile_pic_url, occupation, country
        
if __name__ == "__main__":
    load_dotenv()
    # Test with Donald Trump during debug
    get_summary_and_interesting_facts(name="Donald Trump")