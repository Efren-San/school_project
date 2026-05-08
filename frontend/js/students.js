const user = JSON.parse(
    localStorage.getItem("user")
)

if(!user){

    window.location.href = "login.html"
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
            </tr>
        `
    })
}

function goBack(){

    window.location.href = "dashboard.html"
}

loadStudents()