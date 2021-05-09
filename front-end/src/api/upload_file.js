import request from '@/utils/request'

export function remove_img(img_path) {
  return request({
    url: 'file/remove_train',
    method: 'delete',
    data: img_path
  })
}
