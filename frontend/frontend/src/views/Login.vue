<template>
  <div class="relative h-screen w-screen">
    <video class="absolute top-0 left-0 w-full h-full" style="object-fit: cover; filter: brightness(60%)" src="@/assets/intro.mp4" autoplay muted loop></video>

    <div class="z-10 absolute top-0 left-0 w-full h-full flex justify-center">
      <div class="flex flex-col p-12 h-auto">
        <div class="relative flex flex-col items-center bg-white rounded-md" style="width: 480px;">
          <img class="absolute top-0 left-0 select-none" src="@/assets/img/pattern.png" style="filter: hue-rotate(120deg)">
          <img src="@/assets/img/logo.gif" class="z-10 w-64 my-6">
          <div class="z-10 text-center text-sm w-2/3 text-gray-500 mb-6">Nhập tên đăng nhập và mật khẩu của bạn để truy cập vào trang quản trị.</div>
          <form @submit.prevent="handleSubmit" class="pt-6 px-6 w-full z-10">
            <div class="mb-6">
              <label class="text-sm text-gray-700 font-bold mb-2 block" for="username">Tên đăng nhâp</label>
              <input
                v-model="username"
                id="username"
                class="px-4 py-2 w-full placeholder:text-gray-600 text-gray-800 rounded-md transition-all duration-200
                border border-orange-400 focus:outline-none"
                type="text"
              >
            </div>
            <div class="mb-6">
              <label class="text-sm text-gray-700 font-bold mb-2 block" for="password">Mật khẩu</label>
              <input
                v-model="password"
                id="password"
                class="px-4 py-2 w-full placeholder:text-gray-600 text-gray-800 rounded-md transition-all duration-200
                border border-orange-400 focus:outline-none"
                type="password"
              >
            </div>
            <div class="flex justify-center mb-1">
              <button
                class="px-6 py-2 w-full text-sm focus:outline-none focus:shadow-outline rounded-md transition-all duration-200 mb-6"
                :class="{ 'bg-gray-400 text-gray-600': logining, 'bg-orange-700 hover:bg-orange-800 text-white': !logining }"
              >
                <template v-if="logining">
                  Đang đăng nhập
                </template>

                <template v-else>
                  Đăng nhập
                </template>
              </button>
            </div>
          </form>

          <div class="text-center text-sm text-gray-500 mb-2"><a href="#">Quên mật khẩu?</a></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: '',
      logining: false
    }
  },

  methods: {
    async handleSubmit () {
      try {
        this.logining = true
        await this.$store.dispatch('doLogin', { username: this.username, password: this.password })
        this.$router.push({ name: 'Home' })
        console.log('hi')
      } catch (error) {
        console.log(error)
      } finally {
        this.logining = false
      }
    }
  }
}
</script>
