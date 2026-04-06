from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from pydantic import BaseModel

class UserContext(BaseModel):
    role: str
    user_id: Optional[int] = None

async def get_current_user(x_user_role: Optional[str] = Header(None), x_user_id: Optional[int] = Header(None)) -> UserContext:
    if not x_user_role or x_user_role not in ['viewer', 'analyst', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-User-Role header"
        )
    return UserContext(role=x_user_role, user_id=x_user_id)

def require_role(required_role: str):
    def role_checker(current_user: UserContext = Depends(get_current_user)):
        role_order = {'viewer': 1, 'analyst': 2, 'admin': 3}
        if role_order[current_user.role] < role_order[required_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient role. Requires {required_role}, got {current_user.role}"
            )
        return current_user
    return role_checker

# Usage: @router.get(..., dependencies=[Depends(require_role('admin'))])
viewer_dep = Depends(require_role('viewer'))
analyst_dep = Depends(require_role('analyst'))
admin_dep = Depends(require_role('admin'))

