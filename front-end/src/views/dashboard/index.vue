<template>
  <div class="dashboard-container">
    <component :is="currentRole" />
    <dropzone />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import adminDashboard from './admin'
import editorDashboard from './editor'
import dropzone from '@/views/components-demo/dropzone'

export default {
  name: 'Dashboard',
  components: { adminDashboard, editorDashboard ,dropzone},
  data() {
    return {
      currentRole: 'adminDashboard'
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    debugger
    if (!this.roles.includes('admin')) {
      this.currentRole = 'editorDashboard'
    }
  }
}
</script>
