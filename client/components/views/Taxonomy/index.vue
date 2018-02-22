<template>
  <section class="section content">
    <h1>Taxonomy</h1>
    <div class="taxonomy">
      <item v-for="item in children" :id="item.id" :key="item.id"></item>
    </div>
  </section>
</template>

<script>
  import Item from './TaxonomyItem'

  export default {
    components: { Item },

    data() {
      return {
        children: tozti.me.relationships.groups.data
      }
    }
  }
</script>
