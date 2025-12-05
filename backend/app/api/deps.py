from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.sessions import get_db

# HTTP Bearer token security scheme
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
  
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        uid = decoded_token["uid"]
        
        user = db.query(User).filter(User.uid == uid).first()
        
        # If user doesn't exist, create them
        if not user:
            # Extract email from Firebase token if available
            firebase_email = decoded_token.get("email")
            # Default role is 'student'
            user = User(
                uid=uid, 
                email=firebase_email,
                role="student"  # Default role
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        return user
        
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Catch any other errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user has admin role.
    
    Usage:
    ```python
    @router.get("/admin-only")
    def admin_endpoint(admin_user: User = Depends(get_current_admin)):
        return {"message": "Admin access granted"}
    ```
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin role required."
        )
    return current_user