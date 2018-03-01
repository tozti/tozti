<template>
  <div class="taxonomy-item">
    <div class="taxonomy-item-media">
      <slot name="media">
        <b-icon pack="mdi" :icon="icon"></b-icon>
      </slot>
    </div>
    <div v-if="loading" class="taxonomy-item-info">
      <p class="title"><span class="placeholder"></span></p>
      <p class="subtitle"><span class="placeholder"></span></p>
    </div>
    <div v-else class="taxonomy-item-info">
      <router-link :to="to" append>
        <p class="title">{{ title }}</p>
        <p class="subtitle">{{ subtitle }}</span></p>
      </router-link>
    </div>
    <div class="taxonomy-item-actions">
      <b-icon pack="mdi" icon="dots-horizontal"></b-icon>
    </div>
  </div>
</template>

<script>

  export default {
    props: {
      icon: {
        type: String,
        default: 'help-circle',
      },

      title: {
        type: String,
        default: '',
      },

      subtitle: {
        type: String,
        default: '',
      },

      to: {
        type: String,
        default: '',
      },

      loading: {
        type: Boolean,
        default: false,
      }
    }
  }
</script>
