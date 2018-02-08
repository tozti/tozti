<template>
  <div class="uk-container uk-padding">
    <h1 class="uk-heading-primary">Dashboard</h1>
    <h3>No widget available just yet :(</h3>

    <workspace-editor :id="0"></workspace-editor>
  </div>
</template>

<script>
  import { resourceMixin } from '../mixins'

  let WorkspaceEditor = {
    mixins: [ resourceMixin('core/user') ],

    template: `
      <div>
        <h3>workspace settings</h3>
        <p>
          <label for="name">name: </label><br>
          <input id="name" v-model="attributes.name">
        </p>
        <span>{{ attributes.name }}</span>
      </div>
    `,
  }

  export default {
    components: { WorkspaceEditor }
  }
</script>
