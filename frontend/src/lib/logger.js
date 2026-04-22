// Lightweight error logger. In production, swap for Sentry/LogRocket etc.
// Keeps noise out of user-facing UI while preserving diagnostics.

export const logError = (scope, err, extra = {}) => {
  if (process.env.NODE_ENV === 'production') {
    // Hook for error monitoring (e.g. Sentry.captureException)
    // window.Sentry?.captureException(err, { tags: { scope }, extra });
  }
  // eslint-disable-next-line no-console
  console.error(`[CodeFuturo:${scope}]`, err?.message || err, extra);
};
