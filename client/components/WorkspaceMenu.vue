<template>
  <div>
    <b-collapse :open="true" animation="fadeInDown">
      <h3 slot="trigger">workspace {{ id }}</h3>
      <nav v-if="resource">
        <router-link
          v-for="{ name, route, props } in workspaceItems"
          :to="{ name: route, params: { id } }"
          :key="name"
          active-class="active">
          <i v-if="props.icon" :class="'nc-icon ' + props.icon"></i>
          {{ name }}
          {{ resource.attributes.name }}
        </router-link>
      </nav>
    </b-collapse>
  </div>
</template>

<script>
  export default {
    props: {
      id: String,
    },

    data: _ => ({
      workspaceItems: tozti.workspaceMenuItems,
      resource: null
    })
  }
</script>
