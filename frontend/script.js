// =====================================
// GLOBAL TOKEN
// =====================================
let token = localStorage.getItem("token") || null;


// =====================================
// GSAP SETUP
// =====================================
gsap.registerPlugin(ScrollTrigger);

// Navbar animation
gsap.from(".navbar", {
    y: -100,
    opacity: 0,
    duration: 1
});

// Hero animation
gsap.from(".hero h1", {
    y: 50,
    opacity: 0,
    duration: 1,
    delay: 0.5
});

gsap.from(".hero p", {
    y: 50,
    opacity: 0,
    duration: 1,
    delay: 0.8
});

gsap.from(".btn", {
    scale: 0,
    opacity: 0,
    duration: 0.8,
    delay: 1.2
});

// Scroll reveal animation
gsap.utils.toArray(".section").forEach(section => {
    gsap.from(section, {
        scrollTrigger: {
            trigger: section,
            start: "top 85%"
        },
        y: 60,
        opacity: 0,
        duration: 1
    });
});


// =====================================
// NAVBAR TOGGLE (Improved)
// =====================================
function toggleMenu() {
    const nav = document.getElementById("navLinks");
    nav.classList.toggle("show");
}


// =====================================
// SIGNUP FUNCTION
// =====================================
async function signup() {

    const name = document.getElementById("signupName").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;
    const role = document.getElementById("signupRole").value;

    if (!name || !email || !password) {
        showMessage("Please fill all fields", "orange");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/auth/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password, role })
        });

        const data = await response.json();

        if (response.status === 201) {
            showMessage("Signup successful! Please login.", "limegreen");
        } else {
            showMessage(data.error || "Signup failed", "red");
        }

    } catch (error) {
        showMessage("Server error during signup", "red");
    }
}


// =====================================
// LOGIN FUNCTION
// =====================================
async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email || !password) {
        showMessage("Enter email & password", "orange");
        return;
    }

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
            showMessage("Login successful 🚀", "limegreen");

            gsap.from(".auth-box", {
                scale: 0.9,
                duration: 0.4
            });

        } else {
            showMessage(data.error || "Invalid credentials", "red");
        }

    } catch (error) {
        showMessage("Server error during login", "red");
    }
}


// =====================================
// LOGOUT
// =====================================
function logout() {
    localStorage.removeItem("token");
    token = null;
    showMessage("Logged out successfully 👋", "orange");
}


// =====================================
// FRAUD CHECK FUNCTION (UPGRADED)
// =====================================
async function checkFraud() {

    const amountValue = document.getElementById("amount").value;
    const typeValue = document.getElementById("type").value;
    const locationValue = document.getElementById("location").value;
    const deviceValue = document.getElementById("device").value;
    const failedAttemptsValue = document.getElementById("failedAttempts").value;
    const timeValue = document.getElementById("time").value;

    const output = document.getElementById("output");
    const savedToken = localStorage.getItem("token");

    if (!savedToken) {
        showMessage("Please login first!", "orange");
        return;
    }

    // Loading animation
    output.innerHTML = "🔍 AI is scanning transaction...";
    output.style.color = "#38bdf8";

    gsap.fromTo("#output",
        { opacity: 0 },
        { opacity: 1, duration: 0.5 }
    );

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

            gsap.fromTo("#output",
                { scale: 0 },
                { scale: 1.1, duration: 0.4, yoyo: true, repeat: 1 }
            );

        } else {
            output.innerHTML = data.error;
            output.style.color = "orange";
        }

    } catch (error) {
        showMessage("Server error during prediction", "red");
    }
}


// =====================================
// CUSTOM MESSAGE FUNCTION (No alerts)
// =====================================
function showMessage(text, color) {

    const message = document.createElement("div");
    message.innerText = text;
    message.style.position = "fixed";
    message.style.bottom = "20px";
    message.style.right = "20px";
    message.style.background = "rgba(0,0,0,0.8)";
    message.style.color = color;
    message.style.padding = "12px 20px";
    message.style.borderRadius = "10px";
    message.style.zIndex = "2000";
    message.style.boxShadow = "0 0 15px " + color;

    document.body.appendChild(message);

    gsap.from(message, { y: 50, opacity: 0, duration: 0.4 });

    setTimeout(() => {
        gsap.to(message, {
            opacity: 0,
            duration: 0.5,
            onComplete: () => message.remove()
        });
    }, 2500);
}


// =====================================
// AUTO CHECK LOGIN STATUS
// =====================================
window.onload = function () {
    if (token) {
        console.log("User already logged in.");
    }
};
