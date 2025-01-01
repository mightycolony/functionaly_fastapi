
from fastapi import APIRouter,Depends,status,HTTPException
import schemas
from database import SessionLocal,engine
from sqlalchemy.orm import Session
import models
import requests
from requests.auth import HTTPBasicAuth

router = APIRouter(
    tags=['Foreman'],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
api_token="527wosiBsgkCwuG4IcHNXw"
username="admin"
headers = {
        "Content-Type": "application/json"
    }

@router.post("/list_hostgroups")
async def list_hostgroups():
        url = f"https://192.168.1.5/api/hostgroups"
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False)   
        hostgroups = {"groups": []}
        dict_new=response.json()
        value=dict_new.get("total")
        for i in range(0, value):
            hostgroups["groups"].append(dict_new.get("results")[i]["name"])
        return "hostgroup for {}".format(hostgroups)

@router.post("/list_hosts")
async def list_hosts():
    url = f"https://192.168.1.5/api/hosts"
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False)   
    return "list of IP in foreman {}".format(response)


@router.post("/add_host")
async def add_hosts():
    pass

@router.post("/add_hostgrou")
async def add_hostgroup():
    pass


@router.post("/add_hostgroup_to_host")
async def add_hostgroup_to_host():
    pass
