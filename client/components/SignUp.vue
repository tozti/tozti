<template>
  <section class="hero is-warning is-fullheight is-bold">
    <div class="hero-body">
      <div class="column is-half is-offset-one-quarter">
        <form class="box is-shadowless" v-on:submit.prevent="signin">
          <b-field label="Identifiant :">
            <b-input v-model="user.login"></b-input>
          </b-field>

          <b-field label="Adresse mail :">
            <b-input type="mail" v-model="user.email"></b-input>
          </b-field>

          <b-field label="Nom d'utilisateur·ice :">
            <b-input v-model="user.name"></b-input>
          </b-field>

          <b-field label="Mot de passe :">
            <b-input v-model="user.passwd" type="password" password-reveal></b-input>
          </b-field>

          <div class="field is-grouped is-grouped-left">
            <p class="control">
              <button type="submit" class="button">
                S'enregistrer
              </button>
            </p>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
  export default {
    data() {
      return {
        user: {
          login: '',
          name: '',
          passwd: '',
          email: '',
        }
      }
    },

    methods: {
      signin() {
        tozti.api
          .post(tozti.api.endpoints.signup, this.user)
          .then(res => {
            this.$snackbar.open({
              message: 'Votre inscription a réussi !',
              type: 'is-success',
              position: 'is-top'
            })
          })
          .catch(err => {
            this.$snackbar.open({
              message: 'Une erreur est survenue lors de l\'inscription',
              type: 'is-danger',
              position: 'is-top'
            })
          })
      },
    },
  }
</script>
