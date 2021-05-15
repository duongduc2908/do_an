<template>
  <div class="flex flex-wrap" style="padding: 24px 50px;">
      
    <!-- <div> -->
        <div v-for="(popupContent,index) in popup" :key="index" class="fit-content place-info bg-white shadow-lg rounded-lg overflow-hidden w-popup-place h-48 flex mr-2">
            <div class="w-48 h-full flex flex-col">
                <img  style="border-radius: 8px 0 0 8px;" class="location-image" alt="" v-if="popupContent.link_image" :src="popupContent.link_image">
            </div>

            <div style="background-color: #fff;border-radius: 0 8px 8px 0;">
                <div class="p-16" style="height: calc(100% - 40px);">
                <div class="align-items flex justify-between m-b-24">
                    <div>
                    {{ popupContent.name }}
                    </div>
                    <!-- <button class="text-xs uppercase px-3 py-1 text-blue-700 hover:bg-blue-200 transition-all duration-200 font-bold rounded-lg">Liên hệ</button> -->
                </div>

                <div class="mb-1 align-items flex items-center">
                    <CheckIcon class="mr-1 block text-green-600" />
                    <span class="text-green-800"> camera vận hành bình thường</span>
                    <!-- <span class="text-green-800">{{ cameras.length }}/{{ cameras.length }} camera vận hành bình thường</span> -->
                </div>
                </div>

                <div @click="popupContent.isActive=!popupContent.isActive;$store.dispatch(`camera/actionCamera`, popupContent)"
                class="cursor tags-view-item tags-view-item-active m-b-16 f-right" :class="{ 'tags-view-item-unactive' : !popupContent.isActive }">
                {{popupContent.isActive ? 'Kích hoạt' : 'Huy kích hoạt'}}
                </div>
            </div>
        </div>
    <!-- </div> -->

  </div>
</template>

<script>
import CheckIcon from 'vue-material-design-icons/Check'
// import AlertIcon from 'vue-material-design-icons/Alert'
// import HelpCircleIcon from 'vue-material-design-icons/HelpCircle'

export default {
  components: {
    CheckIcon
    // AlertIcon,
    // HelpCircleIcon
  },

  data () {
    return {
        popup:[
        {
            "_id" : "5f071ebe052953705061952d",
            "instruction" : "Đi qua cổng trước Chung cư",
            "link_image" : "https://icdn.dantri.com.vn/zoom/1200_630/2019/09/30/dh-dien-luc-1569809433913.jpg",
            "link_stream" : "rtsp://localhost:8554/test",
            "name" : "Camera sảnh C",
            "name_image" : "dh-dien-luc-1569809433913.jpg",
            "create_date" : "",
            "create_by" : "",
            "isActive":false
        },
        {
            "_id" : "5f071ebe052953705061952d",
            "instruction" : "Đi qua cổng trước Chung cư",
            "link_image" : "https://icdn.dantri.com.vn/zoom/1200_630/2019/09/30/dh-dien-luc-1569809433913.jpg",
            "link_stream" : "rtsp://localhost:8554/test",
            "name" : "Camera sảnh C",
            "name_image" : "dh-dien-luc-1569809433913.jpg",
            "create_date" : "",
            "create_by" : "",
            "isActive":true
        },
        {
            "_id" : "5f071ebe052953705061952d",
            "instruction" : "Đi qua cổng trước Chung cư",
            "link_image" : "https://icdn.dantri.com.vn/zoom/1200_630/2019/09/30/dh-dien-luc-1569809433913.jpg",
            "link_stream" : "rtsp://localhost:8554/test",
            "name" : "Camera sảnh C",
            "name_image" : "dh-dien-luc-1569809433913.jpg",
            "create_date" : "",
            "create_by" : "",
            "isActive":true
        },
        {
            "_id" : "5f071ebe052953705061952d",
            "instruction" : "Đi qua cổng trước Chung cư",
            "link_image" : "https://icdn.dantri.com.vn/zoom/1200_630/2019/09/30/dh-dien-luc-1569809433913.jpg",
            "link_stream" : "rtsp://localhost:8554/test",
            "name" : "Camera sảnh C",
            "name_image" : "dh-dien-luc-1569809433913.jpg",
            "create_date" : "",
            "create_by" : "",
            "isActive":true
        },
        {
            "_id" : "5f071ebe052953705061952d",
            "instruction" : "Đi qua cổng trước Chung cư",
            "link_image" : "https://icdn.dantri.com.vn/zoom/1200_630/2019/09/30/dh-dien-luc-1569809433913.jpg",
            "link_stream" : "rtsp://localhost:8554/test",
            "name" : "Camera sảnh C",
            "name_image" : "dh-dien-luc-1569809433913.jpg",
            "create_date" : "",
            "create_by" : "",
            "isActive":true
        }
        ],
        cameraList: false,
    }
  },


  methods: {
  }
}
</script>

<style lang="scss" scoped>
.place-info{
    // box-shadow: 3px 3px 3px grey;
    border-radius: 8px;
    margin: 0 24px 24px 0;
}
.location-image{
    width: 192px;
    height: 192px;
}
.tags-view-item {
    .el-icon-close {
      width: 16px;
      height: 16px;
      vertical-align: 2px;
      border-radius: 50%;
      text-align: center;
      transition: all .3s cubic-bezier(.645, .045, .355, 1);
      transform-origin: 100% 50%;
      &:before {
        transform: scale(.6);
        display: inline-block;
        vertical-align: -3px;
      }
      &:hover {
        background-color: #b4bccc;
        color: #fff;
      }
    }
  }

.tags-view-item-active{
    background-color: #42b983;
    color: #fff;
    border-color: #42b983;
    padding: 8px;
    border-radius: 4px;
    font-size: 13px;
  }
  .tags-view-item-unactive{
    background-color: #ef4d4d !important;
    border-color: #ef4d4d !important;
  }
</style>