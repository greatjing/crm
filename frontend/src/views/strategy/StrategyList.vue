<template>
  <div class="strategy-list">
    <div class="header">
      <h2>策略列表</h2>
      <el-button type="primary" @click="createStrategy">新建策略</el-button>
    </div>
    
    <el-table :data="strategies" style="width: 100%">
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column prop="name" label="策略名称" width="180" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
            {{ scope.row.status === 'active' ? '已启用' : '未启用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template #default="scope">
          <el-button size="small" @click="editStrategy(scope.row)">编辑</el-button>
          <el-button size="small" type="primary" @click="testStrategy(scope.row)">测试</el-button>
          <el-button 
            size="small" 
            :type="scope.row.status === 'active' ? 'warning' : 'success'"
            @click="toggleStatus(scope.row)">
            {{ scope.row.status === 'active' ? '停用' : '启用' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { strategyApi } from '@/api/strategy'

export default {
  name: 'StrategyList',
  setup() {
    const router = useRouter()
    const strategies = ref([
      // 测试数据
      {
        id: 1,
        name: '测试策略1',
        description: '这是一个测试策略',
        status: 'active'
      },
      {
        id: 2,
        name: '测试策略2',
        description: '这是另一个测试策略',
        status: 'inactive'
      }
    ])

    const loadStrategies = async () => {
      try {
        const response = await strategyApi.getStrategies()
        strategies.value = response.data
      } catch (error) {
        ElMessage.error('加载策略列表失败：' + error.message)
      }
    }

    const createStrategy = () => {
      router.push('/strategy/create')
    }

    const editStrategy = (strategy) => {
      router.push(`/strategy/edit/${strategy.id}`)
    }

    const testStrategy = (strategy) => {
      router.push(`/strategy/test/${strategy.id}`)
    }

    const toggleStatus = async (strategy) => {
      try {
        await strategyApi.updateStrategy(strategy.id, {
          ...strategy,
          status: strategy.status === 'active' ? 'inactive' : 'active'
        })
        strategy.status = strategy.status === 'active' ? 'inactive' : 'active'
        ElMessage.success('状态更新成功')
      } catch (error) {
        ElMessage.error('状态更新失败：' + error.message)
      }
    }

    onMounted(() => {
      // 暂时注释掉API调用，等后端ready后再启用
      loadStrategies()
    })

    return {
      strategies,
      createStrategy,
      editStrategy,
      testStrategy,
      toggleStatus
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
.el-button {
  margin-left: 8px;
}
.el-button:first-child {
  margin-left: 0;
}
</style> 