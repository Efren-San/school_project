async function loadStats(){

    try{

        const response = await fetch(
            "http://127.0.0.1:5000/stats"
        )

        const data = await response.json()

        document.getElementById(
            "students-count"
        ).innerText = data.students

        document.getElementById(
            "courses-count"
        ).innerText = data.courses

        document.getElementById(
            "enrollments-count"
        ).innerText = data.enrollments

        document.getElementById(
            "gpa-count"
        ).innerText = data.avg_gpa

    }catch(error){

        console.log(error)
    }
}

loadStats()