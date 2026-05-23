import axios from 'axios'

// Axios 实例配置
// 预留：后端 API 基础 URL
const apiClient = axios.create({
  baseURL: '', // 待填充：后端 API 地址
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 预留：添加认证 token
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => response.data,
  error => {
    // 统一错误处理
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default apiClient
