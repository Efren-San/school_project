const user = JSON.parse(
    localStorage.getItem("user")
)

if(!user){

    window.location.href = "login.html"
}

const API = "http://127.0.0.1:5000"


// =========================
// LOAD COURSES
// =========================
async function loadCourses(){

    try{

        const response = await fetch(

            `${API}/courses`,

            {
                headers:{
                    "Role": user.role
                }
            }
        )

        const data = await response.json()

        const select =
            document.getElementById("course-id")

        select.innerHTML = `
            <option value="">
                Select Course
            </option>
        `

        data.forEach(course => {

            select.innerHTML += `

                <option value="${course.id_course}">

                    ${course.id_course}
                    -
                    ${course.name_course}

                </option>
            `
        })

    }catch(error){

        console.log(
            "Courses error:",
            error
        )
    }
}


// =========================
// LOAD DISTRIBUTION
// =========================
async function loadDistribution(){

    const courseId =
        document.getElementById(
            "course-id"
        ).value

    if(!courseId){

        Swal.fire({

            icon: "warning",

            title: "Select a course"
        })

        return
    }

    try{

        const response = await fetch(

            `${API}/grades/distribution/${courseId}`,

            {
                headers:{
                    "Role": user.role
                }
            }
        )

        const data = await response.json()

        const table =
            document.getElementById(
                "distribution-body"
            )

        table.innerHTML = ""

        data.forEach(item => {

            table.innerHTML += `

                <tr>

                    <td>${item.category}</td>

                    <td>${item.total}</td>

                </tr>
            `
        })

    }catch(error){

        console.log(
            "Distribution error:",
            error
        )
    }
}


// =========================
// NAVIGATION
// =========================
function goBack(){

    window.location.href =
        "dashboard.html"
}

function logout(){

    localStorage.removeItem("user")

    window.location.href =
        "login.html"
}


// =========================
// INIT
// =========================
loadCourses()