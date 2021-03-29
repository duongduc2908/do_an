<template>
  <div>
    <div class="mb-12 py-1 border-b-2 border-gray-400 sticky">
      <h1 class="text-gray-700 uppercase mb-4 text-2xl">Thêm địa điểm mới</h1>
    </div>

    <form @submit.prevent="handleSubmit">

      <div class="mb-12 flex">
        <div class="mr-4 flex-grow">
          <label class="text-sm uppercase text-gray-600 font-bold mb-2 block" for="name">Tên địa điểm</label>
          <input
            v-model="edit.name"
            id="name"
            class="px-4 py-2 w-full bg-white placeholder:text-gray-600 text-gray-800 rounded-md transition-all duration-200
            focus:outline-none focus:shadow-outline"
            type="text"
          >
        </div>

        <div class="flex-grow">
          <label class="text-sm uppercase text-gray-600 font-bold mb-2 block" for="name">Loại</label>
          <input
            v-model="edit.type"
            id="name"
            class="px-4 py-2 w-full bg-white placeholder:text-gray-600 text-gray-800 rounded-md transition-all duration-200
            focus:outline-none focus:shadow-outline"
            type="text"
          >
        </div>
      </div>

      <div class="mb-12">
        <label class="text-sm uppercase text-gray-600 font-bold mb-2 block" for="name">Vị trí</label>

        <MapsPicker class="flex-grow w-full shadow-lg" style="height: 640px" />
      </div>

      <div class="mb-12">
        <label class="text-sm uppercase text-gray-600 font-bold mb-2 block" for="name">Danh sách camera</label>

        <div class="bg-gray-300 p-4 rounded-lg grid grid-cols-3 grid-rows-none gap-4">
          <div v-for="n in 4" :key="n" class="flex flex-col bg-gray-100 h-48 rounded-lg overflow-hidden">
            <div class="flex-grow"></div>
            <div class="h-12 bg-gray-100 flex p-2">
              <button
                class="px-3 py-1 mr-1 w-full bg-blue-200 text-blue-700 hover:bg-blue-300 font-bold text-xs rounded-lg transition-all duration-200">Thay đổi</button>

              <button
                class="px-3 py-1 w-full bg-red-200 text-red-700 hover:bg-red-300 font-bold text-xs rounded-lg transition-all duration-200">Xóa</button>
            </div>
          </div>
          <button class="block flex flex-col items-center justify-center text-gray-500 bg-gray-400 hover:text-gray-600 hover:bg-gray-500 h-48 rounded-lg overflow-hidden transition-all duration-200">
            <CameraPlusIcon size="64" />
          </button>
        </div>
      </div>

      <div class="flex justify-center">
        <button
          class="px-8 py-2 focus:outline-none focus:shadow-outline rounded-md transition-all duration-200 mb-6"
          :class="{ 'bg-gray-400 text-gray-600': editing, 'bg-green-700 hover:bg-green-800 text-white': !editing }"
        >
          <template v-if="editing">
            Đang lưu thay đổi
          </template>

          <template v-else>
            Thay đổi
          </template>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import MapsPicker from '@/components/MapsPicker.vue'
import CameraPlusIcon from 'vue-material-design-icons/CameraPlus'

export default {
  components: {
    MapsPicker,
    CameraPlusIcon
  }
}
</script>
