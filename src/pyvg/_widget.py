import pathlib

import anywidget
import traitlets
import msgspec

from ._tracks import BaseTrack


class _BrowserWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    _genome = traitlets.Unicode().tag(sync=True)
    _locus = traitlets.Unicode().tag(sync=True)
    _tracks = traitlets.List().tag(
        sync=True, to_json=lambda x, _: msgspec.to_builtins(x)
    )


class Browser:
    def __init__(self, genome: str, tracks: list[BaseTrack], locus: str | None = None):
        self._widget = _BrowserWidget(_genome=genome, _locus=locus, _tracks=tracks)

    @property
    def genome(self):
        return self._widget._genome

    @property
    def tracks(self):
        return self._widget._tracks

    def _repr_mimebundle_(self, **kwargs):
        return self._widget._repr_mimebundle_(**kwargs)
