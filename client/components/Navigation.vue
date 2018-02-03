<template>
  <aside class="main-sidebar">

    <nav>
      <li v-for="{ name, route, props } in globalMenuItems">
        <router-link :to="route"><span v-if="props.icon" :uk-icon="props.icon"></span>{{ name }}</router-link>
      </li>
    </nav>
  </aside>
</template>

<script>
  export default {
    data: _ => ({
      globalMenuItems: tozti.globalMenuItems
    })
  }
</script>
