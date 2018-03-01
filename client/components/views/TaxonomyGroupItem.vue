<template>
  <TaxonomyItem
    :loading="loading"
    :to="handle"
    :title="title"
    :subtitle="subtitle"/>
</template>
<script>
  import TaxonomyResourceItem from './TaxonomyResourceItem'

  export default {
    extends: TaxonomyResourceItem,

    props: {
      handle: String,
    },

    methods: {
      onLoaded() {
        this.title = this.resource.body.name
        this.subtitle = this.resource.meta['last-modified']
      }
    }
  }
</script>
