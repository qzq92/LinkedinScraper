import os
import requests

def scrape_linkedin_profile(linkedin_profile_url: str) -> dict:
    """Function which scrapes information from linkedin profiles.

    Args:
        linkedin_profile_url (str): Provided linkedin profile url for scraping.

    Returns:
        dict: Empty dictionary if response status code is not 200. Otherwise will be the dictionary based on https://nubela.co/proxycurl/linkedin.
    """
    # Docs refer to: https://nubela.co/proxycurl/docs#proxycurl-overview-open-api-3-0
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dict = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
    response = requests.get(
        api_endpoint,
        params={"url": linkedin_profile_url, "use_cache": "if-recent", "fallback_to_cache": "on-error"},
        headers=header_dict,
        timeout=10)
    
    # Only status code 200 is ok
    if response.status_code == 200:
        data = response.json()

        # Remove empty or None value response for certain keys as well as people_also_viewed and certifications info
        data = {k: v for k,v in data.items() if v not in ([], "", None) and k not in ["people_also_viewed", "certifications"]}

        # Remove non-informative info.
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")
    else:
        print(f"Error: {response.status_code}")
        return {}
    return data


# Test case if run directly
if __name__ == "__main__":
    print(scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/eden-marco/"))