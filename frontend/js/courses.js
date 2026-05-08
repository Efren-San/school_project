async function loadCourses(){

    const response = await fetch(
        "http://127.0.0.1:5000/courses"
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
            </tr>
        `
    })
}

function goBack(){

    window.location.href = "dashboard.html"
}

loadCourses()