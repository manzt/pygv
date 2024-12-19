import copy
import pathlib
import typing as t

import msgspec
import servir
from msgspec import UNSET, Struct, UnsetType

from ._tracks import Track

_PROVIDER = servir.Provider()
_RESOURCES = set()

FilePathOrUrl = t.Union[str, pathlib.Path]


class Config(Struct, rename="camel", repr_omit_defaults=True, omit_defaults=True):
    """An IGV configuration."""

    genome: t.Union[str, UnsetType] = UNSET  # noqa: FA100
    locus: t.Union[str, list[str], UnsetType] = UNSET  # noqa: FA100
    show_sample_names: t.Union[bool, UnsetType] = UNSET  # noqa: FA100
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
                track.get("format", guess_format(track.get("url"))),
            )

        return msgspec.convert(config, type=Config)

    def servable(self) -> "Config":
        """Returns a new config with tracks that are ensured to be servable."""  # noqa: D401
        copy = msgspec.convert(msgspec.to_builtins(self), type=Config)

        for track in copy.tracks:
            if track.url != msgspec.UNSET:
                track.url = resolve_file_or_url(track.url)

            if track.index_url != msgspec.UNSET:
                track.index_url = resolve_file_or_url(track.index_url)

        return copy


def is_href(s: str) -> bool:
    return s.startswith(("http", "https"))


def resolve_file_or_url(path_or_url: t.Union[str, pathlib.Path]) -> str:  # noqa: FA100
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


def resolve_track_type(  # noqa: C901, PLR0911, PLR0912
    type_: t.Union[str, None],  # noqa: FA100
    format_: t.Union[str, None],  # noqa: FA100
) -> str:
    if type_ == "annotation" or format_ in {"bed", "gff", "gff3", "gtf", "bedpe"}:
        return "annotation"

    if type_ == "wig" or format_ in {"bigWig", "bw", "bg", "bedGraph"}:
        return "wig"

    if type_ == "alignment" or format_ in {"bam", "cram"}:
        return "alignment"

    if type_ == "variant" or format_ in {"vcf"}:
        return "variant"

    if type_ == "mut" or format_ in {"mut", "maf"}:
        return "mut"

    if type_ == "seg" or format_ in {"mut", "seg"}:
        return "seg"

    if type_ == "gwas" or format_ in {"bed", "gwas"}:
        return "gwas"

    if type_ == "interact" or format_ in {"bedpe", "interact", "bigInteract"}:
        return "interact"

    if type_ == "qtl" or format_ in {"qtl"}:
        return "qtl"

    if type_ == "junction" or format_ in {"bed"}:
        return "junction"

    if type_ == "cnvpytor" or format_ in {"pytor", "vcf"}:
        return "cnvpytor"

    if type_ == "arc" or format_ in {"bp", "bed"}:
        return "arc"

    if type_ == "merged":
        return "merged"

    msg = "Unknown track type, got: {}"
    raise ValueError(msg)


def guess_format(filename: t.Union[str, None]) -> t.Union[str, None]:  # noqa: FA100
    if filename is None:
        return None
    parts = filename.split(".")
    filetype = parts[-1].lower()
    if filetype == "gz":
        filetype = parts[-2].lower()
    return filetype
