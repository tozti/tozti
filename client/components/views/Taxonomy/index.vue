<template>
  <section class="section content">
    <h1>Taxonomy</h1>
    <div class="taxonomy">
      <item v-for="id in children" :id="id" :key="id"></item>
    </div>
  </section>
</template>

<script>
  import Item from './TaxonomyItem'

  export default {
    components: { Item },

    data() {
      return {
        children: [0, 1, 2, 3, 4]
      }
    }
  }
</script>
