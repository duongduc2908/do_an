<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import Vue from 'vue'
import io from 'socket.io-client'
import "@/assets/styles/main.scss"
import VueSocketio from 'vue-socket-io';

export default {
  name: 'App',
  created(){
    this.initSocket();
  },
  methods:{
    initSocket(){
      const socket =  Vue.use(VueSocketio, 'http://localhost:4321/');
      this.$socket.on('imageConversionByClient', (obj) => {
        // let binary = ''
        // const bytes = new Uint8Array(obj.buffer)
        // const len = bytes.byteLength
        // for (let i = 0; i < len; i++) {
        //   binary += String.fromCharCode(bytes[i])
        // }
        // this.url = 'data:image/jpeg;base64,' + window.btoa(binary)
      });
    }
  }
}
</script>
