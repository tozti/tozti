<template>
  <div v-if="resource" class="taxonomy">
    <p>
      <a class="button" @click="displayCreationModal('core/folder')">Nouveau dossier</a>
      <b-dropdown style="margin-left: 10px;">
        <a class="button" slot="trigger">
          <b-icon pack="mdi" icon="file-plus"></b-icon>
        </a>

        <b-dropdown-item 
          v-for="{ type, name, gender } in resourceTypes"
          @click="displayCreationModal(type)"
          :key="type">
          <template v-if="gender == 'm'">Nouveau</template>
          <template v-else>Nouvelle</template>
          {{ name }}
        </b-dropdown-item>
      </b-dropdown>
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
        :key="item.id"
        :root="resource" />
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
      },

      resourceTypes() {
        return tozti.resourceTypes
      }
    },

    methods: {
      getItemComponent({ type }) {
        if (taxonomyItems.has(type)) {
          return taxonomyItems.get(type)
        }
        return DefaultItem
      },

      getFormForType(type) {
        if (type == 'core/folder') {
          return NewFolderForm
        }

        for (let res of this.resourceTypes) {
          if (type == res.type) {
            return res.creationForm
          }
        }
      },

      displayCreationModal(type) {
        ModalProgrammatic.open({
          parent: this,
          component: this.getFormForType(type),
          scroll: 'keep',
          props: {
            root: this.resource
          }
        })
      }
    }

  }
</script>
