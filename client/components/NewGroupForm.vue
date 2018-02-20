<template>
  <form action="">
    <div class="modal-card" style="width: auto">
      <header>
        <p class="modal-card-head">Nouveau groupe</p>
      </header>
      <section class="modal-card-body">
        <b-field label-for="name" label="Nom">
          <b-input
            v-model="group.name"
            required>
          </b-input>
        </b-field>
        <b-field label-for="handle" label="Identifiant">
          <b-input
            v-model="group.handle"
            required>
          </b-input>
        </b-field>
      </section>
      <footer class="modal-card-foot">
        <button class="button" type="button" @click="$parent.close()">Annuler</button>
        <a class="button is-primary" :class="{ 'is-loading': attempting }" @click="attemptNewGroup">Créer</a>
      </footer>
    </div>
  </form>
</template>

<script>
  export default {
    data() {
      return {
        attempting: false,
        group: {
          name: '',
          handle: '',
        }
      }
    },

    methods: {
      attemptNewGroup() {
        this.attempting = true

        const data = {
          type: 'core/group',
          attributes: this.group,
        }

        let group = null

        tozti.api
          .post(tozti.api.endpoints.resources, { data })

          .then(({ data }) => {
            let url = window.location.origin + tozti.me.relationships.groups.self
            group = data
            return tozti.api.post(url, {
              data: [{ type: 'core/group', id: data.id }]
            })
          })

          .then(res => {
            this.attempting = false

            tozti.me.relationships.groups.data.push(group)

            this.$parent.close()
            this.$toast.open({
              message: `Le groupe ${this.group.name} vient d'être créé.`,
              type: 'is-success',
              position: 'is-top'
            })
          })

          .catch(res => {
            this.$toast.open({
              message: 'Une erreur est survenue lors de la création du groupe',
              type: 'is-danger',
              position: 'is-top'
            })

            this.attempting = false
          })
      }
    }
  }
</script>
