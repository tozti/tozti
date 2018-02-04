<template>
  <div>
    <h3>workspace {{ id }}</h3>
    <nav>
      <router-link
        v-for="{ name, route, props } in workspaceItems"
        :to="{ name: route, params: { id } }"
        :key="name">
        <i v-if="props.icon" :class="'nc-icon ' + props.icon"></i>
        {{ name }}
      </router-link>
    </nav>
  </div>
</template>

<script>
  import { resourceMixin } from '../mixins'

  export default {
    mixins: [ resourceMixin ],
    data: _ => ({
      workspaceItems: tozti.workspaceMenuItems
    })
  }
</script>
