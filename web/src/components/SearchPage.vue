<script lang="ts" setup>
import { reactive, ref } from 'vue';

import { ElNotification as notify } from 'element-plus';

import { useRouter } from 'vue-router'

import ApiService from "../service/ApiService";
import store from '../store';

const router = useRouter()

const form = reactive({
    keyword: ''
})

const data = ref([])

const onClickSearch = () => {
    if (form.keyword !== ''){
        router.push({name:'search', query: {
            threadname: form.keyword
        }})
        init(form.keyword)
    } else {
        notify({title:'Info', message:"キーワードを入力してください", type:'info'})
    }
}

store.commit("setDestination", {name: '', params: ''})

const onClickTop = () => {
    router.push({name:'top'})
}

const onClickProfile = () => {
    router.push({name:'profile', params: {
        id: store.getters.loggedIn
    }})
}

const threadName = router.currentRoute.value.query.threadname
const onClickLogout = () => {
    store.commit("setUserId", 0)
    notify({title:'Success', message:'ログアウトしました', type:'success'})
}


const init = (threadName) => {
    ApiService.getThreadList(threadName)
    .then((response) => {
        if (response.data.status === "error") {
            notify({title:'Info', message:response.data.content, type:'info'})
        } else {
            data.value = response.data.list
        }
    })
    .catch((error) => {
        notify({title:'Error', message:error, type:'error'})
    })
}

const onClickSignin = () => {
    store.commit("setDestination", {name:'search', params:threadName})
    router.push({name:'signin'})
}

const onClickSignup = () => {
    store.commit("setDestination", {name:'search', params:threadName})
    router.push({name:'signup'})
}

const onClickNewThread = () => {
    router.push({name:'new_thread'})
}

const onClickThread = (threadId) => {
    router.push({name:'thread', params: {
        threadId: threadId
    }})
}

if (threadName) {
    init(threadName)
} else {
    init('')
}
</script>

<template>
  <el-page-header :icon="null">
    <template #title>
      <span @click="onClickTop">Taiyo Channel</span>
    </template>
    <template #extra>
        <el-button type="primary" v-if="store.getters.loggedIn !== 0" @click="onClickLogout">ログアウト</el-button>
        <el-button type="primary" v-if="store.getters.loggedIn !== 0" @click="onClickProfile">プロフィール</el-button>
        <el-button type="primary" v-if="store.getters.loggedIn === 0" @click="onClickSignin">ログイン</el-button>
        <el-button type="primary" v-if="store.getters.loggedIn === 0" @click="onClickSignup">新規作成</el-button>
    </template>
  </el-page-header>
  <br/>
  <el-form :inline='true' :model="form" class="items-center-flex">
    <el-form-item style="width:50%" label="スレッドを検索">
      <el-input v-model="form.keyword" placeholder="キーワードを入力" @keypress.enter="onClickSearch"/>
      <el-input type="text" name="dummy" style="position:absolute;visibility:hidden" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onClickSearch">検索</el-button>
    </el-form-item>
  </el-form>
  <br />
  <el-row v-for="(d, index) in data" :key="d">
    <el-card shadow="hover" style="width:100%;font-size:20px" @click="onClickThread(d.thread_id)">
      <span>{{ index + 1 }}.{{ d.thread_name }}</span>
    </el-card>
    <br />
  </el-row>
  <br />
  <el-form>
    <el-form-item>
        <el-button v-if="store.getters.loggedIn !== 0" type="primary" class="items-center" style="width:50%" @click="onClickNewThread">スレッドの作成</el-button>
    </el-form-item>
  </el-form>
</template>