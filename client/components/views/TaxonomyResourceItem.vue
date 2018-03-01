<template>
  <TaxonomyItem :loading="loading" :title="title" :subtitle="subtitle"/>
</template>

<script>
  import { resourceMixin } from '../../mixins'
  import TaxonomyItem from './TaxonomyItem'

  export default {
    components: { TaxonomyItem },
    mixins: [ resourceMixin ],

    props: {
      handle: {
        type: String,
      }
    },

    data() {
      return {
        title: '',
        subtitle: '',
      }
    },

    watch: {
      loading() {
        this.title = this.id
        this.subtitle = this.resource.meta['last-modified']
      }
    }
  }
</script>
