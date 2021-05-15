<template>
  <div class="dashboard-container">
    <component :is="currentRole" />
    <div class="p-24 flex">
      <div style="width:75%">
        <img class="img-current w-full" :src="url"/>
      </div>
      <div class="list-imt-his">
        <img v-for="(item,index) in listImg" :key="index" class="img-his" :src="item"/>
      </div>
    </div>
    
    
    <dropzone />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import adminDashboard from './admin'
import editorDashboard from './editor'
import dropzone from '@/views/components-demo/dropzone'
import io from 'socket.io-client'
import throttle from 'lodash.throttle'

export default {
  name: 'Dashboard',
  components: { adminDashboard, editorDashboard ,dropzone},
  data() {
    return {
      currentRole: 'adminDashboard',
      socket: null,
      listImg:[],
      url:""
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    if (!this.roles.includes('admin')) {
      this.currentRole = 'editorDashboard'
    }
  },
mounted(){
    this.$socket.on('imageConversionByClient', (obj) => {
        let binary = ''
        const bytes = new Uint8Array(obj.buffer)
        const len = bytes.byteLength
        for (let i = 0; i < len; i++) {
          binary += String.fromCharCode(bytes[i])
        }
        this.url = 'data:image/jpeg;base64,' + window.btoa(binary)
        this.listImg.unshift(this.url);
        if(this.listImg && this.listImg.length >10){
          this.listImg.splice(10,1);
        }
    })
  }
}
</script>

<style scoped>
.img-current{
  height: 772px;
}
.list-imt-his{
  overflow: auto;
  width: 25%;
  height: 772px;
}
.img-his{
  margin: 0 16px 8px 16px;
  width: calc(100% - 32px);
  height: 250px;
}
</style>