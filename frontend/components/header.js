window.addEventListener("DOMContentLoaded", () => {

    const user = JSON.parse(
        localStorage.getItem("user")
    )

    const header = document.getElementById(
        "header-container"
    )

    if(header){

        header.innerHTML = `

        <div class="topbar">

            <h1>
                School Management System
            </h1>

            <div class="user-box">

                Logged as:
                <strong>
                    ${user?.role || "guest"}
                </strong>

            </div>

        </div>

        `
    }
})