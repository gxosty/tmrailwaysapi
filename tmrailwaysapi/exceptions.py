from typing import Dict, Any


class APIStatusError(Exception):
    def __init__(self, id: str, message: str) -> None:
        ex_message = "{} (id: {})".format(message, id)
        super().__init__(ex_message)
        self._id = id
        self._message = message

    @property
    def message(self) -> str:
        return self._message

    @property
    def id(self) -> str:
        return self._id

    @staticmethod
    def raise_for_status(json_data: Dict[str, Any]) -> None:
        if not json_data["success"]:
            if "error" in json_data:
                error = json_data["error"]
            elif "errors" in json_data:
                error = json_data["errors"][0]
            raise APIStatusError(error["id"], error["message"])
