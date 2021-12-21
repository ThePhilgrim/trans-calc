import appdirs
from pathlib import Path


def get_user_config_dir():
    config_dir = Path(appdirs.user_config_dir("Trans-Calc", "ThePhilgrim"))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


class Client:
    def __init__(self) -> None:
        # self.client_name -> str
        # self.full_rate -> float
        # self.currency -> str
        # self.matrix -> dict
        pass

# Client -> currency, matrix, full rate
# Support adding client, changing client name, changing client matrix, changing full rate
# Support deleting client, deleting matrix ROW, deleting whole matrix
