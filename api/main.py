import json
from contextlib import asynccontextmanager
from pathlib import Path

import yaml
from elasticsearch import Elasticsearch
from fastapi import FastAPI

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"
config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))

es = Elasticsearch(config["elasticsearch"]["host"])


def create_index_if_missing() -> None:
    index = config["elasticsearch"]["index"]
    if es.indices.exists(index=index):
        return
    mapping_path = Path(__file__).resolve().parent.parent / config["elasticsearch"]["mapping_file"]
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    es.indices.create(index=index, mappings=mapping["mappings"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_index_if_missing()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    try:
        connected = es.ping()
    except Exception:
        connected = False
    return {"status": "ok", "elasticsearch": "connected" if connected else "disconnected"}
