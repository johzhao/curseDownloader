import logging

from sqlalchemy import Column, Integer, String, Binary
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.exceptions import *

logger = logging.getLogger(__name__)

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    id_ = Column(Integer, autoincrement=True, primary_key=True)
    project_id = Column(String)
    project_url = Column(String)

    def __repr__(self):
        return '<Project(id: {}, project id: {}, url: {})>'.format(self.id_, self.project_id, self.project_url)


class Mod(Base):
    __tablename__ = 'mods'

    id_ = Column(Integer, autoincrement=True, primary_key=True)
    project_id = Column(String)
    file_id = Column(String)
    filename = Column(String)
    content = Column(Binary)

    def __repr__(self):
        return '<Mod(id: {}, project id: {}, file id: {}, filename: {})>'.format(self.id_, self.project_id,
                                                                                 self.file_id, self.filename)


class Database:

    def __init__(self):
        self.engine = create_engine('sqlite:///curse.db', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def exist(self, project_id: str, file_id: str) -> bool:
        session = self.Session()
        mod = session.query(Mod).filter_by(project_id=project_id, file_id=file_id).first()
        session.close()
        return mod is not None

    def get_project_url(self, project_id: str) -> str:
        session = self.Session()
        project = session.query(Project).filter_by(project_id=project_id).first()
        if project is None:
            raise ProjectNotFoundException(project_id)
        session.close()
        return project.project_url

    def set_project_url(self, project_id: str, project_url: str):
        session = self.Session()
        project = Project(project_id=project_id, project_url=project_url)
        session.add(project)
        session.commit()
        session.close()

    def get_data(self, project_id: str, file_id: str) -> (str, bytes):
        session = self.Session()
        mod = session.query(Mod).filter_by(project_id=project_id, file_id=file_id).first()
        if mod is None:
            raise ModNotFoundException(project_id, file_id)
        session.close()
        return mod.filename, mod.content

    def set_data(self, project_id: str, file_id: str, filename: str, data: bytes):
        session = self.Session()
        mod = Mod(project_id=project_id, file_id=file_id, filename=filename, content=data)
        session.add(mod)
        session.commit()
        session.close()
