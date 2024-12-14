<template>
  <div class="strategy-test">
    <div class="header">
      <h2>策略测试</h2>
    </div>
    
    <el-form :model="form" label-width="120px">
      <el-form-item label="测试数据">
        <el-input v-model="form.testData" type="textarea" :rows="5" placeholder="请输入测试数据（JSON格式）" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="runTest">运行测试</el-button>
        <el-button @click="back">返回</el-button>
      </el-form-item>
    </el-form>
    
    <div v-if="testResult" class="test-result">
      <h3>测试结果</h3>
      <el-card>
        <pre>{{ testResult }}</pre>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StrategyTest',
  data() {
    return {
      form: {
        testData: ''
      },
      testResult: null
    }
  },
  methods: {
    runTest() {
      // TODO: 实现测试逻辑
      this.testResult = {
        status: 'success',
        message: '测试执行成功',
        data: {
          // 测试结果数据
        }
      }
    },
    back() {
      this.$router.push('/strategy')
    }
  }
}
</script>

<style scoped>
.strategy-test {
  padding: 20px;
}
.header {
  margin-bottom: 20px;
}
.test-result {
  margin-top: 20px;
}
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
