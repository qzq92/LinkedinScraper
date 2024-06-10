import os
import requests

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    """Function which scrapes information from linkedin profiles

    Args:
        linkedin_profile_url (str): _description_
        mock (bool, optional): _description_. Defaults to False.
    """

    # Fallback to mockup if mock is set to True
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"

        # Try requests and end if timeout after 10sec
        response = requests.get(linkedin_profile_url, timeout=10)
    
    else:
        # https://nubela.co/proxycurl/docs#proxycurl-overview-open-api-3-0
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dict = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url, "use_cache": "if-recent", "fallback_to_cache": "on-error"},
            headers=header_dict,
            timeout=10)
    if response.status_code == 200:
        data = response.json()

        # Remove empty or None value response for certain keys as well as people_also_viewed and certifications info
        data = {k: v for k,v in data.items() if v not in ([], "", None) and k not in ["people_also_viewed", "certifications"]}

        # Remove profile pic url in groups since it is not informative at all
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")
    else:
        print(f"Error: {response.status_code}")
        data = {}
    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/eden-marco/")
)