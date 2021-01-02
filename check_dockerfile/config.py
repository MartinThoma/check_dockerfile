# Core Library modules
from pathlib import Path
from typing import List

# Third party modules
import yaml
from pydantic import BaseModel


class Config(BaseModel):
    trusted_images: List[str] = ["alpine", "python", "node", "ubuntu"]


def load_config() -> Config:
    cfg_path = Path(".check_dockerfile.yaml")
    if cfg_path.exists():
        with open(cfg_path) as fp:
            data = fp.read()
        config_dict = yaml.load(data)
        config = Config.parse_obj(config_dict)
    else:
        config = Config()
    return config
