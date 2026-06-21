let currentPage = 0;
const limit = 12;

async function loadLibros(offset = 0) {
    currentPage = Math.floor(offset / limit);

    const q = document.getElementById("search-input")?.value || "";
    const categoria = document.getElementById("category-select")?.value || "";
    const disponibilidad = document.getElementById("availability-filter")?.value || "";

    try {
        const queryParams = new URLSearchParams({
            limit: limit,
            offset: offset,
            ...(q && { q }),
            ...(categoria && { categoria }),
        });

        const response = await apiFetch(`/libros?${queryParams}`);
        populateCategorias(response.items);

        const filteredItems = response.items.filter((libro) => {
            if (disponibilidad === "disponible") return libro.disponibles > 0;
            if (disponibilidad === "agotado") return libro.disponibles <= 0;
            return true;
        });

        displayLibros(filteredItems);
        setupPagination(response.total, offset);
    } catch (error) {
        console.error("Error:", error);
        const container = document.getElementById("books-container");
        if (container) {
            clearChildren(container);
            const message = appendText(container, "div", `Error: ${error.message}`, "alert alert-danger");
            message.setAttribute("role", "alert");
        }
    }
}

function populateCategorias(libros) {
    const select = document.getElementById("category-select");
    if (!select || select.dataset.loaded === "true") return;

    const categorias = [...new Set(libros.map((libro) => libro.categoria).filter(Boolean))].sort();

    categorias.forEach((categoria) => {
        const option = document.createElement("option");
        option.value = categoria;
        option.textContent = categoria;
        select.appendChild(option);
    });

    select.dataset.loaded = "true";
}

function displayLibros(libros) {
    const container = document.getElementById("books-container");
    if (!container) return;

    clearChildren(container);

    if (libros.length === 0) {
        appendText(container, "div", "No se encontraron libros con los filtros seleccionados.", "empty-state");
        return;
    }

    libros.forEach((libro) => {
        const card = document.createElement("article");
        card.className = "book-card";

        const content = document.createElement("div");
        content.className = "book-card-content";
        card.appendChild(content);

        appendText(content, "h3", libro.titulo);

        const meta = document.createElement("div");
        meta.className = "book-meta";
        appendText(meta, "span", `Autor: ${libro.autor}`);
        appendText(meta, "span", `Categoria: ${libro.categoria}`);
        if (libro.isbn) appendText(meta, "span", `Codigo: ${libro.isbn}`);
        if (libro.anio_publicacion) appendText(meta, "span", `Ano: ${libro.anio_publicacion}`);
        content.appendChild(meta);

        appendText(
            content,
            "span",
            libro.disponibles > 0 ? `${libro.disponibles} disponible(s)` : "Sin disponibilidad",
            libro.disponibles > 0 ? "badge badge-success" : "badge badge-danger"
        );

        if (libro.descripcion) appendText(content, "p", libro.descripcion, "book-description");

        const actions = document.createElement("div");
        actions.className = "actions";
        content.appendChild(actions);

        if (libro.disponibles > 0) {
            appendButton(actions, "Solicitar libro", "btn btn-primary", () => {
                if (!isLoggedIn()) {
                    window.location.href = "/login.html";
                    return;
                }
                requestPrestamoFromCard(libro.id);
            });
        } else {
            const button = appendButton(actions, "No disponible", "btn btn-secondary", () => {});
            button.disabled = true;
        }

        container.appendChild(card);
    });
}

function setupPagination(total, currentOffset) {
    const container = document.getElementById("pagination");
    if (!container) return;

    clearChildren(container);

    const totalPages = Math.ceil(total / limit);
    const currentPageNum = Math.floor(currentOffset / limit);

    if (totalPages <= 1) return;

    if (currentPageNum > 0) {
        appendButton(container, "Primera", "", () => loadLibros(0));
        appendButton(container, "Anterior", "", () => loadLibros((currentPageNum - 1) * limit));
    }

    for (let i = Math.max(0, currentPageNum - 1); i <= Math.min(totalPages - 1, currentPageNum + 1); i++) {
        const offset = i * limit;
        const button = appendButton(container, String(i + 1), "", () => loadLibros(offset));
        button.disabled = i === currentPageNum;
    }

    if (currentPageNum < totalPages - 1) {
        appendButton(container, "Siguiente", "", () => loadLibros((currentPageNum + 1) * limit));
        appendButton(container, "Ultima", "", () => loadLibros((totalPages - 1) * limit));
    }
}

async function requestPrestamoFromCard(libroId) {
    try {
        await apiFetch("/prestamos", {
            method: "POST",
            body: JSON.stringify({ libro_id: libroId }),
        });
        alert("Pedido enviado correctamente");
        loadLibros(currentPage * limit);
    } catch (error) {
        alert("Error: " + error.message);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadLibros(0);

    const searchBtn = document.getElementById("search-btn");
    if (searchBtn) searchBtn.addEventListener("click", () => loadLibros(0));

    const searchInput = document.getElementById("search-input");
    if (searchInput) {
        searchInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") loadLibros(0);
        });
    }

    ["category-select", "availability-filter", "material-filter"].forEach((id) => {
        const element = document.getElementById(id);
        if (element) element.addEventListener("change", () => loadLibros(0));
    });
});
