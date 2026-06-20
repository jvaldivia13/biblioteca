async function loadAdminLibros() {
    if (!isAdmin()) {
        window.location.href = "/index.html";
        return;
    }

    try {
        const response = await apiFetch("/libros?limit=100");
        displayAdminLibros(response.items);
    } catch (error) {
        console.error("Error:", error);
        const container = document.getElementById("libros-container");
        if (container) {
            clearChildren(container);
            const message = appendText(container, "p", `Error: ${error.message}`);
            message.style.color = "red";
        }
    }
}

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

async function crearLibro(e) {
    e.preventDefault();

    const libroData = {
        titulo: document.getElementById("titulo").value,
        autor: document.getElementById("autor").value,
        isbn: document.getElementById("isbn").value || undefined,
        categoria: document.getElementById("categoria").value,
        anio_publicacion:
            parseInt(document.getElementById("anio_publicacion").value) || undefined,
        stock_total: parseInt(document.getElementById("stock_total").value) || 1,
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
    if (!confirm("Estas seguro de que deseas eliminar este libro?")) {
        return;
    }

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

document.addEventListener("DOMContentLoaded", () => {
    if (!isAdmin()) {
        window.location.href = "/index.html";
        return;
    }

    setupAuthUI();

    if (document.getElementById("libro-form")) {
        document.getElementById("libro-form").addEventListener("submit", crearLibro);
        loadAdminLibros();
    }
});
