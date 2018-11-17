import axios from 'axios';
import { getCookie } from '../utils'

axios.interceptors.request.use(  // 统一http request 拦截器
    config => {
        cookie = getCookie();
        if ( cookie ) {  // 判断是否存在cookie，如果存在的话，则每个http header都加上cookie
            config.headers.Cookie = cookie;
        }
        return config;
    },
    err => {
        return Promise.reject(err);
    }
);
