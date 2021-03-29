<template>
  <div class="fixed top-0 left-0 w-full h-full flex items-center justify-center">
    <div @click="$emit('closeModal')" class="absolute top-0 left-0 w-full h-full flex items-center justify-center bg-gray-700 bg-opacity-25">
    </div>
    <div class="relative w-3/5 rounded-lg shadow-lg bg-white overflow-hidden flex flex-col z-40">
      <img v-if="url" :src="url" alt="" class="w-full">
      <template v-if="box">
        <div v-for="(b, index) in box" :key="index" class="absolute border-2 border-yellow-600"
          :style="{
            left: `${b[0] * 100}%`,
            top: `${b[1] * 100}%`,
            width: `${(b[2] - b[0]) * 100}%`,
            height: `${(b[3] - b[1]) * 100}%`,
            }">
        </div>
      </template>
    </div>
  </div>
</template>

<script>
// import axios from '@/apis/axios'
// import io from 'socket.io-client'

export default {
  props: {
    camera: {
      type: Object,
      default: null
    },

    place: {
      type: Object,
      default: null
    },

    url: String,

    box: Array
  },

  data () {
    return {
      // url: ''
    }
  },

  async mounted () {
    // try {
    //   await axios.get(`http://27.72.147.222:8888/api/stream/connection_api/connect?place_id=${this.place._id}&camera_id=${this.camera.camera_id}&rtsp_link=/media/server/A6F2-8B3D/CodeChuan/Core_Python_Flask/video1.mp4&username&password&selectedProtocol=1`)
    // } catch (error) {
    //   console.error(error)
    // }
    //
    // console.log('hello')
    //
    // const socket = io('http://27.72.147.222:8888')
    //
    // setTimeout(async () => {
    //   await axios.get(`http://27.72.147.222:8888/api/stream/connection_api/disconnect?place_id=${this.place._id}&camera_id=${this.camera.camera_id}`)
    //   socket.emit('disconnect')
    // }, 10000)
    //
    // socket.on('connection', (obj) => {
    //   console.log(obj)
    //   this.log.push(obj)
    // })
    //
    // socket.on('imageConversionByClient', (obj) => {
    //   let binary = ''
    //   const bytes = new Uint8Array(obj.buffer)
    //   const len = bytes.byteLength
    //   for (let i = 0; i < len; i++) {
    //     binary += String.fromCharCode(bytes[i])
    //   }
    //   this.url = 'data:image/jpeg;base64,' + window.btoa(binary)
    // })
  }

  // watch: {
  //   box (to) {
  //     console.log(to[0][0], to[0][1], to[0][2], to[0][3])
  //   }
  // }
}
</script>
