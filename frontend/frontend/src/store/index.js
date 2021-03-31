import Vue from 'vue'
import Vuex from 'vuex'
import axios from '@/apis/axios'
import { gmapsInit } from '@/utils/gmaps'

import hospitals from '@/data/hospitals'
// import places from '@/data/cameras'
import fireStations from '@/data/fire-stations'
import { v4 as uuidv4 } from 'uuid'

Vue.use(Vuex)

const BASE_URL = 'localhost:4321/api/v1'

const getMarkerImage = (type) => {
  switch (type) {
    case 'place':
      return require('@/assets/img/camera-green.png')
    case 'hospital':
      return require('@/assets/img/hospital-box.png')
    case 'fire-station':
      return require('@/assets/img/fire-hydrant.png')
    default:
      throw new Error('Cannot find an icon for this type of marker.')
  }
}

const addMarker = (object, type, google, map) => {
  const marker = new google.maps.Marker({
    position: { lat: object.location.lat, lng: object.location.lng },
    icon: getMarkerImage(type),
    map: map,
    title: object.name
  })
  object.marker = marker
}

export default new Vuex.Store({
  state: {
    mapsApi: {
      map: null,
      google: null,
      geocoder: null,
      directionsRenderer: null
    },
    auth: null,
    hospitals: [],
    places: [],
    fireStations: []
  },

  getters: {
    safePlaces (state) {
      return state.places.filter(place => {
        return place.status === 'safe'
      })
    },

    alarmPlaces (state) {
      return state.places.filter(place => {
        return place.status === 'warn' || place.status === 'fire'
      })
    },

    warnPlaces (state) {
      return state.places.filter(place => {
        return place.status === 'warn'
      })
    },

    firePlaces (state) {
      return state.places.filter(place => {
        return place.status === 'fire'
      })
    },

    places (state) {
      return state.places
    }
  },

  mutations: {
    setMapsApi (state, payload) {
      state.mapsApi = payload
      // state.mapsApi.map = payload.map
      // state.mapsApi.google = payload.google
      // state.mapsApi.geocoder = payload.geocoder
      // state.mapsApi.directionsRenderer = payload.directionsRenderer
    },

    addHospital (state, payload) {
      state.hospitals.push(payload.hospital)
    },

    addPlace (state, payload) {
      state.places.push(payload.place)
    },

    clearPlaces (state) {
      state.places = []
    },

    addFireStation (state, payload) {
      state.fireStations.push(payload.fireStation)
    },

    setCameraActivated (state, payload) {
      const place = state.places.find(p => p._id === payload.placeId)
      const camera = place.cameras.find(c => c.camera_id === payload.cameraId)

      camera.activated = true
    },

    setCameraDeactivated (state, payload) {
      const place = state.places.find(p => p._id === payload.placeId)
      const camera = place.cameras.find(c => c.camera_id === payload.cameraId)

      camera.activated = false
    },

    setAlarm (state, payload) {
      const place = state.places.find(p => p._id === payload.placeId)
      const camera = place.cameras.find(c => c.camera_id === payload.cameraId)

      if (place.status === 'warn' || place.status === 'fire') {
        return
      }

      place.status = 'warn'
      place.marker.setIcon(require('@/assets/img/camera-yellow.png'))

      camera.status = 'warn'

      state.mapsApi.google.maps.event.trigger(place.marker, 'click')
      this._vm.toast.warning(`Có phát hiện đám cháy tại ${place.name}.`, 'Chú ý', {
        position: 'topCenter',
        timeout: 10000
      })
    },

    setAlarmConfirmed (state, payload) {
      const place = state.places.find(p => p._id === payload.id)
      place.status = 'fire'
      place.marker.setIcon(require('@/assets/img/fire-red.png'))
    },

    dismissAlarm (state, payload) {
      // TODO convert to action and send request to dismiss alarm too
      const place = state.places.find(p => p._id === payload.id)
      place.status = 'safe'
      place.cameras.map(c => {
        c.status = 'safe'
        return c
      })
      place.marker.setIcon(require('@/assets/img/camera-green.png'))
    },

    setBestFireStationRoute (state, payload) {
      const place = state.places.find(p => p._id === payload.placeId)

      place.bestFireStationRoute = {
        fireStationId: payload.fireStationId,
        distance: payload.distance,
        duration: payload.duration
      }
    },

    setAuth (state, payload) {
      state.auth = payload
    }
  },

  actions: {
    async initMap (context, payload) {
      const google = await gmapsInit()
      const geocoder = new google.maps.Geocoder()
      const map = new google.maps.Map(payload.element, {
        disableDefaultUI: true
      })

      const directionsRenderer = new google.maps.DirectionsRenderer()
      directionsRenderer.setMap(map)

      const trafficLayer = new google.maps.TrafficLayer()

      geocoder.geocode({ address: 'Ha Noi' }, (results, status) => {
        if (status !== 'OK' || !results[0]) {
          throw new Error(status)
        }

        map.setCenter(results[0].geometry.location)
        map.fitBounds(results[0].geometry.viewport)
      })

      context.commit('setMapsApi', {
        map,
        google,
        geocoder,
        directionsRenderer,
        trafficLayer
      })
    },

    async loadHospitals (context) {
      // const res = await axios(`${BASE_URL}/hospital/get_all_page_search?page_size=30&page_number=0`)
      // const hospitals = res.data.data.results
      hospitals.forEach(hospital => {
        hospital.category = 'hospital'
        hospital._id = uuidv4()
        addMarker(hospital, 'hospital', context.state.mapsApi.google, context.state.mapsApi.map)
        context.commit('addHospital', { hospital })
      })
    },

    async loadPlaces (context) {
      const oldPlaces = context.state.places
      oldPlaces.forEach(place => {
        place.marker.setMap(null)
      })
      context.commit('clearPlaces')

      const res = await axios(`${BASE_URL}/place/get_all_page_search?page_size=30&page_number=0`)
      const places = res.data.data.results
      places.forEach(place => {
        place.category = 'place'
        place.status = 'safe'
        place.bestFireStationRoute = null
        place.cameras.map(c => {
          c.activated = false
          c.status = 'safe'
          return c
        })
        addMarker(place, 'place', context.state.mapsApi.google, context.state.mapsApi.map)
        context.commit('addPlace', { place })
      })
    },

    async loadFireStations (context) {
      fireStations.forEach(fireStation => {
        fireStation.category = 'fire-station'
        fireStation._id = uuidv4()
        addMarker(fireStation, 'fire-station', context.state.mapsApi.google, context.state.mapsApi.map)
        context.commit('addFireStation', { fireStation })
      })
    },

    async confirmAlarm (context, payload) {
      context.commit('setAlarmConfirmed', { id: payload.id })
      await context.dispatch('findNearestFireStation', { placeId: payload.id })
    },

    async findNearestFireStation (context, payload) {
      const google = context.state.mapsApi.google
      const place = context.state.places.find(p => p._id === payload.placeId)

      const fireStations = context.state.fireStations

      const service = new google.maps.DistanceMatrixService()

      const placesLatLngArr = [new google.maps.LatLng(place.location.lat, place.location.lng)]
      const fireStationsLatLngArr = fireStations.map(fireStation => {
        return new google.maps.LatLng(fireStation.location.lat, fireStation.location.lng)
      })

      service.getDistanceMatrix(
        {
          origins: fireStationsLatLngArr,
          destinations: placesLatLngArr,
          travelMode: 'DRIVING'
        }, (response, status) => {
          if (status !== 'OK') {
            throw new Error('Cannot find nearest fire station right now.')
          }

          const rows = response.rows.map((r, index) => {
            r.fireStationId = fireStations[index]._id
            return r
          })

          const sortedRow = rows.sort((r1, r2) => r1.elements[0].duration.value - r2.elements[0].duration.value)

          const bestRow = sortedRow[0]

          const bestFireStation = context.state.fireStations.find(fireStation => fireStation._id === bestRow.fireStationId)

          context.commit('setBestFireStationRoute', {
            placeId: payload.placeId,
            fireStationId: bestFireStation._id,
            duration: bestRow.elements[0].duration.text,
            distance: bestRow.elements[0].distance.text
          })

          context.dispatch('getDirection', {
            placeId: payload.placeId,
            fireStationId: bestFireStation._id
          })
        }
      )
    },

    getDirection (context, payload) {
      const fireStation = context.state.fireStations.find(fireStation => fireStation._id === payload.fireStationId)
      const place = context.state.places.find(place => place._id === payload.placeId)

      const google = context.state.mapsApi.google
      // const map = context.state.mapsApi.map
      // const trafficLayer = context.state.mapsApi.trafficLayer
      const directionsRenderer = context.state.mapsApi.directionsRenderer
      const directionsService = new context.state.mapsApi.google.maps.DirectionsService()

      // trafficLayer.setMap(map)

      directionsService.route(
        {
          origin: new google.maps.LatLng(fireStation.location.lat, fireStation.location.lng),
          destination: new google.maps.LatLng(place.location.lat, place.location.lng),
          travelMode: 'DRIVING',
          drivingOptions: {
            departureTime: new Date(),
            trafficModel: 'bestguess'
          }
        },
        (response, status) => {
          if (status === 'OK') {
            directionsRenderer.setDirections(response)
          } else {
            window.alert('Directions request failed due to ' + status)
          }
        }
      )
    },

    async doLogin (context, payload) {
      const res = await axios.post(`${BASE_URL}/auth/login`, payload)
      localStorage.setItem('auth', JSON.stringify(res.data.data))
      context.commit('setAuth', res.data.data)
    },

    async activateCamera (context, payload) {
      context.commit('setCameraActivated', payload)
      try {
        await axios.get(`localhost:4321/api/stream/connection_api/connect?place_id=${payload.placeId}&camera_id=${payload.cameraId}&rtsp_link=${payload.rtspLink}&username&password&selectedProtocol=1`)
      } catch (error) {
        console.error(error)
      }
    },

    async deactivateCamera (context, payload) {
      context.commit('setCameraDeactivated', payload)
      try {
        await axios.get(`localhost:4321/api/stream/connection_api/disconnect?place_id=${payload.placeId}&camera_id=${payload.cameraId}`)
      } catch (error) {
        console.error(error)
      }
    }
  },

  modules: {
  }
})
