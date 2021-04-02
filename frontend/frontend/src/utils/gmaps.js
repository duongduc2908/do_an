const API_KEY = 'AIzaSyBFkVAiXK4xUSXMqt6QKw7Isplc2jn7w2Y'
const CALLBACK_NAME = 'gmapsCallback'

let initialized = !!window.google
let resolveInitPromise
let rejectInitPromise

// This promise handles the initialization
// status of the google maps script.
const initPromise = new Promise((resolve, reject) => {
  resolveInitPromise = resolve
  rejectInitPromise = reject
})

export function gmapsInit () {
  // If Google Maps already is initialized
  // the `initPromise` should get resolved
  // eventually.
  if (initialized) return initPromise

  initialized = true
  // The callback function is called by
  // the Google Maps script if it is
  // successfully loaded.
  window[CALLBACK_NAME] = () => resolveInitPromise(window.google)

  // We inject a new script tag into
  // the `<head>` of our HTML to load
  // the Google Maps script.
  const script = document.createElement('script')
  script.async = true
  script.defer = true
  script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}&callback=${CALLBACK_NAME}`
  script.onerror = rejectInitPromise
  document.querySelector('head').appendChild(script)

  return initPromise
}

/**
 * Returns the Popup class.
 *
 * Unfortunately, the Popup class can only be defined after
 * google.maps.OverlayView is defined, when the Maps API is loaded.
 * This function should be called by initMap.
 */
export function createPopupClass (google) {
  /**
   * A customized popup on the map.
   * @param {!google.maps.LatLng} position
   * @param {!Element} content The bubble div.
   * @constructor
   * @extends {google.maps.OverlayView}
   */
  function Popup (position, content) {
    this.position = position

    content.classList.add('popup-bubble')

    // This zero-height div is positioned at the bottom of the bubble.
    var bubbleAnchor = document.createElement('div')
    bubbleAnchor.classList.add('popup-bubble-anchor')
    bubbleAnchor.appendChild(content)

    // This zero-height div is positioned at the bottom of the tip.
    this.containerDiv = document.createElement('div')
    this.containerDiv.classList.add('popup-container')
    this.containerDiv.appendChild(bubbleAnchor)

    // Optionally stop clicks, etc., from bubbling up to the map.
    google.maps.OverlayView.preventMapHitsAndGesturesFrom(this.containerDiv)
  }
  // ES5 magic to extend google.maps.OverlayView.
  Popup.prototype = Object.create(google.maps.OverlayView.prototype)

  /** Called when the popup is added to the map. */
  Popup.prototype.onAdd = function () {
    this.getPanes().floatPane.appendChild(this.containerDiv)
  }

  /** Called when the popup is removed from the map. */
  Popup.prototype.onRemove = function () {
    if (this.containerDiv.parentElement) {
      this.containerDiv.parentElement.removeChild(this.containerDiv)
    }
  }

  /** Called each frame when the popup needs to draw itself. */
  Popup.prototype.draw = function () {
    var divPosition = this.getProjection().fromLatLngToDivPixel(this.position)

    // Hide the popup when it is far out of view.
    var display =
        Math.abs(divPosition.x) < 4000 && Math.abs(divPosition.y) < 4000 ? 'block' : 'none'

    if (display === 'block') {
      this.containerDiv.style.left = divPosition.x + 'px'
      this.containerDiv.style.top = divPosition.y + 'px'
    }
    if (this.containerDiv.style.display !== display) {
      this.containerDiv.style.display = display
    }
  }

  return Popup
}
