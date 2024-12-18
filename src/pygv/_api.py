from __future__ import annotations

import dataclasses
import json
import pathlib
import typing

from ._browser import Browser
from ._config import Config, is_href
from ._tracks import Track

__all__ = ["Browser", "browse", "load", "loads", "locus", "ref", "track"]


@dataclasses.dataclass
class Context:
    genome: str = "hg38"
    locus: str | None = None
    current: Browser | None = None


_CONTEXT = Context()

FilePathOrUrl = typing.Union[str, pathlib.Path]
TrackArgument = typing.Union[
    FilePathOrUrl,
    tuple[FilePathOrUrl, FilePathOrUrl],
    Track,
]


def locus(locus: str) -> None:
    """Set the initial locus for the browsers in this session."""
    _CONTEXT.locus = locus


def ref(genome: str) -> None:
    """Set the reference genome for the browsers in this session."""
    _CONTEXT.genome = genome


def track(targ: TrackArgument | None = None, /, **kwargs) -> Track:  # noqa: ANN003
    if isinstance(targ, Track):
        return targ

    if targ is None:
        url = kwargs["url"]
    elif isinstance(targ, (str, pathlib.Path)):
        url = kwargs["url"] = str(targ)
        kwargs["indexURL"] = None
    else:
        url = kwargs["url"] = str(targ[0])
        kwargs["indexURL"] = str(targ[1])

    if "name" not in kwargs:
        kwargs["name"] = url if is_href(url) else pathlib.Path(url).name

    return Config.from_dict({"tracks": [kwargs]}).tracks[0]


def browse(*tracks: TrackArgument) -> Browser:
    """Create a new genome browser instance.

    Parameters
    ----------
    tracks : tuple[TrackArgument, ...]
        A list of tracks to display in the browser.

    Returns
    -------
    Browser
        The browser widget.
    """
    _CONTEXT.current = Browser(
        Config(
            genome=_CONTEXT.genome,
            locus=_CONTEXT.locus,
            tracks=[track(t) for t in tracks],
        ),
    )
    return _CONTEXT.current


def load(file: typing.IO[str]) -> Browser:
    """Load an existing IGV configuration from a file-like."""
    return loads(file.read())


def loads(json_config: str) -> Browser:
    """Load a JSON-encoded IGV configuration."""
    config = json.loads(json_config)
    _CONTEXT.current = Browser(Config.from_dict(config))
    return _CONTEXT.current
