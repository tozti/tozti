<template>
  <div class="uk-container uk-padding">
    <h1 class="uk-heading-primary">Dashboard</h1>
    <h3>No widget available just yet :(</h3>

    <user-editor></user-editor>
  </div>
</template>

<script>

  let UserEditor = {

    mounted() {
      tozti
        .store.get(tozti.uid)
        .then(user => {
          console.log(user)
          this.user = user
        })
    },

    template: `
      <div v-if="user">
        <h3>user settings</h3>
        <p>
          <label for="name">name: </label><br>
          <input id="name" v-model="user.attributes.name">
        </p>
      </div>
    `,

    data: _ => ({
      user: null
    })

  }

  export default {
    components: { UserEditor }
  }
</script>
