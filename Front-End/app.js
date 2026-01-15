
const API_URL = "";

// ==========================================
// 1. LOGIN LOGIC (For login.html)
// ==========================================
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        const errorMsg = document.getElementById('errorMsg');

        try {
            const res = await fetch(`${API_URL}/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            if (!res.ok) throw new Error("Invalid Email or Password");

            const data = await res.json();
            
            // Save token and redirect
            localStorage.setItem("token", data.access_token);
            window.location.href = "disease.html"; 

        } catch (err) {
            errorMsg.innerText = err.message;
            errorMsg.style.display = "block";
        }
    });
}

// ==========================================
// 2. SIGNUP LOGIC (For signup.html)
// ==========================================
if (document.getElementById('signupForm')) {
    document.getElementById('signupForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const errorMsg = document.getElementById('signupError');
        errorMsg.style.display = 'none'; // Reset error

        // Gather all fields
        const payload = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            age: parseInt(document.getElementById('age').value),
            gender: document.getElementById('gender').value,
            contact_no: document.getElementById('contact').value,
            patient_id: document.getElementById('pid').value
        };

        try {
            const res = await fetch(`${API_URL}/auth/signup`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Signup failed");
            }

            alert("Account created successfully! Please login.");
            window.location.href = "login.html";

        } catch (err) {
            errorMsg.innerText = err.message;
            errorMsg.style.display = "block";
        }
    });
}

// ==========================================
// 3. DISEASE PREDICTION LOGIC (For disease.html)
// ==========================================
if (document.getElementById('diseaseForm')) {
    
    // A. Check if user is logged in
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "login.html"; // Redirect if no token
    }

    // B. Handle Form Submit
    document.getElementById('diseaseForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            age: 30, // Default or fetch from profile if you add that later
            gender: "Male",
            weight: parseFloat(document.getElementById('weight').value),
            height: parseFloat(document.getElementById('height').value),
            disease: document.getElementById('disease').value
        };

        try {
            const res = await fetch(`${API_URL}/diet/predict`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}` // Send the key!
                },
                body: JSON.stringify(payload)
            });

            if (res.status === 401) {
                alert("Session expired. Please login again.");
                logout();
                return;
            }

            const data = await res.json();

            // C. Show Results
            document.getElementById('bmiDisplay').innerText = `${data.bmi_value} (${data.bmi_category})`;
            document.getElementById('dietDisplay').innerText = data.diet_type;
            document.getElementById('caloriesDisplay').innerText = data.calories + " kcal";
            document.getElementById('avoidDisplay').innerText = Array.isArray(data.avoid_foods) 
                ? data.avoid_foods.join(", ") 
                : data.avoid_foods;

            // Hide Form, Show Result
            document.getElementById('inputSection').classList.add('hidden');
            document.getElementById('resultSection').classList.remove('hidden');

        } catch (err) {
            console.error(err);
            alert("Error generating plan. Is the backend running?");
        }
    });

    // C. Handle "Go Back" Button
    document.getElementById('backBtn').addEventListener('click', () => {
        document.getElementById('resultSection').classList.add('hidden');
        document.getElementById('inputSection').classList.remove('hidden');
    });
}

// ==========================================
// 4. LOGOUT FUNCTION
// ==========================================
function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}