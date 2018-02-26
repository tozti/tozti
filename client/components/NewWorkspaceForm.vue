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
        <b-field label-for="handle" 
                 label="Identifiant"
                 :type="typing || !handle ? '' : !availableHandle ? 'is-danger': 'is-success'">
          <b-input v-model="handle" required :loading="checkingHandle">
          </b-input>
        </b-field>
      </section>
      <footer class="modal-card-foot">
        <input
          class="button is-primary"
          type="submit"
          :disabled="checkingHandle || typing || attempting || !handleStatus || !handle"
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
        attempting: false,
        checkingHandle: false,
        availableHandle: false,
        typing: false,
        workspace: {
          name: '',
        },
        handle: '',
      }
    },

    computed: {
      handleStatus() {
        return !this.checkingHandle && this.availableHandle
      }
    },

    mounted() {
      this.$refs.name.focus()
    },

    watch: {
      handle: (function() {
        let timestamp, timeout
        let delay = 400

        function later() {
          let last = Date.now() - timestamp

          if (last < delay && last >= 0) {
            window.clearTimeout(timeout)
            timeout = window.setTimeout(later.bind(this), delay - last)
          }
          else {
            timeout = null
            this.typing = false
            if (this.handle)
              this.checkHandle()
          }
        }

        return function() {
          this.typing = true
          timestamp = Date.now()
          timeout = window.setTimeout(later.bind(this), delay)
        }
      })()
    },

    methods: {
      checkHandle() {
        this.checkingHandle = true
        tozti.api.checkHandle(this.handle)
          .then(() => { this.availableHandle = true })
          .catch(() => { this.availableHandle = false })
          .finally(() => { this.checkingHandle = false })
      },

      attemptNewWorkspace() {
      }
    }
  }
</script>
