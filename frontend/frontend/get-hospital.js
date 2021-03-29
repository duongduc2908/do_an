const axios = require('axios')

async function exe () {
  const res = await axios.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=21.0456457,105.7924969&radius=50000&type=fire-station&keyword=tram%20cuu%20hoa&key=AIzaSyDDfaJaPHE80oCA_zN_k2EfnYrr27zEPmQ')
  const data = res.data
  const markers = data.results.map(m => {
    const hospital = {
      location: m.geometry.location,
      name: m.name
    }
    if (m.photos) {
      const photoRef = m.photos[0].photo_reference
      hospital.photo = `https://maps.googleapis.com/maps/api/place/photo?photoreference=${photoRef}&sensor=false&maxheight=500&maxwidth=500&key=AIzaSyDDfaJaPHE80oCA_zN_k2EfnYrr27zEPmQ`
    }
    return hospital
  })
  console.log(markers)
}

exe()
