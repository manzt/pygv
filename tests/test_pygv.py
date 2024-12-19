import json
import pathlib

import pytest
from inline_snapshot import snapshot

from pygv import Config
from pygv._api import load
from pygv._tracks import AlignmentTrack


@pytest.fixture
def config_dict():
    return {
        "genome": "hg38",
        "locus": "chr8:127,736,588-127,739,371",
        "tracks": [
            {
                "name": "HG00103",
                "url": "https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram",
                "indexURL": "https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram.crai",
                "format": "cram",
            },
        ],
    }


def test_loads_config(config_dict: dict) -> None:
    assert Config.from_dict(config_dict) == snapshot(
        Config(
            genome="hg38",
            locus="chr8:127,736,588-127,739,371",
            tracks=[
                AlignmentTrack(
                    name="HG00103",
                    url="https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram",
                    index_url="https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram.crai",
                    format="cram",
                )
            ],
        )
    )


def test_loads_file(config_dict: dict, tmp_path: pathlib.Path) -> None:
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config_dict), encoding="utf-8")

    with path.open() as f:
        browser = load(f)

    assert browser._genome == snapshot("hg38")  # noqa: SLF001
    assert browser._locus == snapshot("chr8:127,736,588-127,739,371")  # noqa: SLF001
    assert browser._tracks == snapshot(  # noqa: SLF001
        [
            AlignmentTrack(
                name="HG00103",
                url="https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram",
                index_url="https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram.crai",
                format="cram",
            )
        ]
    )
