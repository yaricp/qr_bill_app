from loguru import logger
from prometheus_client import Counter, Histogram


# login, scan_receipt, open_analytics, change_language
USER_ACTIONS = Counter(
    "qracun_user_actions_total",
    "Total number of user actions",
    ["action_type"]
)

USER_ACTION_DURATION = Histogram(
    "qracun_user_action_duration_seconds",
    "Time spent on user actions in seconds",
    ["action_type"]
)


def metric_user_track_action(action_type: str):
    """
    Increments the counter for a specific user action.
    """
    USER_ACTIONS.labels(action_type=action_type).inc()
    logger.debug(f"User action tracked: {action_type}")


def metric_user_track_action_duration(action_type: str, duration: float):
    """
    Fixed: Records the duration of a specific user action.
    """
    USER_ACTION_DURATION.labels(action_type=action_type).observe(duration)
