<template>
  <div class="strategy-edit">
    <div class="header">
      <h2>{{ isEdit ? '编辑策略' : '新建策略' }}</h2>
    </div>
    
    <el-form :model="form" label-width="120px" :rules="rules" ref="formRef">
      <el-form-item label="策略名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入策略名称" />
      </el-form-item>
      
      <el-form-item label="策略描述" prop="description">
        <el-input v-model="form.description" type="textarea" placeholder="请输入策略描述" />
      </el-form-item>
      
      <el-form-item label="SQL代码" prop="sqlCode" class="code-editor-item">
        <div class="editor-wrapper">
          <MonacoEditor
            v-model="form.sqlCode"
            language="sql"
          />
        </div>
        <div class="editor-tips">
          <el-tag size="small" type="info">支持 SQL 代码提示</el-tag>
        </div>
      </el-form-item>
      
      <el-form-item label="Python代码" prop="pythonCode" class="code-editor-item">
        <div class="editor-wrapper">
          <MonacoEditor
            v-model="form.pythonCode"
            language="python"
          />
        </div>
        <div class="editor-tips">
          <el-tag size="small" type="info">支持 Python 代码提示</el-tag>
        </div>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSave">保存</el-button>
        <el-button @click="cancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import MonacoEditor from '@/components/MonacoEditor.vue'
import { strategyApi } from '@/api/strategy'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)

const form = ref({
  name: '',
  description: '',
  sqlCode: '',
  pythonCode: ''
})

const rules = {
  name: [
    { required: true, message: '请输入策略名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入策略描述', trigger: 'blur' }
  ],
  sqlCode: [
    { required: true, message: '请输入SQL代码', trigger: 'blur' }
  ],
  pythonCode: [
    { required: true, message: '请输入Python代码', trigger: 'blur' }
  ]
}

const isEdit = computed(() => route.params.id !== undefined)

const handleSave = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (isEdit.value) {
      await strategyApi.updateStrategy(route.params.id, form.value)
      ElMessage.success('策略更新成功')
    } else {
      await strategyApi.createStrategy(form.value)
      ElMessage.success('策略创建成功')
    }
    
    router.push('/strategy')
  } catch (error) {
    if (error.name === 'ValidationError') {
      ElMessage.error('请检查表单填写是否正确')
    } else {
      ElMessage.error('保存失败：' + error.message)
    }
  }
}

const cancel = () => {
  router.push('/strategy')
}

const loadStrategy = async () => {
  if (!isEdit.value) return
  
  try {
    const response = await strategyApi.getStrategy(route.params.id)
    form.value = response.data
  } catch (error) {
    ElMessage.error('加载策略失败：' + error.message)
    router.push('/strategy')
  }
}

onMounted(() => {
  loadStrategy()
})
</script>

<style>
.strategy-edit {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.code-editor-item {
  margin-bottom: 22px;
}

.code-editor-item :deep(.el-form-item__content) {
  height: auto;
}

.editor-wrapper {
  height: 300px;
  background-color: #1e1e1e;
  border-radius: 4px;
  overflow: hidden;
}

.editor-tips {
  margin-top: 8px;
  display: flex;
  gap: 8px;
}

.el-tag {
  font-size: 12px;
}
</style>
