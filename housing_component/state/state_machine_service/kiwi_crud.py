import requests
from typing import List
from housing_component.state.schemas import KiwiUser, Permission
from housing_component.core.auth import get_session_key
from housing_component.access_points.schemas import PermissionEnum
from housing_component.settings import (
    FETCH_USER_URL,
    CREATE_USER_URL,
    GRANT_PERMISSIONS_URL,
    SENSOR_URL,
    REMOVE_PERMISSION_URL,
)


class KiwiCrud:
    def __init__(self) -> None:
        self.session_key = get_session_key()

    def get_user_by_username(self, username: str) -> KiwiUser | None:
        params = {"username": username, "session_key": self.session_key}
        resp = requests.get(FETCH_USER_URL, params=params)
        if resp.status_code == 200:
            resp_json = resp.json().get("result", {})
            user = resp_json.get("user", {})
            user = {**user, **user["contact"]}
            del user["contact"]
            user["language"] = user.get("language", None)
            return KiwiUser.model_validate(user)
        return None

    def create_user(
        self, first_name: str, last_name: str, email_address: str
    ) -> KiwiUser | None:
        data = {
            "country": "DE",
            "email": email_address,
            "i_have_read_and_accepted_kiwidotki_agb": True,
            "lang": "en",
            "lastname": last_name,
            "name": first_name,
            "password": "password123",
            "segment_id": "10",
            "session_key": self.session_key,
            "skip_verification": False,
        }
        resp = requests.post(CREATE_USER_URL, json=data)
        if resp.status_code == 200:
            resp_json = resp.json().get("result", {})
            user = resp_json.get("user", {})
            return KiwiUser.model_validate(user)
        return None

    def grant_sensor_permission_to_the_user(
        self, sensors: List[int], username: str
    ) -> int | None:
        data = {
            "permission": PermissionEnum.IS_GUEST.value,
            "sensors": sensors,
            "session_key": self.session_key,
            "users": [username],
            "weekdays": "monday,tuesday,wednesday,thursday,friday,saturday,sunday",
        }
        resp = requests.post(GRANT_PERMISSIONS_URL, json=data)
        if resp.status_code == 200:
            resp_json = resp.json().get("result", {})
            return resp_json.get("task_id", int)
        return None

    def get_sensor_permissions(self, sensor_id: int) -> List[Permission]:
        params = {"page_number": 1, "page_size": 20, "session_key": self.session_key}
        resp = requests.get(f"{SENSOR_URL}/{sensor_id}/permissions", params=params)
        if resp.status_code == 200:
            resp_json = resp.json().get("result", {})
            return [
                Permission.model_validate(permission)
                for permission in resp_json.get("permissions", [])
            ]
        return []

    def remove_permission(self, permission_id: int) -> None:
        params = {"session_key": self.session_key}
        resp = requests.get(f"{REMOVE_PERMISSION_URL}/{permission_id}", params=params)
        if resp.status_code == 200:
            resp.json().get("result", {}).get("task_id")
