from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

import anywidget
import msgspec
import traitlets

if TYPE_CHECKING:
    from ._config import Config


class Browser(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _genome = traitlets.Unicode().tag(sync=True)
    _locus = traitlets.Unicode().tag(sync=True)
    _tracks = traitlets.List().tag(
        sync=True,
        to_json=lambda x, _: msgspec.to_builtins(x),
    )

    def __init__(self, config: Config) -> None:
        super().__init__(
            _genome=config.genome,
            _locus=config.locus,
            _tracks=config.tracks,
        )
