<template>
  <div class="flex flex-grow">
    <SideBar
      class="bg-gray-100 transition-all duration-500"
      :class="{
        'opacity-0 w-0': !sidebarShow,
        'opacity-100 w-sidebar': sidebarShow
        }" />

    <GoogleMaps class="flex-grow shadow-lg w-full h-full" />
  </div>
</template>

<script>
import GoogleMaps from '@/components/GoogleMaps.vue'
import SideBar from '@/components/SideBar'
// import ExpandIcon from 'vue-material-design-icons/ChevronRight'
// import CollapseIcon from 'vue-material-design-icons/ChevronLeft'

export default {
  name: 'Home',

  components: {
    GoogleMaps,
    SideBar
    // ExpandIcon,
    // CollapseIcon
  },

  data () {
    return {
      sidebarShow: true
    }
  }
}
</script>
