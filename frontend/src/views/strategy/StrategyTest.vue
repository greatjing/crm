<template>
  <div class="strategy-test">
    <div class="header">
      <h2>策略测试</h2>
    </div>

    <!-- 测试数据生成器 -->
    <el-card class="data-generator">
      <template #header>
        <div class="card-header">
          <span>测试数据生成器</span>
        </div>
      </template>
      
      <el-form :model="generatorConfig" label-width="120px">
        <el-form-item label="生成数量">
          <el-input-number v-model="generatorConfig.count" :min="1" :max="100" />
        </el-form-item>
        
        <el-form-item label="信用分数范围">
          <el-col :span="11">
            <el-input-number v-model="generatorConfig.data_patterns.credit_score.min" :min="300" :max="850" />
          </el-col>
          <el-col :span="2" class="text-center">-</el-col>
          <el-col :span="11">
            <el-input-number v-model="generatorConfig.data_patterns.credit_score.max" :min="300" :max="850" />
          </el-col>
        </el-form-item>
        
        <el-form-item label="贷款金额范围">
          <el-col :span="11">
            <el-input-number v-model="generatorConfig.data_patterns.loan_amount.min" :min="1000" :max="1000000" />
          </el-col>
          <el-col :span="2" class="text-center">-</el-col>
          <el-col :span="11">
            <el-input-number v-model="generatorConfig.data_patterns.loan_amount.max" :min="1000" :max="1000000" />
          </el-col>
        </el-form-item>
        
        <el-form-item label="年收入范围">
          <el-col :span="11">
            <el-input-number v-model="generatorConfig.data_patterns.annual_income.min" :min="10000" :max="1000000" />
          </el-col>
          <el-col :span="2" class="text-center">-</el-col>
          <el-col :span="11">
            <el-input-number v-model="generatorConfig.data_patterns.annual_income.max" :min="10000" :max="1000000" />
          </el-col>
        </el-form-item>
        
        <el-form-item label="包含边界值">
          <el-switch v-model="generatorConfig.include_edge_cases" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="generateData">生成测试数据</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 测试数据预览 -->
    <el-card v-if="testData.length > 0" class="data-preview">
      <template #header>
        <div class="card-header">
          <span>测试数据预览</span>
          <el-button type="primary" @click="runTests">运行测试</el-button>
        </div>
      </template>
      
      <el-table :data="testData" height="400" border>
        <el-table-column prop="input_data.credit_score" label="信用分数" width="120" />
        <el-table-column prop="input_data.loan_amount" label="贷款金额" width="120" />
        <el-table-column prop="input_data.annual_income" label="年收入" width="120" />
      </el-table>
    </el-card>

    <!-- 测试结果 -->
    <el-card v-if="currentBatchId" class="test-results">
      <template #header>
        <div class="card-header">
          <span>测试结果</span>
          <div>
            <el-tag :type="getBatchStatusType(batchStatus)">{{ getBatchStatusText(batchStatus) }}</el-tag>
            <el-button v-if="testReport" type="primary" class="ml-2" @click="exportReport">导出报告</el-button>
          </div>
        </div>
      </template>
      
      <div v-if="batchStatus === 'running'" class="loading-state">
        <el-icon class="is-loading"><Loading /></el-icon>
        <p>正在执行测试...</p>
      </div>

      <div v-else-if="testReport">
        <!-- 测试统计 -->
        <div class="statistics">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-card shadow="hover">
                <template #header>总用例数</template>
                <div class="statistic-value">{{ testReport.statistics.total_cases }}</div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card shadow="hover">
                <template #header>通过用例数</template>
                <div class="statistic-value success">{{ testReport.statistics.passed_cases }}</div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card shadow="hover">
                <template #header>失败用例数</template>
                <div class="statistic-value danger">{{ testReport.statistics.failed_cases }}</div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card shadow="hover">
                <template #header>错误用例数</template>
                <div class="statistic-value warning">{{ testReport.statistics.error_cases }}</div>
              </el-card>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" class="mt-4">
            <el-col :span="8">
              <el-card shadow="hover">
                <template #header>平均执行时间</template>
                <div class="statistic-value">{{ testReport.statistics.avg_execution_time.toFixed(2) }} ms</div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="hover">
                <template #header>最长执行时间</template>
                <div class="statistic-value">{{ testReport.statistics.max_execution_time }} ms</div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="hover">
                <template #header>最短执行时间</template>
                <div class="statistic-value">{{ testReport.statistics.min_execution_time }} ms</div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <!-- 图表展示 -->
        <div class="charts mt-4">
          <el-row :gutter="20">
            <el-col :span="8" v-if="testReport.charts_data.results_distribution">
              <el-card shadow="hover" class="chart-card">
                <template #header>测试结果分布</template>
                <img :src="'data:image/png;base64,' + testReport.charts_data.results_distribution" />
              </el-card>
            </el-col>
            <el-col :span="8" v-if="testReport.charts_data.risk_level_distribution">
              <el-card shadow="hover" class="chart-card">
                <template #header>风险等级分布</template>
                <img :src="'data:image/png;base64,' + testReport.charts_data.risk_level_distribution" />
              </el-card>
            </el-col>
            <el-col :span="8" v-if="testReport.charts_data.execution_time_distribution">
              <el-card shadow="hover" class="chart-card">
                <template #header>执行时间分布</template>
                <img :src="'data:image/png;base64,' + testReport.charts_data.execution_time_distribution" />
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <!-- 测试用例详情 -->
        <div class="test-cases mt-4">
          <el-card shadow="hover">
            <template #header>测试用例详情</template>
            <el-table :data="testReport.test_cases" border stripe>
              <el-table-column prop="status" label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="input_data" label="输入数据" width="300">
                <template #default="{ row }">
                  <pre>{{ JSON.stringify(row.input_data, null, 2) }}</pre>
                </template>
              </el-table-column>
              <el-table-column prop="actual_output" label="输出结果" width="300">
                <template #default="{ row }">
                  <pre v-if="row.actual_output">{{ JSON.stringify(row.actual_output, null, 2) }}</pre>
                </template>
              </el-table-column>
              <el-table-column prop="execution_time" label="执行时间" width="120">
                <template #default="{ row }">
                  {{ row.execution_time }} ms
                </template>
              </el-table-column>
              <el-table-column prop="error_message" label="错误信息" min-width="200">
                <template #default="{ row }">
                  <span class="error-message" v-if="row.error_message">{{ row.error_message }}</span>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { testApi } from '@/api/test'
// import { strategyApi } from '@/api/strategy'

const route = useRoute()
const strategyId = route.params.id

const generatorConfig = ref({
  count: 10,
  data_patterns: {
    credit_score: {
      type: 'random_int',
      min: 300,
      max: 850
    },
    loan_amount: {
      type: 'random_float',
      min: 1000,
      max: 1000000
    },
    annual_income: {
      type: 'random_float',
      min: 10000,
      max: 1000000
    }
  },
  include_edge_cases: true
})

const testData = ref([])
const currentBatchId = ref(null)
const testReport = ref(null)
const pollingTimer = ref(null)
const batchStatus = ref('pending')

const generateData = async () => {
  try {
    const response = await testApi.generateTestData(generatorConfig.value)
    testData.value = response.data
    ElMessage.success('测试数据生成成功')
  } catch (error) {
    ElMessage.error('生成测试数据失败：' + error.message)
  }
}

const runTests = async () => {
  try {
    const response = await testApi.createTestBatch({
      name: `策略${strategyId}测试批次`,
      description: '自动生成的测试批次',
      strategy_id: parseInt(strategyId),
      test_cases: testData.value
    })
    
    currentBatchId.value = response.data.id
    ElMessage.success('测试批次已创建，开始执行测试')
    console.log('Created test batch:', response.data)
    
    // 立即开始轮询
    await pollTestStatus()
    startPolling()
  } catch (error) {
    console.error('Create test batch error:', error)
    ElMessage.error('创建测试批次失败：' + (error.response?.data?.detail || error.message))
  }
}

const pollTestStatus = async () => {
  try {
    console.log('Polling test status for batch:', currentBatchId.value)
    const response = await testApi.getTestBatch(currentBatchId.value)
    console.log('Poll response:', response.data)
    
    batchStatus.value = response.data.status
    if (batchStatus.value === 'completed' || batchStatus.value === 'failed') {
      console.log('Test batch completed with status:', batchStatus.value)
      stopPolling()
      await loadTestReport()
    } else {
      console.log('Test batch still running:', batchStatus.value)
    }
  } catch (error) {
    console.error('Poll status error:', error)
    stopPolling()
    ElMessage.error('获取测试状态失败：' + (error.response?.data?.detail || error.message))
  }
}

const startPolling = () => {
  pollingTimer.value = setInterval(pollTestStatus, 2000)
}

const stopPolling = () => {
  if (pollingTimer.value) {
    clearInterval(pollingTimer.value)
    pollingTimer.value = null
  }
}

const loadTestReport = async () => {
  try {
    console.log('Loading test report for batch:', currentBatchId.value)
    const response = await testApi.getTestReport(currentBatchId.value)
    console.log('Test report:', response.data)
    testReport.value = response.data
    ElMessage.success('测试执行完成')
  } catch (error) {
    console.error('Load report error:', error)
    ElMessage.error('加载测试报告失败：' + (error.response?.data?.detail || error.message))
  }
}

const exportReport = () => {
  // TODO: 实现报告导出功能
  ElMessage.info('报告导出功能开发中')
}

const getStatusType = (status) => {
  const statusMap = {
    pending: 'info',
    running: 'warning',
    passed: 'success',
    failed: 'danger',
    error: 'danger'
  }
  return statusMap[status] || 'info'
}

// 添加状态文本映射
const getStatusText = (status) => {
  const statusMap = {
    pending: '等待执行',
    running: '执行中',
    passed: '通过',
    failed: '失败',
    error: '错误'
  }
  return statusMap[status] || status
}

// 添加批次状态文本映射
const getBatchStatusText = (status) => {
  const statusMap = {
    pending: '等待执行',
    running: '执行中',
    completed: '执行完成',
    failed: '执行失败'
  }
  return statusMap[status] || status
}

// 添加批次状态类型映射
const getBatchStatusType = (status) => {
  const statusMap = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return statusMap[status] || 'info'
}

onMounted(() => {
  if (!strategyId) {
    ElMessage.error('策略ID不能为空')
    return
  }
})
</script>

<style>
.strategy-test {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.data-generator {
  margin-bottom: 20px;
}

.data-preview {
  margin-bottom: 20px;
}

.text-center {
  text-align: center;
  line-height: 32px;
}

.mt-4 {
  margin-top: 16px;
}

.chart-container {
  background: #fff;
  padding: 16px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.chart-container h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
}

.chart-container img {
  width: 100%;
  height: auto;
}

pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 12px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.loading-state .el-icon {
  font-size: 32px;
  margin-bottom: 16px;
}

.statistic-value {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}

.statistic-value.success {
  color: #67C23A;
}

.statistic-value.danger {
  color: #F56C6C;
}

.statistic-value.warning {
  color: #E6A23C;
}

.chart-card {
  height: 100%;
}

.chart-card img {
  width: 100%;
  height: auto;
}

.error-message {
  color: #F56C6C;
  white-space: pre-wrap;
  word-break: break-word;
}

.ml-2 {
  margin-left: 8px;
}
</style>
