function logout() {
    localStorage.removeItem("user");
    window.location.href = "login.html";
}

function go(page) {
    window.location.href = page;
}