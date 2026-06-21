async function loadDashboard() {
    setupAuthUI();

    if (!isLoggedIn()) return;

    try {
        const response = await apiFetch("/prestamos/mis-prestamos?limit=5");
        const pedidos = response.items || [];
        const activos = pedidos.filter((item) => item.estado === "activo");
        const entregados = pedidos.filter((item) => item.estado !== "activo");

        setStat("stat-pendientes", activos.filter((item) => item.vencido).length);
        setStat("stat-aprobados", activos.filter((item) => !item.vencido).length);
        setStat("stat-rechazados", 0);
        setStat("stat-entregados", entregados.length);
        renderDashboardPedidos(pedidos);
    } catch (error) {
        const container = document.getElementById("dashboard-pedidos");
        if (container) {
            clearChildren(container);
            appendText(container, "div", `Error: ${error.message}`, "alert alert-danger");
        }
    }
}

function setStat(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = String(value);
}

function renderDashboardPedidos(pedidos) {
    const container = document.getElementById("dashboard-pedidos");
    if (!container) return;

    clearChildren(container);

    if (pedidos.length === 0) {
        appendText(container, "div", "No tienes pedidos recientes.", "empty-state");
        return;
    }

    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const headRow = document.createElement("tr");
    ["Pedido", "Libro", "Estado"].forEach((header) => appendText(headRow, "th", header));
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    pedidos.forEach((pedido) => {
        const row = document.createElement("tr");
        appendText(row, "td", `PED-${String(pedido.id).padStart(4, "0")}`);
        appendText(row, "td", pedido.libro.titulo);
        const state = pedido.estado === "activo" ? "Aprobado" : "Entregado";
        const cell = document.createElement("td");
        appendText(cell, "span", state, pedido.estado === "activo" ? "badge badge-aprobado" : "badge badge-entregado");
        row.appendChild(cell);
        tbody.appendChild(row);
    });
    table.appendChild(tbody);
    container.appendChild(table);
}

document.addEventListener("DOMContentLoaded", loadDashboard);
