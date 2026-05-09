const user = JSON.parse(
    localStorage.getItem("user")
)

if(!user){

    window.location.href = "login.html"
}

// =========================
// LOAD GRADES
// =========================

async function loadGrades(){

    const response = await fetch(
        "http://127.0.0.1:5000/grades",
        {
            headers:{
                "Role": user.role
            }
        }
    )

    const data = await response.json()

    const table = document.getElementById(
        "grades-body"
    )

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
                        user.role === "teacher"
                        || user.role === "admin"
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
}

// =========================
// EDIT GRADE
// =========================

async function editGrade(id){

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

    if(!newGrade) return

    const response = await fetch(
        `http://127.0.0.1:5000/grades/${id}`,
        {
            method: "PUT",

            headers:{
                "Content-Type":"application/json",
                "Role": user.role
            },

            body: JSON.stringify({
                final_grade: parseFloat(newGrade)
            })
        }
    )

    const data = await response.json()

    await Swal.fire({

        icon: data.error ? "error" : "success",

        title: data.error ? "Error" : "Updated",

        text: data.message || data.error
    })

    loadGrades()
}

// =========================
// NAVIGATION
// =========================

function goBack(){

    window.location.href = "dashboard.html"
}

loadGrades()