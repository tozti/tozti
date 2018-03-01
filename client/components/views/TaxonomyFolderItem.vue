<template>
  <TaxonomyItem
    icon="folder"
    :loading="loading"
    :title="title"
    :to="handle"
    :subtitle="date"
  />
</template>

<script>
  import TaxonomyItem from './TaxonomyItem'
  import { resourceMixin } from '../../mixins'

  export default {
    components: { TaxonomyItem },
    mixins: [ resourceMixin ],

    props: {
      handle: String,
    },

    data() {
      return {
        title: '',
        date: '',
      }
    },

    watch: {
      loading() {
        this.title = this.resource.body.name
        this.date = this.resource.meta['last-modified']
        this.url = this.resource.meta['last-modified']
      }
    }
  }
</script>
