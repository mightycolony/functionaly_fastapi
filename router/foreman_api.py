
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

@router.get("/list_update_foreman_inv")
async def list_hosts(db: Session = Depends(get_db)):
    url = f"https://192.168.1.5/api/hosts"
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False)   
    dict_new=response.json()
    value=dict_new.get("total")
    hosts=[]
    for i in range(0, value):
            
            list_of_id=dict_new.get("results")[i]["id"]

            name=dict_new.get("results")[i]["certname"]
            ip=dict_new.get("results")[i]["ip"]
            hstgrp_id=dict_new.get("results")[i]["hostgroup_id"]
            search_url = f"https://192.168.1.5/foreman_puppet/api/hostgroups/{hstgrp_id}/puppetclasses"
            response_class = requests.get(search_url, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False) 
            class_names=response_class.json().get("results")
            # print(type(class_names))
            # print(class_names.values())
              
            hstgrp_name=dict_new.get("results")[i]["hostgroup_name"]
            

            existing_host = db.query(models.foreman_db).filter(models.foreman_db.ip == ip).first()
            try: 
                if (existing_host.name != name or 
                    existing_host.hostgroup_id != hstgrp_id or 
                    existing_host.hostgroupname != hstgrp_name or
                    existing_host.ip != ip or
                    existing_host.actual_id != list_of_id):
                    
                    existing_host.actual_id = list_of_id
                    existing_host.name = name
                    existing_host.hostgroup_id = hstgrp_id
                    existing_host.hostgroupname = hstgrp_name
                    db.commit()
                    db.refresh(existing_host)
            except AttributeError as e:
                    new_foreman_data=models.foreman_db(actual_id=list_of_id,name=name,ip=ip,hostgroup_id=hstgrp_id,hostgroupname=hstgrp_name)
                    db.add(new_foreman_data)
                    db.commit()
                    db.refresh(new_foreman_data)
            # hosts[list_of_id] = []
            # hosts[list_of_id].append({"name": name, "ip": ip, "hostgroup_id": hstgrp_id, "hostgroup_name": hstgrp_name })
            hosts.append({"org_id": list_of_id, "name": name, "ip": ip, "hostgroup_id": hstgrp_id, "hostgroup_name": hstgrp_name })

    return hosts



@router.put("/add_host_to_hostgroup/{actual_id}")
async def add_hosts(actual_id: int, foreman_input: schemas.foreman):
    url = f"https://192.168.1.5/api/hosts/{actual_id}"
    data = {
    "host": {
        "ip": "{}".format(foreman_input.ip),
        "hostgroup_id": "{}".format(foreman_input.hostgroup_id)
    }
    }
    response = requests.put(url, headers=headers, json=data, auth=HTTPBasicAuth(username, api_token), verify=False)   
    if response.status_code == 200:
        return "Success {}".format(response.status_code)
    else:
        return "{}".format(response)



