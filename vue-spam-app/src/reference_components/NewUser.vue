<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const inputUsername = ref("");
const inputPassword = ref("");
const inputVerifyPassword = ref("");

async function registerUser(e) {

    e.preventDefault(); // Prevent the default form submission behavior
    if (!inputUsername.value) {
        alert("Username cannot be empty!");
    } else if (!inputPassword.value) {
        alert("Password cannot be empty!");
    } else if (inputPassword.value !== inputVerifyPassword.value) {
        alert("Passwords do not match!");
    } else if (inputPassword.value.length < 8) {
        alert("Password must be at least 8 characters long!");
    } else {
        const url = "http://localhost:3000/accounts"; //URL to fetch the news data from

        try {
            const response = await fetch(url);
            const accounts = await response.json(); //turning the response into the usable data
            let addUser = true;

            for (const account of accounts) {
                if (account.username === inputUsername.value) {
                    alert("Username already exists!");
                    addUser = false;
                    break;
                }
            }
            if (addUser) {
                const postAccount = await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        username: inputUsername.value,
                        password: inputPassword.value,
                        isAdmin: false, // Default to false for new users
                    }),
                });
                const responseData = await postAccount.json();
                console.log("User registered:", responseData);
                alert("User registered successfully!");
                router.push("/login"); // Redirect to the login page after successful registration

            }
        } catch (error) {
            console.error("Error fetching accounts:", error);
        }
    }
}
</script>

<template>
    <div class="row text-start justify-content-between">
        <div class="col-sm-10 col-md-10 col-lg-4">
            <h1>New User Registration</h1>
        </div>
        <div class="col-sm-10 col-md-10 col-lg-4">
            <form @submit="registerUser" class="row g-3">
                <div class="col-md-6">
                    <label for="inputUsername" class="form-label">Username</label>
                    <input name="username" type="text" class="form-control" id="inputUsername" v-model="inputUsername"
                        v-autofocus />
                </div>
                <div class="col-md-6">
                    <label for="inputPassword" class="form-label">Password</label>
                    <input name="password" type="password" class="form-control" id="inputPassword"
                        v-model="inputPassword" />
                </div>
                <div class="col-md-6">
                    <label for="inputVerifyPassword" class="form-label">Verify Password</label>
                    <input type="password" class="form-control" id="inputVerifyPassword"
                        v-model="inputVerifyPassword" />
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">Register</button>
                </div>
            </form>
        </div>
    </div>
</template>
