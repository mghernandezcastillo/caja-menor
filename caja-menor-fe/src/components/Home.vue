import axios from 'axios';
import jwt_decode from 'jwt-decode';
<template>
  <div class="home">
    <div class="home-data">
      <h1 class="login__subtitle">Caja Menor</h1>
      <h2 class="login__subtitle">{{ name }}</h2>
      <img src="../assets/img/home_img.png" alt="" />
      <div class="input-group-home">
        <button v-on:click="loadCreateReport()" class="btn-home-1">
          Nuevo reporte
        </button>
      </div>

      <div class="input-group-home">
        <p>o</p>
      </div>

      <div class="input-group-home">
        <button v-on:click="loadHistorial()" class="btn-home-2">
          Historial reportes
        </button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import jwt_decode from "jwt-decode";
export default {
  name: "Home",
  data: function () {
    return {
      email: localStorage.getItem("email") || "none",
      is_admin: false,
      name: "",
    };
  },

  methods: {
    verifyAuth: function () {
      this.is_auth = localStorage.getItem("isAuth") || false;
      if (this.is_auth == false) {
        this.$router.push("logIn");
      }
    },
    loadCreateReport: function () {
      this.$router.push("createReport");
    },
    loadHistorial: function () {
      this.$router.push("historialGeneral");
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
    this.verifyAuth();
    this.name = localStorage.getItem("name") || "";
    this.is_admin = JSON.parse(localStorage.getItem("isAdmin")) || false;
  },
};
</script>
<style>
.home-data {
  text-align: center;
  width: 60%;
  margin-bottom: 10%;
}
.home-data img {
  width: 150px;
  margin-bottom: 5%;
}

.crear_equipo_container {
  padding: 10px;
}

.crear_equipo_container a {
  color: #ffffff;
  text-decoration: none;
  cursor: pointer;
}

.home {
  height: 100%;
  width: 100%;
  background-color: #262626;
  display: flex;
  justify-content: center;
  align-items: center;
}
.home h1 {
  font-size: 50px;
  color: #2a7ae4;
}
.home h2 {
  font-size: 50px;
  color: #7e7e7e;
}
.home span {
  color: crimson;
  font-weight: bold;
}

.input-group-home {
  position: relative;
  width: 100%;
  margin: 0 auto;
  margin-bottom: 1.5rem;
}

.input-group-home button {
  border: 1px solid #7e7e7e;
  border-radius: 5px;
  padding: 0.7rem 0;
  width: 30%;
  line-height: 1.6rem;
  font-size: 1.3rem;
  transition: 0.3s ease-in-out all;
  font-weight: 500;
}

.btn-home-1 {
  background-color: #262626;
  color: #ffffff;
}

.btn-home-1:hover {
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.226);
}

.btn-home-2 {
  background-color: #262626;
  color: #ffffff;
}

.btn-home-2:hover {
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.226);
}

@media screen and (max-width: 768px) {
  .btn-home-2 {
    width: 100%;
  }
  .btn-home-1 {
    width: 100%;
  }
  .home-data h1 {
    font-size: 30px;
  }
  .home-data h2 {
    font-size: 25px;
    margin-bottom: 3rem;
  }
  .home-data img {
    width: 100px;
    margin-bottom: 10%;
  }

  .input-group-home button {
    width: 100%;
    padding: 0.5rem 0;
  }
}
</style>