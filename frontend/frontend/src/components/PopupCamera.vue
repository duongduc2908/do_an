<template>
  <div class="flex items-end">
    <div class="place-info bg-white shadow-lg rounded-lg overflow-hidden w-popup-place h-48 flex mr-2">
      <div class="w-48 h-full flex flex-col">
        <img class="w-full h-full location-image" alt="" v-if="popupContent.link_image" :src="popupContent.link_image">
      </div>

      <div class="bg-white flex-grow p-4 flex flex-col justify-between">
        <div>
          <div class="mb-4 font-bold text-lg text-gray-800 flex justify-between">
            <div>
              {{ popupContent.name }}
            </div>
            <button class="text-xs uppercase px-3 py-1 text-blue-700 hover:bg-blue-200 transition-all duration-200 font-bold rounded-lg">Liên hệ</button>
          </div>

          <div class="mb-1 flex items-center">
            <CheckIcon class="mr-1 block text-green-600" />
            <span class="text-green-800">{{ cameras.length }}/{{ cameras.length }} camera vận hành bình thường</span>
          </div>

          <div class="flex items-center text-xs">
            <template v-if="popupContent.status === 'warn'">
              <HelpCircleIcon class="mr-1 block text-yellow-600" />
              <span class="text-yellow-800">Có báo động cháy</span>
            </template>

            <template v-else-if="popupContent.status === 'fire'">
              <AlertIcon class="mr-1 block text-red-600" />
              <span class="text-red-800">Đã xác nhận cháy</span>
            </template>

            <template v-else-if="popupContent.status === 'safe'">
              <CheckIcon class="mr-1 block text-green-600" />
              <span class="text-green-800">Không phát hiện cháy</span>
            </template>
          </div>
        </div>

        <div class="flex flex-between">
          <div v-if="popupContent.status === 'warn'" class="flex">
            <button @click.prevent="confirmAlarm" class="px-4 py-2 bg-red-700 hover:bg-red-800 text-white font-bold rounded-lg mr-2 transition-all duration-200">Xác nhận cháy</button>
            <button @click.prevent="dismissAlarm" class="px-4 py-2 bg-green-200 hover:bg-green-300 text-green-700 font-bold rounded-lg transition-all duration-200">Không có cháy</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="cameras" class="overflow-hidden transition-all duration-500 camera-info bg-white bg-white shadow-lg rounded-lg h-popup-cam p-4"
      :class="{'w-0 opacity-0': !cameraList, 'w-popup-cam opacity-100': cameraList}"
    >
      <div class="mb-6 font-bold text-lg">
        Camera tại địa điểm này
      </div>

      <div class="mb-6">
        <!-- <div class="mb-3 text-gray-600 text-xs uppercase font-bold">Không phát hiện cháy</div> -->
        <div class="hover:bg-gray-300 transition-all duration-200 rounded-lg" v-for="(camera, index) in cameras" :key="index">
          <div class="flex justify-between p-2 mb-1">
            <div class="flex">
              <img src="@/assets/img/camera-green.png" class="w-6 h-6 mr-2" alt="">
              <div>
                <div class="font-bold mb-1 uppercase">{{ camera.name }}</div>
                <div class="text-gray-700">{{ camera.instruction }}</div>
              </div>
            </div>
            <div>
              <template v-if="camera.activated">
                <button @click="$store.dispatch('deactivateCamera', { placeId: popupContent._id, cameraId: camera.camera_id })"
                  class="bg-red-200 hover:bg-red-300 text-red-800 hover:text-red-900 focus:outline-none px-2 py-1 rounded-lg mr-1">
                  Hủy kích hoạt
                </button>

                <button @click="$emit('startStream', popupContent._id, camera.camera_id)"
                  class="bg-blue-200 hover:bg-blue-300 text-blue-800 hover:text-blue-900 focus:outline-none px-2 py-1 rounded-lg">
                  Quan sát
                </button>
              </template>

              <button v-else @click="$store.dispatch('activateCamera', { placeId: popupContent._id, cameraId: camera.camera_id, rtspLink: camera.link_stream })"
                class="bg-yellow-200 hover:bg-yellow-300 text-yellow-800 hover:text-yellow-900 focus:outline-none px-2 py-1 rounded-lg">
                Kích hoạt
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CheckIcon from 'vue-material-design-icons/Check'
import AlertIcon from 'vue-material-design-icons/Alert'
import HelpCircleIcon from 'vue-material-design-icons/HelpCircle'

export default {
  components: {
    CheckIcon,
    AlertIcon,
    HelpCircleIcon
  },

  props: {
    popupContent: Object
  },

  data () {
    return {
      cameraList: false
    }
  },

  computed: {
    cameras () {
      return this.popupContent.cameras
    }
  },

  mounted () {
    window.setTimeout(() => {
      this.cameraList = true
    }, 400)
  },

  methods: {
    confirmAlarm () {
      this.$store.dispatch('confirmAlarm', { id: this.popupContent._id })
    },

    dismissAlarm () {
      this.$store.commit('dismissAlarm', { id: this.popupContent._id })
    }
  }
}
</script>
