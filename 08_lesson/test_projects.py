import requests
import pytest

class TestYougileProjects:
    BASE_URL = "https://yougile.com/api-v2"
    
    def setup_class(self):
        self.company_id = "0fbb00de-ae52-4603-9f25-5fdedda09ad0"
        self.token = "U92d18aA9EVVkHlhsch-9dHTxI3iFDnUoAvuqXDGyZu4WzgJ4LMxbOFVBehMtMLI"
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.created_project_id = None

    def test_create_project_positive(self):
        url = f"{self.BASE_URL}/projects"
        payload = {
            "title": f"Test Project {pytest.current_test}",
            "access": "public"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        print(f"Create project response: {response.status_code} - {response.text}")  # Для диагностики
        assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
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
            "title": "Updated Test Project"
        }
        response = requests.put(url, json=payload, headers=self.headers)
        assert response.status_code == 200

    def test_create_project_negative(self):
        url = f"{self.BASE_URL}/projects"
        payload = {}
        response = requests.post(url, json=payload, headers=self.headers)
        assert response.status_code == 400

    def test_get_project_negative(self):
        url = f"{self.BASE_URL}/projects/invalid_id"
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 404

    def test_update_project_negative(self):
        url = f"{self.BASE_URL}/projects/invalid_id"
        payload = {
            "title": "Updated Test Project"
        }
        response = requests.put(url, json=payload, headers=self.headers)
        assert response.status_code == 404

    def teardown_class(self):
        if self.created_project_id:
            url = f"{self.BASE_URL}/projects/{self.created_project_id}"
            requests.delete(url, headers=self.headers)