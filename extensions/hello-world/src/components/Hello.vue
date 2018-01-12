<template>
  <div>
    <p>{{ count }}</p>
    <button v-on:click="increase">+1</button>
    <button v-on:click="decrease">-1</button>
  </div>
</template>

<script>
	export default {
    methods: {
      increase: function() {
        this.count += 1
      },
      decrease: function() {
        this.count -= 1
      }
    },

		data () {
			return {
				count: 0
			}
		}
	}
</script>
