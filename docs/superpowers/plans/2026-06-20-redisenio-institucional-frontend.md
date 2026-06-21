# Redisenio Institucional Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the current static BiblioApp frontend into a sober, modern, institutional library request system interface.

**Architecture:** Keep the existing HTML/CSS/JavaScript frontend and FastAPI integration. Update shared CSS tokens and layout primitives, then update each screen to use consistent app shell, cards, tables, badges, forms and responsive behavior.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, existing FastAPI API, Python `http.server` for local frontend hosting.

---

### Task 1: Shared Visual System

**Files:**
- Modify: `frontend/css/styles.css`
- Modify: `frontend/css/components.css`
- Modify: `frontend/css/layout.css`

- [ ] Replace the color tokens with institutional palette variables.
- [ ] Add base typography, focus states, responsive containers and utility classes.
- [ ] Redesign buttons, forms, cards, badges, tables, empty states and pagination.
- [ ] Add app shell, sidebar, topbar, dashboard grid and responsive mobile layout.

### Task 2: Public And Auth Screens

**Files:**
- Modify: `frontend/index.html`
- Modify: `frontend/login.html`
- Modify: `frontend/register.html`

- [ ] Replace corrupted visible text with correct Spanish ASCII-compatible labels where possible.
- [ ] Update login/register to use centered institutional auth cards.
- [ ] Update catalog page to use app shell, page header, search filters and professional content areas.

### Task 3: Pedidos Screens

**Files:**
- Modify: `frontend/mis-prestamos.html`
- Create: `frontend/dashboard.html`
- Create: `frontend/nuevo-pedido.html`
- Create: `frontend/pedido-detalle.html`
- Modify: `frontend/js/prestamos.js`
- Modify: `frontend/js/libros.js`

- [ ] Add dashboard page with statistic cards and quick actions.
- [ ] Add new request form page prepared for current book request workflow.
- [ ] Add request detail page as administrative ficha scaffold.
- [ ] Update loan/request table and catalog cards to use professional classes and labels.

### Task 4: Admin Screens

**Files:**
- Modify: `frontend/admin/libros.html`
- Modify: `frontend/admin/prestamos.html`
- Modify: `frontend/admin/usuarios.html`
- Modify: `frontend/js/admin.js`

- [ ] Update admin pages to use the same institutional app shell.
- [ ] Improve library manager panel layout, table styling and action buttons.
- [ ] Add filters/header structure for received requests.

### Task 5: Verification

**Files:**
- Read/verify served frontend and backend endpoints.

- [ ] Run `node --check frontend/js/api.js`.
- [ ] Run `node --check frontend/js/libros.js`.
- [ ] Run `node --check frontend/js/prestamos.js`.
- [ ] Run `node --check frontend/js/admin.js`.
- [ ] Run `python -m pytest tests/test_config.py tests/test_libros.py -q` from `backend`.
- [ ] Verify `http://127.0.0.1:3000/index.html` serves updated scripts.
- [ ] Verify `http://127.0.0.1:8000/api/v1/libros` returns catalog data.
