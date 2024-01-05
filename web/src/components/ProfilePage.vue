<script lang="ts" setup>
import {
    reactive,
} from 'vue';

import {
    useRouter,
} from 'vue-router'

import ApiService from "../service/ApiService";
import store from '../store';
import { ElNotification as notify} from 'element-plus';

const router = useRouter()

const profile = reactive({
    userName: '',
    explain: '',
    email: '',
    password: '',
    allowed: false
})

const onClickTop = () => {
    router.push({name:'top'})
}

store.commit("setDestination", {name: '', params: ''})
const userId = router.currentRoute.value.params.id
if (isNaN(userId) === true || userId === null || userId == "0") {
    router.back()
}

const init = () => {
        ApiService.getProfile(store.getters.loggedIn, userId)
        .then((response) => {
          if (response.data.status === "error") {
            notify({title:'Info', message:response.data.content, type:'info'})
            router.back()
          } else {
            profile.userName = response.data.userName
            profile.explain = response.data.explain
            if ("email" in response.data) {
                profile.email = response.data.email[0] + "*******@" + response.data.email[response.data.email.indexOf("@")+1] + "*****"
                profile.password = "********"
                profile.allowed = true
            }
          }
        })
        .catch((error) => {
            profile.userName= ''
            profile.explain = ''
            profile.email = ''
            profile.password = ''
            notify({title:'Error', message:error, type:'error'})
        })
}

const onClickUpdate = (content: string) => {
  router.push({name:'update_profile',params: {
          content: content
      }
  })
}

const onClickLogout = () => {
    store.commit("setUserId", 0)
    notify({title:'Success', message:'ログアウトしました', type:'success'})
    router.push({name:'top'})
}

init()
</script>

<template>
  <el-page-header :icon="null">
    <template #title>
      <span @click="onClickTop">Taiyo Channel</span>
    </template>
    <template #extra>
        <el-button type="primary" @click="onClickLogout">ログアウト</el-button>
    </template>
  </el-page-header>
  <br />
  <el-card>
    <template #header>
    <span>ユーザ名</span>
    <el-button v-if='profile.allowed===true' style="float:right" type="primary" @click="onClickUpdate('userName')">変更</el-button>
    </template>
    <span>{{profile.userName}}</span>
  </el-card>
  <br />
  <el-card>
    <template #header>
    <span>自己紹介</span>
    <el-button v-if='profile.allowed===true' style="float:right" type="primary" @click="onClickUpdate('explain')">変更</el-button>
    </template>
    <span>{{profile.explain}}</span>
  </el-card>
  <br />
  <el-card v-if='profile.allowed===true'>
    <template #header>
    <span>メールアドレス</span>
    <el-button style="float:right" type="primary" @click="onClickUpdate('email')">変更</el-button>
    </template>
    <span>{{profile.email}}</span>
  </el-card>
  <br />
  <el-card v-if='profile.allowed===true'>
    <template #header>
    <span>パスワード</span>
    <el-button style="float:right" type="primary" @click="onClickUpdate('password')">変更</el-button>
    </template>
    <span>{{profile.password}}</span>
  </el-card>
</template>