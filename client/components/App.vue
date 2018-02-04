<template>
  <div>
    <header class="main-header">
      <section class="branding">
        <a href="#"><img src="~assets/img/logo.svg" alt="tozti"></a>
      </section>

      <section class="search">
        <label for="search-field">
          <i class="nc-icon nc-zoom-2"></i>
        </label>
        <input type="text" id="search-field" placeholder="Ne pas utiliser.">
      </section>

      <section class="user">
        <a href="#" class="notifications">
          <i class="nc-icon nc-bell-53"></i>
        </a>

        <a href="#" class="logged">
          <div class="avatar">
          </div>
          Romain
          <i class="material-icons">arrow_drop_down</i>
        </a>
      </section>
    </header>

    <navigation></navigation>

    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
  import NotificationCenter from './NotificationCenter.vue'
  import Navigation from './Navigation.vue'

  export default {
    components: {
      NotificationCenter,
      Navigation,
    }
  }
</script>
