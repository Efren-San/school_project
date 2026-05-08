const user = JSON.parse(
    localStorage.getItem("user")
)

if(!user){

    window.location.href = "login.html"
}

if(
    user.role !== "admin"
    &&
    user.role !== "teacher"
){

    document.getElementById(
        "form-container"
    ).style.display = "none"
}

async function loadEnrollments(){

    const response = await fetch(
        "http://127.0.0.1:5000/enrollments",
        {
            headers:{
                "Role": user.role
            }
        }
    )

    const data = await response.json()

    const table = document.getElementById(
        "enrollment-body"
    )

    table.innerHTML = ""

    data.forEach(enrollment => {

        table.innerHTML += `
            <tr>

                <td>${enrollment.id_enrollment}</td>

                <td>${enrollment.id_student}</td>

                <td>${enrollment.id_course}</td>

                <td>${enrollment.semester}</td>

                <td>

                    ${
                        user.role === "admin"
                        ||

                        user.role === "teacher"

                        ?

                        `
                        <button onclick="deleteEnrollment(${enrollment.id_enrollment})">
                            Drop
                        </button>
                        `

                        :

                        ""
                    }

                </td>

            </tr>
        `
    })
}

async function createEnrollment(){

    const enrollment = {

        id_student:
            document.getElementById(
                "id_student"
            ).value,

        id_course:
            parseInt(
                document.getElementById(
                    "id_course"
                ).value
            ),

        semester:
            document.getElementById(
                "semester"
            ).value
    }

    const response = await fetch(
        "http://127.0.0.1:5000/enrollments",
        {
            method: "POST",

            headers:{
                "Content-Type":"application/json",
                "Role": user.role
            },

            body: JSON.stringify(enrollment)
        }
    )

    const data = await response.json()

    alert(data.message || data.error)

    loadEnrollments()
}

async function deleteEnrollment(id){

    if(!confirm("Drop this course?")){

        return
    }

    const response = await fetch(
        `http://127.0.0.1:5000/enrollments/${id}`,
        {
            method: "DELETE",

            headers:{
                "Role": user.role
            }
        }
    )

    const data = await response.json()

    alert(data.message || data.error)

    loadEnrollments()
}

function goBack(){

    window.location.href = "dashboard.html"
}

function logout(){

    localStorage.removeItem("user")

    window.location.href = "login.html"
}

function goEnrollments(){

    window.location.href =
        "enrollments.html"
}

loadEnrollments()