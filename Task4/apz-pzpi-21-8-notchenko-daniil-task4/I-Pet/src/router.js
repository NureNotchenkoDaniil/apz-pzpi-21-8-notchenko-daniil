import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import SignInPage from './components/SignInPage.vue';
import SignUpPage from './components/SignUpPage.vue';
import CreateNewPetPage from './components/CreateNewPetPage.vue'
import PetsPage from './components/PetsPage.vue'
import SpecificPetPage from './components/SpecificPetPage.vue'
import CreateDeseasePage from './components/CreateDeseasePage.vue'
import ProfilePage from './components/ProfilePage.vue'
import AdminPage from './components/AdminPage.vue'

const routes = [
  { path: '/', name: "Home", component: HomePage },
  { path: '/signin', name: "SignIn", component: SignInPage },
  { path: '/signup', name: "SignUp", component: SignUpPage },
  { path: '/newpet', name: "CreateNewPetPage", component: CreateNewPetPage },
  { path: '/pets', name: "PetsPage", component: PetsPage },
  { path: '/petsserch', name: "SpecificPetPage", component: SpecificPetPage },
  { path: '/newdesease', name: "CreateDeseasePage", component: CreateDeseasePage },
  { path: '/profile', name: "ProfilePage", component: ProfilePage },
  { path: '/admin', name: "AdminPage", component: AdminPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

