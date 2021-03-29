<template>
  <div class="">
    <div ref="map" id="map" class="w-full h-full"></div>

    <div ref="popup" class="hidden mb-8 transition-all duration-500 overflow-hidden">
      <PopupCamera v-if="popupContent && popupContent.category === 'place'" @startStream="startStream" :popupContent="popupContent" />
      <PopupHospital class="w-popup h-48" v-if="popupContent && popupContent.category === 'hospital'" :popupContent="popupContent" />
      <PopupFireStation class="w-popup h-48" v-if="popupContent && popupContent.category === 'fire-station'" :popupContent="popupContent" />
    </div>

    <StreamModal v-if="showStreamModal" @closeModal="showStreamModal = false" :camera="streamingCamera" :place="streamingPlace" :url="streamImageUrl"
      :box="streamFireBox" />
  </div>
</template>

<script>
/* eslint-disable */

import PopupCamera from './PopupCamera'
import PopupHospital from './PopupHospital'
import PopupFireStation from './PopupFireStation'
import CheckIcon from 'vue-material-design-icons/Check'
import { createPopupClass } from '@/utils/gmaps'
import StreamModal from './StreamModal'
import io from 'socket.io-client'
import throttle from 'lodash.throttle'

export default {
  components: {
    CheckIcon,
    PopupCamera,
    PopupHospital,
    PopupFireStation,
    StreamModal
  },

  props: {
    editMode: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      markers: [],
      Popup: null,
      popup: null,
      popupContent: {
        name: '',
        type: null,
        photo: '',
        marker: null
      },
      showStreamModal: false,
      streamingCamera: null,
      streamingPlace: null,
      socket: null,
      streamImageUrl: null,
      streamFireBox: null
    }
  },

  computed: {
    places () {
      return this.$store.state.places
    },

    hospitals () {
      return this.$store.state.hospitals
    },

    fireStations () {
      return this.$store.state.fireStations
    },

    google () {
      return this.$store.state.mapsApi.google
    },

    gmaps () {
      return this.$store.state.mapsApi.map
    },

    geocoder () {
      return this.$store.state.mapsApi.geocoder
    }
  },

  async mounted () {
    try {
      const element = this.$refs.map

      await this.$store.dispatch('initMap', { element })
      await this.$store.dispatch('loadHospitals')
      await this.$store.dispatch('loadPlaces')
      await this.$store.dispatch('loadFireStations')

      this.Popup = createPopupClass(this.google)

      this.addMarkerEvents()
      this.hideStyles()
      // this.getDirection()
      this.startSocket()

      this.google.maps.event.addListener(this.gmaps, 'click', (event) => {
        this.removePopup()
      })
    } catch (error) {
      console.error(error)
    }
  },

  methods: {
    startSocket () {
      const socket = io('http://27.72.147.222:8888')

      const func = throttle((obj) => {
        const bytes = new Uint8Array(obj.buffer)
        const boxes = obj.boxes

        if (boxes.length > 0) {
          // const place = this.places[0]
          // console.log(place)
          // const camera = place.cameras.find(camera => camera.activated === true)
          console.log(obj.place_id, obj.camera_id)
          this.$store.commit('setAlarm', { placeId: obj.place_id, cameraId: obj.camera_id })

          this.streamFireBox = obj.boxes
        } else {
          this.streamFireBox = null
        }

        let binary = ''
        const len = bytes.byteLength
        for (let i = 0; i < len; i++) {
          binary += String.fromCharCode(bytes[i])
        }
        this.streamImageUrl  = 'data:image/jpeg;base64,' + window.btoa(binary)
        //
        //         this.streamImageUrl = URL.createObjectURL(new Blob(bytes, {type : 'image/jpeg' }))
        //
      }, 600)

      socket.on('imageConversionByClient', func)

      this.socket = socket
    },

    startStream (placeId, cameraId) {
      this.showStreamModal = true

      const place = this.places.find(p => p._id === placeId)
      const camera = place.cameras.find(c => c.camera_id === cameraId)

      this.streamingCamera = camera
      this.streamingPlace = place
    },

    createPopup (obj) {
      this.popup = new this.Popup(
        new this.google.maps.LatLng(obj.location.lat, obj.location.lng),
        this.$refs.popup
      )
      this.popup.setMap(this.gmaps)
      this.popupContent = obj
    },

    removePopup () {
      this.popup.setMap(null)
      this.popupContent = null
    },

    hideStyles () {
      const styles = {
        hide: [
          {
            featureType: 'poi',
            stylers: [{visibility: 'off'}]
          }
        ]
      }

      this.gmaps.setOptions({styles: styles['hide']})
    },

    addMarkerEvents () {
      this.addHospitalEvents()
      this.addPlaceEvents()
      this.addFireStationEvents()
    },

    addPlaceEvents () {
      this.places.forEach(place => {
        place.marker.addListener('click', () => {
          this.popupContent = null
          this.gmaps.panTo(place.marker.getPosition())
          this.createPopup(place)
        })
      })
    },

    addHospitalEvents () {
      this.hospitals.forEach(hospital => {
        hospital.marker.addListener('click', () => {
          this.popupContent = null
          this.gmaps.panTo(hospital.marker.getPosition())
          this.createPopup(hospital)
        })
      })
    },

    addFireStationEvents () {
      this.fireStations.forEach(fireStation => {
        fireStation.marker.addListener('click', () => {
          this.popupContent = null
          this.gmaps.panTo(fireStation.marker.getPosition())
          this.createPopup(fireStation)
        })
      })
    },

    getDirection () {
      var directionsService = new this.google.maps.DirectionsService()
      var directionsRenderer = new this.google.maps.DirectionsRenderer()
      directionsRenderer.setMap(this.gmaps)

      directionsService.route(
        {
          origin: new google.maps.LatLng(hospitals[0].location),
          destination: new google.maps.LatLng(hospitals[1].location),
          travelMode: 'DRIVING'
        },
        function(response, status) {
          if (status === 'OK') {
            directionsRenderer.setDirections(response)
          } else {
            window.alert('Directions request failed due to ' + status)
          }
      })
    }
  }
}
</script>

<style>
.popup-bubble {
  @apply absolute flex top-0 left-0 overflow-y-auto;
  /* Position the bubble centred-above its parent. */
  transform: translate(-50%, -100%);
}

.popup-container {
  @apply absolute cursor-auto h-0 w-64;
  margin-top: -48px;
}

.location-image {
  object-fit: cover;
}
</style>
