<template>
  <div ref="editorContainer" class="monaco-editor-container"></div>
</template>

<script>
import * as monaco from 'monaco-editor'
import { onMounted, onBeforeUnmount, watch, ref } from 'vue'

export default {
  name: 'MonacoEditor',
  props: {
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
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    let editor = null
    const editorContainer = ref(null)

    const initMonaco = () => {
      editor = monaco.editor.create(editorContainer.value, {
        value: props.modelValue,
        language: props.language,
        ...props.options
      })

      editor.onDidChangeModelContent(() => {
        const value = editor.getValue()
        emit('update:modelValue', value)
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
      }
    })

    return {
      editorContainer
    }
  }
}
</script>

<style scoped>
.monaco-editor-container {
  width: 100%;
  height: 100%;
}
</style> 