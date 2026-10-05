# Changelog

## 5.0.0 — 2026-10-05

- Add `OnlineMap.getDefinitionFromCookies(color, parameters, maxZoom=22)` for offline Cartograph generation without login or browser imports.
- Preserve the historical credential-based API and default zoom while sharing the same generator.
- Require Python >=3.9 and use stravacookies 2.0.0, pinned to the reviewed GitHub commit, replacing the obsolete mechanize authentication dependency.
- Fresh login requires a Playwright browser. HTTP 403 for new automated browser sessions remains a known upstream limitation; no claim of a general 403 fix.
- GitHub release only; no PyPI publication.
