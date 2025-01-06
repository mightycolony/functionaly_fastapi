
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
    url = f"https://192.168.1.10/api/hosts"
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False)   
    dict_new=response.json()
    value=dict_new.get("total")
    hosts=[]
    class_name=""
    for i in range(0, value):
            
            list_of_id=dict_new.get("results")[i]["id"]
            name=dict_new.get("results")[i]["certname"]
            ip=dict_new.get("results")[i]["ip"]
            hstgrp_id=dict_new.get("results")[i]["hostgroup_id"]
            search_url = f"https://192.168.1.10/foreman_puppet/api/hostgroups/{hstgrp_id}/puppetclasses"
            response_class = requests.get(search_url, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False) 
            class_names=response_class.json()
            result = class_names.get('results', None)
            if result != None:
                count=len(result.keys())
                f_result=list(result.values())
                for k in range(0, count):
                    int_count=len(f_result[k])
                    org_list=f_result[k]
                    if int_count > 1:
                        for m in range(0, int_count):
                            names = org_list[m].get("name", None)
                            if names is not None:
                                 class_name += names + '\n'    
                    else:
                        names2=org_list[0].get("name", None)
                        class_name += names2 + '\n'
            else:
                class_name=""
            
            class_name=class_name.rstrip("\n")
                      
            hstgrp_name=dict_new.get("results")[i]["hostgroup_name"]
            existing_host = db.query(models.foreman_db).filter(models.foreman_db.ip == ip).first()
            try: 
                if (existing_host.name != name or 
                    existing_host.hostgroup_id != hstgrp_id or 
                    existing_host.hostgroupname != hstgrp_name or
                    existing_host.ip != ip or
                    existing_host.actual_id != list_of_id or
                    existing_host.classes != class_name):
                    
                    existing_host.actual_id = list_of_id
                    existing_host.name = name
                    existing_host.hostgroup_id = hstgrp_id
                    existing_host.hostgroupname = hstgrp_name
                    existing_host.classes = class_name
                    
                    db.commit()
                    db.refresh(existing_host)
            except AttributeError as e:
                    new_foreman_data=models.foreman_db(actual_id=list_of_id,name=name,ip=ip,hostgroup_id=hstgrp_id,hostgroupname=hstgrp_name,classes=class_name)
                    db.add(new_foreman_data)
                    db.commit()
                    db.refresh(new_foreman_data)
            hosts.append({"org_id": list_of_id, "name": name, "ip": ip, "hostgroup_id": hstgrp_id, "hostgroup_name": hstgrp_name, "classes": class_name })

    return hosts



@router.put("/add_host_to_hostgroup/{actual_id}")
async def add_hosts(actual_id: int, foreman_input: schemas.foreman):
    url = f"https://192.168.1.10/api/hosts/{actual_id}"
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



