<script setup>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useStore();
const url = "http://localhost:3000/news"; // Base URL for news items
const article = ref({
    title: "",
    content: "",
    category: "",
    date: new Date().toISOString().split("T")[0], // Default to today's date
    likes: [],
    image: ""
});

const maxFileSize = 5 * 1024 * 1024; //Max img size

const categories = [
    "Education", "Art", "Technology", "Community", "Transport", "Science",
    "Events", "Business", "Heritage", "Sports", "Music", "Environment"
];

onMounted(() => {
    if (store.state.editingArticle.id) {
        article.value.title = store.state.editingArticle.title;
        article.value.content = store.state.editingArticle.content;
        article.value.category = store.state.editingArticle.category;
        article.value.date = store.state.editingArticle.date;
        article.value.image = store.state.editingArticle.image || "";
    }
});

async function postArticle(e) {
    e.preventDefault(); // Prevent the default form submission behavior

    if (!article.value.title) {
        alert("Title cannot be empty!");
    } else if (!article.value.content) {
        alert("Content cannot be empty!");
    } else if (!article.value.category) {
        alert("Category cannot be empty!");
    } else {
        try {
            let method = "POST";
            let endpoint = url;
            if (store.state.editingArticle.id) {
                method = "PUT";
                endpoint = `${url}/${store.state.editingArticle.id}`;
            }
            const response = await fetch(endpoint, {
                method: method,
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(article.value)
            });

            const responseData = await response.json();
            alert(responseData + " saved successfully!");
            router.push("/news");
        } catch (error) {
            console.error("Error saving article:", error);
        }
    }
}

function handleImageUpload(event) {
    const file = event.target.files[0];

    if (file.size > maxFileSize) {
        alert('Image file size must be less than 5MB');
        event.target.value = '';
        return;
    }

    const reader = new FileReader();

    reader.onload = (e) => {
        article.value.image = e.target.result;
    }

    reader.readAsDataURL(file);
}

function removeImage() {
    article.value.image = "";
    const fileInput = document.getElementById('imageUpload');
    if (fileInput)
        fileInput.value = '';
}
</script>

<template>
    <div class="container" v-if="!store.state.authorised">
        <div class="row text-start justify-content-center">
            <div class="col-sm-10 col-md-10 col-lg-10">
                <h1>Article Editor</h1>
                <p>You must have administration privileges to edit articles.</p>
            </div>
        </div>
    </div>
    <div class="container" v-if="store.state.authorised">
        <div class="row text-start justify-content-center">
            <div class="col-sm-10 col-md-10 col-lg-10">
                <h1>Article Editor</h1>
                <h2 v-if="!store.state.editingArticle.id">(New Article)</h2>
                <h2 v-else>(Editing Article: {{ store.state.editingArticle.title }})</h2>
            </div>
            <div class="col-sm-10 col-md-10 col-lg-10">
                <form @submit=postArticle>
                    <div class="mb-3">
                        <label for="title" class="form-label">Title</label>
                        <input type="text" class="form-control" id="title" v-model="article.title">
                    </div>
                    <div class="mb-3">
                        <label for="category" class="form-label">Category</label>
                        <select class="form-select" id="category" v-model="article.category">
                            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="content" class="form-label">Content</label>
                        <textarea class="form-control" id="content" v-model="article.content"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="imageUpload" class="form-label">Article Image (Optional)</label>
                        <input type="file" class="form-control" id="imageUpload" accept=".jpeg,.png,.jpg"
                            @change="handleImageUpload">
                        <div class="form-text">Upload an image to display with your article (Max 5MB, JPEG/PNG/JPG)
                        </div>
                        <div v-if="article.image" class="mt-2">
                            <span class="text-success">✓ Image uploaded successfully</span>
                            <button type="button" class="btn btn-sm btn-outline-danger ms-2" @click="removeImage">
                                Remove Image
                            </button>
                        </div>
                        <button type="submit" class="btn btn-primary">Save Article</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>