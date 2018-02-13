<template>
  <a href="" class="uk-icon-link" uk-icon="icon: bell">
    <span class="uk-badge" v-if="count > 0">{{ count }}</span>
  </a>
</template>

<script>
  export default {
    data() {
      return { count: 0 }
    }
  }
</script>
