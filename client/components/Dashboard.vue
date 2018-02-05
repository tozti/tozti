<template>
  <div class="uk-container uk-padding">
    <h1 class="uk-heading-primary">Dashboard</h1>
    <h3>No widget available just yet :(</h3>

    <user-editor :id="0"></user-editor>
    <user-editor :id="0"></user-editor>
  </div>
</template>

<script>
  let UserEditor = {
    template: `
      <form>
        <input v-model="attributes.name">
        <span>{{ attributes.name }}</span>
      </form>
    `,
    props: {
      id: Number
    },
    data() {
      return tozti.store.get('core/user', this.id)
    }
  }

  export default {
    components: { UserEditor }
  }
</script>
