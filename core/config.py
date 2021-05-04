from pathlib import Path

from utils.common import dotdict


def get_project_root() -> Path:
    return Path(__file__).parent.parent


class Config:
    def __init__(self, env: str):
        data_path = get_project_root() / "data" / env
        data_path.mkdir(parents=True, exist_ok=True)

        self.counter = data_path / "counter"
        self.crawler = dotdict({
            "linksA": data_path / "linksA",
            "linksB": data_path / "linksB",
            "bloom_filter": data_path / "bloom_filter",
            "doc_id_mapping": data_path / "doc_id_mapping",
            "doc_raw": data_path / "doc_raw",
            "seed_url": "https://www.inside.com.tw"
        })

        self.data_path = data_path
