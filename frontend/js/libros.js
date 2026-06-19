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
            container.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    }
}

function displayLibros(libros) {
    const container = document.getElementById("books-container");
    if (!container) return;

    if (libros.length === 0) {
        container.innerHTML = "<p>No se encontraron libros.</p>";
        return;
    }

    container.innerHTML = libros
        .map(
            (libro) => `
        <div class="book-card">
            <div class="book-card-content">
                <h3>${libro.titulo}</h3>
                <p><strong>Autor:</strong> ${libro.autor}</p>
                <p><strong>Categoría:</strong> ${libro.categoria}</p>
                ${libro.isbn ? `<p><strong>ISBN:</strong> ${libro.isbn}</p>` : ""}
                ${libro.anio_publicacion ? `<p><strong>Año:</strong> ${libro.anio_publicacion}</p>` : ""}
                <div class="disponibles">
                    ${libro.disponibles > 0 ? `${libro.disponibles} disponible${libro.disponibles !== 1 ? 's' : ''}` : "No disponible"}
                </div>
                ${libro.descripcion ? `<p>${libro.descripcion}</p>` : ""}
                <div class="actions">
                    ${libro.disponibles > 0 && isLoggedIn() ? `<button class="btn btn-success" onclick="requestPrestamoFromCard(${libro.id})">Solicitar</button>` : ""}
                </div>
            </div>
        </div>
    `
        )
        .join("");
}

function setupPagination(total, currentOffset) {
    const container = document.getElementById("pagination");
    if (!container) return;

    const totalPages = Math.ceil(total / limit);
    const currentPageNum = Math.floor(currentOffset / limit);

    let html = "";

    if (currentPageNum > 0) {
        html += `<button onclick="loadLibros(0)">Primera</button>`;
        html += `<button onclick="loadLibros(${(currentPageNum - 1) * limit})">Anterior</button>`;
    }

    for (let i = Math.max(0, currentPageNum - 1); i <= Math.min(totalPages - 1, currentPageNum + 1); i++) {
        const offset = i * limit;
        html += `<button onclick="loadLibros(${offset})" ${i === currentPageNum ? "disabled" : ""}>${i + 1}</button>`;
    }

    if (currentPageNum < totalPages - 1) {
        html += `<button onclick="loadLibros(${(currentPageNum + 1) * limit})">Siguiente</button>`;
        html += `<button onclick="loadLibros(${(totalPages - 1) * limit})">Última</button>`;
    }

    container.innerHTML = html;
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
        alert("Préstamo solicitado correctamente");
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
