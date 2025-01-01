from pydantic import BaseModel

class server_info_schema(BaseModel):
    os_name: str
    ip: str

class reponse_server_info(BaseModel):
       id: int
       os_name: str
       ip: str
       
class server_ip_delete(BaseModel):
       id: int

class foreman(BaseModel):
       hostgroup: str