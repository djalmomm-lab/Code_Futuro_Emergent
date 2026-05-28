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
    // initPyodide is a module-level singleton (stable reference);
    // `mounted` is local to this effect's closure — no deps needed.
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /**
   * Run Python code with optional stdin.
   * stdin is split by '\n' and fed line-by-line so multiple input() calls work.
   * A fresh stdin handler is created every call — no state bleeds between runs.
   */
  const run = async (code, stdin = '') => {
    if (!pyRef.current) throw new Error('Pyodide not ready');
    const py = pyRef.current;

    // Capture stdout
    let out = '';
    py.setStdout({ batched: (s) => { out += s + '\n'; } });

    // Feed stdin line by line. Always set handler to avoid OSError [Errno 29].
    const lines = typeof stdin === 'string' && stdin.length > 0
      ? stdin.split('\n')
      : [];
    let lineIdx = 0;
    py.setStdin({
      stdin: () => {
        if (lineIdx < lines.length) return lines[lineIdx++] + '\n';
        return null; // EOF
      },
    });

    try {
      await py.runPythonAsync(code);
      return { stdout: out.replace(/\n$/, ''), error: null };
    } catch (e) {
      return { stdout: out.replace(/\n$/, ''), error: String(e.message || e) };
    }
  };

  /**
   * Run Python code against EACH test case independently.
   * Returns array of { stdin, expected, stdout, error, passed }.
   */
  const runTests = async (code, testCases) => {
    if (!pyRef.current) throw new Error('Pyodide not ready');
    const results = [];
    for (const tc of testCases) {
      const { stdout, error } = await run(code, tc.stdin ?? '');
      const expected = (tc.expected_stdout || tc.expected || '').trim();
      const actual = (stdout || '').trim();
      results.push({ ...tc, stdout, error, passed: !error && actual === expected });
    }
    return results;
  };

  return { ready, loading, error, run, runTests };
}
