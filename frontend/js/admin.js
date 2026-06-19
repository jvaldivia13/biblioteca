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
            container.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    }
}

function displayAdminLibros(libros) {
    const container = document.getElementById("libros-container");
    if (!container) return;

    const html = `
        <table>
            <thead>
                <tr>
                    <th>Título</th>
                    <th>Autor</th>
                    <th>Categoría</th>
                    <th>Stock Total</th>
                    <th>Disponibles</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                ${libros
                    .map(
                        (l) => `
                    <tr>
                        <td>${l.titulo}</td>
                        <td>${l.autor}</td>
                        <td>${l.categoria}</td>
                        <td>${l.stock_total}</td>
                        <td>${l.disponibles}</td>
                        <td>
                            <button class="btn btn-danger" onclick="confirmarEliminarLibro(${l.id})">Eliminar</button>
                        </td>
                    </tr>
                `
                    )
                    .join("")}
            </tbody>
        </table>
    `;

    container.innerHTML = html;
}

async function crearLibro(e) {
    e.preventDefault();

    const libroData = {
        titulo: document.getElementById("titulo").value,
        autor: document.getElementById("autor").value,
        isbn: document.getElementById("isbn").value || undefined,
        categoria: document.getElementById("categoria").value,
        anio_publicacion: parseInt(document.getElementById("anio_publicacion").value) || undefined,
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
    if (!confirm("¿Estás seguro de que deseas eliminar este libro?")) {
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
