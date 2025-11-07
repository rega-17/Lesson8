import pytest
import requests
from unittest.mock import Mock, patch


class TestYougileProjectsMock:
    """Тесты с заглушками (mocks) для Yougile API"""

    def test_create_project_positive_mock(self):
        """Позитивный тест создания проекта с заглушкой"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "test_project_123",
            "title": "Test Project",
            "description": "Test description"
        }

        with patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            
            response = requests.post(
                "https://ru.yougile.com/api-v2/projects",
                json={"title": "Test Project", "description": "Test description"},
                headers={"Authorization": "Bearer fake_token"}
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["id"] == "test_project_123"
            assert data["title"] == "Test Project"

    def test_get_project_positive_mock(self):
        """Позитивный тест получения проекта с заглушкой"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "test_project_123",
            "title": "Test Project",
            "description": "Test description"
        }

        with patch('requests.get') as mock_get:
            mock_get.return_value = mock_response
            
            response = requests.get(
                "https://ru.yougile.com/api-v2/projects/test_project_123",
                headers={"Authorization": "Bearer fake_token"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test_project_123"
            assert data["title"] == "Test Project"

    def test_update_project_positive_mock(self):
        """Позитивный тест обновления проекта с заглушкой"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "test_project_123",
            "title": "Updated Project",
            "description": "Updated description"
        }

        with patch('requests.put') as mock_put:
            mock_put.return_value = mock_response
            
            response = requests.put(
                "https://ru.yougile.com/api-v2/projects/test_project_123",
                json={"title": "Updated Project", "description": "Updated description"},
                headers={"Authorization": "Bearer fake_token"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Updated Project"
            assert data["description"] == "Updated description"

    def test_create_project_negative_unauthorized_mock(self):
        """Негативный тест без авторизации с заглушкой"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": "Unauthorized"
        }

        with patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            
            response = requests.post(
                "https://ru.yougile.com/api-v2/projects",
                json={"title": "Test Project"},
                headers={"Content-Type": "application/json"}
            )
            
            assert response.status_code == 401
            data = response.json()
            assert data["error"] == "Unauthorized"

    def test_get_project_negative_not_found_mock(self):
        """Негативный тест проекта не найден с заглушкой"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "error": "Project not found"
        }

        with patch('requests.get') as mock_get:
            mock_get.return_value = mock_response
            
            response = requests.get(
                "https://ru.yougile.com/api-v2/projects/non_existent_id",
                headers={"Authorization": "Bearer fake_token"}
            )
            
            assert response.status_code == 404
            data = response.json()
            assert data["error"] == "Project not found"