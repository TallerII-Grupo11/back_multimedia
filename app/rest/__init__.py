from fastapi import Depends
from app.conf.config import Settings, get_settings
from app.rest.metric_client import MetricClient


def get_restclient_metrics(settings: Settings = Depends(get_settings)) -> MetricClient:
    return MetricClient(settings.metrics_api)
