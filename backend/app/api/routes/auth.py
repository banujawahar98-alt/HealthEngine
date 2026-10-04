"""
Authentication API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserRegisterRequest, UserLoginRequest, PasswordChangeRequest
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register")
async def register(req: UserRegisterRequest):
    try:
        data = await auth_service.register_user(
            name=req.name,
            email=req.email,
            password=req.password,
            confirm_password=req.confirm_password,
            age_range=req.age_range,
            role=req.role or "USER"
        )
        return {
            "success": True,
            "message": "Registration successful.",
            "data": data
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"success": False, "message": str(e), "error_code": "REGISTRATION_FAILED"})

@router.post("/login")
async def login(req: UserLoginRequest):
    try:
        data = await auth_service.authenticate_user(email=req.email, password=req.password)
        return {
            "success": True,
            "message": "Login successful.",
            "data": data
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail={"success": False, "message": str(e), "error_code": "INVALID_CREDENTIALS"})

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    return {
        "success": True,
        "message": "Logged out successfully.",
        "data": None
    }

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    user_data = {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"],
        "age_range": current_user.get("age_range"),
        "created_at": current_user.get("created_at", ""),
        "updated_at": current_user.get("updated_at")
    }
    return {
        "success": True,
        "message": "Current user loaded.",
        "data": user_data
    }

@router.put("/change-password")
async def change_password(req: PasswordChangeRequest, current_user: dict = Depends(get_current_user)):
    try:
        await auth_service.change_password(current_user["id"], req.current_password, req.new_password)
        return {
            "success": True,
            "message": "Password changed successfully.",
            "data": None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"success": False, "message": str(e), "error_code": "PASSWORD_CHANGE_FAILED"})

@router.delete("/account")
async def delete_account(current_user: dict = Depends(get_current_user)):
    await auth_service.delete_account(current_user["id"])
    return {
        "success": True,
        "message": "Account deleted successfully.",
        "data": None
    }
