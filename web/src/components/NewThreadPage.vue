<script lang="ts" setup>
import { reactive } from 'vue';

import { ElNotification as notify} from 'element-plus';

import { useRouter } from 'vue-router'

import store from '../store';
import ApiService from "../service/ApiService";

const router = useRouter()

store.commit("setDestination", {name: '', params: ''})
if (store.getters.loggedIn === 0) {
  router.back()
}

const form = reactive({
    threadName: '',
    text: ''
})

const onClickTop = () => {
    router.push({name:'top'})
}

const onClickProfile = () => {
    router.push({name:'profile', params: {
        id: store.getters.loggedIn
    }})
}

const onClickLogout = () => {
    store.commit("setUserId", 0)
    notify({title:'Success', message:'ログアウトしました', type:'success'})
    router.push({name:'top'})
}

const submitForm = () => {
    ApiService.newThread(form.threadName, form.text, store.getters.loggedIn)
    .then((response) => {
        if (response.data.status === "error") {
            notify({title:'Info', message:response.data.content, type:'info'})
        } else {
            notify({title:'Success', message:"作成しました", type:'success'})
            router.push({name:'thread', params: {
                threadId: response.data.id
            }})
        }
    })
    .catch((error) => {
        notify({title:'Error', message:error, type:'error'})
    })
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
    </template>
  </el-page-header>
  <br/>
  <el-form :model="form" class="items-center" style="width:50%">
    <span>スレッドのタイトル</span>
    <el-form-item style="width:100%">
        <el-input v-model="form.threadName" maxlength="50" show-word-limit type="text" placeholder="スレッドのタイトルを入力" autocomplete="off" />
    </el-form-item>
    <span>本文</span>
    <el-form-item style="width:100%">
        <el-input v-model="form.text" :rows="4"  maxlength="255" show-word-limit type="textarea" placeholder="本文を入力" autocomplete="off" />
    </el-form-item>
    <el-form-item>
        <el-button type="primary" @click="submitForm" class="items-center">変更</el-button>
    </el-form-item>
  </el-form>
</template>