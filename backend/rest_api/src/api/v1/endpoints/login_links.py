# from uuid import UUID
# from typing import List, MutableSequence

from fastapi import BackgroundTasks

from ... import app
from ...config import URLPathsConfig

from ..services.login_link import countdown_deleting_login_link


@app.get(
    URLPathsConfig.PREFIX + "/login_links/countdown/{id}",
    tags=['Login links'],
    response_model=bool
)
async def login_links_countdown_route(
    id, background_tasks: BackgroundTasks
) -> bool:
    background_tasks.add_task(countdown_deleting_login_link, id)
    return {"message": "Start countdown for deleting login link"}
