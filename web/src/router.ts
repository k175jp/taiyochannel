import { createRouter,createWebHistory } from 'vue-router';
import Top from './components/TopPage.vue';
import Signin from './components/Signin.vue';
import Signup from './components/SignupPage.vue';
import Profile from './components/ProfilePage.vue';
import UpdateProfile from './components/UpdateProfilePage.vue';
import Search from './components/SearchPage.vue';
import Thread from './components/ThreadPage.vue';
import NewThread from './components/NewThreadPage.vue';
import NotFound from './components/NotFoundPage.vue';

const routes = [
    { path: '/', name: 'top', component: Top },
    { path: '/:catchAll(.*)', name: 'not_found', component: NotFound},
    { path: '/signin', name: 'signin', component: Signin },
    { path: '/signup', name: 'signup', component: Signup},
    { path: '/profile/:id', name: 'profile', component: Profile},
    { path: '/update_profile/:content', name: 'update_profile', component: UpdateProfile},
    { path: '/search', name: 'search', component: Search },
    { path: '/thread/:threadId', name: 'thread', component: Thread },
    { path: '/new_thread', name: 'new_thread', component: NewThread },
]

const router = createRouter({
    history: createWebHistory(),
    routes:routes,
})

export default router;