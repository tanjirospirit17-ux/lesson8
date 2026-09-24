"""Tests for YouGile Projects API."""
import os
import uuid
import pytest
import requests
from yougile_api import YouGileAPI


@pytest.fixture(scope="module")
def api() -> YouGileAPI:
    """Provide an instance of YouGileAPI."""
    return YouGileAPI()


@pytest.fixture
def project_title() -> str:
    """Generate a unique project title for testing."""
    return f"Test Project {uuid.uuid4().hex}"


@pytest.fixture
def created_project(api: YouGileAPI, project_title: str):
    """Create a project before test and delete it after (teardown)."""
    response = api.create_project(project_title)
    assert response.status_code in (200, 201), f"Failed to create project: {response.text}"
    
    data = response.json()
    project_id = data.get("id")
    assert project_id is not None, f"Project ID not found in response: {data}"
    
    yield project_id, project_title
    
    if project_id:
        api.delete_project(project_id)


class TestProjectsPOST:
    """Tests for POST /api-v2/projects endpoint."""

    def test_create_project_positive(self, api: YouGileAPI, project_title: str) -> None:
        response = api.create_project(project_title)
        assert response.status_code in (200, 201)
        
        data = response.json()
        assert "id" in data, f"Project ID not found in response: {data}"
        
        project_id = data.get("id")
        if project_id:
            api.delete_project(project_id)

    def test_create_project_negative_invalid_token(self, project_title: str) -> None:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer invalid_token_xyz"
        }
        base_url = os.getenv("YOUGILE_BASE_URL", "https://yougile.com/api-v2")
        response = requests.post(
            f"{base_url}/projects", 
            json={"title": project_title}, 
            headers=headers
        )
        assert response.status_code == 401
        data = response.json()
        assert "error" in data or "message" in data or "unauthorized" in str(data).lower()


class TestProjectsGET:
    """Tests for GET /api-v2/projects/{id} endpoint."""

    def test_get_project_positive(self, api: YouGileAPI, created_project) -> None:
        project_id, project_title = created_project
        response = api.get_project(project_id)
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data or "project" in data

    def test_get_project_negative_invalid_id(self, api: YouGileAPI) -> None:
        response = api.get_project("invalid_project_id_12345")
        assert response.status_code in (400, 404)
        data = response.json()
        assert "error" in data or "message" in data


class TestProjectsPUT:
    """Tests for PUT /api-v2/projects/{id} endpoint."""

    def test_update_project_positive(self, api: YouGileAPI, created_project) -> None:
        project_id, _ = created_project
        new_title = f"Updated Project {uuid.uuid4().hex}"
        
        response = api.update_project(project_id, new_title)
        assert response.status_code in (200, 201)
        
        get_response = api.get_project(project_id)
        assert get_response.status_code == 200
        
        get_data = get_response.json()
        assert (
            get_data.get("title") == new_title or 
            (get_data.get("project") and get_data["project"].get("title") == new_title)
        )

    def test_update_project_negative_invalid_id(self, api: YouGileAPI) -> None:
        new_title = f"Updated Project {uuid.uuid4().hex}"
        response = api.update_project("invalid_project_id_12345", new_title)
        assert response.status_code in (400, 404)
        data = response.json()
        assert "error" in data or "message" in data