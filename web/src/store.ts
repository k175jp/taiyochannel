import { createStore } from 'vuex'


import createPersistedState from 'vuex-persistedstate'

const store = createStore({
    state: {
        userId: 0,
        destination: {name:'', params:''}
    },
    getters: {
        loggedIn: (state) => {
            return state.userId
        },
        destinationName: (state) => {
            return state.destination.name
        },
        destinationParams: (state) => {
            return state.destination.params
        }
    },
    mutations: {
        setUserId(state, userId) {
            state.userId = userId
        },
        setDestination(state, destination) {
            state.destination.name = destination.name
            state.destination.params = destination.params
        },
    },
    actions: {},
    plugins: [createPersistedState({
        key: 'userData',
        storage: window.sessionStorage
    })]
});

export default store;