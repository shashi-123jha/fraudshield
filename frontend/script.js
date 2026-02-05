async function checkFraud() {
    const amount = document.getElementById("amount").value;
    const location = document.getElementById("location").value;
    const type = document.getElementById("type").value;

    const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            amount: Number(amount),
            location: Number(location),
            transaction_type: Number(type)
        })
    });

    const data = await response.json();
    document.getElementById("output").innerHTML =
        `Result: <b>${data.prediction}</b>`;
}
