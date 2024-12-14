<template>
  <div class="strategy-edit">
    <div class="header">
      <h2>{{ isEdit ? '编辑策略' : '新建策略' }}</h2>
    </div>
    
    <el-form :model="form" label-width="120px">
      <el-form-item label="策略名称">
        <el-input v-model="form.name" placeholder="请输入策略名称" />
      </el-form-item>
      
      <el-form-item label="策略描述">
        <el-input v-model="form.description" type="textarea" placeholder="请输入策略描述" />
      </el-form-item>
      
      <el-form-item label="SQL代码">
        <div class="editor-container">
          <MonacoEditor
            v-model="form.sqlCode"
            language="sql"
            :options="editorOptions"
          />
        </div>
      </el-form-item>
      
      <el-form-item label="Python代码">
        <div class="editor-container">
          <MonacoEditor
            v-model="form.pythonCode"
            language="python"
            :options="editorOptions"
          />
        </div>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="saveStrategy">保存</el-button>
        <el-button @click="cancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
// import * as monaco from 'monaco-editor'
import MonacoEditor from '@/components/MonacoEditor.vue'

export default {
  name: 'StrategyEdit',
  components: {
    MonacoEditor
  },
  data() {
    return {
      form: {
        name: '',
        description: '',
        sqlCode: '',
        pythonCode: ''
      },
      editorOptions: {
        theme: 'vs-dark',
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        fontSize: 14,
        automaticLayout: true
      }
    }
  },
  computed: {
    isEdit() {
      return this.$route.params.id !== undefined
    }
  },
  methods: {
    saveStrategy() {
      // TODO: 实现保存逻辑
      this.$router.push('/strategy')
    },
    cancel() {
      this.$router.push('/strategy')
    }
  }
}
</script>

<style scoped>
.strategy-edit {
  padding: 20px;
}
.header {
  margin-bottom: 20px;
}
.editor-container {
  height: 300px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}
</style>
