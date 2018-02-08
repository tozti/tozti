<template>
  <div>
    <b-collapse :open="true" animation="fadeInDown">
      <h3 slot="trigger">workspace {{ attributes.name }}</h3>
      <nav v-if="resource.loaded">
        <router-link
          v-for="{ name, route, props } in workspaceItems"
          :to="{ name: route, params: { id } }"
          :key="name"
          active-class="active">
          <i v-if="props.icon" :class="'nc-icon ' + props.icon"></i>
          {{ name }}
        </router-link>
      </nav>
    </b-collapse>
  </div>
</template>

<script>
  import { resourceMixin } from '../mixins'

  export default {
    mixins: [ resourceMixin('core/workspace') ],

    data: _ => ({
      workspaceItems: tozti.workspaceMenuItems
    })
  }
</script>
