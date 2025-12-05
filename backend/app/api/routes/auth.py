from fastapi import APIRouter, Depends, HTTPException # api router from Fastapi
from app.api.deps import get_current_user, get_current_admin
from app.schemas.user import UserRead
from app.db.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/admin-test")
async def admin_test_endpoint(
    admin_user: User = Depends(get_current_admin)
):
    #  admin users only
    return {
        "message": "Admin access granted",
        "user": {
            "id": admin_user.id,
            "uid": admin_user.uid,
            "role": admin_user.role
        }
    }



@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
   # get current authenticated user info
    return current_user


@router.get("/status")
def auth_status():
    # check if auth is running.
    # no authentication needed
    return {"auth":"ready", "firebase":"intergrated"}




#study:
# apirouter allows me to group related endpoints together.