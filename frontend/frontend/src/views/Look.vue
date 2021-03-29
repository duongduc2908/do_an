<template>
  <div class="log font-mono bg-black text-green-400 rounded-lg p-12 m-12">
    <div class="relative">
      <img :src="url" alt="" class="w-full">
    </div>

    <div class="mb-1" v-for="(item, index) in log" :key="index">{{ item }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import io from 'socket.io-client'

export default {
  data () {
    return {
      log: [],
      url: ''
    }
  },

  async mounted () {
    try {
      await axios.get('http://27.72.147.222:8888/api/stream/connection_api/connect?rtsp_link=/media/server/A6F2-8B3D/CodeChuan/Core_Python_Flask/video1.mp4&username&password&selectedProtocol=1')
    } catch (error) {
      console.error(error)
    }

    console.log('hello')

    const socket = io('http://27.72.147.222:8888')

    setTimeout(async () => {
      await axios.get('http://27.72.147.222:8888/api/stream/connection_api/disconnect')
      socket.emit('disconnect')
    }, 10000)

    socket.on('connection', (obj) => {
      console.log(obj)
      this.log.push(obj)
    })

    socket.on('imageConversionByClient', (obj) => {
      let binary = ''
      const bytes = new Uint8Array(obj.buffer)
      const len = bytes.byteLength
      for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i])
      }
      this.url = 'data:image/jpeg;base64,' + window.btoa(binary)
    })
  }
}
</script>
