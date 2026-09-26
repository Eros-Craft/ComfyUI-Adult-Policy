// ErosCraft: the ➕ Civitai Red LoRA picker for Qwen Image 2.1.
//
// WHY THE SERVER SEARCHES: ComfyUI serves its page with `Content-Security-Policy: connect-src 'self' data:`, so a
// fetch from this page to civitai.red is refused by the browser (measured on the brand's Krea 2 product, 2026-09-18).
// The search and the download both go through this pack's own routes, same-origin. The download also has to: it is
// the only place the Civitai token exists, and the token is never sent to this page nor written into a workflow.
//
// WHAT IS HIDDEN, on the server, at search time AND again at download time: anything flagged as a real person's
// likeness, a minor, or SFW-only, and anything whose name or tags suggest a minor, a likeness or non-consent. The
// page draws only what the server returned.
import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

const PICKER_NODE = "Qwen21LoraPicker";
const PICKER_WIDGET = "lora_name";
const ROW_BUTTON = "qwen21-civitai-pick";

async function post(route, body) {
  const r = await api.fetchApi(route, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.error || `the server answered ${r.status}`);
  return d;
}

function modal() {
  const back = document.createElement("div");
  back.style.cssText = "position:fixed;inset:0;background:#000c;z-index:10000;display:flex;"
    + "align-items:center;justify-content:center";
  const box = document.createElement("div");
  box.style.cssText = "background:#1e1e1e;color:#eee;width:min(900px,92vw);height:min(80vh,720px);"
    + "border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:10px;font:13px system-ui";
  box.innerHTML = `
    <div style="display:flex;gap:8px;align-items:center">
      <strong style="flex:1">Civitai Red · Qwen Image 2.1 LoRAs</strong>
      <input class="q" placeholder="search" style="flex:2;padding:6px 8px;border-radius:6px;
             border:1px solid #555;background:#111;color:#eee">
      <button class="go" style="padding:6px 12px;border-radius:6px;cursor:pointer">Search</button>
      <button class="x" style="padding:6px 12px;border-radius:6px;cursor:pointer">Close</button>
    </div>
    <div class="note" style="opacity:.7">Real-person, minor and SFW-only resources are not listed. Picking one
      downloads it with the server's own Civitai token. Qwen Image 2.1 is research and non-commercial use only.</div>
    <div class="grid" style="flex:1;overflow:auto;display:grid;
         grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px"></div>
    <div class="status" style="min-height:1.2em;opacity:.8"></div>`;
  back.appendChild(box);
  document.body.appendChild(back);
  const close = () => back.remove();
  box.querySelector(".x").onclick = close;
  back.onclick = (e) => { if (e.target === back) close(); };
  return { close, grid: box.querySelector(".grid"), status: box.querySelector(".status"),
           q: box.querySelector(".q"), go: box.querySelector(".go") };
}

// BUILT WITH DOM METHODS, NOT innerHTML. Every string here (a model's name, its creator, a preview URL) was written
// by a stranger who uploaded to a public catalogue; textContent cannot run it, and the URL is checked for https.
function card(title, sub, imageUrl, badge) {
  const c = document.createElement("div");
  c.style.cssText = "border:1px solid #444;border-radius:8px;overflow:hidden;cursor:pointer";
  if (imageUrl && /^https:\/\//i.test(imageUrl)) {
    const el = document.createElement("img");
    el.src = imageUrl;
    el.loading = "lazy";
    el.style.cssText = "width:100%;height:150px;object-fit:cover";
    c.appendChild(el);
  }
  const body = document.createElement("div");
  body.style.padding = "8px";
  if (badge) {
    const b = document.createElement("div");
    b.style.cssText = "font-size:11px;opacity:.8;margin-bottom:4px";
    b.textContent = badge;
    body.appendChild(b);
  }
  const t = document.createElement("div");
  t.style.fontWeight = "600";
  t.textContent = title || "(untitled)";
  const s = document.createElement("div");
  s.style.opacity = ".7";
  s.textContent = sub || "";
  body.append(t, s);
  c.appendChild(body);
  return c;
}

async function pick(versionId, label, ui, onPicked) {
  ui.status.textContent = `fetching ${label}`;
  try {
    const d = await post("/qwen21/civitai/fetch", { versionId });
    ui.status.textContent = `✔ ${d.name}`;
    onPicked(d);
    ui.close();
  } catch (e) {
    ui.status.textContent = `✖ ${e.message}`;
  }
}

function openPicker(onPicked) {
  const ui = modal();
  const run = async (query) => {
    ui.grid.innerHTML = "";
    ui.status.textContent = "searching";
    try {
      const d = await post("/qwen21/civitai/search", { query: query || "", cursor: "" });
      if (!query) {
        for (const r of d.recommended || []) {
          const c = card(r.name, `${r.creator} · ${r.why}`, null, "★ recommended");
          c.onclick = () => pick(r.versionId, r.name, ui, onPicked);
          ui.grid.appendChild(c);
        }
      }
      const items = d.items || [];
      ui.status.textContent = `${items.length} result(s)`;
      for (const m of items) {
        const v = (m.modelVersions || [])[0];
        if (!v) continue;
        const c = card(m.name, `${m.creator || ""} · ${v.name || ""} · ${v.baseModel || ""}`,
                       (v.images || [])[0]?.url, null);
        c.onclick = () => pick(v.id, v.name, ui, onPicked);
        ui.grid.appendChild(c);
      }
    } catch (e) {
      ui.status.textContent = `✖ ${e.message}. Civitai hides adult content in some regions.`;
    }
  };
  ui.go.onclick = () => run(ui.q.value.trim());
  ui.q.onkeydown = (e) => { if (e.key === "Enter") run(ui.q.value.trim()); };
  run("");
}

// The App panel draws no button widgets, so the form gets a real DOM button placed into the LoRA row, found by the
// row's data-widget-key.
function decorate() {
  const gid = app.rootGraph?.id;
  if (!gid) return;
  for (const node of app.rootGraph.nodes || []) {
    if (node.type !== PICKER_NODE) continue;
    const row = document.querySelector(`[data-widget-key="${gid}:${node.id}:${PICKER_WIDGET}"]`);
    if (!row || row.querySelector(`.${ROW_BUTTON}`)) continue;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = ROW_BUTTON;
    btn.textContent = "➕ Browse Civitai Red";
    btn.style.cssText = "display:block;width:100%;margin-top:6px;padding:6px 10px;border-radius:8px;"
      + "border:1px dashed currentColor;background:transparent;color:inherit;cursor:pointer;opacity:.85";
    btn.onclick = (e) => {
      e.preventDefault(); e.stopPropagation();
      openPicker((d) => {
        const combo = node.widgets?.find((w) => w.name === PICKER_WIDGET);
        if (!combo) return;
        if (!combo.options.values.includes(d.name)) combo.options.values.push(d.name);
        combo.value = d.name;
        node.onWidgetChanged?.(PICKER_WIDGET, d.name);
        app.graph.setDirtyCanvas(true, true);
        const word = (d.trainedWords || [])[0];
        if (word) alert(`Added ${d.name}.\n\nIts trigger word is "${word}": put that in your prompt.`);
      });
    };
    row.appendChild(btn);
  }
}

app.registerExtension({
  name: "eroscraft.qwen21.civitai_picker",
  async setup() {
    new MutationObserver(() => decorate()).observe(document.body, { childList: true, subtree: true });
    decorate();
  },
});
