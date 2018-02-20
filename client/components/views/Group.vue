<template>
  <section v-if="resource" class="section content">
    <h1>{{ resource.attributes.name }}</h1>
    <p class="grouped">
      <button class="button" @click="deleteGroup" :disabled="deleting">
        Supprimer
      </button>
    </p>
    <div class="tabs">
      <ul>
        <li class="is-active"><a>Membres <span class="badge">{{ memberCount }}</span></a></li>
        <li><a>Paramètres</a></li>
      </ul>
    </div>
    <div class="group-list">
      <user-preview v-for="user in members" :key="user.id" :id="user.id"></user-preview>
    </div>
  </section>
</template>

<script>
  import { resourceMixin } from '../../mixins'
  import UserPreview from '../UserPreview.vue'

  export default {
    mixins: [ resourceMixin ],
    components: { UserPreview },

    data() {
      return {
        deleting: false,
      }
    },

    computed: {
      members() {
        return this.resource.relationships.members.data
      },

      memberCount() {
        return this.members.length
      }
    },

    methods: {
      deleteGroup() {
        this.$dialog.confirm({
          message: 'Voulez-vous supprimer définitivement ce groupe ?',
          confirmText: 'Oui',
          cancelText: 'Annuler',
          type: 'is-danger',
          onConfirm: () => {
            let target = window.location.origin + tozti.me.relationships.groups.self
            let target2 = tozti.api.resourceURL(this.id)
            this.deleting = true
            tozti
              .api.delete(target, { data: [ this.resource ]})
              .then(() => tozti.api.delete(target2))
              .then(() => {
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
