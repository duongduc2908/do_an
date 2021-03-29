<template>
  <div class="h-full">
    <div class="h-full w-sidebar">
      <div class="h-full flex flex-col transition-all duration-500">
        <div>
          <template v-if="alarmPlaces.length === 0">
            <div class="bg-gray-200 flex px-3 py-4">
              <CheckIcon class="mr-2 text-green-600" />

              <div class="flex flex-col">
                <div class="font-bold tracking-wide text-lg mb-2 text-green-800">Mọi khu vực đều an toàn</div>
                <div class="leading-tight text-gray-600 text-sm">Không phát hiện đám cháy ở camera nào.</div>
              </div>
            </div>
          </template>

          <template v-else-if="firePlaces.length > 0">
            <div class="bg-red-200 flex px-3 py-4">
              <AlertIcon class="mr-2 text-red-600" />
              <div class="flex flex-col">
                <div class="font-bold tracking-wide text-lg mb-2 text-red-700">Đã xác nhận có đám cháy</div>
                <div class="leading-tight text-red-600 text-sm">Yêu cầu quan sát và điều hành cho đến khi đám cháy được xử lý.</div>
              </div>
            </div>
          </template>

          <template v-else-if="alarmPlaces.length > 0">
            <div class="bg-yellow-200 flex px-3 py-4">
              <HelpCircleIcon class="mr-2 text-yellow-600" />
              <div class="flex flex-col">
                <div class="font-bold tracking-wide text-lg mb-2 text-yellow-700">Yêu cầu hành động</div>
                <div class="leading-tight text-yellow-600 text-sm">Đã phát hiện có cháy tại một hoặc nhiều khu vực.</div>
              </div>
            </div>
          </template>
        </div>

        <div class="content flex flex-col overflow-hidden w-full">
          <div class="m-4 my-2 flex text-gray-600 uppercase text-sm font-bold">
            <button class="mr-6 py-2 border-b-2 border-gray-400 focus:outline-none" :class="{ 'border-blue-400 text-blue-600': currentTab === 'places' }" @click.prevent="currentTab = 'places'">Điểm theo dõi</button>
            <button class="mr-6 py-2 border-b-2 border-gray-400 focus:outline-none" :class="{ 'border-blue-400 text-blue-600': currentTab === 'fire-stations' }" @click.prevent="currentTab = 'fire-stations'">Trạm cứu hỏa</button>
            <button class="py-2 border-b-2 border-gray-400 focus:outline-none" :class="{ 'border-blue-400 text-blue-600': currentTab === 'hospitals' }" @click.prevent="currentTab = 'hospitals'">Bệnh viện</button>
          </div>

          <div class="m-4 my-2 flex">
            <input class="flex-grow bg-gray-200 placeholder:text-gray-900 px-4 py-2 w-full rounded-full focus:shadow-outline transition-all duration-200" type="text" placeholder="Nhập từ khóa cần tìm kiếm">
            <div v-if="editMode">
              <button
                @click="$emit('startAdd')"
                class="block ml-1 w-auto px-4 py-2 bg-green-200 text-green-800 hover:bg-green-300 rounded-full transition-all duration-200">
                <PlusIcon />
              </button>
            </div>
          </div>

          <div v-if="currentTab === 'places'" class="tab-content p-4 overflow-y-auto">
            <template v-if="alarmPlaces.length > 0">
              <div class="uppercase font-bold tracking-wide text-xs mb-4 text-yellow-600">Điểm có báo động</div>
              <PlaceList v-for="(place, index) in alarmPlaces" :key="`a-${index}`" :place="place" :editMode="editMode" @startEdit="$emit('startEdit', place._id)" />
            </template>

            <template v-if="safePlaces.length > 0">
              <div class="uppercase font-bold tracking-wide text-xs mb-4 text-gray-600">Điểm an toàn</div>
              <PlaceList v-for="(place, index) in safePlaces" :key="`b-${index}`" :place="place" :editMode="editMode" @startEdit="$emit('startEdit', place._id)" />
            </template>
          </div>

          <div v-if="currentTab === 'fire-stations'" class="tab-content p-4 overflow-y-auto">
            <div class="uppercase font-bold tracking-wide text-xs mb-4 text-gray-600">Đang hoạt động</div>
            <div v-for="(place, index) in fireStations" :key="index" class="mb-4 rounded-lg overflow-hidden bg-white w-full flex">
              <div class="flex flex-col" style="min-width: 90px; width: 90px; height: 150px">
                <img class="w-full h-full location-image" alt="" v-if="place.photo" :src="place.photo">
              </div>

              <div class="bg-white p-4 flex flex-col justify-between">
                <div class="mb-2">
                  <div class="mb-1 font-bold">
                    {{ place.name }}
                  </div>

                  <div class="mb-1 flex items-center text-xs">
                    <CheckIcon class="mr-1 block text-green-600" />
                    <span class="text-green-800">Đang hoạt động</span>
                  </div>
                </div>

                <div v-if="editMode">
                  <button
                    class="px-3 py-1 mr-1 bg-blue-200 text-blue-700 hover:bg-blue-300 font-bold text-xs rounded-lg transition-all duration-200">Thay đổi</button>

                  <button
                    class="px-3 py-1 bg-red-200 text-red-700 hover:bg-red-300 font-bold text-xs rounded-lg transition-all duration-200">Xóa</button>
                </div>

                <div v-else>
                  <button @click.prevent="openFireStation(index)"
                    class="px-3 py-1 bg-blue-200 text-blue-700 hover:bg-blue-300 font-bold text-xs rounded-lg transition-all duration-200">Tìm trên bản đồ</button>
                </div>
              </div>
            </div>
          </div>

          <div v-if="currentTab === 'hospitals'" class="tab-content p-4 overflow-y-auto">
            <div class="uppercase font-bold tracking-wide text-xs mb-4 text-gray-600">Đang mở cửa</div>
            <div v-for="(place, index) in hospitals" :key="index" class="mb-4 rounded-lg overflow-hidden bg-white w-full flex">
              <div class="flex flex-col" style="min-width: 90px; width: 90px; height: 150px">
                <img class="w-full h-full location-image" alt="" v-if="place.photo" :src="place.photo">
              </div>

              <div class="bg-white p-4 flex flex-col justify-between">
                <div class="mb-2">
                  <div class="mb-1 font-bold">
                    {{ place.name }}
                  </div>

                  <div class="mb-1 flex items-center text-xs">
                    <CheckIcon class="mr-1 block text-green-600" />
                    <span class="text-green-800">Đang mở cửa</span>
                  </div>
                </div>

                <div v-if="editMode">
                  <button
                    class="px-3 py-1 mr-1 bg-blue-200 text-blue-700 hover:bg-blue-300 font-bold text-xs rounded-lg transition-all duration-200">Thay đổi</button>

                  <button
                    class="px-3 py-1 bg-red-200 text-red-700 hover:bg-red-300 font-bold text-xs rounded-lg transition-all duration-200">Xóa</button>
                </div>
                <div v-else>
                  <button @click.prevent="openHospital(index)"
                    class="px-3 py-1 bg-blue-200 text-blue-700 hover:bg-blue-300 font-bold text-xs rounded-lg transition-all duration-200">Tìm trên bản đồ</button>
                </div>
              </div>
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
import PlaceList from './tab-content/PlaceList'
import HelpCircleIcon from 'vue-material-design-icons/HelpCircle'
import PlusIcon from 'vue-material-design-icons/Plus'

export default {
  components: {
    CheckIcon,
    AlertIcon,
    PlaceList,
    HelpCircleIcon,
    PlusIcon
  },

  props: {
    editMode: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      currentTab: 'places'
    }
  },

  computed: {
    places () {
      return this.$store.state.places
    },

    safePlaces () {
      return this.$store.getters.safePlaces
    },

    alarmPlaces () {
      return this.$store.getters.alarmPlaces
    },

    firePlaces () {
      return this.$store.getters.firePlaces
    },

    fireStations () {
      return this.$store.state.fireStations
    },

    hospitals () {
      return this.$store.state.hospitals
    },

    google () {
      return this.$store.state.mapsApi.google
    }
  },

  methods: {
    openHospital (index) {
      const marker = this.hospitals[index].marker
      this.google.maps.event.trigger(marker, 'click')
    },

    openFireStation (index) {
      const marker = this.fireStations[index].marker
      this.google.maps.event.trigger(marker, 'click')
    }
  }
}
</script>
