const user = JSON.parse(
    localStorage.getItem("user")
)

if(!user){

    window.location.href = "login.html"
}

if(user.role !== "admin"){

    document.getElementById(
        "form-container"
    ).style.display = "none"
}

async function loadStudents(){

    const response = await fetch(
        "http://127.0.0.1:5000/students",
        {
            headers:{
                "Role": user.role
            }
        }
    )

    const data = await response.json()

    const table = document.getElementById(
        "students-body"
    )

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
                        ?

                        `
                        <button onclick="deleteStudent('${student.id_student}')">
                            Delete
                        </button>

                        <button onclick="editStudent('${student.id_student}')">
                            Edit
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

async function createStudent(){

    const student = {

        id_student:
            document.getElementById("id_student").value,

        name_student:
            document.getElementById("name_student").value,

        birthdate:
            document.getElementById("birthdate").value,

        gender:
            document.getElementById("gender").value,

        enrollment_year:
            parseInt(
                document.getElementById(
                    "enrollment_year"
                ).value
            ),

        id_department:
            parseInt(
                document.getElementById(
                    "id_department"
                ).value
            )
    }

    const response = await fetch(
        "http://127.0.0.1:5000/students",
        {
            method: "POST",

            headers:{
                "Content-Type":"application/json",
                "Role": user.role
            },

            body: JSON.stringify(student)
        }
    )

    const data = await response.json()

    alert(data.message || data.error)

    loadStudents()
}

async function deleteStudent(id){

    if(!confirm("Delete student?")){

        return
    }

    const response = await fetch(
        `http://127.0.0.1:5000/students/${id}`,
        {
            method: "DELETE",

            headers:{
                "Role": user.role
            }
        }
    )

    const data = await response.json()

    alert(data.message || data.error)

    loadStudents()
}

async function editStudent(id){

    const newName = prompt(
        "New student name:"
    )

    if(!newName){

        return
    }

    const response = await fetch(
        `http://127.0.0.1:5000/students/${id}`,
        {
            method: "PUT",

            headers:{
                "Content-Type":"application/json",
                "Role": user.role
            },

            body: JSON.stringify({

                name_student: newName,

                birthdate: "2000-01-01",

                gender: "M",

                enrollment_year: 2024,

                id_department: 1
            })
        }
    )

    const data = await response.json()

    alert(data.message || data.error)

    loadStudents()
}

function goBack(){

    window.location.href = "dashboard.html"
}

function logout(){

    localStorage.removeItem("user")

    window.location.href = "login.html"
}

loadStudents()