
from fastapi import APIRouter,Depends,status,HTTPException,Request
import schemas
from database import SessionLocal,engine
from sqlalchemy.orm import Session
import models
import inspect
import importlib
router = APIRouter(
    tags=['Servers'],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


###FUNCTION GETTER######
import os
import importlib.util
import inspect
# from mainfunctionality.functionality import ssh_connection

path=os.getcwd() + "/mainfunctionality/kernelspace_scripts/kernel_functions.py"
file_name = path.split('/')[-1].replace('.py','')
print(file_name)
spec = importlib.util.spec_from_file_location(file_name, path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)




@router.get("/kernelspace_list")
def kernelspace_list():
    functions_dict={}
    count=0
    for name, obj in inspect.getmembers(mod):
            if inspect.isfunction(obj):
                count+=1
                curr_dict={"function_name": f"{name}", "function_content": f"{inspect.getsource(obj)}" }
                functions_dict[name] = curr_dict

    return functions_dict

@router.post("/execute_action")
async def execute_action(request: Request):
    body = await request.json()
    function = body.get("function")
    ip_os_details = body.get("ip_os_details")
    print(function,ip_os_details)
    return "value found!!"
