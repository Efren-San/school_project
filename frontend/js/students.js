const user = JSON.parse(localStorage.getItem("user"))

// auth guar
if (!user) {
    window.location.href = "login.html"
}

// Si no es admin, ocultamos formulario
if (user.role !== "admin") {
    const form = document.getElementById("form-container")
    if (form) form.style.display = "none"
}

const API = "http://127.0.0.1:5000"
async function loadStudents() {

    try {

        const response = await fetch(`${API}/students`, {
            headers: {
                "Role": user.role
            }
        })

        const data = await response.json()

        const table = document.getElementById("students-body")
        table.innerHTML = ""

        data.forEach(student => {

            table.innerHTML += `
                <tr>
                    <td>${student.id_student}</td>
                    <td>${student.name_student}</td>
                    <td>${student.birthdate}</td>
                    <td>${student.gender}</td>
                    <td>${student.enrollment_year}</td>
                    <td>${student.id_department}</td>

                    <td>
                        ${
                            user.role === "admin"
                                ? `
                                    <button class="btn btn-danger btn-sm"
                                        onclick="deleteStudent('${student.id_student}')">
                                        Delete
                                    </button>

                                    <button class="btn btn-primary btn-sm"
                                        onclick="editStudent('${student.id_student}')">
                                        Edit
                                    </button>
                                `
                                : ""
                        }
                    </td>
                </tr>
            `
        })

    } catch (error) {
        console.error("Error loading students:", error)
    }
}

async function createStudent() {

    const student = {
        id_student: document.getElementById("id_student").value,
        name_student: document.getElementById("name_student").value,
        birthdate: document.getElementById("birthdate").value,
        gender: document.getElementById("gender").value,
        enrollment_year: parseInt(document.getElementById("enrollment_year").value),
        id_department: document.getElementById("id_department").value
    }

    const response = await fetch(`${API}/students`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Role": user.role
        },
        body: JSON.stringify(student)
    })

    const data = await response.json()

    await Swal.fire({
        icon: data.error ? "error" : "success",
        title: data.error ? "Error" : "Success",
        text: data.message || data.error
    })

    loadStudents()
}

async function deleteStudent(id) {

    const result = await Swal.fire({
        title: "Delete student?",
        text: "This action cannot be undone",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete",
        cancelButtonText: "Cancel"
    })

    if (!result.isConfirmed) return

    const response = await fetch(`${API}/students/${id}`, {
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

    loadStudents()
}

async function editStudent(id) {

    const { value: newName } = await Swal.fire({
        title: "Edit student name",
        input: "text",
        inputPlaceholder: "Enter new student name",
        showCancelButton: true
    })

    if (!newName) return

    const response = await fetch(`${API}/students/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Role": user.role
        },
        body: JSON.stringify({
            name_student: newName,
            birthdate: "2000-01-01",
            gender: "M",
            enrollment_year: 2024,
            id_department: "D001"
        })
    })

    const data = await response.json()

    await Swal.fire({
        icon: data.error ? "error" : "success",
        title: data.error ? "Error" : "Success",
        text: data.message || data.error
    })

    loadStudents()
}

function goBack() {
    window.location.href = "dashboard.html"
}


loadStudents()