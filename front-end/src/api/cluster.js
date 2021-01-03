import request from '@/utils/request'

export function getNodeInfo() {
  return request({
    url: '/cluster/node',
    method: 'get',
  })
}

export function saveNodeInfo(data) {
  return request({
    url: '/cluster/node',
    method: 'post',
    data
  })
}
