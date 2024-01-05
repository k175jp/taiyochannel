<script lang="ts" setup>
import { useRouter } from 'vue-router'
const router = useRouter()
router.replace('/notfound')
const onClick = () => {
    router.push({name:'top'})
}
</script>

<template>
    <!-- <h1>こんなパスねえよ！！！</h1> -->
    <h1>Not Found</h1>
    <el-button type="primary" @click="onClick">トップに戻る</el-button>
</template>