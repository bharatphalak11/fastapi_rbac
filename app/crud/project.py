from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.project import Project

def create_project(session: Session, project: Project):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def update_project(session: Session, project: Project):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

def get_projects(session: Session):
    return session.exec(select(Project)).all()

def get_project_by_id(session: Session, project_id: int) -> Project:
    project = session.exec(select(Project).where(Project.id == project_id)).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

def delete_project_by_object(session: Session, project: Project):
    session.delete(project)
    session.commit()
    return True