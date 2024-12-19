import json
import pathlib

import pytest
from inline_snapshot import snapshot

from pygv import Config
from pygv._api import load
from pygv._tracks import (
    AlignmentTrack,
    AnnotationTrack,
    MergedTrack,
    SegmentedCopyNumberTrack,
    WigTrack,
)


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


def test_merged() -> None:
    assert Config.from_dict(
        {
            "genome": "hg19",
            "locus": "chr4:40,174,668-40,221,204",
            "tracks": [
                {
                    "name": "Merged - individual autoscaled",
                    "type": "merged",
                    "tracks": [
                        {
                            "type": "wig",
                            "format": "bigwig",
                            "url": "https://www.encodeproject.org/files/ENCFF000ASJ/@@download/ENCFF000ASJ.bigWig",
                            "color": "red",
                            "autoscale": True,
                        },
                        {
                            "type": "wig",
                            "format": "bigwig",
                            "url": "https://www.encodeproject.org/files/ENCFF351WPV/@@download/ENCFF351WPV.bigWig",
                            "color": "green",
                            "autoscale": True,
                        },
                    ],
                },
            ],
        }
    ) == snapshot(
        Config(
            genome="hg19",
            locus="chr4:40,174,668-40,221,204",
            tracks=[
                MergedTrack(
                    name="Merged - individual autoscaled",
                    tracks=[
                        WigTrack(
                            url="https://www.encodeproject.org/files/ENCFF000ASJ/@@download/ENCFF000ASJ.bigWig",
                            format="bigwig",
                            color="red",
                            autoscale=True,
                        ),
                        WigTrack(
                            url="https://www.encodeproject.org/files/ENCFF351WPV/@@download/ENCFF351WPV.bigWig",
                            format="bigwig",
                            color="green",
                            autoscale=True,
                        ),
                    ],
                )
            ],
        )
    )


def test_seg() -> None:
    assert Config.from_dict(
        {
            "genome": "hg19",
            "showSampleNames": True,
            "tracks": [
                {
                    "name": "Explicit Samples",
                    "type": "seg",
                    "format": "seg",
                    "samples": [
                        "TCGA-06-0168-01A-02D-0236-01",
                        "TCGA-02-0115-01A-01D-0193-01",
                        "TCGA-02-2485-01A-01D-0784-01",
                        "TCGA-06-0151-01A-01D-0236-01",
                    ],
                    "url": "https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
                    "height": 100,
                },
                {
                    "name": "Segmented Copy Number",
                    "type": "seg",
                    "format": "seg",
                    "url": "https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
                },
                {
                    "name": "Indexed",
                    "type": "seg",
                    "format": "seg",
                    "url": "https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
                    "indexURL": "https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz.tbi",
                },
                {
                    "name": "Indexed with visibility window",
                    "type": "seg",
                    "format": "seg",
                    "url": "https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
                    "indexURL": "https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz.tbi",
                    "visibilityWindow": "100000000",
                },
            ],
        }
    ) == snapshot(
        Config(
            genome="hg19",
            show_sample_names=True,
            tracks=[
                SegmentedCopyNumberTrack(
                    url="https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
                    name="Explicit Samples",
                    format="seg",
                    height=100,
                ),
                SegmentedCopyNumberTrack(
                    url="https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
                    name="Segmented Copy Number",
                    format="seg",
                ),
                SegmentedCopyNumberTrack(
                    url="https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
                    name="Indexed",
                    index_url="https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz.tbi",
                    format="seg",
                ),
                SegmentedCopyNumberTrack(
                    url="https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
                    name="Indexed with visibility window",
                    index_url="https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz.tbi",
                    format="seg",
                    visibility_window="100000000",
                ),
            ],
        )
    )


def test_basic_config():
    assert Config.from_dict(
        {
            "genome": "hg19",
            "locus": "chr1:155,160,475-155,184,282",
            "tracks": [
                {
                    "url": "https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
                    "name": "GBM Copy # (TCGA Broad GDAC)",
                },
                {
                    "type": "annotation",
                    "format": "bed",
                    "url": "https://data.broadinstitute.org/igvdata/annotations/hg19/dbSnp/snp137.hg19.bed.gz",
                    "indexURL": "https://data.broadinstitute.org/igvdata/annotations/hg19/dbSnp/snp137.hg19.bed.gz.tbi",
                    "visibilityWindow": 200_000,
                    "name": "dbSNP 137",
                },
                {
                    "type": "wig",
                    "format": "bigwig",
                    "url": "https://s3.amazonaws.com/igv.broadinstitute.org/data/hg19/encode/wgEncodeBroadHistoneGm12878H3k4me3StdSig.bigWig",
                    "name": "Gm12878H3k4me3",
                },
                {
                    "type": "alignment",
                    "format": "bam",
                    "url": "https://1000genomes.s3.amazonaws.com/phase3/data/HG02450/alignment/HG02450.mapped.ILLUMINA.bwa.ACB.low_coverage.20120522.bam",
                    "indexURL": "https://1000genomes.s3.amazonaws.com/phase3/data/HG02450/alignment/HG02450.mapped.ILLUMINA.bwa.ACB.low_coverage.20120522.bam.bai",
                    "name": "HG02450",
                },
            ],
        }
    ) == snapshot(
        Config(
            genome="hg19",
            locus="chr1:155,160,475-155,184,282",
            tracks=[
                SegmentedCopyNumberTrack(
                    url="https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
                    name="GBM Copy # (TCGA Broad GDAC)",
                ),
                AnnotationTrack(
                    url="https://data.broadinstitute.org/igvdata/annotations/hg19/dbSnp/snp137.hg19.bed.gz",
                    name="dbSNP 137",
                    index_url="https://data.broadinstitute.org/igvdata/annotations/hg19/dbSnp/snp137.hg19.bed.gz.tbi",
                    format="bed",
                    visibility_window=200000,
                ),
                WigTrack(
                    url="https://s3.amazonaws.com/igv.broadinstitute.org/data/hg19/encode/wgEncodeBroadHistoneGm12878H3k4me3StdSig.bigWig",
                    name="Gm12878H3k4me3",
                    format="bigwig",
                ),
                AlignmentTrack(
                    url="https://1000genomes.s3.amazonaws.com/phase3/data/HG02450/alignment/HG02450.mapped.ILLUMINA.bwa.ACB.low_coverage.20120522.bam",
                    name="HG02450",
                    index_url="https://1000genomes.s3.amazonaws.com/phase3/data/HG02450/alignment/HG02450.mapped.ILLUMINA.bwa.ACB.low_coverage.20120522.bam.bai",
                    format="bam",
                ),
            ],
        )
    )
