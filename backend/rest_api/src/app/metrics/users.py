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
    Увеличивает счетчик действия.
    """
    USER_ACTIONS.labels(action_type=action_type).inc()


def metric_user_track_action_duration(action_type: str, duration: float):
    """
    Фиксирует длительность выполнения действия.
    """
    USER_ACTION_DURATION.labels(action_type=action_type).observe(duration)
