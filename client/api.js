/**
 * A very generic API to communicate with the tozti backend
 */

const API = {}

API.origin = window.location.origin + '/api/store'

// API endpoints
API.resourcesURL = API.origin + '/resources'
API.resourceURL = id => API.resourcesURL + '/' + id
API.typeURL = type => API.origin + '/types/' + id

const config = {
  mode: 'same-origin',

  // allow the request to send & receive cookies
  credentials: 'same-origin',

  headers: new Headers({
    'Content-type': 'application/vnd.api+json',
    'Accept': 'application/vnd.api+json'
  })
}

function request(url, config) {
  // the fetch() Promise always resolves to the response,
  // whether it was successful or not
  return fetch(url, config)
    .then(res => res.ok ? Promise.resolve(res) : Promise.reject(res))
}

API.post = url => {
  const conf = Object.assign({}, config, { method: 'POST' })
  return request(url, conf)
}

API.patch = url => {
  const conf = Object.assign({}, config, { method: 'PATCH' })
  return request(url, conf)
}

API.delete = url => {
  const conf = Object.assign({}, config, { method: 'DELETE' })
  return request(url, conf)
}

API.get = url => {
  const conf = Object.assign({}, config, { method: 'GET' })
  return request(url, conf)
}

export default API
