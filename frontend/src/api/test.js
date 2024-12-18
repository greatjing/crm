import axios from 'axios'

const baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL,
  timeout: 5000
})

export const testApi = {
  // 生成测试数据
  generateTestData(config) {
    return api.post('/api/tests/generate-data', config)
  },

  // 创建测试批次
  createTestBatch(data) {
    return api.post('/api/tests/batches', data)
  },

  // 获取测试批次信息
  getTestBatch(id) {
    return api.get(`/api/tests/batches/${id}`)
  },

  // 获取测试报告
  getTestReport(id) {
    return api.get(`/api/tests/batches/${id}/report`)
  }
} 