window.addEventListener("DOMContentLoaded", () => {

    const sidebarContainer =
        document.getElementById(
            "sidebar-container"
        )

    if(sidebarContainer){

        sidebarContainer.innerHTML = `

        <div class="sidebar">

            <div class="logo">
                SCHOOL SYS
            </div>

            <a href="dashboard.html">
                Dashboard
            </a>

            <a href="students.html">
                Students
            </a>

            <a href="courses.html">
                Courses
            </a>

            <a href="grades.html">
                Grades
            </a>

            <a href="enrollments.html">
                Enrollments
            </a>

            <button
                class="logout-btn"
                onclick="logout()"
            >
                Logout
            </button>

        </div>

        `
    }
})

function logout(){

    localStorage.removeItem("user")

    window.location.href =
        "login.html"
}