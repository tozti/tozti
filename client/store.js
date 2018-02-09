import api from './api'

// TODO(flupe): read about WeakMaps to see if it can help freeing memory

// contains the proxied resources
const storage = new Map()
const pending = new Map()

const store = {

  schemas: {},

  /**
   * Find a resource in the store associated with the given id.
   * Returns a Promise resolving to the proxied queried resource.
   * It rejects to the server response, giving access to status codes.
   *
   * @param {string} id - The uuid of the queried resource.
   */
  get(id) {
    if (storage.has(id)) {
      return Promise.resolve(storage.get(id))
    }
    else if (pending.has(id)) {
      return pending.get(id)
    }
    else {
      return store.fetchResource(id)
    }
  },


  /**
   * Fetch a resource from the server associated with the given id.
   * Returns a Promise resolving to the proxied queried resource.
   *
   * @param {string} id - The uuid of the queried resource.
   */
  fetchResource(id) {
    const promise = api
      .get(api.resourceURL(id))
      .then(res => res.json())
      .then(({ data }) => {
        cache.set(id, data)

        if (storage.has(id)) {
          updateProxy(id)
          return storage.get(id)
        }
        else {
          let proxy = createProxy(data)
          storage.set(id, proxy)
          return proxy
        }
      })

    pending.set(id, promise)

    // maybe move this inside the promise definition.
    // note that this is not very robust to other type of queries.
    promise.finally(_ => {
      pending.delete(id)
    })

    return promise
  },


  /**
   * Store a resource in the cache,
   * This should only be used with resources coming from the server.
   */
  saveResource(resource) {

  },


  /**
   * Fetch every resource matching the given type
   * (/api/type/[type])
   */
  fetchByType(type) {
    return api
      .get(API.origin + '/type/' + type)
      .then(res => {
        let data = res.json().data
        if (data !== null)
          data.forEach(resource => saveResource(data))
        return data
      })
  },

  registerSchema(name, schema) {
    store.schemas[name] = schema
  }

}

// TODO(flupe): aussi
function updateProxy(id) {
}

// TODO(flupe): oui
function createProxy(data) {
  return data
}

export default store

