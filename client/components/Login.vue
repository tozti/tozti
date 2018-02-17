<template>
  <div class="login">
    <section class="content">
      <p class="content-header">
        <img src="~assets/img/logo.svg" width="50">
      </p>
      <div class="box">
        <form v-on:submit.prevent="attemptLogin">
          <b-field label="Identifiant :">
            <b-input v-model="user.login"></b-input>
          </b-field>

          <b-field label="Mot de passe :">
            <b-input v-model="user.passwd" type="password"></b-input>
          </b-field>

          <div class="field is-grouped is-grouped-left">
            <p class="control">
              <button type="submit" class="button">
                Se connecter
              </button>
            </p>
            <p class="control">
              <router-link class="button is-text" to="/signup">S'enregistrer</router-link>
            </p>
          </div>

        </form>
      </div>
    </section>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        user: {
          login: '',
          passwd: ''
        }
      }
    },

    methods: {
      attemptLogin() {
        tozti.api
          .post(tozti.api.endpoints.login, this.user)
          .then(({ uid }) => tozti.store.get(uid))
          .then(user => {
            tozti.me = user
            this.$router.push('/')
            this.$toast.open({
              message: `Bienvenue, ${user.attributes.name} !`,
              type: 'is-success',
              position: 'is-top'
            })
          })
          .catch(err => {
            this.$snackbar.open({
              message: 'Une erreur est survenue lors de la connexion',
              type: 'is-danger',
              position: 'is-top'
            })
          })
      }
    },
  }
</script>
