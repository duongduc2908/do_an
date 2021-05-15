import request from '@/utils/request'

export function actionCamera(param) {
  return request({
    url: `http://localhost:4321/api/stream/connection_api/${!param.isActive ? "connect" : "disconnect"}?camera_id=${param._id}${ !param.isActive ? `&rtsp_link=${param.link_stream}&username&password&selectedProtocol=1`  : ""}`,
    method: 'get',
    data: param
  })
}

