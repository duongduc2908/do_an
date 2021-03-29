<template>
  <div class="fixed top-0 left-0 w-full h-full flex items-center justify-center">
    <div class="absolute top-0 left-0 w-full h-full flex items-center justify-center bg-gray-700 bg-opacity-25">
    </div>
    <div class="w-2/5 z-40 rounded-lg shadow-lg bg-white overflow-hidden flex flex-col" v-if="camera">
      <div class="flex-grow p-4">
        <div class="mb-6 py-1 sticky">
          <h1 class="text-gray-700 mb-4 text-xl">Sửa camera: <strong>{{ camera.name }}</strong></h1>
        </div>

        <label class="text-sm uppercase text-gray-600 font-bold mb-2 block">Tên camera</label>
        <input
          id="name"
          v-model="editingCamera.name"
          class="mb-6 px-4 py-2 w-full bg-gray-200 placeholder:text-gray-600 text-gray-800 rounded-md transition-all duration-200
          focus:outline-none focus:shadow-outline"
          type="text"
          placeholder="Ví dụ: Camera sảnh C,..."
        >

        <label class="text-sm uppercase text-gray-600 font-bold mb-2 block">Hướng dẫn di chuyển</label>
        <textarea
          id="name"
          v-model="editingCamera.instruction"
          class="mb-4 px-4 py-2 w-full bg-gray-200 placeholder:text-gray-600 text-gray-800 rounded-md transition-all duration-200
          focus:outline-none focus:shadow-outline"
          type="text"
          placeholder="Ví dụ: Đi tới phía Đông tòa nhà, sau đó đi xuống cầu thang bộ gần nhất."
        ></textarea>

        <label class="text-sm uppercase text-gray-600 font-bold mb-2 block">Liên kết RTSP</label>
        <input
          id="name"
          v-model="editingCamera.link_stream"
          class="mb-6 px-4 py-2 w-full bg-gray-200 placeholder:text-gray-600 text-gray-800 rounded-md transition-all duration-200
          focus:outline-none focus:shadow-outline"
          type="text" placeholder="rtsp://"
        >
      </div>

      <div class="bg-gray-200 flex justify-end">
        <div class="flex p-4">
        <button
          @click="confirmEdit"
          class="w-32 px-4 py-3 mr-3 bg-blue-700 text-white hover:bg-blue-800 font-bold text-xs rounded-lg transition-all duration-200">Thay đổi</button>

        <button
          @click="closePopup"
          class="w-32 px-4 py-3 bg-gray-300 text-gray-700 hover:bg-gray-400 font-bold text-xs rounded-lg transition-all duration-200">Hủy bỏ</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    camera: {
      type: Object,
      default: null
    }
  },

  data () {
    return {
      editingCamera: {
        name: '',
        instruction: '',
        link_stream: '',
        link_image: '',
        name_image: '',
        camera_id: ''
      }
    }
  },

  methods: {
    confirmEdit () {
      this.$emit('confirmEdit', this.editingCamera)
    },

    closePopup () {
      this.$emit('closePopup')
    },

    cloneCamera () {
      this.editingCamera = {
        name: this.camera.name,
        instruction: this.camera.instruction,
        link_stream: this.camera.link_stream,
        link_image: this.camera.link_image,
        name_image: this.camera.link_image,
        camera_id: this.camera.camera_id
      }
    }
  },

  created () {
    this.cloneCamera()
  }
}
</script>
