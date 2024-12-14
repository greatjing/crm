<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-content">
        <h1>信贷信用风险策略测试平台</h1>
      </div>
    </el-header>
    
    <el-container>
      <el-aside width="200px">
        <el-menu
          router
          :default-active="$route.path"
          class="app-menu">
          <el-menu-item index="/strategy">
            <el-icon><Document /></el-icon>
            <span>策略管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { Document } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    Document
  }
}
</script>

<style>
.app-container {
  height: 100vh;
}

.app-header {
  background-color: #409EFF;
  color: white;
  padding: 0 20px;
}

.header-content {
  height: 60px;
  display: flex;
  align-items: center;
}

.header-content h1 {
  margin: 0;
  font-size: 20px;
}

.app-menu {
  height: 100%;
  border-right: solid 1px #e6e6e6;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}
</style>