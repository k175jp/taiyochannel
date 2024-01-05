<script lang="ts" setup>
import {
    reactive,
} from 'vue';

import {
    ElNotification as notify,
} from 'element-plus'

import {
    useRouter,
} from 'vue-router'

import store from '../store'

import ApiService from "../service/ApiService"

const router = useRouter()

const pattern = /^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@{1}[A-Za-z0-9_.-]+\.[A-Za-z0-9]+$/

const form = reactive({
    userName: '',
    email: '',
    password: '',
    checkPassword: '',
})

const submitForm = () => {
    if (form.password === form.checkPassword) {
        if (pattern.test(form.email)) {
            ApiService.signup(form.userName,form.email,form.password)
                .then((response) => {
                    if (response.data.status === "error") {
                        notify({title:'Info', message:response.data.content, type:'info'})
                        form.email = ''
                        form.password = ''
                        form.checkPassword = ''
                    } else {
                        notify({title:'Success', message:'登録しました', type:'success'})
                        router.push({name:'signin'})
                    }
                })
            .catch((error) => {
                form.password = ''
                form.checkPassword = ''
                notify({title:'Error', message:error, type:'error'})
            })
        } else {
            notify({title:'Info', message:'正しいメールアドレスを入力してください', type:'info'})
            form.email = ''
            form.password = ''
            form.checkPassword = ''
        }
    } else {
        form.password = ''
        form.checkPassword = ''
        notify({title:'Info', message:'パスワードが異なります', type:'info'})
    }
}

const onClickSignin = () => {
    router.push({name:'signin'})
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
        <span> 新規登録 </span>
    </template>
    <template #extra>
        <el-button type="primary" @click="onClickSignin">ログイン</el-button>
    </template>
  </el-page-header>
  <br/>
  <el-form :model="form" class="items-center" style="width:50%">
    <span>ユーザ名(必須)</span>
    <el-form-item style="width:100%">
        <el-input v-model="form.userName" type="text" placeholder="メールアドレスを入力" autocomplete="off" />
    </el-form-item>
    <span>メールアドレス(必須)</span>
    <el-form-item style="width:100%">
        <el-input v-model="form.email" type="email" placeholder="メールアドレスを入力" autocomplete="off" />
    </el-form-item>
    <span>パスワード(必須)</span>
    <el-form-item style="width:100%">
        <el-input v-model="form.password" type="password" placeholder="パスワードを入力" autocomplete="off"/>
    </el-form-item>
    <span>パスワード(確認)</span>
    <el-form-item style="width:100%">
        <el-input v-model="form.checkPassword" type="password" placeholder="パスワードを入力" autocomplete="off"/>
    </el-form-item>
    <el-form-item>
        <el-button type="primary" @click="submitForm" class="items-center">登録</el-button>
    </el-form-item>
  </el-form>
</template>