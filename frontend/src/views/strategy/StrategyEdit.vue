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
      
      <el-form-item label="SQL代码" prop="sql_code" class="code-editor-item">
        <div class="editor-wrapper">
          <MonacoEditor
            v-if="isDataReady"
            v-model="form.sql_code"
            language="sql"
          />
        </div>
        <div class="editor-tips">
          <el-tag size="small" type="info">支持 SQL 代码提示</el-tag>
          <el-button size="small" type="primary" @click="insertSqlTemplate">插入SQL模板</el-button>
        </div>
      </el-form-item>
      
      <el-form-item label="Python代码" prop="python_code" class="code-editor-item">
        <div class="editor-wrapper">
          <MonacoEditor
            v-if="isDataReady"
            v-model="form.python_code"
            language="python"
          />
        </div>
        <div class="editor-tips">
          <el-tag size="small" type="info">支持 Python 代码提示</el-tag>
          <el-button size="small" type="primary" @click="insertPythonTemplate">插入Python模板</el-button>
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
const isDataReady = ref(false)

const sqlTemplate = `-- 信贷风险评估SQL模板
SELECT 
    customer_id,
    credit_score,
    loan_amount,
    CASE 
        WHEN credit_score >= 700 THEN 'LOW'
        WHEN credit_score >= 600 THEN 'MEDIUM'
        ELSE 'HIGH'
    END as risk_level
FROM customer_credit_data
WHERE application_date >= :start_date
  AND application_date <= :end_date;`

const pythonTemplate = `# 信贷风险评估Python模板
def evaluate_credit_risk(data):
    """
    评估信贷风险
    :param data: 包含客户信息的字典
    :return: 风险评估结果
    """
    try:
        # 提取关键指标
        credit_score = data.get('credit_score', 0)
        loan_amount = data.get('loan_amount', 0)
        income = data.get('annual_income', 0)
        
        # 计算基础风险分数
        risk_score = 0
        
        # 信用分数评估
        if credit_score >= 700:
            risk_score += 40
        elif credit_score >= 600:
            risk_score += 25
        else:
            risk_score += 10
            
        # 贷款金额与收入比评估
        loan_to_income = loan_amount / income if income > 0 else float('inf')
        if loan_to_income <= 0.3:
            risk_score += 30
        elif loan_to_income <= 0.5:
            risk_score += 20
        else:
            risk_score += 10
            
        # 返回风险评估结果
        return {
            'risk_score': risk_score,
            'risk_level': 'LOW' if risk_score >= 60 else 'MEDIUM' if risk_score >= 40 else 'HIGH',
            'evaluation_factors': {
                'credit_score': credit_score,
                'loan_to_income_ratio': loan_to_income
            }
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'risk_level': 'ERROR'
        }
`

const form = ref({
  name: '',
  description: '',
  sql_code: '',
  python_code: ''
})

const rules = {
  name: [
    { required: true, message: '请输入策略名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入策略描述', trigger: 'blur' }
  ],
  sql_code: [
    { required: true, message: '请输入SQL代码', trigger: 'blur' }
  ],
  python_code: [
    { required: true, message: '请输入Python代码', trigger: 'blur' }
  ]
}

const isEdit = computed(() => route.params.id !== undefined)

const insertSqlTemplate = () => {
  form.value.sql_code = sqlTemplate
}

const insertPythonTemplate = () => {
  form.value.python_code = pythonTemplate
}

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
  if (!isEdit.value) {
    isDataReady.value = true
    return
  }
  
  try {
    const response = await strategyApi.getStrategy(route.params.id)
    form.value = response.data
    console.log('Strategy loaded:', form.value)
    isDataReady.value = true
  } catch (error) {
    ElMessage.error('加载策略失败：' + error.message)
    router.push('/strategy')
  }
}

onMounted(async () => {
  await loadStrategy()
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
  align-items: center;
}

.el-tag {
  font-size: 12px;
}
</style>
