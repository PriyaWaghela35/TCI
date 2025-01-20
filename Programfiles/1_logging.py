import requests
import json
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Log all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('app.log', mode='w', encoding='utf-8')  # Log to a file
    ]
)

# Set the URL and headers
url = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=AGM%2FEGM&strPrevDate=20241017&strScrip=540005&strSearch=P&strToDate=20250117&strType=C&subcategory=AGM"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9",
    "Connection": "keep-alive",
    "Dnt": "1",
    "Host": "api.bseindia.com",
    "Referer": "https://www.bseindia.com/",
    "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
}

# Send a GET request
logging.info(f"Sending GET request to: {url}")
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    logging.info("Request successful. Status Code: 200")
    try:
        preview_data = response.json()  # Extract the JSON data
        logging.debug("Response JSON data successfully parsed.")
        
        # Log the data preview (only a portion, to avoid large output)
        logging.debug(f"Preview Data: {json.dumps(preview_data, indent=4)[:500]}...")  # First 500 chars

        # Save the Preview data to a file
        with open("preview_output.json", "w", encoding="utf-8") as file:
            json.dump(preview_data, file, indent=4, ensure_ascii=False)
        
        logging.info("Preview data has been saved to 'preview_output.json'")

    except json.JSONDecodeError:
        logging.error("Error: The response is not in JSON format.")
else:
    logging.error(f"Failed to fetch data. Status Code: {response.status_code}")
