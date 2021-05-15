
import { actionCamera } from '@/api/camera'

const mutations = {
    setCameraActivated (state, payload) {
        // const place = state.places.find(p => p._id === payload.placeId)
        // const camera = place.cameras.find(c => c.camera_id === payload.cameraId)

        camera.activated = true
    },
}
const actions = {
  async actionCamera (context, payload) {
    // context.commit('setCameraActivated', payload)
    return new Promise((resolve, reject) => {
        actionCamera(payload).then(response => {
        const { data } = response
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })

  }
}

export default {
  namespaced: true,
  actions,
  mutations
}
