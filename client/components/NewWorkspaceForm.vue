<template>
  <form v-on:submit.prevent="attemptNewWorkspace">
    <div class="modal-card" style="width: auto">
      <header>
        <p class="modal-card-head">Nouveau dossier</p>
      </header>
      <section class="modal-card-body">
        <b-field label-for="name" label="Nom">
          <b-input
            v-model="workspace.name"
            ref="name"
            required>
          </b-input>
        </b-field>

        <t-handle-field v-model="workspace.handle"
                        :root="root"
                        :available.sync="available">
        </t-handle-field>

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
    props: {
      root: {
        type: Object,
        default: null,
        validate(root) {
          return root && [
            'core/group',
            'core/folder',
          ].indexOf(root.type) > -1
        }
      }
    },

    data() {
      console.log(this.root)
      return {
        workspace: {
          name: '',
          handle: '',
          children: { data: {} }
        },
        available: false,
        attempting: false,
      }
    },

    mounted() {
      this.$refs.name.focus()
    },

    methods: {
      attemptNewWorkspace() {
        this.attempting = true

        tozti
          // create the workspace
          .store.create({
            type: 'core/folder',
            body: this.workspace
          }, false)

          // pin the workspace to the root
          .then(({ id, type }) => {
            let linkage = { id, type }
            if (this.root)
              return tozti.store
                .rels.add(this.root.body.children, {
                  [this.workspace.handle]: linkage
                })

            else {
              return tozti.api
                .post(tozti.api.handleURL(this.workspace.handle), {
                  data: linkage
                })
            }
          })

          .then(() => {
            this.attempting = false

            this.$parent.close()
            this.$toast.open({
              message: `L'espace ${this.workspace.name} vient d'être créé.`,
              type: 'is-success',
              position: 'is-top'
            })
          })

          .catch(res => {
            this.$toast.open({
              message: 'Une erreur est survenue lors de la création de l\'espace',
              type: 'is-danger',
              position: 'is-top'
            })

            this.attempting = false
          })
      }
    }
  }
</script>
