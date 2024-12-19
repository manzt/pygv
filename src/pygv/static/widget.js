import igv from "https://esm.sh/igv@3.1.2";

/** @typedef {{ _genome: string, _tracks: Record<string, unknown>[], _locus: string }} Model */

/** @type {import("npm:@anywidget/types").Render<Model>} */
async function render({ model, el }) {
  const browser = await igv.createBrowser(el, {
    genome: model.get("_genome"),
    locus: model.get("_locus"),
    tracks: model.get("_tracks"),
  });
  return () => {
    igv.removeBrowser(browser);
  };
}

export default { render };
