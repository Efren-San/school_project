async function login(){

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    const response = await fetch(
        "http://127.0.0.1:5000/login",
        {
            method: "POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        }
    )

    const data = await response.json()

    console.log("LOGIN RESPONSE:", data)

    if(data.success){

        // guardar usuario
        localStorage.setItem(
            "user",
            JSON.stringify(data.user)
        )

        // 🔥 SIEMPRE IR A UN SOLO DASHBOARD
        window.location.href = "./dashboard.html"

    } else {

        document.getElementById("message").innerText =
            data.message
    }
}