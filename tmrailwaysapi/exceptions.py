class APIStatusError(Exception):
    def __init__(self, message) -> None:
        super().__init__("API Status error -> {}".format(message))
        self._message = message

    @property
    def message(self) -> str:
        return self._message

    @staticmethod
    def raise_for_status(json_data) -> None:
        if not json_data["success"]:
            raise APIStatusError("Unknown")

