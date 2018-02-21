<template>
  <div>
    <tozti-header></tozti-header>
    <tozti-sidebar></tozti-sidebar>
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
  import ToztiHeader from './header'
  import ToztiSidebar from './sidebar'

  export default {
    components: { ToztiHeader, ToztiSidebar }
  }
</script>
