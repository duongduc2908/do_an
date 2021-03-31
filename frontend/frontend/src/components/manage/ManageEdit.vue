<template>
  <div>
    <div class="mb-12 py-1 border-b-2 border-gray-400 sticky">
      <h1 class="text-gray-700 uppercase mb-4 text-2xl">{{ current.name }}</h1>
    </div>

    <form v-if="edit" @submit.prevent="handleSubmit">

      <div class="mb-12 flex">
        <div class="mr-4 flex-grow">
          <label class="text-sm uppercase text-gray-600 font-bold mb-2 block">Tên địa điểm</label>
          <input
            v-model="edit.name"
            id="name"
            class="px-4 py-2 w-full bg-white placeholder:text-gray-600 text-gray-800 rounded-md transition-all duration-200
            focus:outline-none focus:shadow-outline"
            type="text"
          >
        </div>

        <div class="flex-grow">
          <label class="text-sm uppercase text-gray-600 font-bold mb-2 block">Loại</label>
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
        <label class="text-sm uppercase text-gray-600 font-bold mb-2 block" for="photo">Hình ảnh</label>
        <div class="mb-2">
          <label class="inline-block px-3 py-1 text-sm text-blue-800 bg-blue-200 hover:bg-blue-300 cursor-pointer rounded-md transition-all duration-200" for="photo">Chọn ảnh</label>
          <input
            @change="choosePhoto"
            class="hidden px-4 py-2 w-full bg-white placeholder:text-gray-600 text-gray-800 rounded-md transition-all duration-200
            focus:outline-none focus:shadow-outline"
            type="file"
            id="photo"
            accept="image/png, image/jpeg">
        </div>
          <img v-if="uploadingImage" class="block w-48 h-48" style="object-fit: cover" :src="uploadingImageUrl">
          <img v-else class="block w-48 h-48" style="object-fit: cover" :src="edit.link_image">
      </div>

      <div class="mb-12">
        <label class="text-sm uppercase text-gray-600 font-bold mb-2 block" for="name">Vị trí</label>
        <div class="flex mb-2">
          <input class="flex-grow mr-2 px-4 py-2 rounded-md bg-gray-400 text-gray-600" :value="edit.location.lat" disabled>
          <input class="flex-grow px-4 py-2 rounded-md bg-gray-400 text-gray-600" :value="edit.location.lng" disabled>
        </div>
        <MapsPicker @locationChanged="locationChanged" class="flex-grow w-full shadow-lg" style="height: 640px" :location="edit.location" />
      </div>

      <div class="mb-12">
        <label class="text-sm uppercase text-gray-600 font-bold mb-2 block" for="name">Danh sách camera</label>

        <div class="bg-gray-300 p-4 rounded-lg grid grid-cols-3 grid-rows-none gap-4">
          <div v-for="(camera, index) in edit.cameras" :key="index" class="relative flex flex-col rounded-lg overflow-hidden">
            <div class="h-8 ml-1 text-gray-600 uppercase font-bold text-sm flex py-1 px-1 w-full">
              {{ camera.name }}
            </div>
            <div class="flex-grow bg-gray-100 h-48 rounded-lg overflow-hidden"><img class="w-full h-full" style="object-fit: cover" :src="camera.link_image"></div>
            <div class="h-12 bg-black bg-opacity-50 flex p-2 absolute bottom-0 left-0 w-full">
              <button
                @click.prevent="editCamera(camera)"
                class="px-3 py-1 mr-1 w-full bg-blue-200 text-blue-700 hover:bg-blue-300 font-bold text-xs rounded-lg transition-all duration-200">Thay đổi</button>

              <button
                class="px-3 py-1 w-full bg-red-200 text-red-700 hover:bg-red-300 font-bold text-xs rounded-lg transition-all duration-200">Xóa</button>
            </div>
          </div>
          <div class="">
            <div class="h-8"></div>
            <button @click.prevent="addCamera" class="block flex flex-col items-center justify-center text-gray-500 bg-gray-400 hover:text-gray-600 hover:bg-gray-500 w-full h-48 rounded-lg overflow-hidden transition-all duration-200">
              <CameraPlusIcon :size="64" />
            </button>
          </div>
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
            Xác nhận
          </template>
        </button>
      </div>
    </form>
    <CameraModal v-if="showCameraModal" :camera="editingCamera" @confirmEdit="confirmEditCamera" @closePopup="showCameraModal = false" />
  </div>
</template>

<script>
import axios from '@/apis/axios'
import MapsPicker from '@/components/MapsPicker.vue'
import CameraModal from '@/components/manage/CameraModal.vue'
import CameraPlusIcon from 'vue-material-design-icons/CameraPlus'

const BASE_URL = 'localhost:4321/api/v1'

export default {
  components: {
    MapsPicker,
    CameraPlusIcon,
    CameraModal
  },

  props: {
    current: {
      type: Object,
      default: null
    }
  },

  data () {
    return {
      edit: null,
      editing: null,
      uploadingImage: null,
      uploadingImageUrl: '',
      editingCamera: null,
      showCameraModal: false
    }
  },

  mounted () {
    this.cloneEdit()
  },

  methods: {
    async handleSubmit () {
      this.editing = true
      try {
        const place = this.edit
        await axios.put(`${BASE_URL}/place/update?place_id=${place._id}`, place)

        this.$toast.info('Đã lưu thay đổi thành công', 'Thông báo', {
          position: 'topCenter',
          timeout: 4000
        })

        await this.$store.dispatch('loadPlaces')
      } catch (error) {
        console.error(error)
      } finally {
        this.editing = false
      }
    },

    editCamera (camera) {
      this.showCameraModal = true
      this.editingCamera = camera
    },

    addCamera () {
    },

    confirmEditCamera (editedCamera) {
      const cameraId = this.edit.cameras.findIndex(c => c.camera_id === editedCamera.camera_id)

      this.edit.cameras[cameraId] = editedCamera
      this.showCameraModal = false
    },

    choosePhoto (event) {
      const file = event.target.files[0]

      this.uploadingImage = file
      this.uploadingImageUrl = URL.createObjectURL(file)
    },

    locationChanged (location) {
      this.edit.location.lat = location.lat
      this.edit.location.lng = location.lng
    },

    cloneEdit () {
      const place = this.current

      this.edit = {
        _id: place._id,
        name: place.name,
        location: {
          lat: place.location.lat,
          lng: place.location.lng
        },
        link_image: place.link_image,
        name_image: place.name_image,
        cameras: [...place.cameras]
      }
    }
  },

  watch: {
    current (to, from) {
      if (to._id !== from._id) {
        this.cloneEdit()
        this.uploadingImage = null
      }
    }
  }
}
</script>
