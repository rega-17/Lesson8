import pytest
import requests
import os
from datetime import datetime


def pytest_configure(config):
    """Конфигурация pytest при запуске"""
    config.option.htmlpath = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    os.makedirs("reports", exist_ok=True)


@pytest.fixture(scope="session")
def base_url():
    """Базовый URL API"""
    return "https://ru.yougile.com/api-v2"


@pytest.fixture(scope="session")
def api_headers():
    """Заголовки для API запросов"""
    token = "YOUR_API_TOKEN_HERE"  # Заменить на реальный токен
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def unique_project_name():
    """Генератор уникальных имен для проектов"""
    import uuid
    return f"Test Project {uuid.uuid4().hex[:8]}"