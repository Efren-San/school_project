function dashboardRoute(role){

    switch(role){

        case "admin":
            return "dashboard_admin.html"

        case "teacher":
            return "dashboard_teacher.html"

        case "student":
            return "dashboard_student.html"

        default:
            return "login.html"
    }
}