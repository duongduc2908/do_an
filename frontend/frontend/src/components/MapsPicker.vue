<template>
  <div class="relative">
    <div ref="map" id="map" class="w-full h-full"></div>
    <form @submit.prevent.stop="doSearch" class="absolute top-0 left-0 w-full flex justify-center">
      <div class="relative w-2/3 z-10">
        <input v-model="keyword" class="shadow-lg bg-white p-2 m-4 w-full rounded-lg focus:outline-shadow placeholder:text-gray-600" placeholder="Tìm kiếm vị trí...">
        <!-- <div class="absolute bottom-0 left-0 w-full rounded-lg overflow-hidden transform translate-y-12">
             <a href="#" class="w-full p-3 bg-white hover:bg-gray-100" v-for="(suggest, index) in suggests" :key="index">{{ suggest.formatted_address }}</a>
             </div> -->
      </div>
    </form>
  </div>
</template>

<script>
import { gmapsInit } from '@/utils/gmaps'

export default {
  data () {
    return {
      google: null,
      map: null,
      geocoder: null,
      marker: null,
      keyword: '',
      suggests: []
    }
  },

  props: {
    location: {
      type: Object,
      default: null
    }
  },

  async mounted () {
    const google = await gmapsInit()
    const map = new google.maps.Map(this.$refs.map, {
      disableDefaultUI: true
    })
    const geocoder = new google.maps.Geocoder()

    this.google = google
    this.map = map
    this.geocoder = geocoder

    geocoder.geocode({ address: 'Ha Noi' }, (results, status) => {
      if (status !== 'OK' || !results[0]) {
        throw new Error(status)
      }

      map.setCenter(results[0].geometry.location)
      map.fitBounds(results[0].geometry.viewport)
    })

    this.placeMarker()

    this.map.addListener('click', (event) => {
      this.changeMarker(event.latLng)
    })
  },

  methods: {
    doSuggest () {
      this.geocoder.geocode({ address: this.keyword }, (results, status) => {
        if (status !== 'OK' || !results[0]) {
          throw new Error(status)
        }
        if (results.length > 0) {
          this.suggests = results
        }
      })
    },

    doSearch () {
      this.geocoder.geocode({ address: this.keyword }, (results, status) => {
        if (status !== 'OK' || !results[0]) {
          throw new Error(status)
        }
        if (results.length > 0) {
          this.changeMarker(results[0].geometry.location)
        }
      })
    },

    changeMarker (latLng) {
      if (this.marker) {
        this.removeMarker()
      }

      const marker = new this.google.maps.Marker({
        position: latLng,
        map: this.map
      })

      this.map.panTo(latLng)
      this.map.setZoom(16)

      this.marker = marker

      this.$emit('locationChanged', {
        lat: latLng.lat(),
        lng: latLng.lng()
      })
    },

    removeMarker () {
      this.marker.setMap(null)
      this.marker = null
    },

    placeMarker () {
      if (this.location && this.location.lat && this.location.lng) {
        const marker = new this.google.maps.Marker({
          position: { lat: this.location.lat, lng: this.location.lng },
          map: this.map
        })

        this.marker = marker
      } else {
        if (this.marker) {
          this.removeMarker()
        }
      }
    }
  },

  watch: {
    location (to, from) {
      if (to.lat !== from.lat || to.lng !== from.lng) {
        this.placeMarker()
      }
    }
  }
}
</script>
