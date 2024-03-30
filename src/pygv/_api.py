from __future__ import annotations

import dataclasses
import pathlib
import typing

import servir

from ._tracks import AlignmentTrack, AnnotationTrack, Track, WigTrack, VariantTrack
from ._widget import Browser

__all__ = ["ref", "browse", "track"]


_PROVIDER = servir.Provider()
_RESOURCES = set()

FilePathOrUrl = typing.Union[str, pathlib.Path]
TrackArgument = typing.Union[FilePathOrUrl, tuple[FilePathOrUrl, FilePathOrUrl], Track]


@dataclasses.dataclass
class Context:
    genome: str = "hg38"
    locus: str | None = None
    current: Browser | None = None


CONTEXT = Context()


def locus(locus: str) -> None:
    """Set the initial locus for the browsers in this session."""
    CONTEXT.locus = locus


def ref(genome: str) -> None:
    """Set the reference genome for the browsers in this session."""
    CONTEXT.genome = genome


def _resolve_file_or_url(path_or_url: str | pathlib.Path):
    """Resolve a file path or URL to a URL.

    Parameters
    ----------
    path_or_url : str | pathlib.Path
        A file path or URL.

    Returns
    -------
    str
        A URL. If `path_or_url` is a URL, it is returned as-is, otherwise
        a file resource is created and the URL is returned.
    """
    normalized = str(path_or_url)
    if normalized.startswith("http") or normalized.startswith("https"):
        return normalized, False
    path = pathlib.Path(normalized).resolve()
    if not path.is_file() or not path.exists():
        raise FileNotFoundError(path)
    resource = _PROVIDER.create(path)
    _RESOURCES.add(resource)
    return resource.url, True


def track(t: TrackArgument, **kwargs) -> Track:
    if isinstance(t, Track):
        return t

    if isinstance(t, (str, pathlib.Path)):
        url, is_local = _resolve_file_or_url(t)
        index_url = None
        name = pathlib.Path(t).name if is_local else url
    else:
        url, is_local = _resolve_file_or_url(t[0])
        index_url, _ = _resolve_file_or_url(t[1])
        name = pathlib.Path(t[0]).name if is_local else url

    parts = url.split(".")
    filetype = parts[-1].lower()
    if filetype == "gz":
        filetype = parts[-2].lower()

    type_ = kwargs.pop("type", None)
    name = kwargs.pop("name", name)

    if type_ == "alignment" or filetype in {"bam", "cram"}:
        return AlignmentTrack(url=url, index_url=index_url, name=name, **kwargs)
    if type_ == "annotation" or filetype in {"bed", "gff", "gff3", "gtf", "bedpe"}:
        return AnnotationTrack(url=url, index_url=index_url, name=name, **kwargs)
    if type_ == "wig" or filetype in {"bigWig", "bw", "bg", "bedGraph"}:
        return WigTrack(url=url, index_url=index_url, name=name, **kwargs)
    if type_ == "variant" or filetype in {"vcf"}:
        return VariantTrack(url=url, index_url=index_url, name=name, **kwargs)

    raise ValueError(f"Unsupported track or file type: {filetype}")


def browse(*tracks: TrackArgument) -> Browser:
    """Create a new genome browser instance.

    Parameters
    ----------

    args : tuple[TrackArgument, ...]
        A list of tracks to display in the browser.

    Returns
    -------
    Browser
        The browser widget.
    """

    CONTEXT.current = Browser(
        genome=CONTEXT.genome, locus=CONTEXT.locus, tracks=[track(t) for t in tracks]
    )
    return CONTEXT.current
