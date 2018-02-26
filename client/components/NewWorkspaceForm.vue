<template>
  <form v-on:submit.prevent="attemptNewWorkspace">
    <div class="modal-card" style="width: auto">
      <header>
        <p class="modal-card-head">Nouvel espace de travail</p>
      </header>
      <section class="modal-card-body">
        <b-field label-for="name" label="Nom">
          <b-input
            v-model="workspace.name"
            ref="name"
            required>
          </b-input>
        </b-field>
        <t-handle-form v-model="handle"
                       :available.sync="available">
        </t-handle-form>
      </section>
      <footer class="modal-card-foot">
        <input
          class="button is-primary"
          type="submit"
          :disabled="!available"
          value="Créer">
        <button class="button" type="button" @click="$parent.close()">Annuler</button>
        <i v-if="attempting" class="loading-spinner"></i>
      </footer>
    </div>
  </form>
</template>

<script>
  export default {
    data() {
      return {
        workspace: {
          name: '',
        },
        handle: '',
        available: false,
        attempting: false,
      }
    },

    mounted() {
      this.$refs.name.focus()
    },

    methods: {
      attemptNewWorkspace() {
      }
    }
  }
</script>
