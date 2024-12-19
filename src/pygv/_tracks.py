from __future__ import annotations

import typing as t

from msgspec import UNSET, Struct, UnsetType, field

__all__ = [
    "AlignmentTrack",
    "AnnotationTrack",
    "BaseTrack",
    "Track",
    "VariantTrack",
    "WigTrack",
]


class BaseTrack(Struct, rename="camel", repr_omit_defaults=True, omit_defaults=True):
    """Represents a browser track.

    For a full configuration options, see the [IGV.js docs](https://igv.org/doc/igvjs/#tracks/Tracks)
    """

    associated_file_formats: t.ClassVar[set[str]] = set()
    """File formats associated with this track type."""

    name: str
    """Display name (label). Required."""

    url: str
    """URL to the track data resource, such as a file or webservice, or a data URI."""

    index_url: t.Union[str, UnsetType] = field(default=UNSET, name="indexURL")  # noqa: UP007
    """URL to a file index, such as a BAM .bai, tabix .tbi, or tribble .idx file.

    For indexed file access the index URL is required, if absent the entire file
    will be read.
    """

    source_type: t.Union[t.Literal["file", "htsget", "custom"], UnsetType] = UNSET  # noqa: UP007
    """Type of data source."""

    format: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """No default. If not specified, format is inferred from file name extension."""

    indexed: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Explicitly indicate whether the resource is indexed.

    This flag is redundant if `index_url` is provided. It can be used to load small
    BAM files without an index by setting to `False`
    """

    order: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Integer value specifying relative order of track position on the screen.

    To pin a track to the bottom use a very large value.
    If no order is specified, tracks appear in order of their addition.
    """

    color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """CSS color value for track features, e.g. "#ff0000" or "rgb(100,0,100)"."""

    height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Initial height of track viewport in pixels. Default 50."""

    min_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Minimum height of track in pixels. Default 50."""

    max_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Maximum height of track in pixels. Default 500."""

    visibility_window: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Maximum window size in base pairs for which indexed annotations or
    variants are displayed.

    1 MB for variants, 30 KB for alignments, whole chromosome for
    other track types.
    """

    removable: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """If true a "remove" item is included in the track menu. Default `True`."""

    headers: t.Union[dict[str, str], UnsetType] = UNSET  # noqa: UP007
    """HTTP headers to include with each request.

    For example `{"Authorization": "Bearer cn389ncoiwuencr"}`.
    """

    oauth_token: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """OAuth token, or function returning an OAuth token.

    The value will be included as a Bearer token with each request.
    """


class AnnotationTrack(BaseTrack, tag="annotation"):
    """Display views of genomic annotations.

    Associated file formats: bed, gff, gff3, gtf, bedpe (and more).

    Ref: https://igv.org/doc/igvjs/#tracks/Annotation-Track

    Example:
    ```py
    AnnotationTrack(
        name="Color by attribute biotype",
        format="gff3",
        display_mode="expanded",
        height=300,
        url="https://s3.amazonaws.com/igv.org.genomes/hg38/Homo_sapiens.GRCh38.94.chr.gff3.gz",
        index_url="https://s3.amazonaws.com/igv.org.genomes/hg38/Homo_sapiens.GRCh38.94.chr.gff3.gz.tbi",
        visibility_window=1000000,
        color_by="biotype",
        color_table={
            "antisense": "blueviolet",
            "protein_coding": "blue",
            "retained_intron": "rgb(0, 150, 150)",
            "processed_transcript": "purple",
            "processed_pseudogene": "#7fff00",
            "unprocessed_pseudogene": "#d2691e",
            "*": "black"
        }
    )
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = {
        "bed",
        "gff",
        "gff3",
        "gtf",
        "bedpe",
    }
    """File formats associated with the annotation type."""

    display_mode: t.Union[t.Literal["COLLAPSED", "EXPANDED", "SQUISHED"], UnsetType] = (  # noqa: UP007
        UNSET
    )
    """Annotation track display mode. Default `"COLLAPSED"`."""

    expanded_row_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Height of each row of features in `"EXPANDED"` mode. Default `30`."""

    squished_row_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Height of each row of features in `"SQUISHED"` mode. Default `15`."""

    name_field: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """For GFF/GTF file formats. Name of column 9 to be used for feature label."""

    max_rows: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Maximum number of rows of features to display. Default `500`."""

    searchable: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Whether feature names for this track can be searched. Default `False`.

    Does not work for indexed tracks. Use with caution; it is memory intensive.
    """

    searchable_fields: t.Union[list[str], UnsetType] = UNSET  # noqa: UP007
    """Field (column 9) names to be included in feature searches.

    For use with the `searchable` option in conjunction with GFF files.

    When searching for feature attributes spaces need to be escaped with a "+"
    sign or percent encoded ("%20).
    """

    filter_types: t.Union[list[str], UnsetType] = UNSET  # noqa: UP007
    """GFF feature types to filter from display. Default `["chromosome", "gene"]`."""

    color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """CSS color value for features. Default `"rgb(0,0,150)"` (i.e. `"#000096"`)."""

    alt_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """If supplied, used for features on negative strand."""

    color_by: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Used with GFF/GTF files. Name of column 9 attribute to color features by."""

    color_table: t.Union[dict[str, str], UnsetType] = UNSET  # noqa: UP007
    """Maps attribute values to CSS colors.

    Used in conjunction with the `color_by` to assign specific colors to attributes.
    """


class GuideLine(Struct):
    """Represents a horizontal guide line."""

    color: str
    """A CSS color value."""
    dotted: bool
    """Whether the line should be dashed."""
    y: int
    """The y position. Should be between min and max."""


class WigTrack(BaseTrack, tag="wig"):
    """Displays quantititive data as either a bar chart, line plot, or points.

    Associated file formats: wig, bigWig, bedGraph.

    Ref: https://igv.org/doc/igvjs/#tracks/Wig-Track/

    Example:
    ```py
    WigTrack(
      name="CTCF",
      url="https://www.encodeproject.org/files/ENCFF356YES/@@download/ENCFF356YES.bigWig",
      min="0",
      max="30",
      color="rgb(0, 0, 150)",
      guide_lines=[
        GuideLine(color="green", dotted=True, y=25),
        GuideLine(color="red", dotted=False, y=5),
      ]
    )
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = {"wig", "bigWig", "bedGraph"}
    """File formats associated with the wig type."""

    autoscale: t.Union[bool, None] = None  # noqa: UP007
    """Autoscale track to maximum value in view."""

    autoscale_group: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """An identifier for an autoscale group.

    Tracks with the same identifier are autoscaled together.
    """

    min: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Minimum value for the data (y-axis) scale. Usually zero."""

    max: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Maximum value for the data (y-axis) scale. Ignored if `autoscale` is `True`."""

    color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """CSS color value. Default `"rgb(150,150,150)"`."""

    alt_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """If supplied, used for negative values."""

    color_scale: t.Union[dict, UnsetType] = UNSET  # noqa: UP007
    """Color scale for heatmap (graphType = "heatmap" ).

    Ref: https://igv.org/doc/igvjs/#tracks/Wig-Track/#color-scale-objects
    """

    guide_lines: t.Union[list[GuideLine], UnsetType] = UNSET  # noqa: UP007
    """Draw a horizontal line for each object in the given array."""

    graph_type: t.Union[t.Literal["bar", "points", "heatmap", "line"], UnsetType] = (  # noqa: UP007
        UNSET
    )
    """Type of graph. Default `"bar"`."""

    flip_axis: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Whether the track is drawn "upside down" with zero at top. Default `False`."""

    window_function: t.Union[t.Literal["min", "max", "mean"], UnsetType] = UNSET  # noqa: UP007
    """Governs how data is summarized when zooming out. Default `"mean"`.

    Applicable to tracks created from bigwig and tdf files.
    """


class AlignmentSorting(Struct, rename="camel"):
    """Representing initial sort order of packed alignment rows."""

    chr: str
    """Sequence (chromosome) name."""

    pos: int
    """Genomic position."""

    option: t.Literal["BASE", "STRAND", "INSERT_SIZE", "MATE_CHR", "MQ", "TAG"]
    """Parameter to sort by."""

    tag: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Tag name to sort by. Include only if option = 'TAG"""

    direction: t.Literal["ASC", "DESC"] = "ASC"
    """Sort directions."""


class AlignmentFiltering(Struct, rename="camel"):
    """Represents filtering options for alignments."""

    vendor_failed: bool = True
    """Filter alignments marked as failing vendor quality checks (bit 0x200)."""

    duplicates: bool = True
    """Filter alignments marked as a duplicate (bit 0x400)."""

    secondary: bool = False
    """Filter alignments marked as secondary (bit 0x100)."""

    supplementary: bool = False
    """Filter alignments marked as supplementary (bit 0x800)."""

    mq: int = 0
    """Filter alignments with mapping quality less than the supplied value."""

    readgroups: t.Union[set[str], UnsetType] = UNSET  # noqa: UP007
    """Read groups ('RG' tag). If present, filter alignments not matching this set."""


class AlignmentTrack(BaseTrack, tag="alignment"):
    """Display views of read alignments from BAM or CRAM files.

    Associated file formats: bam, cram.

    Ref: https://igv.org/doc/igvjs/#tracks/Alignment-Track

    Example:
    ```py
    AlignmentTrack(
      format="bam",
      name="NA12878",
      url="gs://genomics-public-data/platinum-genomes/bam/NA12878_S1.bam",
      index_url="gs://genomics-public-data/platinum-genomes/bam/NA12878_S1.bam.bai",
    )
    ```
    """

    show_coverage: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Show coverage depth track. Default `True`."""

    show_alignments: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Show individual alignments. Default `True`."""

    view_as_pairs: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Whether paired reads are drawn connected with a line. Default `False`."""

    pairs_supported: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Whether paired mate info is ignored during downsampling. Default `True`."""

    color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Default color of alignment blocks. Default `"rgb(170, 170, 170)"`."""

    deletion_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Color of line representing a deletion. Default `"black"`."""

    skipped_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Color of line representing a skipped region (e.g., splice junction).

    Default `"rgb(150, 170, 170)"`.
    """

    insertion_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Color of marker for insertions. Default `"rgb(138, 94, 161)"`."""

    neg_strand_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Color of alignment on negative strand. Default `"rgba(150, 150, 230, 0.75)"`.

    Applicable if `color_by` = `"strand"`.
    """

    pos_strand_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Color of alignment or position strand. Default `"rgba(230, 150, 150, 0.75)"`.

    Applicable if `color_by` = `"strand"`.
    """

    pair_connector_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Color of connector line between read pairs ("view as pairs" mode).

    Defaults to the alignment color.
    """

    color_by: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Color alignment by property. Default `"unexpectedPair"`.

    See: https://igv.org/doc/igvjs/#tracks/Alignment-Track/#colorby-options
    """

    group_by: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Group alignments by property.

    See: https://igv.org/doc/igvjs/#tracks/Alignment-Track/#groupby-options
    """

    sampling_window_size: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Window (bucket) size for alignment downsampling in base pairs. Default `100`."""

    sampling_depth: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Number of alignments to keep per bucket. Default 100.

    WARNING: Setting to a high value can freeze the browser when
    viewing areas of deep coverage.
    """

    readgroup: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Readgroup ID value (tag 'RG')."""

    sort: t.Union[AlignmentSorting, UnsetType] = UNSET  # noqa: UP007
    """Initial sort option.

    See: https://igv.org/doc/igvjs/#tracks/Alignment-Track/#sort-option
    """

    filter: t.Union[AlignmentFiltering, UnsetType] = UNSET  # noqa: UP007
    """Alignment filter options.

    See: https://igv.org/doc/igvjs/#tracks/Alignment-Track/#filter-options
    """

    show_soft_clips: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Show soft-clipped regions. Default `False`."""

    show_mismatches: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Highlight alignment bases which do not match the reference. Default `True`."""

    show_all_bases: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Show all bases of the read sequence. Default `False`."""

    show_insertion_text: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Show number of bases for insertions inline when zoomed in. Default `False`."""

    insertion_text_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Color for insertion count text. Default `"white"`."""

    show_deletion_text: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Show number of bases deleted inline when zoomed in. Default `False`."""

    deletion_text_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Color for deletion count text. Default `"black"`."""

    display_mode: t.Union[t.Literal["EXPANDED", "SQUISHED", "FULL"], UnsetType] = UNSET  # noqa: UP007
    """Display mode for the track. Deault `"EXPANDED"`.

      * `EXPANDED` - Pack alignments densely and draw at `alignment_row_height`
      * `SQUISHED` - Pack alignments densely and draw at `squished_row_height`
      * `FULL`     - Draw 1 alignment per row at `alignment_row_height`.
    """

    alignment_row_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Pixel height for each alignment row in `"EXPANDED"` or `"FULL"` display mode.

    Default `14`.
    """

    squished_row_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Pixel height for each alignment row in `"SQUISHED"` display mode. Default `3`."""

    coverage_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Color of coverage track. Default `"rgb(150, 150, 150)"`."""

    coverage_track_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Height in pixels of the coverage track. Default `3`."""

    autoscale: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Autoscale coverage track to maximum value in view. `True` unless `max` is set."""

    autoscale_group: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """An identifier for an autoscale group for the coverage track.

    Tracks with the same identifier are autoscaled together.
    """

    min: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Minimum value for the data (y-axis) scale. Usually zero."""

    max: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Maximum value for the data (y-axis) scale. Ignored if `autoscale` is `True`."""


class VariantTrack(BaseTrack, tag="variant"):
    """Represents variant data such as VCF files.

    Associated file formats: vcf.

    Ref: https://github.com/igvteam/igv.js/wiki/Variant-Track
    """

    # Display mode. 'COLLAPSED' => show variants only,
    # 'SQUISHED' and 'EXPANDED' => show calls.
    display_mode: t.Literal["COLLAPSED", "EXPANDED", "SQUISHED"] = "EXPANDED"
    # Height of genotype call rows in SQUISHED mode.
    squished_call_height: int = 1
    # Height of genotype call rows in EXPANDED mode
    expanded_call_height: int = 10


Track = t.Union[AnnotationTrack, WigTrack, AlignmentTrack, VariantTrack]
