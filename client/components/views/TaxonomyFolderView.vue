<template>
  <div v-if="resource" class="taxonomy">
    <p>
      <a class="button" @click="displayCreationModal">Nouveau dossier</a>
    </p>
    <div
      v-if="isEmpty"
      class="content has-text-grey has-text-centered has-vertical-space">
      <p>
      <i class="nc-icon nc-grid-45 x3"></i>
      </p>
      <p>Ce dossier est vide.</p>
    </div>
    <div v-else>
      <component
        v-for="(item, handle) in children"
        :is="getItemComponent(item)"
        :id="item.id"
        :handle="handle"
        :key="item.id"/>
    </div>
  </div>
</template>

<script>
  import { ModalProgrammatic } from 'buefy'
  import { resourceMixin } from '../../mixins'
  import DefaultItem from './TaxonomyResourceItem'
  import GroupItem from './TaxonomyGroupItem'
  import FolderItem from './TaxonomyFolderItem'
  import NewFolderForm from '../NewFolderForm'

  export { DefaultItem as TaxonomyItemComponent }

  export function addTaxonomyItem(type, component) {
    taxonomyItems.add(type, component)
  }

  const taxonomyItems = new Map(
    [ ['core/group', GroupItem]
    , ['core/folder', FolderItem]
    ]
  )

  export default {
    mixins: [ resourceMixin ],

    computed: {
      isEmpty() {
        return Object
          .getOwnPropertyNames(this.children)
          .filter(key => this.children.propertyIsEnumerable(key))
          .length == 0
      },

      children() {
        return this.resource.body.children.data
      }
    },

    methods: {
      getItemComponent({ type }) {
        if (taxonomyItems.has(type)) {
          return taxonomyItems.get(type)
        }
        return DefaultItem
      },

      displayCreationModal() {
        ModalProgrammatic.open({
          parent: this,
          component: NewFolderForm,
          scroll: 'keep',
          props: {
            root: this.resource
          }
        })
      }
    }

  }
</script>
