<script setup>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useStore();
const newsItems = ref([]);
const currentPage = ref(1);
const itemsPerPage = ref(6); // Number of items to display per page
const url = "http://localhost:3000/news"; // Base URL for news items
const searchQuery = ref({
  term: "",
  date: "",
  category: "",
}); // Search query for filtering news items
const categories = [
  "Education", "Art", "Technology", "Community", "Transport", "Science",
  "Events", "Business", "Heritage", "Sports", "Music", "Environment"
];

const vDisableLike = {
  mounted(el) {
    if (!store.state.user) {
      el.disabled = true; // Disable the button if no user is logged in
    }
  },
};

onMounted(async () => {
  fetchNewsItems();
});

async function fetchNewsItems() {
  try {
    const response = await fetch(url);
    const data = await response.json();
    newsItems.value = data;
  } catch (error) {
    console.error("Error fetching news data:", error);
  }
}

async function likeItem(item) {
  item.likes.push(store.state.user);
  console.log("Liking news item:", item);
  putLikes(item);
}

async function unlikeItem(item) {
  item.likes.splice(item.likes.indexOf(store.state.user), 1)
  console.log("Unlinking news item:", item);
  putLikes(item);
}

async function putLikes(item) {
  try {
    const sendLike = await fetch(`${url}/${item.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(item)
    });
    const response = await sendLike.json();
    console.log(response);
  } catch (error) {
    console.error("Error updating likes news item:", error);
  }
}

function clickCallback(pageNum) {
  // This function will be called when a page is clicked
  currentPage.value = pageNum;
}

function filteredNewsItems() {
  return newsItems.value.filter(item =>
    item.category.toLowerCase().match(searchQuery.value.category.toLowerCase()) &&
    item.date.toLowerCase().match(searchQuery.value.date.toLowerCase()) &&
    (item.title.toLowerCase().match(searchQuery.value.term.toLowerCase()) ||
      item.content.toLowerCase().match(searchQuery.value.term.toLowerCase()))
  );
}

function getItems() {
  const current = currentPage.value * itemsPerPage.value;
  const start = current - itemsPerPage.value;
  return filteredNewsItems().slice(start, current);
}

function getNumPages() {
  return Math.ceil(filteredNewsItems().length / itemsPerPage.value);
}

async function deleteArticle(id) {
  if (confirm("Are you sure you want to delete this article?")) {
    try {
      const response = await fetch(`${url}/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const msg = await response.json();
      alert(msg + " deleted successfully!");
      fetchNewsItems(); // Refresh the news items after deletion
    } catch (error) {
      console.error("Error deleting article:", error);
    }
  }
}

function editArticle(item) {
  store.commit("editArticle", item);
  router.push("/ArticleEditor");
}

function newArticle() {
  store.commit("clearArticle");
  router.push("/ArticleEditor");
}

</script>

<template>
  <div class="container">
    <div class="row text-start justify-content-center">
      <div class="col-sm-10 col-md-10 col-lg-10">
        <h1>News Page</h1>
        <p>
          Welcome to the news page of our application, where you can find the
          latest updates and announcements related to our project. Stay tuned
          for more information!
        </p>
      </div>

      <div class="col-sm-10 col-md-10 col-lg-10">
        <div class="row">
          <div class="col-sm-6">
            <div class="row">
              <div class="col-sm-6">
                <label for="searchTerm">Article Search:</label>
              </div>
              <div class="col-sm-6">
                <input type="text" class="form-control" placeholder="Search by title or content"
                  v-model="searchQuery.term" id="searchTerm">
              </div>
            </div>
          </div>

          <div class="col-sm-3">
            <select class="form-select" v-model="searchQuery.category" id="categorySelect">
              <option value="" selected>All</option>
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
          <div class="col-sm-3">
            <input type="date" class="form-control" placeholder="Search by date" v-model="searchQuery.date"
              id="dateInput">
          </div>
        </div>
      </div>

      <div class="col-sm-10 col-md-10 col-lg-10">
        <button class="btn btn-primary" @click="newArticle" v-if="store.state.authorised">Create New
          Article</button>
      </div>

      <div v-for="item in getItems()" class="col-sm-10 col-md-6 col-lg-4">
        <h2>{{ item.title }}</h2>
        <img v-if="item.image" :src="item.image" alt="Article image" class="img-fluid mb-3"
          style="max-height: 200px; width: 100%; object-fit: cover; border-radius: 8px;">
        <h5>{{ item.category }}</h5>
        <p>{{ item.date }}</p>
        <p>{{ item.content }}</p>
        <p>
          <button class="btn btn-primary" @click="likeItem(item)" v-if="!item.likes.includes(store.state.user)"
            v-disableLike>Like {{ item.likes.length }}</button>
          <button class="btn btn-outline-primary" @click="unlikeItem(item)"
            v-if="item.likes.includes(store.state.user)">Unlike {{ item.likes.length }}</button>
          <button class="btn btn-secondary" v-if="store.state.authorised" @click="editArticle(item)">Edit
            Article</button>
          <button class="btn btn-danger" v-if="store.state.authorised" @click="deleteArticle(item.id)">Delete
            Article</button>
        </p>
      </div>
      <div class="col-sm-12">
        <paginate class="justify-content-center" :page-count="getNumPages()" :page-range="3" :margin-pages="1"
          :click-handler="clickCallback" :prev-text="'Prev Page'" :next-text="'Next Page'"
          :container-class="'pagination'" :page-class="'page-item'" :active-class="'currentPage'">
        </paginate>
      </div>
    </div>
  </div>
</template>

<style>
.pagination a {
  /* style for the anchor */
  color: black;
  border: 1px solid #ddd;
  float: left;
  padding: 8px 16px;
  text-decoration: none;
}

.currentPage a {
  /* style to indicate the current page  */
  background-color: lightblue;
}
</style>
