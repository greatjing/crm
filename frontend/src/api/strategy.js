import axios from 'axios'

const baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL,
  timeout: 5000
})

export const strategyApi = {
  // 获取策略列表
  getStrategies() {
    return api.get('/api/strategies')
  },

  // 获取单个策略
  getStrategy(id) {
    return api.get(`/api/strategies/${id}`)
  },

  // 创建策略
  createStrategy(data) {
    return api.post('/api/strategies', data)
  },

  // 更新策略
  updateStrategy(id, data) {
    return api.put(`/api/strategies/${id}`, data)
  },

  // 删除策略
  deleteStrategy(id) {
    return api.delete(`/api/strategies/${id}`)
  },

  // 运行策略测试
  runStrategyTest(id, testData) {
    return api.post(`/api/strategies/${id}/test`, testData)
  }
} 