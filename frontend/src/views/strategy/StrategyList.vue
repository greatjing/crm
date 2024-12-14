<template>
  <div class="strategy-list">
    <div class="header">
      <h2>策略列表</h2>
      <el-button type="primary" @click="createStrategy">新建策略</el-button>
    </div>
    
    <el-table :data="strategies" style="width: 100%">
      <el-table-column prop="id" label="ID" width="180" />
      <el-table-column prop="name" label="策略名称" width="180" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="editStrategy(scope.row)">编辑</el-button>
          <el-button size="small" type="primary" @click="testStrategy(scope.row)">测试</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'StrategyList',
  data() {
    return {
      strategies: []  // 这里将来会从API获取数据
    }
  },
  methods: {
    createStrategy() {
      this.$router.push('/strategy/create')
    },
    editStrategy(strategy) {
      this.$router.push(`/strategy/edit/${strategy.id}`)
    },
    testStrategy(strategy) {
      this.$router.push(`/strategy/test/${strategy.id}`)
    }
  }
}
</script>

<style scoped>
.strategy-list {
  padding: 20px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 