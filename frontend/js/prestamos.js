async function loadMisPrestamos() {
    if (!isLoggedIn()) {
        window.location.href = "/login.html";
        return;
    }

    try {
        const response = await apiFetch("/prestamos/mis-prestamos");
        displayPrestamos(response.items);
    } catch (error) {
        console.error("Error:", error);
        const container = document.getElementById("prestamos-container");
        if (container) {
            container.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    }
}

function displayPrestamos(prestamos) {
    const container = document.getElementById("prestamos-container");
    if (!container) return;

    if (prestamos.length === 0) {
        container.innerHTML = "<p>No tienes préstamos.</p>";
        return;
    }

    const html = `
        <table>
            <thead>
                <tr>
                    <th>Libro</th>
                    <th>Autor</th>
                    <th>Fecha Préstamo</th>
                    <th>Vencimiento</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                ${prestamos
                    .map(
                        (p) => `
                    <tr>
                        <td>${p.libro.titulo}</td>
                        <td>${p.libro.autor}</td>
                        <td>${p.fecha_prestamo}</td>
                        <td>${p.fecha_devolucion_esperada}</td>
                        <td>
                            ${
                                p.estado === "activo"
                                    ? `<span class="badge ${p.vencido ? "badge-danger" : "badge-success"}">${p.vencido ? "Vencido" : "Activo"}</span>`
                                    : `<span class="badge badge-success">Devuelto</span>`
                            }
                        </td>
                        <td>
                            ${p.estado === "activo" ? `<button class="btn btn-primary" onclick="devolverPrestamo(${p.id})">Devolver</button>` : "—"}
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

async function devolverPrestamo(prestamoId) {
    if (!confirm("¿Deseas registrar la devolución de este préstamo?")) {
        return;
    }

    try {
        await apiFetch(`/prestamos/${prestamoId}/devolver`, {
            method: "PUT",
        });
        alert("Devolución registrada correctamente");
        loadMisPrestamos();
    } catch (error) {
        alert("Error: " + error.message);
    }
}

document.addEventListener("DOMContentLoaded", loadMisPrestamos);
