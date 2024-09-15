from fastapi import APIRouter, HTTPException
from fastapi import Request, Body
import uuid

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from models import NewEventModel


def url_generator():
    return str(uuid.uuid4())


router = APIRouter()


# @router.post("", response_description="Add new event")
# @router.post("/", response_description="Add new event")
# async def show_posted_json(request: Request, event: dict = Body(...)):
#     print("requested")
#     print(url_generator())
#     print(event)


# Form is only used in form-encoded data! use Body instead...
@router.post("", response_description="Add new event")
@router.post("/", response_description="Add new event")
async def create_new_event(request: Request,
                           eventName: str = Body("eventName"),
                           selectedDates: list = Body("selectedDates"),
                           timeUnit: str = Body("timeUnit"),
                            earliestTime: str = Body("earliestTime"),
                            latestTime: str = Body("latestTime")):
    url = url_generator() # uuid based


    new_event = NewEventModel(
        eventName=eventName,
        selectedDates=selectedDates,
        timeUnit=timeUnit,
        earliestTime=earliestTime,
        latestTime=latestTime,
        url=url
    )

    # new_event = new_event.model_dump()
    # print(new_event)

    new_event = jsonable_encoder(new_event)
    db_event = await request.app.mongodb['Events'].insert_one(new_event)
    created_event = await request.app.mongodb['Events'].find_one({"_id": db_event.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_event)


@router.get("/{event_url}", response_description="Get all events")
async def get_event(request: Request, event_url: str):
    # event = await request.app.mongodb['Events'].find_one({"url": event_url})

    if (event := await request.app.mongodb['Events'].find_one({"url": event_url})) is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=event)
    raise HTTPException(status_code=404, detail="Event not found")

    # if event is None:
    #     return HTTPException(status_code=404, detail="Event not found")
    # return JSONResponse(status_code=status.HTTP_200_OK, content=event)