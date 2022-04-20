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
    <form
      v-on:submit.prevent="processCreateReporte"
      class="create-report__form"
    >
      <div class="create-report__item">
        <span class="create-report__text">Tipo&nbsp;</span>

        <i class="fa fa-caret-down" aria-hidden="true"></i>
        <select
          class="create-report__select"
          id="select_tipo_servicio"
          v-model="report.tipoServicio"
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
          type="text"
          v-model="report.detalle"
          name="detalle"
          id="detalle"
          placeholder="Detalle"
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
          placeholder="Valor"
          required
        />
      </div>
      <!-- CARGA DE IMAGEN -->
      <div class="create-report__item">
        <div class="button-wrapper">
          <span class="label_upload">
            <strong>Evidencia</strong>
          </span>
          <input
            type="file"
            @change="updatePhoto"
            id="upload"
            name="upload"
            class="upload-box"
            required
            placeholder="Upload File"
          />
          <div class="preview-box" v-if="report.evidence">
            <p>Imagen cargada</p>
            <img
              :src="previewImage"
              alt="preview"
              class="preview-image"
              v-if="report.evidence"
              width="100"
              height="100"
            />
          </div>
        </div>
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
import swal from "sweetalert";
export default {
  name: "CreateReport",
  data: function () {
    return {
      is_admin: false,
      name: localStorage.getItem("name") || "none",
      report: {
        tipoServicio: "",
        caja_menor: "1",
        nombre_usuario: localStorage.getItem("name") || "none",
        detalle: "",
        valor: "",
        evidence: "",
      },
      tipoServicios: [],
      userId: "",
      cajaMenor: {},
      startLoader: false,
      previewImage: "",
    };
  },

  methods: {
    verifyAuth: function () {
      this.is_auth = localStorage.getItem("isAuth") || false;
      if (this.is_auth == false) {
        this.$router.push("logIn");
      }
    },

    processCreateReporte: async function () {
      console.log(this.report);
      this.startLoader = true;
      this.upperCase();
      if (
        localStorage.getItem("token_access") === null ||
        localStorage.getItem("token_refresh") === null
      ) {
        this.$emit("logOut");
        return;
      }
      await this.verifyToken(); // esto se utiliza para esperar a que la sección de comprobación y actualización delaccess token terminen, y que solo cuando hayan terminado

      let token = localStorage.getItem("token_access");
      let userId = jwt_decode(token).user_id.toString();
      axios
        .post(
          `https://caja-menor-bk.herokuapp.com/reporte/${userId}`,
          this.report,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          swal("Reporte enviado correctamente", "", "success");
          this.getCajaMenorByUser();
          this.startLoader = false;
        })
        .catch((error) => {
          console.log(error);
          if (error.response.status == "401") {
            this.error_message = "Error en el envío del reporte";
            this.error_createequipo = true;
          } else if (error.response.status == "400") {
            this.error_message = "Error en el envío del reporte";
            this.error_createequipo = true;
          } else if (error.response.status == "500") {
            this.error_message = "Error en el servidor";
            this.error_createequipo = true;
          } else {
            this.error_message = "Error en el servidor";
            this.error_createequipo = true;
          }
          this.startLoader = false;
        });
    },

    updatePhoto(e) {
      let file = e.target.files[0];
      let reader = new FileReader();
      reader.onloadend = (file) => {
        this.report.evidence = reader.result;
      };
      reader.readAsDataURL(file);

      this.previewImage = URL.createObjectURL(e.target.files[0]);
    },

    upperCase: function () {
      this.report.detalle = this.report.detalle.toUpperCase();
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

    getCajaMenorByUser: async function () {
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
        .get(
          `https://caja-menor-bk.herokuapp.com/cajaMenor/${userId}/list/byUser`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          this.cajaMenor = response.data[0];
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
    this.verifyAuth();
    this.is_admin = JSON.parse(localStorage.getItem("isAdmin")) || false;
    this.getTipoServicios();
    this.getCajaMenorByUser();
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

.button-wrapper {
  position: relative;
  width: 80%;
  height: 40px;
  text-align: center;
  margin: 15% auto;
  cursor: pointer;
  display: flex;
}

.button-wrapper span.label_upload {
  position: relative;
  z-index: 0;
  display: inline-block;
  width: 100%;
  background: #00bfff;
  cursor: pointer;
  color: #fff;
  padding: 10px 0;
  text-transform: uppercase;
  font-size: 12px;
}

#upload {
  display: inline-block;
  position: absolute;
  z-index: 1;
  width: 100%;
  height: 50px;
  top: 0;
  left: 0;
  opacity: 0;
  cursor: pointer;
}

.upload-box {
  cursor: pointer;
  width: 150px;
}

.preview-box {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.2rem;
  font-size: 0.7rem;
}

.preview-box p {
  margin-bottom: 0;
}

.preview-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
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
}

.create-report__item {
  width: 423px;
  padding: 5px;
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
  color: gray;
}

.submit-container {
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