import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/user/info',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'get'
  })
}

export function updateUser(data) {
  return request({
    url: '/user',
    method: 'post',
    data
  })
}

export function generateToken() {
  return request({
    url: '/user/token',
    method: 'post'
  })
}

export function getAllUserInfo() {
  return request({
    url: '/setting/user/all',
    method: 'get'
  })
}
