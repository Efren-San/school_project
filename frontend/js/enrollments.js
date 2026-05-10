const user = JSON.parse(localStorage.getItem("user"))

// =========================
// AUTH GUARD
// =========================
if (!user) {
    window.location.href = "login.html"
}

// =========================
// API BASE
// =========================
const API = "http://127.0.0.1:5000"

// =========================
// ROLE UI CONTROL
// =========================
if (user.role !== "admin" && user.role !== "teacher") {
    const form = document.getElementById("form-container")
    if (form) form.style.display = "none"
}

// =========================
// LOAD ENROLLMENTS
// =========================
async function loadEnrollments() {

    try {

        const response = await fetch(`${API}/enrollments`, {
            headers: {
                "Role": user.role
            }
        })

        const data = await response.json()

        const table = document.getElementById("enrollment-body")
        table.innerHTML = ""

        data.forEach(enrollment => {

            table.innerHTML += `
                <tr>
                    <td>${enrollment.id_enrollment}</td>
                    <td>${enrollment.student}</td>
                    <td>${enrollment.course}</td>
                    <td>${enrollment.enrollment_date}</td>
                    <td>${enrollment.semester}</td>

                    <td>
                        ${
                            user.role === "admin" || user.role === "teacher"
                                ? `
                                    <button class="btn btn-danger btn-sm"
                                        onclick="deleteEnrollment(${enrollment.id_enrollment})">
                                        Drop
                                    </button>
                                `
                                : "-"
                        }
                    </td>
                </tr>
            `
        })

    } catch (error) {
        console.error("Error loading enrollments:", error)
    }
}

// =========================
// CREATE ENROLLMENT
// =========================
async function createEnrollment() {

    const enrollment = {
        id_student: document.getElementById("id_student").value,
        id_course: document.getElementById("id_course").value,
        semester: document.getElementById("semester").value
    }

    const response = await fetch(`${API}/enrollments`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Role": user.role
        },
        body: JSON.stringify(enrollment)
    })

    const data = await response.json()

    await Swal.fire({
        icon: data.error ? "error" : "success",
        title: data.error ? "Error" : "Success",
        text: data.message || data.error
    })

    loadEnrollments()
}

// =========================
// DELETE ENROLLMENT
// =========================
async function deleteEnrollment(id) {

    const result = await Swal.fire({
        title: "Drop this course?",
        text: "This action cannot be undone",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, drop",
        cancelButtonText: "Cancel"
    })

    if (!result.isConfirmed) return

    const response = await fetch(`${API}/enrollments/${id}`, {
        method: "DELETE",
        headers: {
            "Role": user.role
        }
    })

    const data = await response.json()

    await Swal.fire({
        icon: data.error ? "error" : "success",
        title: data.error ? "Error" : "Success",
        text: data.message || data.error
    })

    loadEnrollments()
}

// =========================
// NAVIGATION (UNIFIED DASHBOARD)
// =========================

// 🔥 DASHBOARD ÚNICO
function goBack() {
    window.location.href = "dashboard.html"
}

// =========================
// LOGOUT
// =========================
function logout() {
    localStorage.removeItem("user")
    window.location.href = "login.html"
}

// =========================
// OPTIONAL NAV (si lo usas)
// =========================
function goEnrollments() {
    window.location.href = "enrollments.html"
}

// =========================
// INIT
// =========================
loadEnrollments()