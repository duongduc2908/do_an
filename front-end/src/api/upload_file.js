import request from '@/utils/request'

export function remove_img(img_path) {
  return request({
    url: 'file/remove_train',
    method: 'delete',
    data: img_path
  })
}
export function add_file( files) {
  debugger
  let formData = new FormData();
  formData.append('file', files.file);
  return request({
    url: 'file/upload_train',
    method: 'post',
    data: formData
  })
}
