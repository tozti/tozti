// TODO(flupe): read about WeakMaps to see if it can help freeing memory

// contains the unaltered server data
const cache = new Map()

// contains the proxied resources
const storage = new Map()

const store = {

  schemas: {},

  /**
   * Finds a resource in the store.
   * The type of the resource (its schema) MUST be specified
   * As it allows for resource initialization until the server responds.
   *
   * @param {string} type - The name of the registered schema of the resource.
   * @param {Number} id - The uuid of the queried resource.
   */
  get(type, id) {
    if (storage.has(id)) {
      return storage.get(id)
    }
    else {
      return store.fetch(type, id)
    }
  },

  fetch(type, id) {
    const schema = store.schemas[type]
    const proxied = createSchemaInstance(schema)

    storage.set(id, proxied)

    /**
     * TODO(flupe): send GET request
     * - if it succeeds, update cache
     *   (which should automatically update storage)
     * - if it fails, then what?
     *   - maybe remove item from storage
     */

    return proxied
  },

  registerSchema(name, schema) {
    store.schemas[name] = schema
  }

}

export default store

// placeholder
store.registerSchema('core/user', {
  attributes: {
    name: { type: String },
    email: { type: String },
    login: { type: String },
  },
  relationships: {
    groups: {
      'reverse-of': {
        type: 'core/group',
        path: 'members',
      }
    }
  }
})

store.registerSchema('core/group', {
  attributes: {
    name: { type: String },
  },
  relationships: {
    members: {
      arity: 'to-many',
      type: 'core/user',
    }
  }
})

/**
 * Instanciates an initialized resource following a given schema.
 * The motivation is to give placeholder values that might not follow every
 * constraint (i.e we do not look at constraints such as minLength)
 * but that respect the required nested structure.
 *
 * TODO(flupe): handle relationships
 */
export function createSchemaInstance({ attributes = {}, relationships = {} }) {
  let data = {
    attributes: {},
    relationships: {},
  }

  for (let attr in attributes) {
    if (attributes.hasOwnProperty(attr))
      initAttribute(data.attributes, attr, attributes[attr])
  }

  function initAttribute(target, name, spec) {
    const { type } = spec

    let writable = true
    let value

    if (type === Object) {
      value = {}
      const { required, properties } = spec

      if (required) {
        required.forEach(field => initAttribute(value, field, properties[field]))
        // TODO(flupe): we might actually want to replace the entire
        //              provided that the new value does contain the required fields
        writable = false
      }
    }

    else {
      value = type()
    }

    // TODO(flupe): find why vue is completely lost when properties are defined
    //              with defineProperty

    // Object.defineProperty(target, name, {
    //   enumerable: true,
    //   writable,
    //   value
    // })

    target[name] = value
  }

  return data
}

