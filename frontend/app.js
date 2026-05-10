const API_URL = "http://127.0.0.1:5000/students";

async function loadStudents() {

    const response = await fetch(API_URL);

    const students = await response.json();

    const table = document.getElementById("studentsTable");

    table.innerHTML = "";

    students.forEach(student => {

        table.innerHTML += `
        
        <tr>

            <td>${student.id_student}</td>

            <td>${student.name_student}</td>

            <td>${student.gender}</td>

            <td>${student.id_department}</td>

            <td>

                <button 
                    class="btn btn-danger btn-sm"
                    onclick="deleteStudent('${student.id_student}')"
                >
                    Delete
                </button>

            </td>

        </tr>
        `;
    });

}

async function addStudent() {

    const student = {

        id_student: document.getElementById("id_student").value,

        name_student: document.getElementById("name_student").value,

        birthdate: document.getElementById("birthdate").value,

        gender: document.getElementById("gender").value,

        enrollment_year: document.getElementById("enrollment_year").value,

        id_department: document.getElementById("id_department").value
    };

    await fetch(API_URL, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(student)
    });

    loadStudents();
}

async function deleteStudent(id) {

    await fetch(`${API_URL}/${id}`, {

        method: "DELETE"
    });

    loadStudents();
}

loadStudents();