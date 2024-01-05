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

const form = reactive({
  content: '',
  checkContent: '',
  password: '',
})

if (store.getters.loggedIn === 0) {
  router.back()
}

const content = router.currentRoute.value.params.content
if (content !== 'userName' && content !== 'explain' && content !== 'email' && content !== 'password') {
  router.back()
}

const onClickProfile = () => {
  router.push({name:'profile',params: {
          id: store.getters.loggedIn
      }
  })
}
store.commit("setDestination", {name: '', params: ''})

const onClickTop = () => {
  router.push({name:'top'})
}

const submitForm = () => {
  if (content !== "password" || form.content === form.checkContent) {
    ApiService.updateProfile(store.getters.loggedIn, content, form.content, form.password)
      .then((response) => {
        if (response.data.status === "error") {
          notify({title:'Info', message:response.data.content, type:'info'})
          if (content === 'password' || content === 'email') {
            form.content = ''
            form.checkContent = ''
          }
          form.password = ''
        } else {
          notify({title:'Success', message:'変更しました', type:'success'})
          router.back()
        }
      })
      .catch((error) => {
        if (content === 'password' || content === 'email') {
          form.content = ''
          form.checkContent = ''
        }
        form.password = ''
        notify({title:'Error', message:error, type:'error'})
      })
  } else {
      form.content = ''
      form.checkContent = ''
      form.password = ''
      notify({title:'Info', message:'パスワードが異なります', type:'info'})
  }
}
</script>

<template>
  <el-page-header :icon="null">
    <template #title>
      <span @click="onClickTop">Taiyo Channel</span>
    </template>
    <template #extra>
        <el-button type="primary" @click="onClickProfile">プロフィール</el-button>
    </template>
  </el-page-header>
  <br />
  <el-form :model="form" class="items-center" style="width:50%">
    <div v-if="content === 'userName'">
      <span>新しいユーザ名</span>
      <el-form-item style="width:100%">
        <el-input v-model="form.content" type="text" placeholder="新しいユーザ名を入力" autocomplete="off" />
      </el-form-item>
    </div>
    <div v-if="content === 'explain'">
      <span>新しい自己紹介</span>
      <el-form-item style="width:100%">
        <el-input v-model="form.content" :rows="4" maxlength="255" show-word-limit type="textarea" placeholder="新しい自己紹介を入力" autocomplete="off" />
      </el-form-item>
    </div>
    <div v-if="content === 'email'">
      <span>新しいメールアドレス</span>
      <el-form-item style="width:100%">
        <el-input v-model="form.content" type="email" placeholder="新しいメールアドレスを入力" autocomplete="off" />
      </el-form-item>
    </div>
    <div v-if="content === 'password'">
      <span>新しいパスワード</span>
      <el-form-item style="width:100%">
        <el-input v-model="form.content" type="password" placeholder="新しいパスワードを入力" autocomplete="off" />
      </el-form-item>
      <span>新しいパスワード(確認)</span>
      <el-form-item style="width:100%">
        <el-input v-model="form.checkContent" type="password" placeholder="新しいパスワードを入力" autocomplete="off" />
      </el-form-item>
    </div>
    <span>現在のパスワード</span>
    <el-form-item style="width:100%">
      <el-input v-model="form.password" type="password" placeholder="現在のパスワードを入力" autocomplete="off" />
    </el-form-item>
    <el-form-item>
        <el-button type="primary" @click="submitForm" class="items-center">変更</el-button>
    </el-form-item>
  </el-form>
</template>