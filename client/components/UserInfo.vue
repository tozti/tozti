<template>
  <div href="#" class="logged">
    {{ me.attributes.name }} 
    <b-icon icon="chevron-down" size="is-small"></b-icon>
    <a v-on:click="logout"><b-icon icon="power"></b-icon></a>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        me: tozti.me
      }
    },
    methods: {
      logout() {
        document.cookie = 'auth-token=;expires=Thu, 01 Jan 1970 00:00:01 GMT;'
        tozti.me = null
        this.$toast.open({
          duration: 5000,
          message: 'Vous avez été déconnecté·e',
          type: 'is-success',
          position: 'is-top'
        })
        this.$router.push('/login')
      }
    }
  }
</script>
