<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const store = useStore();
const router = useRouter();


const inputUsername = ref("");
const inputPassword = ref("");

function loginUser(e) {
    e.preventDefault(); // Prevent the default form submission behavior


    if (!inputUsername.value) {
        alert("Username cannot be empty!");
    } else if (!inputPassword.value) {
        alert("Password cannot be empty!");
    } else {
        var url = "http://localhost:3000/accounts"; //URL to fetch the accounts data from
        const accounts = ref([]); // Create a reactive reference for accounts

        fetch(url) //javascript fetch api
            .then((response) => {
                //turning the response into the usable data
                return response.json();
            })
            .then((data) => {
                //This is the data you wanted to get from url
                accounts.value = data;
                let userFound = false;
                let isAdmin = false;
                for (const account of accounts.value) {
                    if (account.username === inputUsername.value && account.password === inputPassword.value) {
                        userFound = true;
                        isAdmin = account.isAdmin; // Check if the user is an admin
                        break;
                    }
                }
                if (userFound) {
                    alert("Login successful!");

                    store.commit("setUser", inputUsername.value);
                    if (isAdmin) {
                        store.commit("setAuthorised", true);
                    }

                    router.push("/");

                } else {
                    alert("Invalid username or password!");
                }
            })
            .catch((error) => {
                console.error("Error fetching accounts data:", error);
            });
    }
}
</script>
<template>
    <div class="row text-start justify-content-between">
        <div class="col-sm-10 col-md-10 col-lg-4">
            <h1>Login</h1>
        </div>
        <div class="col-sm-10 col-md-10 col-lg-4">
            <form @submit="loginUser" class="row g-3">
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
                <div class="col-6">
                    <button type="submit" class="btn btn-primary">Login</button>
                </div>
                <div class="col-6">
                    <button type="button" class="btn btn-secondary" onclick="location.href='/NewUser'">Create
                        Account</button>
                </div>
            </form>
        </div>
    </div>
</template>
