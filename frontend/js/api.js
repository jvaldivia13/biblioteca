const API_BASE = window.location.hostname === "localhost"
    ? "http://localhost:8000/api/v1"
    : "https://biblioapp-api.onrender.com/api/v1";

async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem("token");
    const headers = {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
    };

    const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });

    if (res.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("user_data");
        window.location.href = "/login.html";
        return;
    }

    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Error en la solicitud");
    }

    return res.status === 204 ? null : res.json();
}
