<template>
  <section v-if="resource" class="section content">
    <h1>{{ resource.body.name }}</h1>
    <p class="grouped">
      <button class="button" @click="deleteGroup" :disabled="deleting">
        Supprimer
      </button>
    </p>
    <div class="tabs">
      <ul>
        <li class="is-active"><a>Espaces</a></li>
        <li><a>Membres <span class="badge">{{ memberCount }}</span></a></li>
        <li><a>Paramètres</a></li>
      </ul>
    </div>

    <div class="content has-text-grey has-text-centered has-vertical-space">
      <p>
      <i class="nc-icon nc-grid-45 x3"></i>
      </p>
      <p>Ce groupe ne possède pas d'espace de travail.</p>
      <p>
        <a class="button" @click="createWorkspace">Créer un espace de travail</a>
      </p>
    </div>

  </section>
</template>

<script>
  import UserPreview from '../UserPreview.vue'

  export default {
    props: [ 'handle' ],

    components: { UserPreview },

    data() {
      return {
        deleting: false,
        resource: null,
      }
    },

    computed: {
      members() {
        return this.resource.body.members.data
      },

      memberCount() {
        return this.members.length
      }
    },

    beforeMount() {
      tozti.store
        .handle.get(this.handle)
        .then(resource => {
          this.resource = resource
        })
    },

    methods: {
      createWorkspace() {

      },

      deleteGroup() {
        this.$dialog.confirm({
          message: 'Voulez-vous supprimer définitivement ce groupe ?',
          confirmText: 'Oui',
          cancelText: 'Annuler',
          type: 'is-danger',
          onConfirm: () => {
            this.deleting = true

            tozti.store
              .rels.delete(tozti.me.body.groups, { id: this.id })
              .then(() => tozti.store.rels.delete(tozti.me.body.pinned, { id: this.id }))
              .then(() => tozti.store.delete(this.id))
              .then(() => {
                this.$router.push('/g/')
                this.$toast.open({
                  message: 'Le groupe a été supprimé.',
                  type: 'is-success'
                })
              })
          }
        })
      }
    }
  }
</script>
