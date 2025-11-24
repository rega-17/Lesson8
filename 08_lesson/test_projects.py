import requests
import pytest
import time
from config import TOKEN

class TestYougileProjects:
    BASE_URL = "https://yougile.com/api-v2"
    
    def setup_class(self):
        self.company_id = "0fbb00de-ae52-4603-9f25-5fdedda09ad0"
        self.token = TOKEN
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.created_project_id = None

    # POSITIVE TESTS

    def test_create_project_positive(self):
        url = f"{self.BASE_URL}/projects"
        payload = {
            "title": f"Test Project {int(time.time())}",
            "access": "public"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        self.created_project_id = data["id"]

    def test_get_project_positive(self):
        if not self.created_project_id:
            pytest.skip("No project created")
        url = f"{self.BASE_URL}/projects/{self.created_project_id}"
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.created_project_id

    def test_update_project_positive(self):
        if not self.created_project_id:
            pytest.skip("No project created")
        url = f"{self.BASE_URL}/projects/{self.created_project_id}"
        payload = {
            "title": f"Updated Test Project {int(time.time())}"
        }
        response = requests.put(url, json=payload, headers=self.headers)
        assert response.status_code == 200

    # NEGATIVE TESTS

    def test_create_project_without_token(self):
        """Тест на отсутствие токена"""
        url = f"{self.BASE_URL}/projects"
        payload = {"title": "Test Project"}
        response = requests.post(url, json=payload)
        assert response.status_code == 401

    def test_create_project_with_invalid_token(self):
        """Тест на невалидный токен"""
        url = f"{self.BASE_URL}/projects"
        headers = {"Authorization": "Bearer INVALID_TOKEN"}
        payload = {"title": "Test Project"}
        response = requests.post(url, json=payload, headers=headers)
        assert response.status_code == 401

    def test_create_project_with_invalid_data(self):
        """Тест на некорректные данные"""
        url = f"{self.BASE_URL}/projects"
        payload = {}  # Пустой payload
        response = requests.post(url, json=payload, headers=self.headers)
        assert response.status_code == 400

    def test_get_project_with_invalid_id(self):
        """Тест на несуществующий ID проекта"""
        url = f"{self.BASE_URL}/projects/invalid_project_id_123"
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 404

    def test_update_project_with_invalid_id(self):
        """Тест на обновление несуществующего проекта"""
        url = f"{self.BASE_URL}/projects/invalid_project_id_123"
        payload = {"title": "Updated Project"}
        response = requests.put(url, json=payload, headers=self.headers)
        assert response.status_code == 404

    def teardown_class(self):
        if self.created_project_id:
            url = f"{self.BASE_URL}/projects/{self.created_project_id}"
            requests.delete(url, headers=self.headers)