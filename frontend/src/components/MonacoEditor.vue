<template>
  <div class="monaco-editor-wrapper">
    <div v-show="!isEditorReady" class="editor-loading">
      <el-icon class="is-loading"><Loading /></el-icon>
    </div>
    <div class="monaco-editor-container" ref="editorContainer"></div>
  </div>
</template>

<script setup>
import * as monaco from 'monaco-editor'
import { onMounted, onBeforeUnmount, watch, ref } from 'vue'
import { Loading } from '@element-plus/icons-vue'

const isEditorReady = ref(false)

// 添加debounce函数
const debounce = (fn, delay) => {
  let timer;
  return (...args) => {
    if (timer) {
      clearTimeout(timer);
    }
    timer = setTimeout(() => {
      fn(...args);
    }, delay);
  };
};

// 重写ResizeObserver，减少触发频率
const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver {
  constructor(callback) {
    callback = debounce(callback, 100); // 减少延迟时间
    super(callback);
  }
};

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

// 配置编辑器主题
monaco.editor.defineTheme('custom-theme', {
  base: 'vs-dark',
  inherit: true,
  rules: [
    { token: 'comment', foreground: '6A9955', fontStyle: 'italic' },
    { token: 'keyword', foreground: '569cd6' },
    { token: 'string', foreground: 'ce9178' },
    { token: 'number', foreground: 'b5cea8' }
  ],
  colors: {
    'editor.background': '#1e1e1e',
    'editor.foreground': '#d4d4d4',
    'editorCursor.foreground': '#ffffff',
    'editor.lineHighlightBackground': '#2c313a',
    'editorLineNumber.foreground': '#858585',
    'editor.selectionBackground': '#264f78',
    'editor.inactiveSelectionBackground': '#3a3d41'
  }
})

// 优化默认选项，移除一些不必要的选项
const defaultOptions = {
  theme: 'custom-theme',
  fontSize: 14,
  lineNumbers: 'on',
  minimap: { enabled: false },
  scrollBeyondLastLine: false,
  automaticLayout: true,
  tabSize: 2,
  wordWrap: 'on',
  folding: true,
  contextmenu: true,
  scrollbar: {
    vertical: 'visible',
    horizontal: 'visible'
  }
}

// SQL 代码片段
const sqlSnippets = [
  {
    label: 'SELECT',
    insertText: 'SELECT ${1:*} FROM ${2:table_name} WHERE ${3:condition}',
    documentation: '查询数据',
    kind: monaco.languages.CompletionItemKind.Snippet
  },
  {
    label: 'INSERT',
    insertText: 'INSERT INTO ${1:table_name} (${2:columns}) VALUES (${3:values})',
    documentation: '插入数据',
    kind: monaco.languages.CompletionItemKind.Snippet
  },
  {
    label: 'UPDATE',
    insertText: 'UPDATE ${1:table_name} SET ${2:column} = ${3:value} WHERE ${4:condition}',
    documentation: '更新数据',
    kind: monaco.languages.CompletionItemKind.Snippet
  },
  {
    label: 'DELETE',
    insertText: 'DELETE FROM ${1:table_name} WHERE ${2:condition}',
    documentation: '删除数据',
    kind: monaco.languages.CompletionItemKind.Snippet
  }
]

// Python 代码片段
const pythonSnippets = [
  {
    label: 'def',
    insertText: 'def ${1:function_name}(${2:parameters}):\n\t${3:pass}',
    documentation: '定义函数',
    kind: monaco.languages.CompletionItemKind.Snippet
  },
  {
    label: 'class',
    insertText: 'class ${1:ClassName}:\n\tdef __init__(self):\n\t\t${2:pass}',
    documentation: '定义类',
    kind: monaco.languages.CompletionItemKind.Snippet
  },
  {
    label: 'if',
    insertText: 'if ${1:condition}:\n\t${2:pass}',
    documentation: 'if 条件语句',
    kind: monaco.languages.CompletionItemKind.Snippet
  },
  {
    label: 'for',
    insertText: 'for ${1:item} in ${2:items}:\n\t${3:pass}',
    documentation: 'for 循环',
    kind: monaco.languages.CompletionItemKind.Snippet
  }
]

// 延迟注册代码提示
const registerCompletionProvider = debounce(() => {
  if (props.language === 'sql') {
    monaco.languages.registerCompletionItemProvider('sql', {
      provideCompletionItems: () => ({
        suggestions: sqlSnippets.map(snippet => ({
          ...snippet,
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet
        }))
      })
    })
  } else if (props.language === 'python') {
    monaco.languages.registerCompletionItemProvider('python', {
      provideCompletionItems: () => ({
        suggestions: pythonSnippets.map(snippet => ({
          ...snippet,
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet
        }))
      })
    })
  }
}, 500)

const initEditor = () => {
  if (!editorContainer.value) {
    console.error('Editor container not found')
    return
  }

  // 销毁旧的编辑器实例
  if (editor) {
    editor.dispose()
  }

  const options = {
    ...defaultOptions,
    value: props.modelValue || '',
    language: props.language
  }

  editor = monaco.editor.create(editorContainer.value, options)
  console.log('Editor initialized with value:', props.modelValue)

  // 监听内容变化
  editor.onDidChangeModelContent(debounce(() => {
    const value = editor.getValue()
    if (value !== props.modelValue) {
      emit('update:modelValue', value)
    }
  }, 100))

  // 使用优化后的ResizeObserver
  const resizeObserver = new ResizeObserver(() => {
    if (editor) {
      editor.layout()
    }
  })

  resizeObserver.observe(editorContainer.value)
  editor._resizeObserver = resizeObserver

  // 设置初始值
  if (props.modelValue) {
    console.log('Setting initial value:', props.modelValue)
    editor.setValue(props.modelValue)
  }

  // 延迟注册代码提示
  registerCompletionProvider()
  
  isEditorReady.value = true
}

onMounted(() => {
  console.log('Component mounted, modelValue:', props.modelValue)
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

// 优化 watch
watch(() => props.modelValue, (newValue) => {
  console.log('Watch triggered, new value:', newValue)
  if (editor && newValue !== editor.getValue()) {
    const position = editor.getPosition()
    editor.setValue(newValue || '')
    if (position) {
      editor.setPosition(position)
    }
  }
}, { immediate: true })

watch(() => props.language, (newValue) => {
  if (editor) {
    monaco.editor.setModelLanguage(editor.getModel(), newValue)
    registerCompletionProvider()
  }
})
</script>

<style>
.monaco-editor-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.editor-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 1;
}

.monaco-editor-container {
  width: 100%;
  height: 100%;
}

.monaco-editor {
  width: 100% !important;
  height: 100% !important;
}
</style> 