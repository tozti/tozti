import TaxonomyItem from './TaxonomyItem'

export default {
  extends: TaxonomyItem,

  computed: {
    title() { return this.resource.attributes.name }
  },

  data() {
    return {
      icon: 'account-multiple'
    }
  }
}
