<template>
  <div class="home flex h-screen">
    <div class="w-24 bg-blue-700 flex flex-col items-center justify-between">
      <div class="flex flex-col w-16 h-16 p-2">
        <button class="opacity-80">
          <img class="w-full h-full rounded-full" src="@/assets/img/avatar.png" alt="">
        </button>
      </div>

      <div class="flex flex-col">
        <router-link class="p-3 m-2 rounded-lg hover:bg-blue-500 focus:outline-none"
          :class="{
            'bg-blue-600 text-white': $route.name === 'Home',
            'bg-blue-700 text-blue-200': $route.name !== 'Home'
            }"
          :to="{ name: 'Home' }"
        >
          <MapIcon :size="32" />
        </router-link>
        <router-link class="p-3 m-2 rounded-lg hover:bg-blue-500 focus:outline-none"
          :class="{
            'bg-blue-600 text-white': $route.name === 'Manage',
            'bg-blue-700 text-blue-200': $route.name !== 'Manage'
            }"
          :to="{ name: 'Manage' }"
        >
          <PencilBoxMultipleIcon :size="32" />
        </router-link>
        <button class="p-3 m-2 rounded-lg bg-blue-700 hover:bg-blue-500 focus:outline-none text-blue-200">
          <HistoryIcon :size="32" />
        </button>
      </div>

      <div></div>
    </div>

    <keep-alive>
      <router-view />
    </keep-alive>
  </div>
</template>

<script>
import MapIcon from 'vue-material-design-icons/Map'
import PencilBoxMultipleIcon from 'vue-material-design-icons/PencilBoxMultiple'
import HistoryIcon from 'vue-material-design-icons/History'

export default {
  name: 'Home',

  components: {
    MapIcon,
    PencilBoxMultipleIcon,
    HistoryIcon
  },

  data () {
    return {
      sidebarShow: true
    }
  },

  mounted () {
    // setTimeout(() => {
    //   this.$store.commit('setAlarm', { index: 3 })
    // }, 10000)
  }
}
</script>
