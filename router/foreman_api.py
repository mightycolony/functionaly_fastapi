
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
    url = f"https://192.168.1.8/api/hosts"
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
            search_url = f"https://192.168.1.8/foreman_puppet/api/hostgroups/{hstgrp_id}/puppetclasses"
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
    url = f"https://192.168.1.8/api/hosts/{actual_id}"
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



# to find what hostgroup does a host has
@router.get("/list_host_for_a_hostgroup/{host}")
async def list_host_for_a_hostgroup(host: str):
    url = f"https://192.168.1.8/api/hosts?search={host}"
    response_hstgroup = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False) 
    if response_hstgroup.status_code == 200:
        x = response_hstgroup.json().get('results')[0]["hostgroup_name"]
        if x == None:
            return "No Hostgroup associated"
        else:
            return x
    else:
        return response_hstgroup.status_code


##list puppet class for a hostgroup_id
@router.get("/list_hostgroups/{hostgroupname}")
async def list_hostgroups(hostgroupname: str):
    print(hostgroupname)
    url_search=f"https://192.168.1.8/api/hostgroups?search=name={hostgroupname}"
    get_hostgroup_id = requests.get(url_search, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False) 
    if get_hostgroup_id.status_code == 200:
        hostgroup_id=get_hostgroup_id.json().get("results")[0]["id"]
    class_list=[]
    print(hostgroup_id)
    url=f"https://192.168.1.8/api/hostgroups/{hostgroup_id}"
    rsp_class = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False) 
    if rsp_class.status_code == 200: 
        for i in range(0, len(rsp_class.json()["all_puppetclasses"]) ):
            class_list.append(rsp_class.json()["all_puppetclasses"][i]["name"])
        print(type(class_list))
        return class_list
    
    
    

#get all class

@router.get("/list_classes")
async def list_classes():
    total_class=[]
    url=f"https://192.168.1.8/foreman_puppet/api/puppetclasses"
    get_classes = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False) 
    if get_classes.status_code == 200:
        results=get_classes.json().get("results")
        print(results)
        for key, value in results.items():
            if len(value) > 1:
                for i in range(0, len(value)):
                    final_class = {"value": value[i]["name"], "label": value[i]["name"]}
                    total_class.append(final_class)
                    
            else:
                final_class = {"value": value[0]["name"], "label": value[0]["name"]}
                total_class.append(final_class)

        return  total_class

#add class to a hst group
@router.get("/list_of_class")
async def list_of_class():
    id_list=[]
    
    url=f"https://192.168.1.8/foreman_puppet/api/puppetclasses"
    get_classes = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, api_token), verify=False) 
    result=get_classes.json().get("results")
    for key, value in result.items():
        if len(value) > 1:
            for i in range(0, len(value)):
                x = {value[i]["name"]: value[i]["id"]}
                id_list.append(x)
        else:
            x = {value[0]["name"]: value[0]["id"]}
            id_list.append(x)
    return id_list
            
            
    