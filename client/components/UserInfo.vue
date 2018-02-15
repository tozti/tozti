<template>
  <a href="#" class="logged">
    {{ me.attributes.name }} 
    <b-icon icon="chevron-down" size="is-small"></b-icon>
  </a>
</template>

<script>
  export default {
    data() {
      return {
        me: tozti.me
      }
    }
  }
</script>
