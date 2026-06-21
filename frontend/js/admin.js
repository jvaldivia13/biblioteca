async function loadAdminLibros() {
    try {
        const response = await apiFetch("/libros?limit=100");
        displayAdminLibros(response.items);
    } catch (error) {
        console.error("Error:", error);
        const container = document.getElementById("libros-container");
        if (container) {
            clearChildren(container);
            appendText(container, "div", `Error: ${error.message}`, "alert alert-danger");
        }
    }
}

function displayAdminLibros(libros) {
    const container = document.getElementById("libros-container");
    if (!container) return;

    clearChildren(container);

    if (libros.length === 0) {
        appendText(container, "div", "No hay libros registrados.", "empty-state");
        return;
    }

    const wrap = document.createElement("div");
    wrap.className = "table-wrap";

    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const headRow = document.createElement("tr");
    ["Titulo", "Autor", "Categoria", "Stock", "Disponibles", "Acciones"].forEach((header) =>
        appendText(headRow, "th", header)
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

        const disponibleCell = document.createElement("td");
        appendText(
            disponibleCell,
            "span",
            String(libro.disponibles),
            libro.disponibles > 0 ? "badge badge-success" : "badge badge-danger"
        );
        row.appendChild(disponibleCell);

        const actions = document.createElement("td");
        appendButton(actions, "Eliminar", "btn btn-danger", () => confirmarEliminarLibro(libro.id));
        row.appendChild(actions);
        tbody.appendChild(row);
    });
    table.appendChild(tbody);
    wrap.appendChild(table);
    container.appendChild(wrap);
}

async function crearLibro(e) {
    e.preventDefault();

    const libroData = {
        titulo: document.getElementById("titulo").value,
        autor: document.getElementById("autor").value,
        isbn: document.getElementById("isbn").value || undefined,
        categoria: document.getElementById("categoria").value,
        anio_publicacion: parseInt(document.getElementById("anio_publicacion").value, 10) || undefined,
        stock_total: parseInt(document.getElementById("stock_total").value, 10) || 1,
        descripcion: document.getElementById("descripcion").value || undefined,
    };

    try {
        await apiFetch("/libros", {
            method: "POST",
            body: JSON.stringify(libroData),
        });

        alert("Libro creado exitosamente");
        document.getElementById("libro-form").reset();
        loadAdminLibros();
    } catch (error) {
        alert("Error: " + error.message);
    }
}

async function confirmarEliminarLibro(libroId) {
    if (!confirm("Estas seguro de que deseas eliminar este libro?")) return;

    try {
        await apiFetch(`/libros/${libroId}`, {
            method: "DELETE",
        });
        alert("Libro eliminado correctamente");
        loadAdminLibros();
    } catch (error) {
        alert("Error: " + error.message);
    }
}

async function loadAdminPrestamos() {
    const container = document.getElementById("prestamos-container");
    if (!container) return;

    try {
        const estado = document.getElementById("admin-estado-filter")?.value || "";
        const query = new URLSearchParams({
            limit: 100,
            ...(estado && { estado }),
        });
        const response = await apiFetch(`/prestamos?${query}`);
        displayAdminPrestamos(response.items);
    } catch (error) {
        clearChildren(container);
        appendText(container, "div", `Error: ${error.message}`, "alert alert-danger");
    }
}

function displayAdminPrestamos(prestamos) {
    const container = document.getElementById("prestamos-container");
    clearChildren(container);

    if (prestamos.length === 0) {
        appendText(container, "div", "No hay pedidos para los filtros seleccionados.", "empty-state");
        return;
    }

    const wrap = document.createElement("div");
    wrap.className = "table-wrap";
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const headRow = document.createElement("tr");
    ["Pedido", "Usuario", "Libro", "Fecha", "Estado", "Acciones"].forEach((header) =>
        appendText(headRow, "th", header)
    );
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    prestamos.forEach((prestamo) => {
        const row = document.createElement("tr");
        appendText(row, "td", `PED-${String(prestamo.id).padStart(4, "0")}`);
        appendText(row, "td", `Usuario ${prestamo.usuario_id}`);
        appendText(row, "td", prestamo.libro.titulo);
        appendText(row, "td", prestamo.fecha_prestamo);

        const estadoCell = document.createElement("td");
        const active = prestamo.estado === "activo";
        appendText(estadoCell, "span", active ? "Aprobado" : "Entregado", active ? "badge badge-aprobado" : "badge badge-entregado");
        row.appendChild(estadoCell);

        const actions = document.createElement("td");
        if (active) {
            appendButton(actions, "Marcar entregado", "btn btn-primary", () => marcarEntregado(prestamo.id));
        } else {
            appendText(actions, "span", "Sin acciones", "muted");
        }
        row.appendChild(actions);
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    wrap.appendChild(table);
    container.appendChild(wrap);
}

async function marcarEntregado(prestamoId) {
    if (!confirm("Marcar este pedido como entregado/devuelto?")) return;

    try {
        await apiFetch(`/prestamos/${prestamoId}/devolver`, {
            method: "PUT",
        });
        alert("Pedido actualizado correctamente");
        loadAdminPrestamos();
    } catch (error) {
        alert("Error: " + error.message);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (!isAdmin()) {
        window.location.href = "../index.html";
        return;
    }

    setupAuthUI();

    const form = document.getElementById("libro-form");
    if (form) {
        form.addEventListener("submit", crearLibro);
        loadAdminLibros();
    }

    const filterButton = document.getElementById("admin-filtrar-pedidos");
    if (filterButton) filterButton.addEventListener("click", loadAdminPrestamos);

    if (document.getElementById("prestamos-container")) {
        loadAdminPrestamos();
    }
});
