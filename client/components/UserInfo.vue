<template>
  <a v-if="user" href="#" class="logged">
    <div class="avatar">
    </div>
    {{ user.attributes.name }}
    <i class="material-icons">arrow_drop_down</i>
  </a>
</template>

<script>
  export default {
    mounted() {
      tozti
        .store.get(tozti.uid)
        .then(user => {
          console.log('ok')
          this.user = user
        })
    },

    data: _ => ({
      user: null
    })
  }
</script>
