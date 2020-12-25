import request from "@/utils/request";

export function getPluginLogFull(pluginName) {
  return request({
    url: '/log/plugin/' + pluginName ,
    method: 'get',
  })
}

export function getPluginNewLog(pluginName, lineNumber) {
  return request({
    url: '/log/new/plugin/' + pluginName + '/' + lineNumber,
    method: 'get',
  })
}


export function getAdminLogFull() {
  return request({
    url: '/log/admin',
    method: 'get',
  })
}

export function getAdminNewLog(lineNumber) {
  return request({
    url: '/log/new/admin/' + lineNumber,
    method: 'get',
  })
}
