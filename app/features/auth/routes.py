from fastapi import APIRouter, HTTPException
from app.features.auth.models import UserInManual, UserInOAuth, LoginRequest, TokenOut
from app.features.auth.service import signup_manual, login_manual, login_or_register_oauth,InvalidCredentialsError, NotVerifiedError
 

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=dict)
async def signup(user: UserInManual):
    try:
        await signup_manual(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"msg": "User created"}

@router.post("/login", response_model=TokenOut)
async def login(data: LoginRequest):
    try:
        token = await login_manual(data.email, data.password)
        return {"token": token}
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except NotVerifiedError:
        raise HTTPException(status_code=403, detail="Email not verified")

@router.post("/oauth", response_model=TokenOut)
async def oauth_login(user: UserInOAuth):
    token = await login_or_register_oauth(user)
    return {"token": token}
