"""
Authentication Service
"""
from typing import Dict, Any, Optional
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def register_user(self, name: str, email: str, password: str, confirm_password: str, age_range: Optional[str] = None, role: str = "USER") -> Dict[str, Any]:
        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("An account with this email address already exists.")

        hashed_pwd = hash_password(password)
        user_doc = {
            "name": name,
            "email": email,
            "password_hash": hashed_pwd,
            "role": role if role in ["USER", "PROFESSIONAL", "ADMIN"] else "USER",
            "age_range": age_range
        }
        created = await self.user_repo.create_user(user_doc)
        token = create_access_token({"sub": created["_id"], "email": created["email"], "role": created["role"]})
        
        user_response = {
            "id": created["_id"],
            "name": created["name"],
            "email": created["email"],
            "role": created["role"],
            "age_range": created.get("age_range"),
            "created_at": created["created_at"],
            "updated_at": created.get("updated_at")
        }
        return {"access_token": token, "token_type": "bearer", "user": user_response}

    async def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.get("password_hash", "")):
            raise ValueError("Invalid email address or password.")

        token = create_access_token({"sub": str(user["_id"]), "email": user["email"], "role": user["role"]})
        user_response = {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "age_range": user.get("age_range"),
            "created_at": user.get("created_at", ""),
            "updated_at": user.get("updated_at")
        }
        return {"access_token": token, "token_type": "bearer", "user": user_response}

    async def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not verify_password(current_password, user.get("password_hash", "")):
            raise ValueError("Incorrect current password.")

        new_hash = hash_password(new_password)
        return await self.user_repo.update_user(user_id, {"password_hash": new_hash})

    async def delete_account(self, user_id: str) -> bool:
        return await self.user_repo.delete_user(user_id)
