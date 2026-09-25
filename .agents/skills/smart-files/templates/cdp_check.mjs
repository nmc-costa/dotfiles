// cdp_check.mjs — open a smart file from file:// in headless Chromium, fail on console errors or network.
// Usage: node cdp_check.mjs <file.html> ["<JS expression that must return true>" ...]
// Needs: node >= 22 (global fetch + WebSocket), chromium/chrome on PATH. No npm deps.
import { spawn } from "node:child_process";
import fs from "node:fs"; import os from "node:os";
const [FILE, ...CHECKS] = process.argv.slice(2);
if (!FILE) { console.error("usage: node cdp_check.mjs <file.html> [expr ...]"); process.exit(2); }
const PORT = 9300 + Math.floor(Math.random() * 500), T = fs.mkdtempSync(os.tmpdir() + "/sf-cdp-");
const bin = process.env.CHROME || "chromium";
const chr = spawn(bin, ["--headless=new", "--no-sandbox", "--disable-gpu", `--remote-debugging-port=${PORT}`, `--user-data-dir=${T}`, "about:blank"], { stdio: "ignore" });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map(), errors = [];
const send = (method, params = {}) => new Promise(res => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
let fail = 0;
try {
  let url; for (let i = 0; i < 50 && !url; i++) { try { url = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find(x => x.type === "page")?.webSocketDebuggerUrl; } catch { } if (!url) await sleep(200); }
  if (!url) throw new Error(`could not start ${bin}`);
  ws = new WebSocket(url); await new Promise(r => ws.onopen = r);   // create after the loop: avoids missing 'open'
  ws.onmessage = m => { const d = JSON.parse(m.data);
    if (d.id && pend.has(d.id)) { pend.get(d.id)(d.result); pend.delete(d.id); }
    if (d.method === "Runtime.exceptionThrown") errors.push(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text);
    if (d.method === "Runtime.consoleAPICalled" && d.params.type === "error") errors.push(d.params.args.map(a => a.value).join(" "));
    if (d.method === "Network.requestWillBeSent" && !/^(file|data|blob):/.test(d.params.request.url)) errors.push("NETWORK " + d.params.request.url); };
  await send("Runtime.enable"); await send("Network.enable"); await send("Page.enable");
  await send("Page.navigate", { url: "file://" + fs.realpathSync(FILE) }); await sleep(1200);
  for (const c of CHECKS) {
    // Don't await promises that wait on a dialog/user gesture — wrap them as `(fn(), true)`.
    const r = await send("Runtime.evaluate", { expression: c, awaitPromise: true, returnByValue: true });
    const ok = !r.exceptionDetails && r.result?.value === true;
    console.log(ok ? "  ✓" : "  ✗", c.slice(0, 100)); if (!ok) fail++;
  }
  console.log(errors.length ? "  ✗ console/network:\n    " + errors.join("\n    ") : "  ✓ no console errors, no network requests");
  if (errors.length) fail++;
} catch (e) { console.log("FATAL", e.message); fail++; }
finally { chr.kill(); fs.rmSync(T, { recursive: true, force: true }); process.exit(fail ? 1 : 0); }
