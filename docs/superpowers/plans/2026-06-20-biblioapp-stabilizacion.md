# BiblioApp Stabilization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stabilize BiblioApp v1.0 so it can be tested, demonstrated, and deployed with its documented functional and technical requirements aligned to the code.

**Architecture:** Keep the current layered backend (`routers -> services -> repositories -> models`) and static frontend. The plan fixes reproducibility first, then backend business rules, then frontend safety/usability, then documentation and final verification.

**Tech Stack:** FastAPI, SQLAlchemy 2.0, Pydantic 2, SQLite, pytest, httpx, vanilla JavaScript, Docker Compose.

---

## File Structure

- Modify: `backend/app/config.py`
  - Make local/test startup reproducible without weakening production guidance.
- Create: `backend/.env.example`
  - Document required environment variables used by README, Docker Compose, and deployment docs.
- Modify: `backend/tests/conftest.py`
  - Set test environment before importing the FastAPI app.
- Modify: `backend/app/schemas/usuario.py`
  - Restrict user role input/output to `admin` and `lector`.
- Modify: `backend/app/services/admin_service.py`
  - Enforce self-protection rules correctly for role and account state changes.
- Modify: `backend/app/routers/admin.py`
  - Pass the authenticated admin into service functions that need identity context.
- Modify: `backend/app/services/prestamo_service.py`
  - Allow admins to return any active loan and keep readers restricted to their own loans.
- Modify: `backend/app/repositories/prestamo_repo.py`
  - Add deterministic ordering and optional eager loading if needed by response tests.
- Modify: `backend/app/repositories/libro_repo.py`
  - Preserve partial update semantics while allowing nullable fields to be cleared.
- Modify: `backend/tests/test_admin.py`
  - Cover role validation and self-protection.
- Modify: `backend/tests/test_prestamos.py`
  - Cover admin returning another user's loan, reader restriction, and availability after return.
- Modify: `backend/tests/test_libros.py`
  - Cover category exact case-insensitive filtering and clearing nullable fields.
- Create: `frontend/js/dom.js`
  - Provide small safe DOM rendering helpers.
- Modify: `frontend/js/libros.js`
  - Replace unsafe HTML interpolation for user-controlled book data.
- Modify: `frontend/js/admin.js`
  - Replace unsafe table rendering for user-controlled book data.
- Modify: `frontend/index.html`
  - Load `dom.js` before scripts that use it.
- Modify: `frontend/admin/libros.html`
  - Load `dom.js` before admin scripts.
- Modify: `backend/app/main.py`
  - Add required security headers from RNF-SEG-07.
- Modify: `README.md`
  - Align setup and testing instructions with actual files.
- Modify: `files/RF_requerimientos_funcionales.md`
  - Update traceability status after implementation.

---

### Task 1: Reproducible Backend Configuration

**Files:**
- Create: `backend/.env.example`
- Modify: `backend/app/config.py`
- Modify: `backend/tests/conftest.py`

- [ ] **Step 1: Write the failing configuration test**

Add this test to `backend/tests/test_auth.py`:

```python
def test_app_has_test_jwt_secret_configured(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "BiblioApp API v1.0"
```

- [ ] **Step 2: Run the test to verify current environment behavior**

Run:

```bash
cd backend
python -m pytest tests/test_auth.py::test_app_has_test_jwt_secret_configured -v
```

Expected before fix on a clean machine: FAIL during import if `JWT_SECRET_KEY` is missing, or PASS only if the developer already has a local `.env`.

- [ ] **Step 3: Add `.env.example`**

Create `backend/.env.example`:

```env
DATABASE_URL=sqlite:///./biblioapp.db
JWT_SECRET_KEY=CAMBIAR_POR_CLAVE_SECRETA_LARGA_Y_ALEATORIA
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
DEBUG=false
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

- [ ] **Step 4: Make tests set the secret before app import**

At the top of `backend/tests/conftest.py`, before `from app.main import app`, add:

```python
import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-biblioapp")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
```

- [ ] **Step 5: Keep production explicit in config**

Keep `backend/app/config.py` requiring a real value:

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./biblioapp.db"
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
```

- [ ] **Step 6: Verify**

Run:

```bash
cd backend
python -m pytest tests/test_auth.py::test_app_has_test_jwt_secret_configured -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add backend/.env.example backend/app/config.py backend/tests/conftest.py backend/tests/test_auth.py
git commit -m "test: make backend configuration reproducible"
```

---

### Task 2: Role Validation and Admin Self-Protection

**Files:**
- Modify: `backend/app/schemas/usuario.py`
- Modify: `backend/app/services/admin_service.py`
- Modify: `backend/app/routers/admin.py`
- Modify: `backend/tests/test_admin.py`

- [ ] **Step 1: Add failing tests for invalid role and self-protection**

Append to `backend/tests/test_admin.py`:

```python
def auth_header(usuario):
    token = create_access_token(
        {"user_id": usuario.id, "email": usuario.email, "role": usuario.role}
    )
    return {"Authorization": f"Bearer {token}"}


def test_admin_rechaza_rol_invalido(client: TestClient, usuario_admin, usuario_lector):
    response = client.put(
        f"/api/v1/admin/usuarios/{usuario_lector.id}/rol",
        json={"role": "superadmin"},
        headers=auth_header(usuario_admin),
    )
    assert response.status_code == 422


def test_admin_no_puede_quitarse_su_propio_rol(client: TestClient, usuario_admin):
    response = client.put(
        f"/api/v1/admin/usuarios/{usuario_admin.id}/rol",
        json={"role": "lector"},
        headers=auth_header(usuario_admin),
    )
    assert response.status_code == 409


def test_admin_puede_cambiar_rol_de_otro_admin(client: TestClient, db, usuario_admin):
    from app.models.usuario import Usuario
    from app.utils.password import hash_password

    otro_admin = Usuario(
        nombre="Otro Admin",
        email="otro-admin@test.com",
        password_hash=hash_password("Admin123!"),
        role="admin",
        activo=True,
    )
    db.add(otro_admin)
    db.commit()
    db.refresh(otro_admin)

    response = client.put(
        f"/api/v1/admin/usuarios/{otro_admin.id}/rol",
        json={"role": "lector"},
        headers=auth_header(usuario_admin),
    )
    assert response.status_code == 200
    assert response.json()["role"] == "lector"


def test_admin_no_puede_desactivarse_a_si_mismo(client: TestClient, usuario_admin):
    response = client.put(
        f"/api/v1/admin/usuarios/{usuario_admin.id}/estado",
        json={"activo": False},
        headers=auth_header(usuario_admin),
    )
    assert response.status_code == 409
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
cd backend
python -m pytest tests/test_admin.py -v
```

Expected before fix: invalid role may be accepted, another admin role change may be blocked, and self-deactivation may be accepted.

- [ ] **Step 3: Restrict role schema**

Update `backend/app/schemas/usuario.py`:

```python
from typing import Literal
from pydantic import BaseModel
from datetime import datetime


Role = Literal["admin", "lector"]


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    role: Role
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UsuariosListResponse(BaseModel):
    total: int
    items: list[UsuarioResponse]


class UsuarioEstadoUpdate(BaseModel):
    activo: bool


class UsuarioRolUpdate(BaseModel):
    role: Role
```

- [ ] **Step 4: Pass current admin through router**

Update `backend/app/routers/admin.py` service calls:

```python
@router.put("/usuarios/{id}/estado", response_model=UsuarioResponse)
def cambiar_estado(
    id: int,
    request: UsuarioEstadoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    return admin_service.cambiar_estado_usuario(db, id, request.activo, current_user.id)


@router.put("/usuarios/{id}/rol", response_model=UsuarioResponse)
def cambiar_rol(
    id: int,
    request: UsuarioRolUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    return admin_service.cambiar_rol_usuario(db, id, request.role, current_user.id)
```

- [ ] **Step 5: Fix admin service rules**

Update `backend/app/services/admin_service.py`:

```python
def cambiar_estado_usuario(
    db: Session, usuario_id: int, activo: bool, current_user_id: int
) -> Usuario:
    usuario = usuario_repo.get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.id == current_user_id and not activo:
        raise HTTPException(
            status_code=409, detail="El admin no puede desactivar su propia cuenta"
        )

    return usuario_repo.update_usuario_estado(db, usuario_id, activo)


def cambiar_rol_usuario(
    db: Session, usuario_id: int, role: str, current_user_id: int
) -> Usuario:
    usuario = usuario_repo.get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.id == current_user_id and usuario.role == "admin" and role != "admin":
        raise HTTPException(
            status_code=409, detail="El admin no puede quitarse su propio rol"
        )

    return usuario_repo.update_usuario_rol(db, usuario_id, role)
```

- [ ] **Step 6: Verify**

Run:

```bash
cd backend
python -m pytest tests/test_admin.py -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add backend/app/schemas/usuario.py backend/app/services/admin_service.py backend/app/routers/admin.py backend/tests/test_admin.py
git commit -m "fix: validate roles and protect current admin"
```

---

### Task 3: Loan Return Rules and Availability

**Files:**
- Modify: `backend/app/services/prestamo_service.py`
- Modify: `backend/app/routers/prestamos.py`
- Modify: `backend/tests/test_prestamos.py`

- [ ] **Step 1: Add failing tests**

Append to `backend/tests/test_prestamos.py`:

```python
from datetime import date, timedelta
from app.models.prestamo import Prestamo


def auth_header(usuario):
    token = create_access_token(
        {"user_id": usuario.id, "email": usuario.email, "role": usuario.role}
    )
    return {"Authorization": f"Bearer {token}"}


def crear_libro(db, stock_total=1):
    libro = Libro(
        titulo="Libro Retorno",
        autor="Autora",
        categoria="Pruebas",
        stock_total=stock_total,
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


def crear_prestamo(db, usuario, libro):
    prestamo = Prestamo(
        usuario_id=usuario.id,
        libro_id=libro.id,
        fecha_prestamo=date.today(),
        fecha_devolucion_esperada=date.today() + timedelta(days=14),
        estado="activo",
    )
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo


def test_admin_puede_devolver_prestamo_de_otro_usuario(
    client: TestClient, db, usuario_admin, usuario_lector
):
    libro = crear_libro(db)
    prestamo = crear_prestamo(db, usuario_lector, libro)

    response = client.put(
        f"/api/v1/prestamos/{prestamo.id}/devolver",
        headers=auth_header(usuario_admin),
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "devuelto"


def test_lector_no_puede_devolver_prestamo_de_otro_usuario(
    client: TestClient, db, usuario_lector
):
    from app.models.usuario import Usuario
    from app.utils.password import hash_password

    otro_lector = Usuario(
        nombre="Otro Lector",
        email="otro-lector@test.com",
        password_hash=hash_password("Lector123!"),
        role="lector",
        activo=True,
    )
    db.add(otro_lector)
    db.commit()
    db.refresh(otro_lector)

    libro = crear_libro(db)
    prestamo = crear_prestamo(db, otro_lector, libro)

    response = client.put(
        f"/api/v1/prestamos/{prestamo.id}/devolver",
        headers=auth_header(usuario_lector),
    )

    assert response.status_code == 403


def test_devolucion_incrementa_disponibilidad(client: TestClient, db, usuario_lector):
    libro = crear_libro(db, stock_total=1)
    prestamo = crear_prestamo(db, usuario_lector, libro)

    before = client.get(f"/api/v1/libros/{libro.id}").json()
    assert before["disponibles"] == 0

    response = client.put(
        f"/api/v1/prestamos/{prestamo.id}/devolver",
        headers=auth_header(usuario_lector),
    )
    assert response.status_code == 200

    after = client.get(f"/api/v1/libros/{libro.id}").json()
    assert after["disponibles"] == 1
```

- [ ] **Step 2: Run tests to verify admin return fails**

Run:

```bash
cd backend
python -m pytest tests/test_prestamos.py -v
```

Expected before fix: admin returning another user's loan fails with 403.

- [ ] **Step 3: Update service signature and rule**

Update `backend/app/services/prestamo_service.py`:

```python
def registrar_devolucion(
    db: Session, prestamo_id: int, usuario_id: int, usuario_role: str
) -> Prestamo:
    prestamo = prestamo_repo.get_prestamo_by_id(db, prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")

    if prestamo.estado != "activo":
        raise HTTPException(status_code=409, detail="El prestamo ya fue devuelto")

    if prestamo.usuario_id != usuario_id and usuario_role != "admin":
        raise HTTPException(
            status_code=403, detail="No puedes devolver el prestamo de otro usuario"
        )

    return prestamo_repo.update_prestamo_devolucion(db, prestamo_id, date.today())
```

- [ ] **Step 4: Update router call**

Update `backend/app/routers/prestamos.py`:

```python
prestamo = prestamo_service.registrar_devolucion(
    db, id, current_user.id, current_user.role
)
```

- [ ] **Step 5: Verify**

Run:

```bash
cd backend
python -m pytest tests/test_prestamos.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add backend/app/services/prestamo_service.py backend/app/routers/prestamos.py backend/tests/test_prestamos.py
git commit -m "fix: allow admins to return any loan"
```

---

### Task 4: Book Filtering and Partial Updates

**Files:**
- Modify: `backend/app/repositories/libro_repo.py`
- Modify: `backend/tests/test_libros.py`

- [ ] **Step 1: Add failing tests**

Append to `backend/tests/test_libros.py`:

```python
def auth_header(usuario):
    token = create_access_token(
        {"user_id": usuario.id, "email": usuario.email, "role": usuario.role}
    )
    return {"Authorization": f"Bearer {token}"}


def test_filtrar_categoria_exacta_case_insensitive(client: TestClient, db):
    db.add_all(
        [
            Libro(titulo="A", autor="Autor", categoria="Novela", stock_total=1),
            Libro(titulo="B", autor="Autor", categoria="Novela Historica", stock_total=1),
        ]
    )
    db.commit()

    response = client.get("/api/v1/libros?categoria=novela")

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["categoria"] == "Novela"


def test_actualizar_libro_permite_limpiar_campos_nullable(
    client: TestClient, db, usuario_admin
):
    libro = Libro(
        titulo="Con descripcion",
        autor="Autor",
        categoria="General",
        isbn="123456789",
        anio_publicacion=2020,
        descripcion="Texto temporal",
        stock_total=1,
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)

    response = client.put(
        f"/api/v1/libros/{libro.id}",
        json={"isbn": None, "anio_publicacion": None, "descripcion": None},
        headers=auth_header(usuario_admin),
    )

    assert response.status_code == 200
    assert response.json()["isbn"] is None
    assert response.json()["anio_publicacion"] is None
    assert response.json()["descripcion"] is None
```

- [ ] **Step 2: Run tests to verify failures**

Run:

```bash
cd backend
python -m pytest tests/test_libros.py -v
```

Expected before fix: category may match partial strings and nullable fields remain unchanged.

- [ ] **Step 3: Fix exact case-insensitive category filter**

Update `backend/app/repositories/libro_repo.py`:

```python
if categoria:
    query = query.filter(func.lower(Libro.categoria) == categoria.lower())
```

- [ ] **Step 4: Allow clearing nullable fields**

Update `backend/app/repositories/libro_repo.py`:

```python
def update_libro(db: Session, libro_id: int, data: dict) -> Libro | None:
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if libro:
        for key, value in data.items():
            setattr(libro, key, value)
        db.commit()
        db.refresh(libro)
    return libro
```

- [ ] **Step 5: Verify**

Run:

```bash
cd backend
python -m pytest tests/test_libros.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add backend/app/repositories/libro_repo.py backend/tests/test_libros.py
git commit -m "fix: align book filters and nullable updates"
```

---

### Task 5: Frontend Safe Rendering for Book Data

**Files:**
- Create: `frontend/js/dom.js`
- Modify: `frontend/js/libros.js`
- Modify: `frontend/js/admin.js`
- Modify: `frontend/index.html`
- Modify: `frontend/admin/libros.html`

- [ ] **Step 1: Create DOM helpers**

Create `frontend/js/dom.js`:

```javascript
function clearChildren(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function appendText(parent, tagName, text, className) {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    element.textContent = text ?? "";
    parent.appendChild(element);
    return element;
}

function appendButton(parent, text, className, onClick) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = className;
    button.textContent = text;
    button.addEventListener("click", onClick);
    parent.appendChild(button);
    return button;
}
```

- [ ] **Step 2: Load helper before dependent scripts**

Add to `frontend/index.html` before `js/libros.js`:

```html
<script src="js/dom.js"></script>
```

Add to `frontend/admin/libros.html` before `../js/admin.js`:

```html
<script src="../js/dom.js"></script>
```

- [ ] **Step 3: Replace public book rendering**

In `frontend/js/libros.js`, replace `displayLibros` with:

```javascript
function displayLibros(libros) {
    const container = document.getElementById("books-container");
    if (!container) return;

    clearChildren(container);

    if (libros.length === 0) {
        appendText(container, "p", "No se encontraron libros.");
        return;
    }

    libros.forEach((libro) => {
        const card = document.createElement("div");
        card.className = "book-card";

        const content = document.createElement("div");
        content.className = "book-card-content";
        card.appendChild(content);

        appendText(content, "h3", libro.titulo);
        appendText(content, "p", `Autor: ${libro.autor}`);
        appendText(content, "p", `Categoria: ${libro.categoria}`);
        if (libro.isbn) appendText(content, "p", `ISBN: ${libro.isbn}`);
        if (libro.anio_publicacion) {
            appendText(content, "p", `Anio: ${libro.anio_publicacion}`);
        }

        appendText(
            content,
            "div",
            libro.disponibles > 0
                ? `${libro.disponibles} disponible${libro.disponibles !== 1 ? "s" : ""}`
                : "No disponible",
            "disponibles"
        );

        if (libro.descripcion) appendText(content, "p", libro.descripcion);

        const actions = document.createElement("div");
        actions.className = "actions";
        content.appendChild(actions);

        if (libro.disponibles > 0 && isLoggedIn()) {
            appendButton(actions, "Solicitar", "btn btn-success", () =>
                requestPrestamoFromCard(libro.id)
            );
        }

        container.appendChild(card);
    });
}
```

- [ ] **Step 4: Replace admin table rendering**

In `frontend/js/admin.js`, replace `displayAdminLibros` with:

```javascript
function displayAdminLibros(libros) {
    const container = document.getElementById("libros-container");
    if (!container) return;

    clearChildren(container);

    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const headRow = document.createElement("tr");
    ["Titulo", "Autor", "Categoria", "Stock Total", "Disponibles", "Acciones"].forEach(
        (header) => appendText(headRow, "th", header)
    );
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    libros.forEach((libro) => {
        const row = document.createElement("tr");
        appendText(row, "td", libro.titulo);
        appendText(row, "td", libro.autor);
        appendText(row, "td", libro.categoria);
        appendText(row, "td", String(libro.stock_total));
        appendText(row, "td", String(libro.disponibles));

        const actions = document.createElement("td");
        appendButton(actions, "Eliminar", "btn btn-danger", () =>
            confirmarEliminarLibro(libro.id)
        );
        row.appendChild(actions);
        tbody.appendChild(row);
    });
    table.appendChild(tbody);
    container.appendChild(table);
}
```

- [ ] **Step 5: Manual XSS check**

Run frontend locally:

```bash
cd frontend
python -m http.server 3000
```

Create a book with title:

```html
<img src=x onerror=alert('xss')>
```

Expected: The title appears as text. No alert executes.

- [ ] **Step 6: Commit**

```bash
git add frontend/js/dom.js frontend/js/libros.js frontend/js/admin.js frontend/index.html frontend/admin/libros.html
git commit -m "fix: render book data safely in frontend"
```

---

### Task 6: Security Headers

**Files:**
- Modify: `backend/app/main.py`
- Create or modify: `backend/tests/test_security.py`

- [ ] **Step 1: Add failing test**

Create `backend/tests/test_security.py`:

```python
from fastapi.testclient import TestClient


def test_security_headers_present(client: TestClient):
    response = client.get("/")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
```

- [ ] **Step 2: Run test to verify failure**

Run:

```bash
cd backend
python -m pytest tests/test_security.py -v
```

Expected before fix: FAIL because headers are missing.

- [ ] **Step 3: Add middleware**

Add to `backend/app/main.py` after CORS middleware:

```python
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response
```

- [ ] **Step 4: Verify**

Run:

```bash
cd backend
python -m pytest tests/test_security.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/app/main.py backend/tests/test_security.py
git commit -m "fix: add API security headers"
```

---

### Task 7: Documentation and Traceability Update

**Files:**
- Modify: `README.md`
- Modify: `files/RF_requerimientos_funcionales.md`
- Modify: `files/RT_requerimientos_tecnicos.md`

- [ ] **Step 1: Update README setup**

In `README.md`, keep the setup command and ensure the referenced file exists:

```bash
cd backend
cp .env.example .env
```

Add this Windows PowerShell equivalent:

```powershell
cd backend
Copy-Item .env.example .env
```

- [ ] **Step 2: Update test instructions**

Replace the testing block with:

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

- [ ] **Step 3: Update RF traceability statuses**

In `files/RF_requerimientos_funcionales.md`, change rows implemented by this codebase from `Pendiente` to `Implementado` after tests pass:

```markdown
| RF-AUTH-01 | Auth | 🔴 Alta | POST /auth/register | Implementado |
| RF-AUTH-02 | Auth | 🔴 Alta | POST /auth/login | Implementado |
| RF-AUTH-03 | Auth | 🔴 Alta | Middleware/Dependency | Implementado |
| RF-AUTH-04 | Auth | 🟡 Media | Frontend localStorage | Implementado |
| RF-AUTH-05 | Auth | 🔴 Alta | Dependency `require_admin` | Implementado |
| RF-LIB-01 | Libros | 🔴 Alta | POST /libros | Implementado |
| RF-LIB-02 | Libros | 🔴 Alta | GET /libros | Implementado |
| RF-LIB-03 | Libros | 🔴 Alta | GET /libros?q= | Implementado |
| RF-LIB-04 | Libros | 🔴 Alta | PUT /libros/{id} | Implementado |
| RF-LIB-05 | Libros | 🔴 Alta | DELETE /libros/{id} | Implementado |
| RF-LIB-06 | Libros | 🔴 Alta | GET /libros/{id} | Implementado |
| RF-LIB-07 | Libros | 🟡 Media | GET /libros?categoria= | Implementado |
| RF-LIB-08 | Libros | 🔴 Alta | Campo calculado | Implementado |
| RF-PRE-01 | Préstamos | 🔴 Alta | POST /prestamos | Implementado |
| RF-PRE-02 | Préstamos | 🔴 Alta | Validación stock | Implementado |
| RF-PRE-03 | Préstamos | 🔴 Alta | PUT /prestamos/{id}/devolver | Implementado |
| RF-PRE-04 | Préstamos | 🔴 Alta | GET /prestamos/mis-prestamos | Implementado |
| RF-PRE-05 | Préstamos | 🔴 Alta | GET /prestamos | Implementado |
| RF-PRE-06 | Préstamos | 🟡 Media | Campo calculado `vencido` | Implementado |
| RF-ADM-01 | Admin | 🟡 Media | GET+PUT /admin/usuarios | Implementado |
| RF-ADM-02 | Admin | 🟡 Media | GET /admin/stats | Implementado |
| RF-ADM-03 | Admin | 🟢 Baja | PUT /admin/usuarios/{id}/rol | Implementado |
```

- [ ] **Step 4: Update RT security note**

In `files/RT_requerimientos_tecnicos.md`, under RNF-SEG-07, add:

```markdown
Implementado en `backend/app/main.py` mediante middleware HTTP que agrega
`X-Content-Type-Options: nosniff` y `X-Frame-Options: DENY` a cada respuesta.
```

- [ ] **Step 5: Commit**

```bash
git add README.md files/RF_requerimientos_funcionales.md files/RT_requerimientos_tecnicos.md
git commit -m "docs: align requirements with implementation plan"
```

---

### Task 8: Final Verification

**Files:**
- No code changes expected.

- [ ] **Step 1: Install development dependencies**

Run:

```bash
cd backend
pip install -r requirements-dev.txt
```

Expected: pytest, httpx, and pytest-cov install successfully.

- [ ] **Step 2: Run backend tests**

Run:

```bash
cd backend
python -m pytest tests/ -v
```

Expected: all tests PASS.

- [ ] **Step 3: Run coverage**

Run:

```bash
cd backend
python -m pytest tests/ -v --cov=app --cov-report=term-missing
```

Expected: coverage report prints. If below 70%, add focused tests for services and routers before delivery.

- [ ] **Step 4: Run backend manually**

Run:

```bash
cd backend
uvicorn app.main:app --reload
```

Expected:
- API root works at `http://localhost:8000/`
- Swagger works at `http://localhost:8000/docs`

- [ ] **Step 5: Run frontend manually**

Run in a second terminal:

```bash
cd frontend
python -m http.server 3000
```

Expected:
- Catalog loads at `http://localhost:3000/index.html`
- Login/register pages load
- Admin screens are hidden for lector users
- Admin screens work for admin users

- [ ] **Step 6: Docker Compose smoke test**

Run from repo root:

```bash
docker compose up --build
```

Expected:
- Backend starts on port 8000
- Frontend starts on port 3000
- No missing `JWT_SECRET_KEY` if environment is configured

- [ ] **Step 7: Final commit**

```bash
git status --short
git add -A
git commit -m "chore: complete biblioapp stabilization"
```

---

## Self-Review

**Spec coverage:** This plan covers reproducible setup, auth, role protection, catalog operations, loan return rules, admin user management, frontend XSS risk, RNF security headers, tests, and documentation traceability. It intentionally does not introduce migrations or a new frontend framework because the current MVP uses SQLAlchemy `create_all` and vanilla JavaScript.

**Placeholder scan:** The plan contains concrete file paths, code snippets, commands, and expected outcomes. There are no `TBD` implementation slots.

**Type consistency:** Role values use `Literal["admin", "lector"]`; service and router signatures both pass `current_user.id` where self-protection is required; loan return signatures consistently use `usuario_role`.

