<template>
  <div>
    <header class="main-header">
      <section class="branding">
        <a href="#"><img :src="tozti_logo" alt="tozti"></a>
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
  import tozti_logo from "../assets/img/logo.svg"
  import NotificationCenter from './NotificationCenter.vue'
  import Navigation from './Navigation.vue'

  export default {
    components: {
      NotificationCenter,
      Navigation,
    },
    data: function () {
        return {
            tozti_logo: tozti_logo
        }
    }
  }
</script>
