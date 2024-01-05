<script lang="ts" setup>
import { reactive } from 'vue';
import { ElNotification as notify, } from 'element-plus'
import { useRouter } from 'vue-router'
import store from "../store"

import ApiService from "../service/ApiService";

const router = useRouter()

const form = reactive({
    email: '',
    password: ''
})

if (store.getters.destinationName === '') {
    store.commit("setDestination", {name: 'top', params: ''})
}

const submitForm = () => {
    ApiService.signin(form.email, form.password)
        .then((response) =>{
            if (response.data.status === "error") {
                form.password = ''
                notify({title:'Info', message:response.data.content, type:'info'})
            } else {
                notify({title:'Success',message:'ログインしました', type:'success'})
                store.commit("setUserId",response.data.userId)
                if (store.getters.destinationName === 'top') {
                    router.push({name:'top'})
                } else if (store.getters.destinationName === 'search') {
                    router.push({name:'search', query: {
                        threadname: store.getters.destinationParams
                    }})
                } else if (store.getters.destinationName === 'thread') {
                    router.push({name:'thread', params: {
                        threadId: store.getters.destinationParams
                    }})
                }
            }
        })
        .catch((error) => {
            form.password = ''
            notify({title:'Error', message:error, type:'error'})
        })
}

const onClickSignup = () => {
    router.push({name:'signup'})
}

const onClickTop = () => {
    router.push({name:'top'})
}

if (store.getters.loggedIn !== 0) {
    router.back()
}

</script>

<template>
  <el-page-header :icon="null">
    <template #title>
      <span @click="onClickTop">Taiyo Channel</span>
    </template>
    <template #content>
        <span> ログイン </span>
    </template>
    <template #extra>
        <el-button type="primary" @click="onClickSignup">新規登録</el-button>
    </template>
  </el-page-header>
  <br/>
  <el-form :model="form" class="items-center" style="width:50%">
    <span>メールアドレス</span>
    <el-form-item style="width:100%">
        <el-input v-model="form.email" type="email" placeholder="メールアドレスを入力" autocomplete="off" />
    </el-form-item>
    <span>パスワード</span>
    <el-form-item style="width:100%">
        <el-input v-model="form.password" type="password" placeholder="パスワードを入力" autocomplete="off"/>
    </el-form-item>
    <el-form-item>
        <el-button type="primary" @click="submitForm" class="items-center">ログイン</el-button>
    </el-form-item>
  </el-form>
</template>