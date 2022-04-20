import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import LogIn from "./components/LogIn.vue";
import SignUp from "./components/SignUp.vue";
import Home from "./components/Home.vue";
import CreateReport from "./components/CreateReport.vue";
const routes = [
  {
    path: "/",
    name: "root",
    component: App,
  },
  {
    path: "/logIn",
    name: "logIn",
    component: LogIn,
  },
  {
    path: "/signUp",
    name: "signUp",
    component: SignUp,
  },
  {
    path: "/home",
    name: "home",
    component: Home,
  },
  {
    path: "/createReport",
    name: "createReport",
    component: CreateReport,
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
