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
            clearChildren(container);
            const message = appendText(container, "p", `Error: ${error.message}`);
            message.style.color = "red";
        }
    }
}

function displayPrestamos(prestamos) {
    const container = document.getElementById("prestamos-container");
    if (!container) return;

    clearChildren(container);

    if (prestamos.length === 0) {
        appendText(container, "p", "No tienes prestamos.");
        return;
    }

    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const headRow = document.createElement("tr");
    ["Libro", "Autor", "Fecha Prestamo", "Vencimiento", "Estado", "Acciones"].forEach(
        (header) => appendText(headRow, "th", header)
    );
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    prestamos.forEach((prestamo) => {
        const row = document.createElement("tr");
        appendText(row, "td", prestamo.libro.titulo);
        appendText(row, "td", prestamo.libro.autor);
        appendText(row, "td", prestamo.fecha_prestamo);
        appendText(row, "td", prestamo.fecha_devolucion_esperada);

        const estadoCell = document.createElement("td");
        appendText(
            estadoCell,
            "span",
            prestamo.estado === "activo"
                ? prestamo.vencido
                    ? "Vencido"
                    : "Activo"
                : "Devuelto",
            prestamo.estado === "activo" && prestamo.vencido
                ? "badge badge-danger"
                : "badge badge-success"
        );
        row.appendChild(estadoCell);

        const actions = document.createElement("td");
        if (prestamo.estado === "activo") {
            appendButton(actions, "Devolver", "btn btn-primary", () =>
                devolverPrestamo(prestamo.id)
            );
        } else {
            appendText(actions, "span", "-");
        }
        row.appendChild(actions);
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}

async function devolverPrestamo(prestamoId) {
    if (!confirm("Deseas registrar la devolucion de este prestamo?")) {
        return;
    }

    try {
        await apiFetch(`/prestamos/${prestamoId}/devolver`, {
            method: "PUT",
        });
        alert("Devolucion registrada correctamente");
        loadMisPrestamos();
    } catch (error) {
        alert("Error: " + error.message);
    }
}

document.addEventListener("DOMContentLoaded", loadMisPrestamos);
