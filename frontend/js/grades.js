const user = JSON.parse(
    localStorage.getItem("user")
)

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
            </tr>
        `
    })
}

function goBack(){

    window.location.href = "dashboard.html"
}

loadGrades()