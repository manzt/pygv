from __future__ import annotations

import typing as t

from msgspec import UNSET, Struct, UnsetType, field

__all__ = [
    "AlignmentTrack",
    "AnnotationTrack",
    "ArcTrack",
    "CnvPytorTrack",
    "InteractTrack",
    "MergedTrack",
    "MutationTrack",
    "QtlTrack",
    "SegmentedCopyNumberTrack",
    "SpliceJunctionTrack",
    "Track",
    "VariantTrack",
    "WigTrack",
]


class BaseTrack(Struct, rename="camel", repr_omit_defaults=True, omit_defaults=True):
    """Represents a browser track.

    For a full configuration options, see the [IGV.js docs](https://igv.org/doc/igvjs/#tracks/Tracks)
    """

    name: str
    """Display name (label). Required."""

    url: str
    """URL to the track data resource, such as a file or webservice, or a data URI."""

    index_url: t.Union[str, UnsetType] = field(default=UNSET, name="indexURL")
    """URL to a file index, such as a BAM .bai, tabix .tbi, or tribble .idx file.

    For indexed file access the index URL is required, if absent the entire file
    will be read.
    """

    source_type: t.Union[t.Literal["file", "htsget", "custom"], UnsetType] = UNSET
    """Type of data source."""

    format: t.Union[str, UnsetType] = UNSET
    """No default. If not specified, format is inferred from file name extension."""

    indexed: t.Union[bool, UnsetType] = UNSET
    """Explicitly indicate whether the resource is indexed.

    This flag is redundant if `index_url` is provided. It can be used to load small
    BAM files without an index by setting to `False`
    """

    order: t.Union[int, UnsetType] = UNSET
    """Integer value specifying relative order of track position on the screen.

    To pin a track to the bottom use a very large value.
    If no order is specified, tracks appear in order of their addition.
    """

    color: t.Union[str, UnsetType] = UNSET
    """CSS color value for track features, e.g. "#ff0000" or "rgb(100,0,100)"."""

    height: t.Union[int, UnsetType] = UNSET
    """Initial height of track viewport in pixels. Default 50."""

    min_height: t.Union[int, UnsetType] = UNSET
    """Minimum height of track in pixels. Default 50."""

    max_height: t.Union[int, UnsetType] = UNSET
    """Maximum height of track in pixels. Default 500."""

    visibility_window: t.Union[int, UnsetType] = UNSET
    """Maximum window size in base pairs for which indexed annotations or
    variants are displayed.

    1 MB for variants, 30 KB for alignments, whole chromosome for
    other track types.
    """

    removable: t.Union[bool, UnsetType] = UNSET
    """If true a "remove" item is included in the track menu. Default `True`."""

    headers: t.Union[dict[str, str], UnsetType] = UNSET
    """HTTP headers to include with each request.

    For example `{"Authorization": "Bearer cn389ncoiwuencr"}`.
    """

    oauth_token: t.Union[str, UnsetType] = UNSET
    """OAuth token, or function returning an OAuth token.

    The value will be included as a Bearer token with each request.
    """

    id: t.Union[str, UnsetType] = UNSET
    """An identifier for this track."""

    associated_file_formats: t.ClassVar[set[str]] = field(default_factory=lambda: set())
    """File formats associated with this track type."""


class AnnotationTrack(BaseTrack, tag="annotation"):
    """Display views of genomic annotations.

    Associated file formats: bed, gff, gff3, gtf, bedpe (and more).

    Ref: https://igv.org/doc/igvjs/#tracks/Annotation-Track

    Example:
    ```py
    AnnotationTrack(
        name="Color by attribute biotype",
        format="gff3",
        display_mode="EXPANDED",
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

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {
            "bed",
            "gff",
            "gff3",
            "gtf",
            "bedpe",
        }
    )
    """File formats associated with the annotation type."""

    display_mode: t.Union[t.Literal["COLLAPSED", "EXPANDED", "SQUISHED"], UnsetType] = (
        UNSET
    )
    """Annotation track display mode. Default `"COLLAPSED"`."""

    expanded_row_height: t.Union[int, UnsetType] = UNSET
    """Height of each row of features in `"EXPANDED"` mode. Default `30`."""

    squished_row_height: t.Union[int, UnsetType] = UNSET
    """Height of each row of features in `"SQUISHED"` mode. Default `15`."""

    name_field: t.Union[str, UnsetType] = UNSET
    """For GFF/GTF file formats. Name of column 9 to be used for feature label."""

    max_rows: t.Union[int, UnsetType] = UNSET
    """Maximum number of rows of features to display. Default `500`."""

    searchable: t.Union[bool, UnsetType] = UNSET
    """Whether feature names for this track can be searched. Default `False`.

    Does not work for indexed tracks. Use with caution; it is memory intensive.
    """

    searchable_fields: t.Union[list[str], UnsetType] = UNSET
    """Field (column 9) names to be included in feature searches.

    For use with the `searchable` option in conjunction with GFF files.

    When searching for feature attributes spaces need to be escaped with a "+"
    sign or percent encoded ("%20).
    """

    filter_types: t.Union[list[str], UnsetType] = UNSET
    """GFF feature types to filter from display. Default `["chromosome", "gene"]`."""

    color: t.Union[str, UnsetType] = UNSET
    """CSS color value for features. Default `"rgb(0,0,150)"` (i.e. `"#000096"`)."""

    alt_color: t.Union[str, UnsetType] = UNSET
    """If supplied, used for features on negative strand."""

    color_by: t.Union[str, UnsetType] = UNSET
    """Used with GFF/GTF files. Name of column 9 attribute to color features by."""

    color_table: t.Union[dict[str, str], UnsetType] = UNSET
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

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"wig", "bigWig", "bedGraph"}
    )
    """File formats associated with the wig type."""

    autoscale: t.Union[bool, None] = None
    """Autoscale track to maximum value in view."""

    autoscale_group: t.Union[str, UnsetType] = UNSET
    """An identifier for an autoscale group.

    Tracks with the same identifier are autoscaled together.
    """

    min: t.Union[int, UnsetType] = UNSET
    """Minimum value for the data (y-axis) scale. Usually zero."""

    max: t.Union[int, UnsetType] = UNSET
    """Maximum value for the data (y-axis) scale. Ignored if `autoscale` is `True`."""

    color: t.Union[str, UnsetType] = UNSET
    """CSS color value. Default `"rgb(150,150,150)"`."""

    alt_color: t.Union[str, UnsetType] = UNSET
    """If supplied, used for negative values."""

    color_scale: t.Union[dict, UnsetType] = UNSET
    """Color scale for heatmap (graphType = "heatmap" ).

    Ref: https://igv.org/doc/igvjs/#tracks/Wig-Track/#color-scale-objects
    """

    guide_lines: t.Union[list[GuideLine], UnsetType] = UNSET
    """Draw a horizontal line for each object in the given array."""

    graph_type: t.Union[t.Literal["bar", "points", "heatmap", "line"], UnsetType] = (
        UNSET
    )
    """Type of graph. Default `"bar"`."""

    flip_axis: t.Union[bool, UnsetType] = UNSET
    """Whether the track is drawn "upside down" with zero at top. Default `False`."""

    window_function: t.Union[t.Literal["min", "max", "mean"], UnsetType] = UNSET
    """Governs how data is summarized when zooming out. Default `"mean"`.

    Applicable to tracks created from bigwig and tdf files.
    """


class AlignmentSorting(Struct, rename="camel"):
    """Represents initial sort order of packed alignment rows."""

    chr: str
    """Sequence (chromosome) name."""

    pos: int
    """Genomic position."""

    option: t.Literal["BASE", "STRAND", "INSERT_SIZE", "MATE_CHR", "MQ", "TAG"]
    """Parameter to sort by."""

    tag: t.Union[str, UnsetType] = UNSET
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

    readgroups: t.Union[set[str], UnsetType] = UNSET
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

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"bam", "cram"}
    )
    """File formats associated with the alignment type."""

    show_coverage: t.Union[bool, UnsetType] = UNSET
    """Show coverage depth track. Default `True`."""

    show_alignments: t.Union[bool, UnsetType] = UNSET
    """Show individual alignments. Default `True`."""

    view_as_pairs: t.Union[bool, UnsetType] = UNSET
    """Whether paired reads are drawn connected with a line. Default `False`."""

    pairs_supported: t.Union[bool, UnsetType] = UNSET
    """Whether paired mate info is ignored during downsampling. Default `True`."""

    color: t.Union[str, UnsetType] = UNSET
    """Default color of alignment blocks. Default `"rgb(170, 170, 170)"`."""

    deletion_color: t.Union[str, UnsetType] = UNSET
    """Color of line representing a deletion. Default `"black"`."""

    skipped_color: t.Union[str, UnsetType] = UNSET
    """Color of line representing a skipped region (e.g., splice junction).

    Default `"rgb(150, 170, 170)"`.
    """

    insertion_color: t.Union[str, UnsetType] = UNSET
    """Color of marker for insertions. Default `"rgb(138, 94, 161)"`."""

    neg_strand_color: t.Union[str, UnsetType] = UNSET
    """Color of alignment on negative strand. Default `"rgba(150, 150, 230, 0.75)"`.

    Applicable if `color_by` = `"strand"`.
    """

    pos_strand_color: t.Union[str, UnsetType] = UNSET
    """Color of alignment or position strand. Default `"rgba(230, 150, 150, 0.75)"`.

    Applicable if `color_by` = `"strand"`.
    """

    pair_connector_color: t.Union[str, UnsetType] = UNSET
    """Color of connector line between read pairs ("view as pairs" mode).

    Defaults to the alignment color.
    """

    color_by: t.Union[str, UnsetType] = UNSET
    """Color alignment by property. Default `"unexpectedPair"`.

    See: https://igv.org/doc/igvjs/#tracks/Alignment-Track/#colorby-options
    """

    group_by: t.Union[str, UnsetType] = UNSET
    """Group alignments by property.

    See: https://igv.org/doc/igvjs/#tracks/Alignment-Track/#groupby-options
    """

    sampling_window_size: t.Union[int, UnsetType] = UNSET
    """Window (bucket) size for alignment downsampling in base pairs. Default `100`."""

    sampling_depth: t.Union[int, UnsetType] = UNSET
    """Number of alignments to keep per bucket. Default 100.

    WARNING: Setting to a high value can freeze the browser when
    viewing areas of deep coverage.
    """

    readgroup: t.Union[str, UnsetType] = UNSET
    """Readgroup ID value (tag 'RG')."""

    sort: t.Union[AlignmentSorting, UnsetType] = UNSET
    """Initial sort option.

    See: https://igv.org/doc/igvjs/#tracks/Alignment-Track/#sort-option
    """

    filter: t.Union[AlignmentFiltering, UnsetType] = UNSET
    """Alignment filter options.

    See: https://igv.org/doc/igvjs/#tracks/Alignment-Track/#filter-options
    """

    show_soft_clips: t.Union[bool, UnsetType] = UNSET
    """Show soft-clipped regions. Default `False`."""

    show_mismatches: t.Union[bool, UnsetType] = UNSET
    """Highlight alignment bases which do not match the reference. Default `True`."""

    show_all_bases: t.Union[bool, UnsetType] = UNSET
    """Show all bases of the read sequence. Default `False`."""

    show_insertion_text: t.Union[bool, UnsetType] = UNSET
    """Show number of bases for insertions inline when zoomed in. Default `False`."""

    insertion_text_color: t.Union[str, UnsetType] = UNSET
    """Color for insertion count text. Default `"white"`."""

    show_deletion_text: t.Union[bool, UnsetType] = UNSET
    """Show number of bases deleted inline when zoomed in. Default `False`."""

    deletion_text_color: t.Union[str, UnsetType] = UNSET
    """Color for deletion count text. Default `"black"`."""

    display_mode: t.Union[t.Literal["EXPANDED", "SQUISHED", "FULL"], UnsetType] = UNSET
    """Display mode for the track. Deault `"EXPANDED"`.

      * `EXPANDED` - Pack alignments densely and draw at `alignment_row_height`
      * `SQUISHED` - Pack alignments densely and draw at `squished_row_height`
      * `FULL`     - Draw 1 alignment per row at `alignment_row_height`.
    """

    alignment_row_height: t.Union[int, UnsetType] = UNSET
    """Pixel height for each alignment row in `"EXPANDED"` or `"FULL"` display mode.

    Default `14`.
    """

    squished_row_height: t.Union[int, UnsetType] = UNSET
    """Pixel height for each alignment row in `"SQUISHED"` display mode. Default `3`."""

    coverage_color: t.Union[str, UnsetType] = UNSET
    """Color of coverage track. Default `"rgb(150, 150, 150)"`."""

    coverage_track_height: t.Union[int, UnsetType] = UNSET
    """Height in pixels of the coverage track. Default `3`."""

    autoscale: t.Union[bool, UnsetType] = UNSET
    """Autoscale coverage track to maximum value in view. `True` unless `max` is set."""

    autoscale_group: t.Union[str, UnsetType] = UNSET
    """An identifier for an autoscale group for the coverage track.

    Tracks with the same identifier are autoscaled together.
    """

    min: t.Union[int, UnsetType] = UNSET
    """Minimum value for the data (y-axis) scale. Usually zero."""

    max: t.Union[int, UnsetType] = UNSET
    """Maximum value for the data (y-axis) scale. Ignored if `autoscale` is `True`."""


class VariantTrack(BaseTrack, tag="variant"):
    """Displays variant records from "VCF" files or equivalents.

    Associated file formats: vcf.

    Ref: https://igv.org/doc/igvjs/#tracks/Variant-Track/

    Example:
    ```py
    # Basic

    VariantTrack(
        format="vcf",
        url="https://s3.amazonaws.com/1000genomes/release/20130502/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
        index_url="https://s3.amazonaws.com/1000genomes/release/20130502/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz.tbi",
        name="1KG variants (chr22)",
        squished_call_height=1,
        expanded_call_height=4,
        display_mode="SQUISHED",
        visibility_window=1000
    )

    # Color-by info field with color table

    VariantTrack(
        url="https://s3.amazonaws.com/igv.org.demo/nstd186.GRCh38.variant_call.vcf.gz",
        index_url="https://s3.amazonaws.com/igv.org.demo/nstd186.GRCh38.variant_call.vcf.gz.tbi",
        name="Color by table, SVTYPE",
        visibility_window=-1,
        color_by="SVTYPE",
        color_table={
            "DEL": "#ff2101",
            "INS": "#001888",
            "DUP": "#028401",
            "INV": "#008688",
            "CNV": "#8931ff",
            "BND": "#891100",
            "*": "#002eff",
        },
    )
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"vcf"}
    )
    """File formats associated with the variant type."""

    display_mode: t.Union[t.Literal["COLLAPSED", "EXPANDED", "SQUISHED"], UnsetType] = (
        UNSET
    )
    """Display option.  Default `"EXPANDED"`.

        * 'COLLAPSED' => show variants only
        * 'SQUISHED' and 'EXPANDED' => show calls.
    """

    squished_call_height: t.Union[int, UnsetType] = UNSET
    """Height of genotype call rows in `"SQUISHED"` mode. Default `1`."""

    expanded_call_height: t.Union[int, UnsetType] = UNSET
    """Height of genotype call rows in EXPANDED mode. Default `10`."""

    # Variant color options

    color: t.Union[str, UnsetType] = UNSET
    """A CSS color value for a variant."""

    color_by: t.Union[str, UnsetType] = UNSET
    """Specify an `INFO` field to color variants by.

    Optional, if specified takes precedence over `color` property.
    """

    color_table: t.Union[dict[str, str], UnsetType] = UNSET
    """Color table mapping `INFO` field values to colors.

    Use in conjunction with `color_by`.

    Optional, if not specified a color table will be generated.
    """

    # Genotype color options

    no_call_color: t.Union[str, UnsetType] = UNSET
    """Color for no-calls. Default `"rgb(250, 250, 250)"`."""

    homevar_color: t.Union[str, UnsetType] = UNSET
    """CSS color for homozygous non-reference calls. Default `"rgb(17,248,254)"`"""

    hetvar_color: t.Union[str, UnsetType] = UNSET
    """CSS color for heterozygous calls. Default `"rgb(34,12,253)"`."""

    homref_color: t.Union[str, UnsetType] = UNSET
    """CSS color for homozygous reference calls. Default `"rgb(200, 200, 200)"`."""


class MutationTrack(BaseTrack, tag="mut"):
    """Displays data from the National Cancer Institute's "mut" and "maf" file formats.

    Associated file formats: mut, maf.

    Ref: https://igv.org/doc/igvjs/#tracks/Mutation-Track

    Example:
    ```py
    MutationTrack(
        format="maf",
        url="https://s3.amazonaws.com/igv.org.demo/TCGA.BRCA.mutect.995c0111-d90b-4140-bee7-3845436c3b42.DR-10.0.somatic.maf.gz",
        indexed=False,
        height=700,
        display_mode="EXPANDED",
    )
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"mut", "maf"}
    )
    """File formats associated with the mut type."""

    display_mode: t.Union[t.Literal["EXPANDED", "SQUISHED", "COLLAPSED"], UnsetType] = (
        UNSET
    )
    """The track display mode. Default `"EXPANDED"`."""


class SegmentedCopyNumberSorting(Struct, rename="camel"):
    """Represents initial sort order of segmented copy number rows."""

    chr: str
    """Sequence (chromosome) name."""

    start: int
    """Position start."""

    end: int
    """Position end."""

    direction: t.Literal["ASC", "DESC"]
    """Sort direction."""


class SegmentedCopyNumberTrack(BaseTrack, tag="seg"):
    """Displays segmented copy number values as a heatmap.

    Associated file formats: seg.

    Ref: https://igv.org/doc/igvjs/#tracks/Seg-Track

    * Red = amplifications
    * Blue = deletions

    There are 2 common conventions for values in segmented copy number files,
    the copy number itself, and a log score computed from:

    ```py
    score = 2 * np.log2(copy_number / 2)
    ```

    The value type is indicated by the `is_log` property.

    If no value is set for `is_log`, it is inferred by the values in the file:

    * all positive values => `is_log` = `False`
    * any negative values => `is_log` = `True`

    Example:
    ```py
    SegmentedCopyNumberTrack(
        format="seg",
        url="https://s3.amazonaws.com/igv.org.demo/GBM-TP.seg.gz",
        indexed=False,
        is_log=True,
        name="GBM Copy # (TCGA Broad GDAC)",
        sort=SegmentedCopyNumberSorting(
            direction="DESC",
            chr="chr7",
            start=55174641,
            end=55175252,
        ),
    )
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"seg"}
    )
    """File formats associated with the seg type."""

    display_mode: t.Union[t.Literal["EXPANDED", "SQUISHED", "FILL"], UnsetType] = UNSET
    """Track display mode.

    Affects the sample height (height of each row). The "FILL" value will result in all
    samples visible in the track view.
    """

    sort: t.Union[SegmentedCopyNumberSorting, UnsetType] = UNSET
    """The initial sort order."""


class GwasColumns(Struct, rename="camel"):
    """Declaration of column number for chrom, position, & value."""

    chromosome: int
    """Chromosome number"""
    position: int
    """Genomic position"""
    value: int
    """Value."""


class GwasTrack(BaseTrack, tag="gwas"):
    """Display genome wide association data as a "manhattan" style plot.

    Associated file formats: bed, gwas.

    Ref: https://igv.org/doc/igvjs/#tracks/GWAS

    Example:
    ```py
    GwasTrack(
        format="gwas",
        name="GWAS sample",
        url="https://s3.amazonaws.com/igv.org.demo/gwas_sample.tsv.gz",
        indexed=False,
        columns=GwasColumns(
            chromosome=12,
            position=13,
            value=28,
        ),
    )
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"bed", "gwas"}
    )
    """File formats associated with the gwas type."""

    min: t.Union[int, UnsetType] = UNSET
    """Sets the minimum value for the data (y-axis) scale. Default `0`."""

    max: t.Union[int, UnsetType] = UNSET
    """Sets the maximum value for the data (y-axis) scale.

    Default `25` for p-value (-log10(pvalue)), `1` for posterior probability.
    """

    posterior_probability: t.Union[bool, UnsetType] = UNSET
    """Whether to interpret values as probabilities within range 0-1. Default `False`.

    By default values are treated as p-values and plotted as -log10(P-value).
    """

    dot_size: t.Union[int, UnsetType] = UNSET
    """Diameter of dots in pixels. Default `3`."""

    columns: t.Union[GwasColumns, UnsetType] = UNSET
    """Declaration of column number for chromosome, position, and value.

    For gwas format only.
    """

    color_table: t.Union[dict[str, str], UnsetType] = UNSET
    """Object mapping chromosome names -> colors.

    If supplied all chromosomes in data should be included.

    See defaults: https://igv.org/doc/igvjs/#tracks/GWAS/#default-color-table
    """


class InteractTrack(BaseTrack, tag="interact"):
    """Display pairwise interactions between genome regions as arcs.

    Associated file formats: bedpe, interact, bigInteract

    Ref: https://igv.org/doc/igvjs/#tracks/Interact

    Example:
    ```py
    Config(
        genome="hg38",
        locus="chr2:65,489,209-65,795,733",
        tracks=[
            InteractTrack(
                url="https://s3.amazonaws.com/igv.org.demo/GSM1872886_GM12878_CTCF_PET.bedpe.txt",
                format="bedpe",
                name="CTCF PET - proportional",
                arc_type="proportional",
                arc_orientation="UP",
                color="rgb(0,200,0)",
                log_scale=true,
                max=80,
                visibility_window=10_000_000,
            ),
            InteractTrack(
                url="https://s3.amazonaws.com/igv.org.demo/GSM1872886_GM12878_CTCF_PET.bedpe.txt",
                format="bedpe",
                name="CTCF PET - nested",
                arc_type="nested",
                arc_orientation="DOWN",
                color="blue",
                alpha=0.15,
                visibility_window=10_000_000,
            ),
        ],
    )
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"bedpe", "interact", "bigInteract"}
    )
    """File formats associated with the gwas type."""

    arc_type: t.Union[
        t.Literal["nested", "proportional", "inView", "partialInView"], UnsetType
    ] = UNSET
    """The arc type. Default `"nested"`.

    * nested - Arc height is proportional to feature width.
    * propotional - Arc height is proportional to feature score.
    * inView - Proportional, only draw arcs that are completely in view.
    * partialInView - Proportional, only draw arcs that are whole or partially in view.
    """

    arc_orientation: t.Union[t.Literal["UP", "DOWN"], UnsetType] = UNSET
    """Direction of arcs ("UP" or "DOWN"). Default `"UP"`."""

    alpha: t.Union[float, UnsetType] = UNSET
    """Alpha transparency to apply to arcs that extend beyond viewport.

    Must be between `0` and `1`. Default `0.5`.
    """

    thickness: t.Union[int, UnsetType] = UNSET
    """Line thickness. Default `2`."""


class QtlTrack(BaseTrack, tag="qtl"):
    """Displays xQTL data.

    Associated file formats: qtl

    Ref: https://igv.org/doc/igvjs/#tracks/QTL-Track

    Example:
    ```py
    QtlTrack(
        format="qtl",
        name="B cell eQTL",
        url="https://igv-genepattern-org.s3.amazonaws.com/test/qtl/B.cell_eQTL.tsv.gz",
        index_url="https://igv-genepattern-org.s3.amazonaws.com/test/qtl/B.cell_eQTL.tsv.gz.tbi",
        visibility_window=4_000_000,
    )
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"qtl"}
    )
    """File formats associated with the gwas type."""

    min: t.Union[float, UnsetType] = UNSET
    """Minimum value of y-axis in -log10 units. Default `3.5`."""

    max: t.Union[float, UnsetType] = UNSET
    """Maximum value of y-axis in -log10 units.

    Optional, if not specified max is set as a percentile of values in view.
    """

    autoscale_percentile: t.Union[float, UnsetType] = UNSET
    """Upper percentile for setting max value when autoscaling.

    Number between `0` and `100`. Default `98`.
    """


class SpliceJunctionTrack(BaseTrack, tag="junction"):
    """Displays splice junction information.

    Associated file formats: bed.

    Ref: https://igv.org/doc/igvjs/#tracks/Splice-Junctions

    Example:
    ```python
    SpliceJunctionTrack(
        name="Junctions",
        format="bed",
        url="https://www.dropbox.com/s/nvmy55hhe24plpv/splice_junction_track_test_cases_sampleA.chr15-92835700-93031800.SJ.out.bed.gz?dl=0",
        index_url="https://www.dropbox.com/s/iv5tcg3t8v3xu23/splice_junction_track_test_cases_sampleA.chr15-92835700-93031800.SJ.out.bed.gz.tbi?dl=0",
        display_mode="COLLAPSED",
        min_uniquely_mapped_reads=1,
        min_total_reads=1,
        max_fraction_multi_mapped_reads=1,
        min_spliced_alignment_overhang=0,
        thickness_based_on="numUniqueReads",
        bounce_height_based_on="random",
        color_by="isAnnotatedJunction",
        label_unique_read_count=True,
        label_multi_mapped_read_count=True,
        label_total_read_count=False,
        label_motif=False,
        label_is_annotated_junction=" [A]",
        hide_annotated_junctions=False,
        hide_unannotated_junctions=False,
        hide_motifs=["GT/AT", "non-canonical"],
    )
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"bed"}
    )
    """File formats associated with the splice junction track type."""

    # Display Options

    color_by: t.Union[
        t.Literal[
            "numUniqueReads", "numReads", "isAnnotatedJunction", "strand", "motif"
        ],
        UnsetType,
    ] = UNSET
    """Splice junction color. Default `"numUniqueReads"`."""

    color_by_num_reads_threshold: t.Union[int, UnsetType] = UNSET
    """Threshold for `color_by`. Default `5`.

    If `color_by` is set to `"numUniqueReads"` or `"numReads"`, junction color will
    be darker when number of reads exceeds this threshold.
    """

    thickness_based_on: t.Union[
        t.Literal["numUniqueReads", "numReads", "isAnnotatedJunction"], UnsetType
    ] = UNSET
    """Splice junction line thickness. Default `"numUniqueReads"`."""

    bounce_height_based_on: t.Union[
        t.Literal["random", "distance", "thickness"], UnsetType
    ] = UNSET
    """Splice junction curve height. Default `"random"`."""

    label_unique_read_count: t.Union[bool, UnsetType] = UNSET
    """Add unique read counts to splice junction label. Default `True`."""

    label_multi_mapped_read_count: t.Union[bool, UnsetType] = UNSET
    """Add multi-mapped read counts to splice junction label. Default `True`."""

    label_total_read_count: t.Union[bool, UnsetType] = UNSET
    """Add total read counts to splice junction label. Default `False`."""

    label_motif: t.Union[bool, UnsetType] = UNSET
    """Add splice junction motif to its label. Default `False`."""

    label_annotated_junction: t.Union[str, UnsetType] = UNSET
    """Label annotation for junction.

    If defined, the string will be appended to the labels of splice junctions that exist
    in known gene models.
    """

    # Filtering Options

    min_uniquely_mapped_reads: t.Union[int, UnsetType] = UNSET
    """Junction must be supported by at least this many uniquely-mapped reads.

    Default `0`.
    """

    min_total_reads: t.Union[int, UnsetType] = UNSET
    """Junction must be supported by at least this many uniquely-mapped + multi-mapped reads.

    Default `0`.
    """  # noqa: E501

    max_fraction_multi_mapped_reads: t.Union[float, UnsetType] = UNSET
    """(Uniquely-mapped reads) / (Total reads) must be <= this threshold.

    Default `1`.
    """

    min_spliced_alignment_overhang: t.Union[int, UnsetType] = UNSET
    """Minimum spliced alignment overhang in base pairs. Default `0`.

    See [STAR aligner docs](https://github.com/alexdobin/STAR/blob/master/doc/STARmanual.pdf) for details.
    """  # noqa: E501

    hide_strand: t.Union[t.Literal["+", "-"], UnsetType] = UNSET
    """Set to "+" or "-" to hide junctions on the plus or minus strand."""

    hide_annotated_junctions: t.Union[bool, UnsetType] = UNSET
    """Whether to hide annotated junctions. Default `False`.

    If `True`, only novel junctions will be shown (e.g., those not found in gene models passed to the aligner).
    """  # noqa: E501

    hide_unannotated_junctions: t.Union[bool, UnsetType] = UNSET
    """Whether to hide unannotated junctions. Default `False`.

    If `True`, only annotated junctions will be shown (eg. those found in gene models passed to the aligner).
    """  # noqa: E501

    hide_motifs: t.Union[list[str], UnsetType] = UNSET
    """A list of strings for motif values to hide.

    For example: ["GT/AT", "non-canonical"]
    """


class CnvPytorTrack(BaseTrack, tag="cnvpytor"):
    """Displays read depth and B-allele frequency (BAF) of variants.

    Associated file formats: pytor, vcf

    Ref: https://igv.org/doc/igvjs/#tracks/CNVPytor

    Example:
    ```python
    CnvPytorTrack(
        id="pytor_track",
        name="HepG2 pytor",
        url="https://storage.googleapis.com/cnvpytor_data/HepG2_WGS.pytor",
    )
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"pytor", "vcf"}
    )
    """File formats associated with the splice cnvpytor track type."""

    signal_name: t.Union[t.Literal["rd_snp", "rd", "snp"], UnsetType] = field(
        default=UNSET, name="signal_name"
    )
    """Signal name. Default `"rd_nsp"`

    * rd_snp : Read Depth and BAF Likelihood
    * rd : Read depth
    * snp : BAF likelihood
    """

    cnv_caller: t.Union[t.Literal["ReadDepth", "2D"], UnsetType] = field(
        default=UNSET, name="cnv_caller"
    )
    """Name of CNV caller. Default `"2D"`.

    Shows data based on available caller data.

    * ReadDepth: Uses Read depth information only
    * 2D: Uses both Read depth and BAF information
    """

    bin_size: t.Union[int, UnsetType] = field(default=UNSET, name="bin_size")
    """Bin size. Default `100_000`.

    * pytor file: Bin size should be avialable in the pytor file
    * vcf: Bin size should be multiple of 10,000
    """

    colors: t.Union[list[str], UnsetType] = UNSET
    """Color of the signals. Signal details are in file format section.

    Default `["gray", "black", "green", "blue"]`.
    """


class MergedTrack(BaseTrack, tag="merged"):
    """Overlay multiple wig tracks.

    Ref: https://igv.org/doc/igvjs/#tracks/Merged/

    Example:
    ```py
    MergedTrack(
        name="Merged",
        height=50,
        alpha=0.5,
        tracks=[
            WigTrack(
                format="bigwig",
                url="https://www.encodeproject.org/files/ENCFF000ASJ/@@download/ENCFF000ASJ.bigWig",
                color="red",
            ),
            WigTrack(
                format="bigwig",
                url="https://www.encodeproject.org/files/ENCFF351WPV/@@download/ENCFF351WPV.bigWig",
                color="green",
            ),
        ],
    )
    ```
    """

    tracks: list[WigTrack] = []
    """Child wig tracks."""

    alpha: t.Union[float, UnsetType] = UNSET
    """Alpha transparency to apply to individual track colors.

    Number between `0` and `1`. Default `0.5`.
    """


class ArcTrack(BaseTrack, tag="arc"):
    """Displays RNA secondary structures in arcs connecting base pairs.

    Associated file formats: bp, bed

    Ref: https://igv.org/doc/igvjs/#tracks/Arc-Track

    Alternative structures, where one nucleotide is involved in more than one base pair,
    and pseudo knots, where arcs cross, can be accommodated.

    Example:
    ```py
    ArcTrack(format="bp", name="RNA Struct BP", url="example.bp")
    ```
    """

    associated_file_formats: t.ClassVar[set[str]] = field(
        default_factory=lambda: {"bp", "bed"}
    )
    """File formats associated with the arc type."""

    arc_orientation: t.Union[t.Literal["UP", "DOWN"], UnsetType] = UNSET
    """Direction of arcs ("UP" or "DOWN"). Default `"UP"`."""


Track = t.Union[
    AnnotationTrack,
    WigTrack,
    AlignmentTrack,
    VariantTrack,
    MutationTrack,
    SegmentedCopyNumberTrack,
    InteractTrack,
    QtlTrack,
    SpliceJunctionTrack,
    CnvPytorTrack,
    MergedTrack,
    ArcTrack,
]
