import { remove_img } from '@/api/upload_file'


const actions = {
  remove_img(path) {
    return new Promise((resolve, reject) => {
        remove_img({ file_path: path.trim() }).then(response => {
        const { data } = response
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

export default {
  actions
}
