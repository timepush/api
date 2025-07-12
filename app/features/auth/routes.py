from fastapi import APIRouter, HTTPException, Response, Request
from app.features.auth.models import UserInManual, UserInOAuth, LoginRequest, TokenOut, RefreshRequest
from app.features.auth.service import signup_manual, login_manual, login_or_register_oauth, refresh_access_token, InvalidCredentialsError, NotVerifiedError
 

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=dict)
async def signup(user: UserInManual):
    try:
        await signup_manual(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"msg": "User created"}

@router.post("/login", response_model=TokenOut)
async def login(data: LoginRequest, response: Response):
    try:
        token, refresh_token = await login_manual(data.email, data.password)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60*60*24*7  # 7 days
        )
        return {"token": token}
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except NotVerifiedError:
        raise HTTPException(status_code=403, detail="Email not verified")

@router.post("/oauth", response_model=TokenOut)
async def oauth_login(user: UserInOAuth, response: Response):
    token, refresh_token = await login_or_register_oauth(user)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60*60*24*7
    )
    return {"token": token}

@router.post("/refresh", response_model=TokenOut)
async def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    try:
        token = await refresh_access_token(refresh_token)
        return {"token": token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
