import request from "@/utils/request";

export function manualScan(data) {
  return request({
    url: '/scan/manual'  ,
    method: 'post',
    data
  })
}
