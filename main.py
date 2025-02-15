import requests
import os
from fastapi import FastAPI, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

# FatSecret API credentials being loaded from .env file
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


app = FastAPI()

# Accessing the client IDs and receiving the access_token to use it in GET method.

def get_access_token():
    token_url = "https://oauth.fatsecret.com/connect/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": "premier",
    }
    response = requests.post(token_url, auth=(CLIENT_ID, CLIENT_SECRET), headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch access token")



@app.get("/search_food/")    
async def foods_search(Your_food: str ):
    try:
        
        access_token = get_access_token()
        
        
        url = "https://platform.fatsecret.com/rest/server.api"
        
        # Request headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            
        }
        
       # The params accessible in the basic version of fatsecret api are mentioned. All the rest params require premier
        params = {
             "method": "foods.search.v3",
            "search_expression": Your_food,
            "include_sub_categories": "true",
            "servings" :"true",
            "max_results": 30,
            "format": "json",
            
        }
        
       
        response = requests.get(url, headers=headers, params=params)
        
        
        response.raise_for_status()
        
        return response.json()
       
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching food data: {str(e)}"
        )

    




