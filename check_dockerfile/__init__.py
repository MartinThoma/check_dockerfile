__version__ = "0.1.0"

# Core Library modules
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

# Third party modules
from dockerfile_parse import DockerfileParser

# First party modules
from check_dockerfile.config import load_config


def check(dockerfile: Path) -> List[Tuple[str, str, bool]]:
    """Return True if everything looks fine, otherwise false."""
    config = load_config()
    dfp = DockerfileParser()
    with open(dockerfile) as fp:
        content = fp.read()
    dfp.content = content

    checks = []
    checks.append(
        (
            "Use a trusted base image",
            dfp.baseimage,
            is_trusted_base_image(config.trusted_images, dfp.baseimage),
        )
    )
    return checks


def is_trusted_base_image(trusted_images: List[str], base_image: str) -> bool:
    image2tags: Dict[str, List[str]] = defaultdict()
    for trusted_image in trusted_images:
        if ":" in trusted_image:
            image, tag = trusted_image.split(":")
            image2tags[image].append(tag)
        else:
            image2tags[trusted_image].append("*")
    if ":" in base_image:
        base_image, tag = base_image.split(":")
    return base_image in image2tags and (
        "*" in image2tags[base_image] or tag in image2tags[base_image]
    )