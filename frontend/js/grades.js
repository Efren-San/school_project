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
// LOAD GRADES
// =========================
async function loadGrades() {

    try {

        const response = await fetch(`${API}/grades`, {
            headers: {
                "Role": user.role
            }
        })

        const data = await response.json()

        const table = document.getElementById("grades-body")
        table.innerHTML = ""

        data.forEach(grade => {

            table.innerHTML += `
                <tr>
                    <td>${grade.student}</td>
                    <td>${grade.course}</td>
                    <td>${grade.final_grade}</td>
                    <td>${grade.gpa}</td>

                    <td>
                        ${
                            user.role === "admin" || user.role === "teacher"
                                ? `
                                    <button class="btn btn-primary btn-sm"
                                        onclick="editGrade('${grade.id_enrollment}')">
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
        console.error("Error loading grades:", error)
    }
}

// =========================
// EDIT GRADE
// =========================
async function editGrade(id) {

    const { value: newGrade } = await Swal.fire({
        title: "Update grade",
        input: "number",
        inputLabel: "Final grade (0 - 100)",
        inputAttributes: {
            min: 0,
            max: 100,
            step: 1
        },
        showCancelButton: true
    })

    if (newGrade === null || newGrade === "") return

    const response = await fetch(`${API}/grades/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Role": user.role
        },
        body: JSON.stringify({
            final_grade: parseFloat(newGrade)
        })
    })

    const data = await response.json()

    await Swal.fire({
        icon: data.error ? "error" : "success",
        title: data.error ? "Error" : "Updated",
        text: data.message || data.error
    })

    loadGrades()
}

// =========================
// NAVIGATION (UNIFIED DASHBOARD)
// =========================

// 🔥 DASHBOARD ÚNICO
function goBack() {
    window.location.href = "dashboard.html"
}

// =========================
// INIT
// =========================
loadGrades()