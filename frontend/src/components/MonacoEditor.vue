<template>
  <div ref="editorContainer" class="monaco-editor-container"></div>
</template>

<script setup>
import * as monaco from 'monaco-editor'
import { onMounted, onBeforeUnmount, watch, ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'javascript'
  },
  options: {
    type: Object,
    default: () => ({})
  },
  readOnly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'save'])

// Python 代码片段
const pythonSnippets = [
  {
    label: 'def',
    insertText: 'def ${1:function_name}(${2:parameters}):\n\t${3:pass}',
    documentation: '创建一个函数'
  },
  {
    label: 'class',
    insertText: 'class ${1:ClassName}:\n\tdef __init__(self):\n\t\t${2:pass}',
    documentation: '创建一个类'
  },
  {
    label: 'if',
    insertText: 'if ${1:condition}:\n\t${2:pass}',
    documentation: 'if 条件语句'
  },
  {
    label: 'for',
    insertText: 'for ${1:item} in ${2:items}:\n\t${3:pass}',
    documentation: 'for 循环'
  },
  {
    label: 'try',
    insertText: 'try:\n\t${1:pass}\nexcept ${2:Exception} as e:\n\t${3:pass}',
    documentation: '异常处理'
  }
]

// SQL 代码片段
const sqlSnippets = [
  {
    label: 'SELECT',
    insertText: 'SELECT ${1:*}\nFROM ${2:table_name}\nWHERE ${3:condition}',
    documentation: '查询数据'
  },
  {
    label: 'INSERT',
    insertText: 'INSERT INTO ${1:table_name} (${2:columns})\nVALUES (${3:values})',
    documentation: '插入数据'
  },
  {
    label: 'UPDATE',
    insertText: 'UPDATE ${1:table_name}\nSET ${2:column} = ${3:value}\nWHERE ${4:condition}',
    documentation: '更新数据'
  },
  {
    label: 'DELETE',
    insertText: 'DELETE FROM ${1:table_name}\nWHERE ${2:condition}',
    documentation: '删除数据'
  },
  {
    label: 'JOIN',
    insertText: 'SELECT ${1:*}\nFROM ${2:table1}\nJOIN ${3:table2} ON ${4:condition}',
    documentation: '表连接'
  }
]

// 配置编辑器主题
monaco.editor.defineTheme('customTheme', {
  base: 'vs-dark',
  inherit: true,
  rules: [
    { token: 'keyword', foreground: '569CD6', fontStyle: 'bold' },
    { token: 'string', foreground: 'CE9178' },
    { token: 'number', foreground: 'B5CEA8' },
    { token: 'comment', foreground: '6A9955', fontStyle: 'italic' }
  ],
  colors: {
    'editor.background': '#1E1E1E',
    'editor.foreground': '#D4D4D4',
    'editor.lineHighlightBackground': '#2F3337',
    'editorCursor.foreground': '#FFFFFF',
    'editor.selectionBackground': '#264F78'
  }
})

let editor = null
const editorContainer = ref(null)

const defaultOptions = {
  theme: 'customTheme',
  fontSize: 14,
  minimap: { enabled: false },
  scrollBeyondLastLine: false,
  automaticLayout: true,
  tabSize: 4,
  wordWrap: 'on',
  wrappingIndent: 'indent',
  autoIndent: 'advanced',
  formatOnPaste: true,
  formatOnType: true,
  suggestOnTriggerCharacters: true,
  snippetSuggestions: 'top',
  lineNumbers: 'on',
  renderWhitespace: 'selection',
  matchBrackets: 'always',
  autoClosingBrackets: 'always',
  autoClosingQuotes: 'always',
  folding: true,
  showFoldingControls: 'always'
}

const registerLanguageProviders = () => {
  if (props.language === 'python') {
    monaco.languages.registerCompletionItemProvider('python', {
      provideCompletionItems: () => {
        const suggestions = pythonSnippets.map(snippet => ({
          label: snippet.label,
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: snippet.insertText,
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          documentation: snippet.documentation
        }))
        return { suggestions }
      }
    })
  } else if (props.language === 'sql') {
    monaco.languages.registerCompletionItemProvider('sql', {
      provideCompletionItems: () => {
        const suggestions = sqlSnippets.map(snippet => ({
          label: snippet.label,
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: snippet.insertText,
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          documentation: snippet.documentation
        }))
        return { suggestions }
      }
    })
  }
}

const initMonaco = () => {
  const options = {
    ...defaultOptions,
    ...props.options,
    value: props.modelValue,
    language: props.language,
    readOnly: props.readOnly
  }

  editor = monaco.editor.create(editorContainer.value, options)
  registerLanguageProviders()

  editor.onDidChangeModelContent(() => {
    const value = editor.getValue()
    emit('update:modelValue', value)
    emit('change', value)
  })

  editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
    emit('save', editor.getValue())
  })

  // 添加格式化命令
  editor.addCommand(monaco.KeyMod.Alt | monaco.KeyMod.Shift | monaco.KeyCode.KeyF, () => {
    editor.getAction('editor.action.formatDocument').run()
  })
}

onMounted(() => {
  initMonaco()
})

onBeforeUnmount(() => {
  if (editor) {
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
    registerLanguageProviders()
  }
})

watch(() => props.readOnly, (newValue) => {
  if (editor) {
    editor.updateOptions({ readOnly: newValue })
  }
})
</script>

<style scoped>
.monaco-editor-container {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  overflow: hidden;
}
</style> 