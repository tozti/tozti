<template>
  <div v-if="!loading">
    <section class="level main-title">
      <h2 class="level-left">
        <i class="material-icons">folder</i> {{ resource.body.name }}
      </h2>
    </section>
    <section class="section">
      <TaxonomyFolderView :id="id"/>
    </section>
  </div>
</template>

<script>
  import { resourceMixin } from '../../mixins'
  import TaxonomyFolderView from './TaxonomyFolderView'

  export default {
    mixins: [ resourceMixin ],
    components: { TaxonomyFolderView },
  }
</script>
