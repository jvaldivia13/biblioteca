function isLoggedIn() {
    return !!localStorage.getItem("token");
}

function getUserData() {
    const data = localStorage.getItem("user_data");
    return data ? JSON.parse(data) : null;
}

function isAdmin() {
    const userData = getUserData();
    return userData && userData.role === "admin";
}

async function login(email, password) {
    const response = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
    });

    localStorage.setItem("token", response.access_token);
    localStorage.setItem(
        "user_data",
        JSON.stringify({
            email: email,
            role: response.role,
        })
    );

    return response;
}

async function register(nombre, email, password) {
    return await apiFetch("/auth/register", {
        method: "POST",
        body: JSON.stringify({ nombre, email, password }),
    });
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user_data");
    window.location.href = "/login.html";
}

function setupAuthUI() {
    const loginLink = document.getElementById("login-link");
    const logoutBtn = document.getElementById("logout-btn");
    const misPrestamosLink = document.getElementById("mis-prestamos-link");
    const adminLibrosLink = document.getElementById("admin-libros-link");
    const adminLink = document.getElementById("admin-link");

    if (isLoggedIn()) {
        if (loginLink) loginLink.style.display = "none";
        if (logoutBtn) {
            logoutBtn.style.display = "block";
            logoutBtn.addEventListener("click", logout);
        }
        if (misPrestamosLink) misPrestamosLink.style.display = "block";
        if (adminLibrosLink && isAdmin()) adminLibrosLink.style.display = "block";
        if (adminLink && isAdmin()) adminLink.style.display = "block";
    } else {
        if (loginLink) loginLink.style.display = "block";
        if (logoutBtn) logoutBtn.style.display = "none";
        if (misPrestamosLink) misPrestamosLink.style.display = "none";
        if (adminLibrosLink) adminLibrosLink.style.display = "none";
        if (adminLink) adminLink.style.display = "none";
    }
}

if (document.querySelector("#login-form")) {
    document.querySelector("#login-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            await login(email, password);
            window.location.href = "/index.html";
        } catch (error) {
            alert("Error: " + error.message);
        }
    });
}

if (document.querySelector("#register-form")) {
    document.querySelector("#register-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const nombre = document.getElementById("nombre").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            await register(nombre, email, password);
            alert("Cuenta creada exitosamente. Inicia sesión ahora.");
            window.location.href = "/login.html";
        } catch (error) {
            alert("Error: " + error.message);
        }
    });
}

document.addEventListener("DOMContentLoaded", setupAuthUI);
