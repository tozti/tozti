export default new Vuex.Store({
  state: {
    notifications: [],
  },
  mutations: {
    addNotification (state, title, content) {
      state.notifications.push({
        seen: false,
        title,
        content
      })
    }
  },
  modules: {}
})
