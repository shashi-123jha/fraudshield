// =============================
// GLOBAL TOKEN
// =============================
let token = localStorage.getItem("token") || null;


// =============================
// NAVBAR TOGGLE (Mobile)
// =============================
function toggleMenu() {
    const nav = document.getElementById("navLinks");

    if (nav.style.display === "flex") {
        nav.style.display = "none";
    } else {
        nav.style.display = "flex";
        nav.style.flexDirection = "column";
    }
}


// =============================
// SIGNUP FUNCTION
// =============================
async function signup() {

    const name = document.getElementById("signupName").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;
    const role = document.getElementById("signupRole").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/api/auth/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password, role })
        });

        const data = await response.json();

        if (response.status === 201) {
            alert("Signup successful! Now login.");
        } else {
            alert(data.error || "Signup failed.");
        }

    } catch (error) {
        alert("Server error during signup.");
    }
}


// =============================
// LOGIN FUNCTION
// =============================
async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok && data.token) {
            token = data.token;
            localStorage.setItem("token", token);
            alert("Login successful!");
        } else {
            alert(data.error || "Invalid credentials.");
        }

    } catch (error) {
        alert("Server error during login.");
    }
}


// =============================
// LOGOUT
// =============================
function logout() {
    localStorage.removeItem("token");
    token = null;
    alert("Logged out successfully.");
}


// =============================
// FRAUD CHECK FUNCTION
// =============================
async function checkFraud() {

    const amountValue = document.getElementById("amount").value;
    const typeValue = document.getElementById("type").value;
    const locationValue = document.getElementById("location").value;
    const deviceValue = document.getElementById("device").value;
    const failedAttemptsValue = document.getElementById("failedAttempts").value;
    const timeValue = document.getElementById("time").value;

    const savedToken = localStorage.getItem("token");

    if (!savedToken) {
        alert("Please login first!");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + savedToken
            },
            body: JSON.stringify({
                amount: Number(amountValue),
                transaction_type: Number(typeValue),
                location: Number(locationValue),
                device: Number(deviceValue),
                failedAttempts: Number(failedAttemptsValue),
                time: Number(timeValue)
            })
        });

        const data = await response.json();
        const output = document.getElementById("output");

        if (response.ok) {

            output.innerHTML = `
                ML Prediction: <b>${data.ml_prediction}</b><br>
                Risk Score: <b>${data.risk_score}</b><br>
                Final Result: <b>${data.final_result}</b>
            `;

            if (data.final_result.includes("Fraud")) {
                output.style.color = "red";
            } else {
                output.style.color = "limegreen";
            }

        } else {
            output.innerHTML = data.error;
            output.style.color = "orange";
        }

    } catch (error) {
        console.error(error);
        alert("Server error during prediction.");
    }
}


// =============================
// AUTO CHECK LOGIN STATUS
// =============================
window.onload = function () {
    if (token) {
        console.log("User already logged in.");
    }
};
