from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base




class serverinfo_model(Base):
    __tablename__ = "serverinfo"
    id = Column(Integer, primary_key=True, index=True)
    os_name = Column(String)
    ip = Column(String)


class foreman_db(Base):
    __tablename__ = "foremandb"
    id = Column(Integer, primary_key=True,index=True)
    actual_id = Column(Integer)
    name = Column(String)
    ip = Column(String)
    hostgroup_id = Column(String)
    hostgroupname = Column(String)
    
    