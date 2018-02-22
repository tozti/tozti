export let resourceMixin = {
  props: { id: String },

  watch: {
    id() {
      tozti.store.get(this.id)
        .then(resource => {
          this.resource = resource
          this.loading = false
        })
    }
  },

  mounted() {
    tozti.store.get(this.id)
      .then(resource => {
        this.resource = resource
        this.loading = false
      })
  },

  data() {
    return {
      loading: true,
      resource: null,
    }
  }
}
