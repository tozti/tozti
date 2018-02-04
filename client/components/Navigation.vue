<template>
  <aside class="main-sidebar">

    <!-- global menu items -->
    <nav>
      <router-link v-for="{ name, route, props } in globalMenuItems" :to="route" :key="name">
        <i v-if="props.icon" :class="'nc-icon ' + props.icon"></i>{{ name }}
      </router-link>
    </nav>

    <!-- workspace items -->
    <workspace-menu v-for="id in workspaces" :key="id" :id="id"></workspace-menu>
  </aside>
</template>

<script>
  import WorkspaceMenu from './WorkspaceMenu.vue'

  export default {
    components: { WorkspaceMenu },
    data: _ => ({
      globalMenuItems: tozti.globalMenuItems,
      workspaces: [0, 1, 2]
    })
  }
</script>
