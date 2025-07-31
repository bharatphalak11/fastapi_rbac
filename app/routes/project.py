from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.helper.enums import RoleEnum
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.crud.project import create_project, get_projects, get_project_by_id, update_project, delete_project_by_object
from app.auth.auth_bearer import JWTBearer
from app.database import get_session

router = APIRouter()

@router.get(path="/", dependencies=[Depends(JWTBearer())])
def list_projects(session: Session = Depends(get_session)):
    return get_projects(session)


@router.post(path="/", dependencies=[Depends(JWTBearer(required_role=RoleEnum.admin))])
def add_project(data: ProjectCreate, session: Session = Depends(get_session)):
    project = Project(name=data.name, description=data.description)
    return create_project(session, project)


@router.get(path="/{project_id}", dependencies=[Depends(JWTBearer())])
def get_project_details(project_id: int, session: Session = Depends(get_session)):
    return get_project_by_id(session, project_id)


@router.put(path="/{project_id}", dependencies=[Depends(JWTBearer(required_role=RoleEnum.admin))])
def update_project_details(project_id: int, updated_data: ProjectUpdate, session: Session = Depends(get_session)):
    project = get_project_by_id(session, project_id)

    # Updating changes
    project.name = updated_data.name or project.name
    project.description = updated_data.description or project.description

    project = update_project(session, project)

    return {
        "message": "Project updated successfully",
        "data": project
    }


@router.delete("/{project_id}", dependencies=[Depends(JWTBearer(required_role=RoleEnum.admin))])
def delete_project(project_id: int, session: Session = Depends(get_session)
):
    project = get_project_by_id(session, project_id)

    # Deleting project
    delete_project_by_object(session, project)

    return {"message": f"Project {project_id} deleted successfully"}