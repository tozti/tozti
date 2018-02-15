<template>
  <div>
    <button class="button is-dark">
      <b-icon pack="mdi" icon="folder-plus"></b-icon>
    </button>
    <button class="button is-dark">
      <b-icon pack="mdi" icon="upload"></b-icon>
    </button>
    <b-table
      :data="[]"
      :columns="columns">
      <template slot="empty">
        <section class="section">
          <div class="content has-text-grey has-text-centered">
            <p>Nothing here.</p>
          </div>
        </section>
      </template>
    </b-table>
  </div>
</template>

<script>
  export default {
    props: [ 'taxonomy' ],
    data() {
      return {
        columns: [
          { field: 'id'
          , label: 'ID'
          , width: 40
          , numeric: true
          },
          { field: 'name'
          , label: 'Nom'
          },
          { field: 'date'
          , label: 'Date'
          }
        ]
      }
    }
  }
</script>
