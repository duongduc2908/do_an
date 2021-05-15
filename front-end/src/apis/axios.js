import axios from 'axios'
import store from '@/store'

axios.interceptors.request.use(function (config) {
  const auth = store.state.auth
  if (auth) {
    const token = auth.access_token
    config.headers.Authorization = 'Bearer ' + token
  }

  return config
})

export default axios
