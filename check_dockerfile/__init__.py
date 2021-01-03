__version__ = "0.1.0"

# Core Library modules
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
    tag = get_tag(dfp.baseimage)
    tag_str = "-" if tag is None else tag
    checks.append(("A tag for the base image is set", tag_str, tag is not None))
    checks.append(("Executes as non-root", "", executes_as_non_root(dfp)))
    checks.append(("COPY added after apt-get update", "", copy_added_after_update(dfp)))
    return checks


def copy_added_after_update(dfp: DockerfileParser) -> bool:
    copy_step: Optional[int] = None
    apt_step: Optional[int] = None
    for step in dfp.structure:
        if step["instruction"] == "RUN":
            if (
                "apt-get update" in step["value"]
                or "apt-get upgrade" in step["value"]
                or "apt-get install" in step["value"]
            ):
                apt_step = (
                    step["startline"]
                    if apt_step is None
                    else min(step["startline"], apt_step)
                )
        elif step["instruction"] == "COPY":
            copy_step = (
                step["startline"]
                if copy_step is None
                else min(step["startline"], copy_step)
            )
    if copy_step is None or apt_step is None:
        return True
    return apt_step < copy_step


def is_trusted_base_image(trusted_images: List[str], base_image: str) -> bool:
    image2tags: Dict[str, List[str]] = defaultdict(list)
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


def get_tag(base_image: str) -> Optional[str]:
    if ":" not in base_image:
        return None
    return base_image.split(":")[1]


def executes_as_non_root(dfp: DockerfileParser) -> bool:
    return any(el for el in dfp.structure if el["instruction"] == "USER")
