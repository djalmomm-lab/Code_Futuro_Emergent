import { useEffect, useState, useRef } from 'react';

// Pyodide loader singleton - runs real Python in the browser via WebAssembly.
// No API key needed. First load ~6-10MB, cached after.

const PYODIDE_VERSION = '0.26.2';
const PYODIDE_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/pyodide.js`;

let pyodidePromise = null;

function loadScript(src) {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) return resolve();
    const s = document.createElement('script');
    s.src = src;
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
  });
}

async function initPyodide() {
  if (pyodidePromise) return pyodidePromise;
  pyodidePromise = (async () => {
    await loadScript(PYODIDE_URL);
    // eslint-disable-next-line no-undef
    const py = await loadPyodide({ indexURL: `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/` });
    return py;
  })();
  return pyodidePromise;
}

export function usePyodide() {
  const [ready, setReady] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const pyRef = useRef(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    initPyodide()
      .then((py) => {
        if (!mounted) return;
        pyRef.current = py;
        setReady(true);
        setLoading(false);
      })
      .catch((e) => {
        if (!mounted) return;
        setError(e);
        setLoading(false);
      });
    return () => { mounted = false; };
  }, []);

  const run = async (code, stdin = '') => {
    if (!pyRef.current) throw new Error('Pyodide not ready');
    const py = pyRef.current;
    // Capture stdout
    py.setStdout({ batched: () => {} });
    let out = '';
    py.setStdout({ batched: (s) => { out += s + '\n'; } });
    if (stdin) py.setStdin({ stdin: () => stdin });
    try {
      await py.runPythonAsync(code);
      return { stdout: out.replace(/\n$/, ''), error: null };
    } catch (e) {
      return { stdout: out.replace(/\n$/, ''), error: String(e.message || e) };
    }
  };

  return { ready, loading, error, run };
}
