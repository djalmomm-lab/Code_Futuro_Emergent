/**
 * Browser-side runners for non-Python lessons.
 *
 * - runJavaScript:  executes the user's JS inside a sandboxed iframe and
 *   captures `console.log` output, errors, and timeouts.
 * - runHTML:        renders the user's HTML inside a sandboxed iframe and
 *   returns the (normalized) outerHTML for validation.
 *
 * All runners auto-cleanup their iframe even on timeout.
 */

const TIMEOUT_MS = 4000;

const stringify = (v) => {
  if (typeof v === 'string') return v;
  try { return JSON.stringify(v); } catch { return String(v); }
};

const buildJSDoc = (code, runId) => `<!doctype html><html><body><script>
(function(){
  var __id = ${JSON.stringify(runId)};
  var send = function(type, payload){
    try { parent.postMessage({ __cfRun: __id, type: type, payload: payload }, '*'); } catch(e){}
  };
  var origLog = console.log;
  console.log = function(){
    var parts = [];
    for (var i = 0; i < arguments.length; i++) {
      var a = arguments[i];
      try { parts.push(typeof a === 'string' ? a : JSON.stringify(a)); }
      catch(e) { parts.push(String(a)); }
    }
    send('log', parts.join(' '));
    try { origLog.apply(console, arguments); } catch(e){}
  };
  window.onerror = function(msg){ send('error', String(msg)); return true; };
  try {
    ${code}
    send('done', null);
  } catch (e) {
    send('error', (e && e.message) ? e.message : String(e));
    send('done', null);
  }
})();
<\/script></body></html>`;

export function runJavaScript(code) {
  return new Promise((resolve) => {
    const runId = Math.random().toString(36).slice(2);
    const iframe = document.createElement('iframe');
    iframe.style.cssText = 'position:absolute;left:-99999px;top:-99999px;width:1px;height:1px;border:0;';
    iframe.sandbox = 'allow-scripts';
    iframe.srcdoc = buildJSDoc(code, runId);

    const logs = [];
    let error = null;
    let finished = false;

    const cleanup = () => {
      try { window.removeEventListener('message', onMessage); } catch {}
      try { iframe.remove(); } catch {}
    };
    const finish = () => {
      if (finished) return;
      finished = true;
      cleanup();
      resolve({ stdout: logs.join('\n'), error });
    };

    const onMessage = (e) => {
      const data = e.data;
      if (!data || data.__cfRun !== runId) return;
      if (data.type === 'log') logs.push(stringify(data.payload));
      else if (data.type === 'error' && !error) error = stringify(data.payload);
      else if (data.type === 'done') finish();
    };
    window.addEventListener('message', onMessage);

    document.body.appendChild(iframe);
    setTimeout(() => {
      if (!finished) {
        if (!error) error = 'Tempo de execução excedido (4s)';
        finish();
      }
    }, TIMEOUT_MS);
  });
}

/**
 * Mount a live HTML preview inside the given container element. Returns the
 * iframe so callers can dispose of it. Replaces any prior content inside the
 * container.
 */
export function mountHTMLPreview(container, html) {
  if (!container) return null;
  container.innerHTML = '';
  const iframe = document.createElement('iframe');
  iframe.title = 'Pré-visualização HTML';
  iframe.style.cssText = 'width:100%;height:100%;border:0;background:#fff;border-radius:8px;';
  iframe.sandbox = 'allow-same-origin';
  iframe.srcdoc = html || '<!doctype html><html><body></body></html>';
  container.appendChild(iframe);
  return iframe;
}

/**
 * Normalize quote style: treat single quotes and double quotes as equivalent.
 * Used to accept both print("hi") and print('hi') as correct answers.
 */
export function normalizeQuotes(s) {
  return String(s || '').replace(/"/g, "'");
}

/** Normalize HTML for textual comparison: collapse whitespace, lowercase tags, normalize quotes. */
export function normalizeHTML(s) {
  if (!s) return '';
  return String(s)
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/"/g, "'")           // both ' and " accepted in attributes
    .replace(/\s+/g, ' ')
    .replace(/>\s+</g, '><')
    .trim()
    .toLowerCase();
}
