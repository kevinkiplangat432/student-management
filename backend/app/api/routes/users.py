
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserRead, UserCreate  
from app.db.sessions import get_db
from app.api.deps import get_current_admin, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/public-test")
def public_test():
    return{"message": "This is a public endpoint"}

# create user - admin only
@router.post("/", response_model = UserRead)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    #create a new user. admin only
    existing_user = db.query(User).filter(User.uid == user.uid).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="UID already registered")
    new_user = User(uid=user.uid, role=user.role)  
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# get all users - admin only
@router.get("/", response_model=list[UserRead])
def get_all_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    # all users admin only
    return db.query(User).all()

# get a specific user- admin or the user themselves
@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # authentication required
):
    # get user by id ...here users can see them selvels  and admins can see everyone
    user = db.query(user). filter(User.id == user_id).first()
    
    #check permision
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to view this user"
        )
    
    return user

# Update user - Admin or self
@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, 
    updated_user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← Authentication required
):
    # update a user ..users can update themselves but admins can update anyone
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check permissions
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to update this user"
        )
    
    # Check if UID is being changed to an existing UID
    if updated_user.uid != user.uid:
        existing = db.query(User).filter(User.uid == updated_user.uid).first()
        if existing:
            raise HTTPException(status_code=400, detail="UID already in use")
    
    user.uid = updated_user.uid
    user.role = updated_user.role
    db.commit()
    db.refresh(user)
    return user

# DELETE USER - Admin only (users shouldn't delete themselves)
@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)  # ← Admin protection
):
    # onlyt admins can do this
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.uid == user.uid).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="UID already registered")
    
    new_user = User(uid=user.uid, role=user.role)  
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if uid is beign changed to an existing uid
    if updated_user.uid != user.uid:
        existing = db.query(User).filter(User.uid == updated_user.uid).first()
        if existing:
            raise HTTPException(status_code=400, detail="UID already in use")
    
    user.uid = updated_user.uid
    user.role = updated_user.role
    db.commit()
    db.refresh(user)
    return user

@router.get("/", response_model=list[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.uid = updated_user.uid
    user.role = updated_user.role
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
