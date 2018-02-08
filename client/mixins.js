const resourceMixins = {}

export function resourceMixin(type)  {
  if (Object.keys(resourceMixins).includes(type)) {
    return resourceMixins[type]
  }

  return resourceMixins[type] = {
    props: { id: Number },

    computed: {
      attributes() { return this.resource.attributes },
      relationships() { return this.resource.relationships },
    },

    data() {
      return {
        resource: tozti.store.get(type, this.id)
      }
    }
  }
}
