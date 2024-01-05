<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { ElNotification as notify} from 'element-plus';
import type { UploadProps, UploadUserFile } from 'element-plus';

import { useRouter } from 'vue-router'

import ApiService from "../service/ApiService";
import store from '../store';

const file = ref<UploadUserFile[]>()

const handleRemove: UploadProps['onRemove'] = (file) => {
  notify({title:'Info', message:`${file.name}が削除されました`, type:'info'})
}

const handleExceed: UploadProps['onExceed'] = () => {
  notify({title:'Info', message:'1つのファイルのみ選択できます', type:'info'})
}

const router = useRouter()
store.commit("setDestination", {name: '', params: ''})

const data = reactive({
    list: [],
    threadName: ''
})

const form = reactive({
    keyword: ''
})

const content = reactive({
  text: '',
})

const onClickSearch = () => {
    if (form.keyword !== ''){
        router.push({name:'search', query: {
            threadname: form.keyword
        }})
    } else {
        notify({title:'Info', message:"キーワードを入力してください", type:'info'})
    }
}

const onClickLogout = () => {
    store.commit("setUserId", 0)
    notify({title:'Success', message:'ログアウトしました', type:'success'})
}

const onClickTop = () => {
    router.push({name:'top'})
}
const onClickProfile = () => {
    router.push({name:'profile', params: {
        id: store.getters.loggedIn
    }})
}

const threadId = router.currentRoute.value.params.threadId

const onClickSignin = () => {
    store.commit("setDestination", {name:'thread', params:threadId})
    router.push({name:'signin'})
}

const onClickSignup = () => {
    store.commit("setDestination", {name:'thread', params:threadId})
    router.push({name:'signup'})
}

const init = () => {
    ApiService.getThread(threadId)
    .then((response) => {
        if (response.data.status === "error") {
            notify({title:'Info', message:response.data.content, type:'info'})
            router.back()
        } else {
            data.list = response.data.list
            for (let i in data.list.text) {
              data.list.text[i] = "<span>" +data.list.text[i] + "</span>"
            }
            data.threadName = response.data.threadName
        }
    })
    .catch((error) => {
        notify({title:'Error', message:error, type:'error'})
    })
}

const onClickUser = (userId) => {
    router.push({name:'profile', params: {
        id: userId
    }})
}

const onClickSubmit = () => {
  if (content.text !== '') {
    if (file.value !== undefined) {
    ApiService.postContentWithFile(file.value[0].raw, content.text, threadId, store.getters.loggedIn)
      .then((response) => {
        if (response.data.status === "error") {
          notify({title:'Info', message:response.data.content, type:'info'})
        } else {
          router.push({name:'thread', params: {
            threadId: threadId
          }})
          content.text = ''
          file.value.splice(0);
          init()
        }
      })
      .catch((error) => {
        notify({title:'Error', message:error, type:'error'})
      })
    } else {
    ApiService.postContent(content.text, threadId, store.getters.loggedIn)
      .then((response) => {
        if (response.data.status === "error") {
          notify({title:'Info', message:response.data.content, type:'info'})
        } else {
          router.push({name:'thread', params: {
            threadId: threadId
          }})
          content.text = ''
          init()
        }
      })
      .catch((error) => {
        notify({title:'Error', message:error, type:'error'})
      })
    }
  } else {
    notify({title:'Info', message:'本文を入力してください', type:'info'})
  }
}

const onEnter = () => {
  if (content.text !== '') {
    if (file.value !== undefined) {
      console.log(file)
    ApiService.postContentWithFile(file.value[0].raw, content.text, threadId, store.getters.loggedIn)
      .then((response) => {
        if (response.data.status) {
          notify({title:'Info', message:response.data.content, type:'info'})
        } else {
          router.replace('/thread/' + threadId)
          file.value.splice(0);
          content.text = ''
          init()
        }
      })
      .catch((error) => {
        notify({title:'Error', message:error, type:'error'})
      })
    } else {
    ApiService.postContent(content.text, threadId, store.getters.loggedIn)
      .then((response) => {
        if (response.data.status === "error") {
          notify({title:'Info', message:response.data.content, type:'info'})
        } else {
          router.replace('/thread/' + threadId)
          content.text = ''
          init()
        }
      })
      .catch((error) => {
        notify({title:'Error', message:error, type:'error'})
      })
    }
  } else {
    notify({title:'Info', message:'本文を入力してください', type:'info'})
  }
}

init()
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
    <el-form-items style="width:50%" label="スレッドを検索">
      <el-input v-model="form.keyword" placeholder="キーワードを入力" @keypress.enter="onClickSearch"/>
      <el-input type="text" name="dummy" style="position:absolute;visibility:hidden" />
    </el-form-items>
    <el-form-items>
      <el-button type="primary" @click="onClickSearch">検索</el-button>
    </el-form-items>
  </el-form>
  <br />
  <el-card style="width:100%" v-if="store.getters.loggedIn !== 0">
    <template #headler>
        <span>投稿</span>
    </template>
    <el-form :model="content">
        <el-form-items>
          <el-input type="textarea" :rows="2" maxlength="255" show-word-limit v-model="content.text" placeholder="本文を入力" @keypress.enter="onEnter"></el-input>
          <el-input type="text" name="dummy" style="position:absolute;visibility:hidden" />
        </el-form-items>

        <el-upload
          v-model:file-list="file"
          :on-remove="handleRemove"
          :limit="1"
          :on-exceed="handleExceed"
          :auto-upload="false"
          accept="image/*"
        >
          <el-button type="primary">ファイルを選択</el-button>
        </el-upload>
        <el-form-items>
          <el-button type="primary" @click="onClickSubmit">送信</el-button>
        </el-form-items>
    </el-form>
</el-card>
  <br />
  <el-card style="width:100%" v-if="data.list.length !== 0">
    <template #header>
      <span>{{ data.threadName }}</span>
    </template>
    <el-row v-for="d in data.list" :key="d">
      <el-card style="width:100%;">
        <template #header>
          <span @click="onClickUser(d.user_id)">{{ d.user_name }}</span> <span style="float:right">{{ d.created_at.split('T')[0] + ' ' + d.created_at.split('T')[1] }}</span>
        </template>
        <div v-html="d.text"></div>
        <br/>
        <img v-if="'img' in d" :src="'data:image/png;base64,' + d.img">
      </el-card>
    <br />
    </el-row>
  </el-card>
</template>
