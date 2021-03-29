<template>
  <div class="mb-4 rounded-lg overflow-hidden bg-white w-full flex">
    <div class="flex flex-col" style="min-width: 90px; width: 90px; height: 150px">
      <img class="w-full h-full location-image" alt="" v-if="place.link_image" :src="place.link_image">
    </div>

    <div class="bg-white flex-grow p-4 flex flex-col justify-between">
      <div class="mb-2">
        <div class="mb-1 font-bold">
          {{ place.name }}
        </div>

        <div class="mb-1 flex items-center text-xs">
          <CheckIcon class="mr-1 block text-green-600" />
          <span class="text-green-800">{{ place.cameras.length }}/{{ place.cameras.length }} camera vận hành bình thường</span>
        </div>

        <div class="flex items-center text-xs">
          <template v-if="place.status === 'warn'">
            <HelpCircleIcon class="mr-1 block text-yellow-600" />
            <span class="text-yellow-800">Có báo động cháy</span>
          </template>

          <template v-else-if="place.status === 'fire'">
            <AlertIcon class="mr-1 block text-red-600" />
            <span class="text-red-800">Đã xác nhận cháy</span>
          </template>

          <template v-else-if="place.status === 'safe'">
            <CheckIcon class="mr-1 block text-green-600" />
            <span class="text-green-800">Không phát hiện cháy</span>
          </template>
        </div>
      </div>
      <div v-if="editMode">
        <button
          @click.prevent="$emit('startEdit')"
          class="px-3 py-1 mr-1 bg-blue-200 text-blue-700 hover:bg-blue-300 font-bold text-xs rounded-lg transition-all duration-200">Thay đổi</button>

        <button
          class="px-3 py-1 bg-red-200 text-red-700 hover:bg-red-300 font-bold text-xs rounded-lg transition-all duration-200">Xóa</button>
      </div>

      <div v-else>
        <button @click.prevent="openPlace"
          class="px-3 py-1 bg-blue-200 text-blue-700 hover:bg-blue-300 font-bold text-xs rounded-lg transition-all duration-200">Tìm trên bản đồ</button>
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
    place: Object,

    editMode: {
      type: Boolean,
      default: false
    }
  },

  computed: {
    google () {
      return this.$store.state.mapsApi.google
    }
  },

  methods: {
    openPlace () {
      this.google.maps.event.trigger(this.place.marker, 'click')
    }
  }
}
</script>
