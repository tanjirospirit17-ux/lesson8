"""YouGile API client for testing purposes."""
import os
import requests
from typing import Dict


class YouGileAPI:
    """Page Object for YouGile Projects API."""

    def __init__(self) -> None:
        self.base_url = os.getenv("YOUGILE_BASE_URL", "https://yougile.com/api-v2")
        self.api_key = os.getenv("YOUGILE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUGILE_API_KEY environment variable is not set")

        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def create_project(self, title: str) -> requests.Response:
        """Create a new project."""
        payload = {"title": title}
        return requests.post(
            f"{self.base_url}/projects",
            json=payload,
            headers=self.headers
        )

    def get_project(self, project_id: str) -> requests.Response:
        """Get project details by ID."""
        return requests.get(
            f"{self.base_url}/projects/{project_id}",
            headers=self.headers
        )

    def update_project(self, project_id: str, title: str) -> requests.Response:
        """Update an existing project."""
        payload = {"title": title}
        return requests.put(
            f"{self.base_url}/projects/{project_id}",
            json=payload,
            headers=self.headers
        )

    def delete_project(self, project_id: str) -> requests.Response:
        """Delete a project by ID (used for test cleanup)."""
        return requests.delete(
            f"{self.base_url}/projects/{project_id}",
            headers=self.headers
        )