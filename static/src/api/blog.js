import request from '../utils/request'

export function fetchList(query) {
  return request({
    url: '/blog',
    method: 'get',
    params: query
  })
}

export function fetchBlog(id) {
  return request({
    url: `/blog/${id}`,
    method: 'get'
  })
}

export function createBlog(data) {
  return request({
    url: '/blog',
    method: 'post',
    data
  })
}

export function updateBlog(data) {
  return request({
    url: `/blog/${data.id}`,
    method: 'put',
    data
  })
}

export function deleteBlog(id) {
  return request({
    url: `/blog/${id}`,
    method: 'delete'
  })
}

