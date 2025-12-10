from fastapi import BackgroundTasks
from src.api import app
from src.api.config import app_config
from src.api.v1.services.login_link import countdown_deleting_login_link


@app.get(
    app_config.REST_API_PREFIX + "/login_links/countdown/{id}",
    tags=["Login links"],
    response_model=dict,
)
async def login_links_countdown_route(id, background_tasks: BackgroundTasks) -> dict:
    """Starts countdown for deleting login link"""
    background_tasks.add_task(countdown_deleting_login_link, id)
    return {"message": "Countdown for deleting login link started!"}
