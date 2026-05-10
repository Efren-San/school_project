const user = JSON.parse(
    localStorage.getItem("user")
)

if(!user){

    window.location.href = "login.html"
}

const API = "http://127.0.0.1:5000"

// =========================
// GET STUDENT ID
// =========================

let studentId = user.id_student

// admin/teacher demo
if(user.role !== "student"){

    studentId = "S001"
}

// =========================
// LOAD TRANSCRIPT
// =========================

async function loadTranscript(){

    const response = await fetch(

        `${API}/transcript/${studentId}`,

        {
            headers:{
                "Role": user.role
            }
        }
    )

    const data = await response.json()

    const table = document.getElementById(
        "transcript-body"
    )

    table.innerHTML = ""

    if(data.transcript.length > 0){

        document.getElementById(
            "student-name"
        ).innerText =
            data.transcript[0].name_student
    }

    document.getElementById(
        "total-credits"
    ).innerText =
        data.total_credits

    document.getElementById(
        "avg-gpa"
    ).innerText =
        data.avg_gpa

    data.transcript.forEach(item => {

        table.innerHTML += `

            <tr>

                <td>${item.course}</td>

                <td>${item.credits}</td>

                <td>${item.final_grade}</td>

                <td>${item.gpa_points}</td>

            </tr>
        `
    })
}

// =========================
// NAVIGATION
// =========================

function goBack(){

    window.location.href = "dashboard.html"
}

loadTranscript()