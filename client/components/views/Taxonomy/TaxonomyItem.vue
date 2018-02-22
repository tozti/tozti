<template>
  <div class="taxonomy-item">
    <div class="taxonomy-item-media">
      <slot name="media">
        <b-icon pack="mdi" :icon="icon"></b-icon>
      </slot>
    </div>
    <div v-if="resource" class="taxonomy-item-info">
      <p class="title">{{ title ? title : id }}</p>
      <p class="subtitle">{{ resource.meta['last-modified'] }}</span></p>
    </div>
    <div v-else class="taxonomy-item-info">
      <p class="title"><span class="placeholder"></span></p>
      <p class="subtitle"><span class="placeholder"></span></p>
    </div>
    <div class="taxonomy-item-actions">
      <b-icon pack="mdi" icon="dots-horizontal"></b-icon>
    </div>
  </div>
</template>

<script>
  import { resourceMixin } from '../../../mixins.js'

  export default {
    mixins: [ resourceMixin ],

    data() {
      return {
        icon: 'help-circle'
      }
    }
  }
</script>
