<template>
  <div class="container columns is-mobile">
    <div class="column is-half is-offset-one-quarter">
      <form class="box" v-on:submit.prevent="attemptLogin">
        <b-field label="Nom d'utilisateur :">
          <b-input v-model="login"></b-input>
        </b-field>

        <b-field label="Mot de passe :">
          <b-input v-model="password" type="password"></b-input>
        </b-field>

        <div class="field is-grouped is-grouped-left">
          <p class="control">
            <button type="submit" class="button">
              Se connecter
            </button>
          </p>
          <p class="control">
            <router-link class="button is-text" to="/signin">S'enregistrer</router-link>
          </p>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        login: '',
        password: ''
      }
    },

    methods: {
      attemptLogin() {
        console.log(this.login, this.password)
      },
    },
  }
</script>
