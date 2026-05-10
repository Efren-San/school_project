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
// LOAD COURSES
// =========================
async function loadCourses() {

    try {

        const response = await fetch(`${API}/courses`, {
            headers: {
                "Role": user.role
            }
        })

        const data = await response.json()

        const table = document.getElementById("courses-body")
        table.innerHTML = ""

        data.forEach(course => {

            table.innerHTML += `
                <tr>
                    <td>${course.id_course}</td>
                    <td>${course.name_course}</td>
                    <td>${course.credits}</td>
                    <td>${course.semester}</td>

                    <td>
                        ${
                            user.role === "admin"
                                ? `
                                    <button class="btn btn-danger btn-sm"
                                        onclick="deleteCourse('${course.id_course}')">
                                        Delete
                                    </button>

                                    <button class="btn btn-primary btn-sm"
                                        onclick="editCourse('${course.id_course}')">
                                        Edit
                                    </button>
                                `
                                : "-"
                        }
                    </td>
                </tr>
            `
        })

    } catch (error) {
        console.error("Error loading courses:", error)
    }
}

// =========================
// DELETE COURSE
// =========================
async function deleteCourse(id) {

    const result = await Swal.fire({
        title: "Delete course?",
        text: "This action cannot be undone",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete",
        cancelButtonText: "Cancel"
    })

    if (!result.isConfirmed) return

    const response = await fetch(`${API}/courses/${id}`, {
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

    loadCourses()
}

// =========================
// EDIT COURSE
// =========================
async function editCourse(id) {

    const { value: newName } = await Swal.fire({
        title: "Edit course name",
        input: "text",
        inputPlaceholder: "Enter new course name",
        showCancelButton: true
    })

    if (!newName) return

    const response = await fetch(`${API}/courses/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Role": user.role
        },
        body: JSON.stringify({
            name_course: newName
        })
    })

    const data = await response.json()

    await Swal.fire({
        icon: data.error ? "error" : "success",
        title: data.error ? "Error" : "Updated",
        text: data.message || data.error
    })

    loadCourses()
}

// =========================
// NAVIGATION FIX (IMPORTANTE)
// =========================

// 🔥 SI USAS DASHBOARD ÚNICO:
function goBack() {
    window.location.href = "dashboard.html"
}

// 🔥 SI CAMBIAS A DASHBOARD POR ROL:
// window.location.href = `dashboard_${user.role}.html`

// =========================
// INIT
// =========================
loadCourses()