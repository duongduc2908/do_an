<template>
    <div class="hidden bg-white w-popup h-48 shadow-lg rounded-lg mb-8 flex">
      <div class="bg-gray-200 w-48 h-full">
        <img class="w-full h-full location-image" alt="" v-if="popupContent.photo" :src="popupContent.photo">
      </div>

      <div class="bg-white flex-grow p-4 flex flex-col justify-between">
        <div>
          <div class="mb-4 font-bold text-lg">
            {{ popupContent.name }}
          </div>

          <div class="mb-4">
            <CheckIcon class="mr-3 text-green-600" />
            <span class="text-green-800">Vận hành bình thường</span>
          </div>

          <div class="mb-4">
            <CheckIcon class="mr-3 text-green-600" />
            <span class="text-green-800">Không phát hiện cháy</span>
          </div>
        </div>

        <div>
          <button class="px-4 py-2 w-24 h-8 bg-green-700 rounded-lg">Liên hệ</button>
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
