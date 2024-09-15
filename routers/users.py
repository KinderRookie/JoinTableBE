from fastapi import APIRouter, HTTPException
from fastapi import Request, Body
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse



router = APIRouter()

@router.get("/{id}", response_description="Get User by ID")
async def get_user_by_id(request: Request, id: str):
    user = await request.app.mongodb['users'].find_one({"_id": id})
    if user:
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")
