import axios from 'axios';
<template>
  <div id="app" class="app">
    <!-- id = cual es la aplicación -->

    <div class="header" id="header" v-if="is_auth">
      <nav>
        <button v-if="is_auth" v-on:click="loadHome">Inicio</button>
        <button v-if="is_auth" v-on:click="logOut">Cerrar Sesión</button>
        <button v-if="is_auth && is_admin" v-on:click="loadSignUp">
          Nuevo Usuario
        </button>
        <!--         
          <button v-if="is_auth && is_admin" v-on:click="loadPortalAdmin">
          Admin
        </button> -->
      </nav>
    </div>

    <div class="main-component">
      <!-- funciones a travez de las cuales los hijos van a comunicarse con el padre -->
      <!-- se implementan en export default -->
      <router-view
        v-on:completedLogIn="completedLogIn"
        v-on:completedSignUp="completedSignUp"
        v-on:logOut="logOut"
        v-on:loadHome="loadHome"
        v-on:loadAdmin="loadAdmin"
        v-on:loadSignUp="loadSignUp"
        v-on:loadLogIn="loadLogIn"
        v-on:verifyToken="verifyToken"
      >
      </router-view>
    </div>

    <!--     <div class="footer">
      <h2>Misión TIC 2022</h2>
    </div> -->
  </div>
</template>

<script>
import axios from "axios";
import jwt_decode from "jwt-decode";
export default {
  name: "App", // nombre del componente
  data: function () {
    // informacion que va a tener el componente y que se va apoder mostrar dentro el template
    return {
      is_auth: false,
      is_admin: false,
      is_client: false,
      name: "",
      userId: "",
      startLoader: false,
    };
  },

  components: {}, //componentes con los que se va a comunicar
  methods: {
    // metodos que definen el comportamiento que tendrá la aplicación
    verifyAuth: function () {
      this.getUserData();
      this.is_auth = localStorage.getItem("isAuth") || false;
      if (this.is_auth == false) {
        this.$router.push({ name: "logIn" });
      } else {
        this.$router.push({ name: "home" });
      }
    },

    loadHome: function () {
      this.$router.push({ name: "home" });
    },
    loadLogIn: function () {
      this.$router.push({ name: "logIn" });
    },
    loadSignUp: function () {
      this.$router.push({ name: "signUp" });
    },

    completedLogIn: function (data) {
      localStorage.setItem("isAuth", true);
      localStorage.setItem("email", data.email);
      localStorage.setItem("token_access", data.token_access);
      localStorage.setItem("token_refresh", data.token_refresh);
      /* alert("Autenticación Exitosa"); */
      this.verifyAuth();
      this.getUserData();
    },
    completedSignUp: function (data) {
      alert("Registro Exitoso");
      this.completedLogIn(data);
    },

    loadHome: function () {
      this.$router.push({ name: "home" });
    },
    logOut: function () {
      localStorage.clear();
      this.verifyAuth();
    },

    getUserData: async function () {
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        return;
      }
      await this.verifyToken(); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();

      axios
        .get(`https://caja-menor-bk.herokuapp.com/user/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.is_admin = response.data.is_admin;
          localStorage.setItem("isAdmin", response.data.is_admin);
          localStorage.setItem("name", response.data.name);
          this.name = response.data.name;
        })
        .catch((error) => {});
    },

    verifyToken: function () {
      return axios
        .post(
          "https://caja-menor-bk.herokuapp.com/refresh",
          { refresh: localStorage.getItem("token_refresh") },
          { headers: {} }
        )
        .then((result) => {
          localStorage.setItem("token_access", result.data.access);
        })
        .catch(() => {
          this.$emit("logOut");
        });
    },
  },
  created: function () {
    // funciones que se ejecutan cada vez que se ejecuta el componente
    this.verifyAuth();
  },
};
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-weight: 300;
}
body {
  font-family: "Source Sans Pro", sans-serif;
  background-color: #262626;
  color: white;
  font-weight: 300;
  margin: 0 0 0 0;
}
body ::-webkit-input-placeholder {
  /* WebKit browsers */
  font-family: "Source Sans Pro", sans-serif;
  color: white;
  font-weight: 300;
}
body :-moz-placeholder {
  /* Mozilla Firefox 4 to 18 */
  font-family: "Source Sans Pro", sans-serif;
  color: white;
  opacity: 1;
  font-weight: 300;
}
body ::-moz-placeholder {
  /* Mozilla Firefox 19+ */
  font-family: "Source Sans Pro", sans-serif;
  color: white;
  opacity: 1;
  font-weight: 300;
}
body :-ms-input-placeholder {
  /* Internet Explorer 10+ */
  font-family: "Source Sans Pro", sans-serif;
  color: white;
  font-weight: 300;
}
#header {
  margin: 0%;
  padding: 0;
  width: 100%;
  height: 10vh;
  min-height: 50px;
  color: #030f1b;
  justify-content: center;
  align-items: center;
  align-items: center;
  position: inherit !important;
  background-color: rgba(0, 0, 0, 0.226);
  z-index: 2;
}
.header nav {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
}
.header nav button {
  color: #e5e7e9;
  background: #262626;
  border-radius: 5px;
  padding: 10px 20px;
  margin: 0 10px;
  cursor: pointer;
  font-weight: 600;
  border: none;
}
.header nav button:hover {
  color: #283747;
  background: #e5e7e9;
}

.app {
  height: 100vh;
}

.main-component {
  margin: 0%;
  background: #262626;
  height: 100vh;
}
.footer {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 10vh;
  min-height: 100px;
  background-color: #262626;
  color: #e5e7e9;
}
.footer h2 {
  width: 100%;
  height: 100%;

  display: flex;
  justify-content: center;
  align-items: center;
}

@media (max-width: 768px) {
  .header nav {
    width: 100%;
  }
  .header nav button {
    margin: 0 5px !important;
    padding: 5px 6px 5px 6px !important;
    font-size: 14px;
  }
}

/* loader in center of screen */

.lds-spinner {
  position: fixed;
  left: 50%;
  top: 50%;
  margin-left: -32px;
  margin-top: -32px;
  width: 64px;
  height: 64px;
  z-index: 100;
}

.lds-spinner div {
  transform-origin: 40px 40px;
  animation: lds-spinner 1.2s linear infinite;
}
.lds-spinner div:after {
  content: " ";
  display: block;
  position: absolute;
  top: 3px;
  left: 37px;
  width: 6px;
  height: 18px;
  border-radius: 20%;
  /* background: #000023e3; */
  background: #007bbd;
}
.lds-spinner div:nth-child(1) {
  transform: rotate(0deg);
  animation-delay: -1.1s;
}
.lds-spinner div:nth-child(2) {
  transform: rotate(30deg);
  animation-delay: -1s;
}
.lds-spinner div:nth-child(3) {
  transform: rotate(60deg);
  animation-delay: -0.9s;
}
.lds-spinner div:nth-child(4) {
  transform: rotate(90deg);
  animation-delay: -0.8s;
}
.lds-spinner div:nth-child(5) {
  transform: rotate(120deg);
  animation-delay: -0.7s;
}
.lds-spinner div:nth-child(6) {
  transform: rotate(150deg);
  animation-delay: -0.6s;
}
.lds-spinner div:nth-child(7) {
  transform: rotate(180deg);
  animation-delay: -0.5s;
}
.lds-spinner div:nth-child(8) {
  transform: rotate(210deg);
  animation-delay: -0.4s;
}
.lds-spinner div:nth-child(9) {
  transform: rotate(240deg);
  animation-delay: -0.3s;
}
.lds-spinner div:nth-child(10) {
  transform: rotate(270deg);
  animation-delay: -0.2s;
}
.lds-spinner div:nth-child(11) {
  transform: rotate(300deg);
  animation-delay: -0.1s;
}
.lds-spinner div:nth-child(12) {
  transform: rotate(330deg);
  animation-delay: 0s;
}
@keyframes lds-spinner {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

/* end loader */

/* class input if intem exist */
.itemExist {
  border: 1.5px solid red !important;
}

/* class input if item is Empty */
.inputEmpty {
  border: 1.5px solid red !important;
}

.atras_container {
  padding: 10px;
  text-align: center;
}

.atras_container a {
  color: #ffffff;
  text-decoration: none;
}

@import "./assets/css/common/reqStatus.css";
</style>