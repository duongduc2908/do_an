<template>
  <div class="w-full h-full flex shadow-lg rounded-lg overflow-hidden">
    <div class="bg-gray-200 w-48 h-48">
      <img class="w-full h-full location-image" alt="" v-if="popupContent.photo" :src="popupContent.photo">
    </div>

    <div class="bg-white flex-grow p-4 flex flex-col justify-between">
      <div>
        <div class="mb-4 font-bold text-lg">
          {{ popupContent.name }}
        </div>

        <div class="mb-1 flex items-center">
          <CheckIcon class="mr-1 block text-green-600" />
          <span class="text-green-800">Đang mở cửa</span>
        </div>
      </div>

      <div>
        <button class="px-4 py-2 bg-green-200 text-green-700 font-bold rounded-lg">Liên hệ</button>
      </div>
    </div>
  </div>
</template>

<script>
import CheckIcon from 'vue-material-design-icons/Check'

export default {
  components: {
    CheckIcon
  },
  props: {
    popupContent: Object
  }
}
</script>
