const user = JSON.parse(localStorage.getItem("user"))
if(!user){

    window.location.href = "login.html"
}

// document.getElementById("role-label").innerText =
//     `Logged as: ${user.role.toUpperCase()}`

async function loadDashboard(){

    try{

        const headers = {

            "Role": user.role,
            "Student-Id":
                user.id_student || "",
            "Instructor-Id":
                user.id_instructor || ""
        }

        const response = await fetch(
            "http://127.0.0.1:5000/dashboard",
            {
                headers
            }
        )

        const data = await response.json()
        // =========================
        // STATS RENDER
        // =========================

        const stats = data.stats

        // CARD 1
        document.getElementById("stat-1-title").innerText =
            stats.card1_title || "Stat 1"
        document.getElementById("stat-1").innerText =
            stats.card1_value || 0

        document.getElementById("stat-2-title").innerText =
            stats.card2_title || "Stat 2"
        document.getElementById("stat-2").innerText =
            stats.card2_value || 0

        document.getElementById("stat-3-title").innerText =
            stats.card3_title || "Stat 3"
        document.getElementById("stat-3").innerText =
            stats.card3_value || 0

        // Revisa esta card
        document.getElementById("stat-4-title").innerText =
            stats.card4_title || "Stat 4"
        document.getElementById("stat-4").innerText =
            stats.card4_value || 0


        const actionsDiv =
            document.getElementById("actions")

        actionsDiv.innerHTML = ""

        data.actions.forEach(action => {

            actionsDiv.innerHTML += `
                <a
                    href="${action.link}"
                    class="btn btn-primary"
                >
                    ${action.name}
                </a>
            `
        })

    }catch(error){

        console.log("Dashboard error:", error)

        document.getElementById("stat-1").innerText = "0"
        document.getElementById("stat-2").innerText = "0"
        document.getElementById("stat-3").innerText = "0"
        document.getElementById("stat-4").innerText = "0"
    }
}

function logout(){

    localStorage.removeItem("user")

    window.location.href =
        "login.html"
}

loadDashboard()