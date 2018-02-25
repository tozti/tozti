<template>
  <section class="section content">
    <h1>Taxonomy</h1>
    <div class="taxonomy">
      <component v-for="linkage in children"
                 :is="getItemComponent(linkage)"
                 :id="linkage.id"
                 :key="linkage.id">
      </component>
    </div>
  </section>
</template>

<script>

  import DefaultItem from './TaxonomyItem'
  import GroupItem from './GroupItem.js'
  import FolderItem from './FolderItem.js'

  export { DefaultItem as TaxonomyItemComponent }

  const taxonomyItems = new Map(
    [ ['core/group', GroupItem]
    , ['core/folder', FolderItem]
    ]
  )

  export function addTaxonomyItem(type, component) {
    taxonomyItems.add(type, component)
  }

  export default {
    data() {
      return {
        children: tozti.me.body.pinned.data
      }
    },

    methods: {
      getItemComponent({ type }) {
        if (taxonomyItems.has(type)) {
          return taxonomyItems.get(type)
        }
        return DefaultItem
      }
    }
  }
</script>
