<template>
  <div class="bg-gray-200 flex-grow flex">
    <SideBar
      class="bg-gray-100 transition-all duration-500 opacity-100 w-sidebar"
      :editMode="true"
      @startEdit="startEdit"
      @startDelete="startDelete"
      @startAdd="startAdd"
    />

    <div class="flex-grow flex justify-center shadow-lg overflow-y-auto">
      <div class="w-full max-w-screen-md py-12 px-2">
        <div v-if="!edit" class="w-full h-full flex flex-col justify-center items-center">
          <img src="@/assets/img/empty.svg" class="mb-4 block w-48" alt="">

          <div class="mb-4 text-gray-700">Vui lòng chọn một địa điểm để chỉnh sửa.</div>

          <div class="mb-4">
            <button
              @click="startAdd"
              class="px-8 py-3 bg-green-700 text-white hover:bg-green-800 font-bold text-xs rounded-lg transition-all duration-200">
              Thêm địa điểm mới
            </button>
          </div>
        </div>

        <ManageEdit v-else-if="current && edit" :current="current" />

        <ManageAdd v-else-if="add" />
      </div>
    </div>
  </div>
</template>

<script>
import SideBar from '@/components/SideBar'
import ManageEdit from '@/components/manage/ManageEdit'
import ManageAdd from '@/components/manage/ManageAdd'

export default {
  components: {
    SideBar,
    ManageEdit,
    ManageAdd
  },

  data () {
    return {
      sidebarShow: true,
      current: null,
      add: null,
      edit: null
    }
  },

  methods: {
    startEdit (id) {
      const place = this.$store.state.places.find(p => p._id === id)
      this.current = place
      this.edit = true
    },

    startAdd () {
      this.add = true
    },

    startDelete (category, id) {

    }
  }
}
</script>
