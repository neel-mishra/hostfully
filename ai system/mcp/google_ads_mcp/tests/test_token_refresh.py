import importlib.util
from pathlib import Path


SERVER_PATH = Path(__file__).resolve().parent.parent / "google_ads_server.py"


def load_server_module():
    spec = importlib.util.spec_from_file_location("google_ads_server", SERVER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    module = load_server_module()
    print(module.env("GOOGLE_ADS_AUTH_TYPE", "service_account"))
    print(module.env("GOOGLE_ADS_CREDENTIALS_PATH", ""))
