// TODO(flupe): fill in the computed attributes & relationships
//              ideally set up an alternative to VueX
export let resourceMixin = {
  props: { id: Number },
  computed: {
    resource: function() {
      return { id: this.id }
    },
  }
}
