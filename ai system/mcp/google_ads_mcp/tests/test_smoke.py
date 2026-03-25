import importlib.util
from pathlib import Path


SERVER_PATH = Path(__file__).resolve().parent.parent / "google_ads_server.py"


def load_server_module():
    spec = importlib.util.spec_from_file_location("google_ads_server", SERVER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_format_customer_id():
    module = load_server_module()
    assert module.format_customer_id("123-456-7890") == "1234567890"
    assert module.format_customer_id("12345") == "0000012345"


def test_build_date_condition():
    module = load_server_module()
    condition = module.build_date_condition(7)
    assert "segments.date BETWEEN" in condition
