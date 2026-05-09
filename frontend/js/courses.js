const user = JSON.parse(
    localStorage.getItem("user")
)

if(!user){

    window.location.href = "login.html"
}

// =========================
// LOAD COURSES
// =========================

async function loadCourses(){

    const response = await fetch(
        "http://127.0.0.1:5000/courses",
        {
            headers:{
                "Role": user.role
            }
        }
    )

    const data = await response.json()

    const table = document.getElementById(
        "courses-body"
    )

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
}

// =========================
// DELETE COURSE
// =========================

async function deleteCourse(id){

    const result = await Swal.fire({

        title: "Delete course?",

        text: "This action cannot be undone",

        icon: "warning",

        showCancelButton: true,

        confirmButtonText: "Yes, delete",

        cancelButtonText: "Cancel"
    })

    if(!result.isConfirmed){

        return
    }

    const response = await fetch(
        `http://127.0.0.1:5000/courses/${id}`,
        {
            method: "DELETE",

            headers:{
                "Role": user.role
            }
        }
    )

    const data = await response.json()

    await Swal.fire({

        icon: data.error ? "error" : "success",

        title: data.error ? "Error" : "Success",

        text: data.message || data.error
    })

    loadCourses()
}

// =========================
// EDIT COURSE (base simple)
// =========================

async function editCourse(id){

    const { value: newName } = await Swal.fire({

        title: "New course name",

        input: "text",

        inputPlaceholder: "Enter new name",

        showCancelButton: true
    })

    if(!newName) return

    const response = await fetch(
        `http://127.0.0.1:5000/courses/${id}`,
        {
            method: "PUT",

            headers:{
                "Content-Type":"application/json",
                "Role": user.role
            },

            body: JSON.stringify({
                name_course: newName
            })
        }
    )

    const data = await response.json()

    await Swal.fire({

        icon: data.error ? "error" : "success",

        title: data.error ? "Error" : "Updated",

        text: data.message || data.error
    })

    loadCourses()
}

// =========================
// NAVIGATION
// =========================

function goBack(){

    window.location.href = "dashboard.html"
}

loadCourses()