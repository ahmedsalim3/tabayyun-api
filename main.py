import os
import requests
import json
import argparse
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tabayyun Business API')
    parser.add_argument('website', nargs='?', help='Website to inquire about')
    parser.add_argument('--output', '-o', default='results', help='default: results')
    
    args = parser.parse_args()
    
    website = args.website if args.website else input("Enter website: ")
    api_key = os.getenv('API_KEY')
    
    assert api_key, "API key not found in .env file"
    
    url = f'https://business.tabayyun.com.sa/business-api/v1/inquiry?inquiry={website}'
    headers = {'X-Authorization': api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        
        output = args.output
        os.makedirs(output, exist_ok=True)
        filename = f'{output}/{website.replace("://", "_").replace("/", "_").replace(".", "_")}.json'
        
        with open(filename, 'w') as f:
            json.dump({
                'status_code': response.status_code,
                'website': website,
                'response': data
            }, f, indent=2)
        
        print(f"Response saved to {filename}")
        # print(f"Data: {data}")
        
    except Exception as e:
        print(f"Error: {e}")