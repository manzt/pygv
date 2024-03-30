import igv from "https://esm.sh/igv@2.15.11";

/** @typedef {{ _genome: string, _tracks: Record<string, unknown>[], _locus: string }} Model */

/** @type {import("npm:@anywidget/types").Render<Model>} */
async function render({ model, el }) {
  const browser = await igv.createBrowser(el, {
    genome: model.get("_genome"),
    locus: model.get("_locus"),
    tracks: model.get("_tracks"),
  });
  globalThis.browser = browser;
  return () => {
    igv.removeBrowser(browser);
  };
}

export default { render };
