from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlmodel import Session
from app.auth.auth_bearer import JWTBearer
from app.crud.user import get_user_by_id, update_user, delete_user_by_object
from app.database import get_session
from app.helper.enums import RoleEnum
from app.schemas.user import UserUpdateRequest
from app.utils.current_user import get_current_user
from app.utils.password import verify_password, hash_password

router = APIRouter()

@router.get(path="/{user_id}", dependencies=[Depends(JWTBearer())])
def user_details(user_id: int, request: Request, session: Session = Depends(get_session)):

    current_user = get_current_user(request)

    # Admins can access any user
    if current_user.role != RoleEnum.admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this user profile."
        )

    user = get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put(path="/{user_id}", dependencies=[Depends(JWTBearer())])
def update_user_details(
    user_id: int,
    update_data: UserUpdateRequest,
    request: Request,
    session: Session = Depends(get_session)
):
    current_user = get_current_user(request)

    # Admins can update any user, others only their own profile
    if current_user.role != RoleEnum.admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this user profile."
        )

    user = get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Regular users can't update role
    if update_data.role is not None and current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can change user role."
        )

    # Handle password change
    if update_data.last_password or update_data.new_password or update_data.confirm_password:

        if not update_data.last_password or not update_data.new_password or not update_data.confirm_password:
            raise HTTPException(status_code=400, detail="All password fields must be provided.")

        if not verify_password(update_data.last_password, user.hashed_password):
            raise HTTPException(status_code=403, detail="Current password is incorrect.")

        user.hashed_password = hash_password(update_data.new_password)

    # Apply updates
    user_data = update_data.model_dump(exclude_unset=True, exclude={"last_password", "new_password", "confirm_password"})

    for key, value in user_data.items():
        setattr(user, key, value)

    update_user(session, user)

    return {
        "message": "User updated successfully",
        "data": user
    }


@router.delete(path="/{user_id}", dependencies=[Depends(JWTBearer(required_role=RoleEnum.admin))])
def delete_user(user_id: int, session: Session = Depends(get_session)
):

    user = get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Deleting user
    delete_user_by_object(session, user)

    return {"message": "User deleted successfully"}
