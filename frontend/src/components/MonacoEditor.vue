<template>
  <div class="monaco-editor-wrapper">
    <div class="monaco-editor-container" ref="editorContainer"></div>
  </div>
</template>

<script setup>
import * as monaco from 'monaco-editor'
import { onMounted, onBeforeUnmount, watch, ref, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'javascript'
  }
})

const emit = defineEmits(['update:modelValue'])
const editorContainer = ref(null)
let editor = null

const initEditor = async () => {
  await nextTick()
  
  if (!editorContainer.value) return
  
  // 销毁旧的编辑器实例
  if (editor) {
    editor.dispose()
  }

  editor = monaco.editor.create(editorContainer.value, {
    value: props.modelValue,
    language: props.language,
    theme: 'vs-dark',
    automaticLayout: false, // 关闭自动布局
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    lineNumbers: 'on',
    roundedSelection: false,
    wordWrap: 'on'
  })

  // 手动处理布局更新
  const updateEditorLayout = () => {
    if (editor) {
      editor.layout()
    }
  }

  const resizeObserver = new ResizeObserver(() => {
    window.requestAnimationFrame(() => {
      updateEditorLayout()
    })
  })

  resizeObserver.observe(editorContainer.value)

  editor.onDidChangeModelContent(() => {
    emit('update:modelValue', editor.getValue())
  })

  // 保存引用以便清理
  editor._resizeObserver = resizeObserver
}

onMounted(() => {
  initEditor()
})

onBeforeUnmount(() => {
  if (editor) {
    if (editor._resizeObserver) {
      editor._resizeObserver.disconnect()
    }
    editor.dispose()
  }
})

watch(() => props.modelValue, (newValue) => {
  if (editor && newValue !== editor.getValue()) {
    editor.setValue(newValue)
  }
})

watch(() => props.language, (newValue) => {
  if (editor) {
    monaco.editor.setModelLanguage(editor.getModel(), newValue)
  }
})
</script>

<style>
.monaco-editor-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.monaco-editor-container {
  width: 100%;
  height: 100%;
  border: 1px solid #dcdfe6;
}

/* 确保编辑器内容区域正确显示 */
.monaco-editor {
  padding: 8px;
}

/* 修复编辑器内容区域的样式 */
.monaco-editor .overflow-guard {
  width: 100% !important;
  height: 100% !important;
}
</style> 