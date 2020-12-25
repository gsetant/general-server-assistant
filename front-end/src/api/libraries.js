import request from '@/utils/request'

export function getLibrariesSettings() {
  return request({
    url: '/libraries/settings',
    method: 'get',
  })
}

export function saveLibrariesSetting(data) {
  return request({
    url: '/libraries/settings',
    method: 'post',
    data
  })
}



export function librariesDetail(data) {
  return request({
    url: '/libraries/detail',
    method: 'post',
    data
  })
}

export function delLibrariesSetting(data) {
  return request({
    url: '/libraries/settings/del',
    method: 'post',
    data
  })
}
