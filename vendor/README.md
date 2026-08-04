# Vendored third-party code

Self-hosted deliberately. The site otherwise makes **no third-party runtime
requests except Google Fonts and the Cloudflare-hosted reel**, and the privacy
notice says so — pulling these from a CDN would quietly make that untrue.

| Path | What | Version | Licence |
|---|---|---|---|
| `model-viewer.min.js` | Google `<model-viewer>` web component | fetched 2026-08-04 from jsDelivr | BSD-3-Clause |
| `draco/draco_wasm_wrapper.js`, `draco/draco_decoder.wasm` | Draco mesh decoder | 1.5.6 | Apache-2.0 |

## Why Draco is here at all

`st-mary-magdalene-building.glb` declares `KHR_draco_mesh_compression` in
`extensionsRequired`, so the model **cannot** be decoded without it.
`model-viewer` would otherwise fetch the decoder from
`https://www.gstatic.com/draco/versioned/decoders/1.5.6/` at runtime. The page
overrides that with:

```js
customElements.get('model-viewer').dracoDecoderLocation = 'vendor/draco/';
```

**If you upgrade `model-viewer`, check which Draco version it expects** and
replace the decoder to match, or the model will silently fail to load.

`CESIUM_RTC` is also declared on the model but is **not** required — the vertices
are already local to the origin, so ignoring it yields correctly-centred geometry.
Do not "fix" this.

## Loading

Nothing in here is loaded on page load. The model section shows a 98 KB poster
render and injects `model-viewer.min.js` only when the visitor presses the button.
