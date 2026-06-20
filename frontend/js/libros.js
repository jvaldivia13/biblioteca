let currentPage = 0;
const limit = 12;

async function loadLibros(offset = 0) {
    const q = document.getElementById("search-input")?.value || "";
    const categoria = document.getElementById("category-select")?.value || "";

    try {
        const queryParams = new URLSearchParams({
            limit: limit,
            offset: offset,
            ...(q && { q }),
            ...(categoria && { categoria }),
        });

        const response = await apiFetch(`/libros?${queryParams}`);
        displayLibros(response.items);
        setupPagination(response.total, offset);
    } catch (error) {
        console.error("Error:", error);
        const container = document.getElementById("books-container");
        if (container) {
            clearChildren(container);
            const message = appendText(container, "p", `Error: ${error.message}`);
            message.style.color = "red";
        }
    }
}

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

function setupPagination(total, currentOffset) {
    const container = document.getElementById("pagination");
    if (!container) return;

    clearChildren(container);

    const totalPages = Math.ceil(total / limit);
    const currentPageNum = Math.floor(currentOffset / limit);

    if (currentPageNum > 0) {
        appendButton(container, "Primera", "", () => loadLibros(0));
        appendButton(container, "Anterior", "", () =>
            loadLibros((currentPageNum - 1) * limit)
        );
    }

    for (
        let i = Math.max(0, currentPageNum - 1);
        i <= Math.min(totalPages - 1, currentPageNum + 1);
        i++
    ) {
        const offset = i * limit;
        const button = appendButton(container, String(i + 1), "", () =>
            loadLibros(offset)
        );
        button.disabled = i === currentPageNum;
    }

    if (currentPageNum < totalPages - 1) {
        appendButton(container, "Siguiente", "", () =>
            loadLibros((currentPageNum + 1) * limit)
        );
        appendButton(container, "Ultima", "", () =>
            loadLibros((totalPages - 1) * limit)
        );
    }
}

async function requestPrestamoFromCard(libroId) {
    if (!isLoggedIn()) {
        window.location.href = "/login.html";
        return;
    }

    try {
        await apiFetch("/prestamos", {
            method: "POST",
            body: JSON.stringify({ libro_id: libroId }),
        });
        alert("Prestamo solicitado correctamente");
        loadLibros(0);
    } catch (error) {
        alert("Error: " + error.message);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadLibros(0);

    const searchBtn = document.getElementById("search-btn");
    if (searchBtn) {
        searchBtn.addEventListener("click", () => loadLibros(0));
    }

    const searchInput = document.getElementById("search-input");
    if (searchInput) {
        searchInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") loadLibros(0);
        });
    }
});
