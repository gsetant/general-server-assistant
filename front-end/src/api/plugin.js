import request from '@/utils/request'

export function getPluginInfos(pluginNames,lang) {
  return request({
    url: '/plugin/info',
    method: 'get',
    params: {pluginNames,lang}
  })
}

export function getPluginInfo(pluginName,lang) {
  return request({
    url: '/plugin/info/'+ lang +'/' + pluginName ,
    method: 'get',
  })
}

export function getPluginSetting(pluginName,lang) {
  return request({
    url: '/plugin/setting/'+ lang +'/' + pluginName ,
    method: 'get',
  })
}

export function savePluginSetting(pluginName, data) {
  return request({
    url: '/plugin/setting/' + pluginName ,
    method: 'post',
    data
  })
}

export function getAllPluginInfo(language) {
  return request({
    url: '/setting/plugin/'+language,
    method: 'get',
  })
}


export function installPlugin(data) {
  return request({
    url: '/setting/plugin/install',
    method: 'post',
    data
  })
}

export function deletePlugin(data) {
  return request({
    url: '/setting/plugin/delete',
    method: 'post',
    data
  })
}


export function getPluginVersions(data) {
  return request({
    url: '/setting/plugin/version' ,
    method: 'post',
    data
  })
}

export function updatePlugin(data) {
  return request({
    url: '/setting/plugin/update',
    method: 'post',
    data
  })
}
