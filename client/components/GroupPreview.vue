<template>
  <router-link :to="{ name: 'group', params: { handle: id } }">
    <div v-if="resource" class="group-item">
      <div class="group-media"></div>
      <div class="group-content">
        <p class="title is-5">{{resource.attributes.name}}</p>
        <p class="subtitle is-6">@{{resource.attributes.handle}}</p>
      </div>
    </div>
  </router-link>
</template>

<script>
  import { resourceMixin } from '../mixins'

  export default {
    mixins: [ resourceMixin ]
  }
</script>
