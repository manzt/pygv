import copy
import pathlib
import typing

import msgspec
import servir

from ._tracks import Track

_PROVIDER = servir.Provider()
_RESOURCES = set()

FilePathOrUrl = typing.Union[str, pathlib.Path]


class Config(msgspec.Struct):
    """An IGV configuration."""

    genome: str = "hg38"
    locus: typing.Union[str, None] = None  # noqa: FA100
    tracks: list[Track] = []

    @classmethod
    def from_dict(
        cls,
        config: dict,
    ) -> "Config":
        config = copy.deepcopy(config)

        for track in config.get("tracks", []):
            track["type"] = resolve_track_type(
                track.get("type"),
                track.get("format", guess_format(track["url"])),
            )

        return msgspec.convert(config, type=Config)

    def servable(self) -> "Config":
        """Returns a new config with tracks that are ensured to be servable."""  # noqa: D401
        copy = msgspec.from_builtins(msgspec.to_builtins(self), type=Config)

        for t in copy.tracks:
            t.url = resolve_file_or_url(t.url)
            if t.index_url:
                t.index_url = resolve_file_or_url(t.index_url)

        return copy


def is_href(s: str) -> bool:
    return s.startswith(("http", "https"))


def resolve_file_or_url(path_or_url: typing.Union[str, pathlib.Path]) -> str:  # noqa: FA100
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
    if is_href(normalized):
        return normalized
    path = pathlib.Path(normalized).resolve()
    if not path.is_file() or not path.exists():
        raise FileNotFoundError(path)
    resource = _PROVIDER.create(path)
    _RESOURCES.add(resource)
    return resource.url


def resolve_track_type(
    type_: typing.Union[str, None],  # noqa: FA100
    format_: str,
) -> str:
    if type_ == "alignment" or format_ in {"bam", "cram"}:
        return "alignment"
    if type_ == "annotation" or format_ in {"bed", "gff", "gff3", "gtf", "bedpe"}:
        return "annotation"
    if type_ == "wig" or format_ in {"bigWig", "bw", "bg", "bedGraph"}:
        return "wig"
    if type_ == "variant" or format_ in {"vcf"}:
        return "variant"

    msg = "Unknown track type, got: {}"
    raise ValueError(msg)


def guess_format(filename: str) -> str:
    parts = filename.split(".")
    filetype = parts[-1].lower()
    if filetype == "gz":
        filetype = parts[-2].lower()
    return filetype
