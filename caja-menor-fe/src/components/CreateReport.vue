<template>
  <main class="create-report">
    <!-- SECTION LOGIN HEADER -->
    <section class="create-report__header">
      <h1 class="create-report__title">Nuevo Reporte</h1>
      <div class="data-item">
        <h2>Usuario</h2>
        <p class="create-report__title">{{ cajaMenor.user }}</p>
      </div>
      <div class="data-item">
        <h2>Saldo actual</h2>
        <p class="create-report__title">$ {{ cajaMenor.saldo }}</p>
      </div>
      <div class="data-item">
        <h2>Gastos a la fecha</h2>
        <p class="create-report__title">$ {{ cajaMenor.gastos }}</p>
      </div>
    </section>

    <!-- SECTION REGISTER FORM -->
    <form v-on:submit.prevent="processCreateReport" class="create-report__form">
      <div class="create-report__item">
        <span class="create-report__text">Tipo&nbsp;</span>

        <i class="fa fa-caret-down" aria-hidden="true"></i>
        <select
          class="create-report__select"
          id="select_tipo_servicio"
          v-model="report.tipo_servicio"
          required
        >
          <option value="" disabled>Tipo de Servicio</option>
          <option v-for="tipoServicio in tipoServicios" :key="tipoServicio">
            {{ tipoServicio.nombre }}
          </option>
        </select>
      </div>
      <div class="create-report__item">
        <span class="create-report__text">Detalle&nbsp;</span>
        <i class="fas fa-info-circle"></i>
        <input
          class="create-report__input"
          type="password"
          v-model="report.detalle"
          name="password"
          id="password"
          placeholder="contraseña"
          required
        />
      </div>
      <div class="create-report__errors">
        <i
          class="fa fa-exclamation-circle"
          id="error-icon"
          v-if="error_message"
        ></i>
        <span v-if="error_message" class="create-report__text text_fail">{{
          " " + error_message
        }}</span>
      </div>
      <div class="create-report__item">
        <span class="create-report__text">Valor&nbsp;</span>
        <i class="fas fa-dollar-sign"></i>
        <input
          class="create-report__input"
          type="text"
          v-model="report.valor"
          id="name"
          name="name"
          placeholder="nombre"
          required
        />
      </div>
      <div class="create-report__item submit-container">
        <button type="submit" class="create-report__submit">Enviar</button>
      </div>
      <br />
      <br />
    </form>
  </main>

  <!-- LOADER -->
  <div class="lds-spinner" v-if="startLoader">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
</template>
<script>
import axios from "axios";
import jwt_decode from "jwt-decode";
export default {
  name: "CreateReport",
  data: function () {
    return {
      is_admin: false,
      name: localStorage.getItem("name") || "none",
      report: {
        tipo_servicio: "",
        caja_menor: "1",
        nombre_usuario: "Michael Hernández",
        detalle: "pasaje",
        valor: "10000",
        evidence: "",
      },
      tipoServicios: [],
      userId: "",
      cajaMenor: {},
    };
  },

  methods: {
    verifyAuth: function () {
      this.is_auth = localStorage.getItem("isAuth") || false;
      if (this.is_auth == false) {
        this.$router.push("logIn");
      }
    },
    getTipoServicios: async function () {
      this.startLoader = true;
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        return;
      }
      await this.$emit("verifyToken"); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();

      axios
        .get(
          `https://caja-menor-bk.herokuapp.com/tipoServicio/${userId}/list`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          this.tipoServicios = response.data;
          this.startLoader = false;
        })

        .catch((error) => {
          console.log(error);
          this.startLoader = false;
        });
    },

    getCajaMenorDataByUserId: function () {
      let cajasMenores = JSON.parse(localStorage.getItem("cajasMenores"));
      this.userId = jwt_decode(localStorage.getItem("token_access")).user_id;
      console.log(cajasMenores);
      this.cajaMenor = cajasMenores.find(
        (cajaMenor) => cajaMenor.userId == this.userId
      );
    },
  },
  created: function () {
    this.verifyAuth();
    this.is_admin = JSON.parse(localStorage.getItem("isAdmin")) || false;
    this.getTipoServicios();
    this.getCajaMenorDataByUserId();
  },
};
</script>
<style>
.create-report {
  margin-top: 1rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  position: relative;
}

.create-report__header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.create-report__title {
  font-size: 2.5rem;
  color: #2a7ae4;
  text-align: center;
}

.data-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.data-item h2 {
  font-size: 1.5rem;
  color: #2a7ae4;
  margin-bottom: 0;
}

.data-item p {
  font-size: 1.2rem;
  color: #ffffff;
  margin-bottom: 0.1rem;
}

.create-report__form form {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  row-gap: 24px;
}

.create-report__item {
  width: 423px;
}

.create-report__item label {
  display: block;
  text-align: left;
  font-size: 14px;
  font-weight: 500;
  line-height: 16.44px;
  color: var(--page-logIn-titleColor);
}

.create-report__item input,
select {
  width: 100%;
  height: 48px;
  border: none;
  border-radius: 4px;
  padding: 16px 12px;
  font-size: 16px;
  font-weight: 400;
  line-height: 20px;
}

.create-report__item input::placeholder {
  color: var(--page-logIn-placeholderColor);
}

.submit-container {
  margin-top: 24px;
  width: 100%;
  height: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.create-report__submit {
  width: 80%;
  height: 62px;
  border: none;
  font-size: 18px;
  font-weight: 600;
  line-height: 21px;
  background-color: #2a7ae4;
  color: #ffffff;
}

/* mobile */
@media (max-width: 768px) {
  .create-report__item {
    width: 275px;
  }
  .create-report__item input {
    height: 41px;
  }

  .create-report__submit {
    height: 40px;
    font-size: 14px;
  }
}

/* tablet */
@media (min-width: 768px) and (max-width: 1024px) {
  .create-report__item {
    width: 275px;
  }
  .create-report__item input {
    height: 41px;
  }
  .create-report__submit {
    height: 40px;
    font-size: 18px;
  }
}
</style>