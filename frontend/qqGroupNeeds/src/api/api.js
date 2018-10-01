import axios from 'axios'
import { buildUrl } from '../utils'

// 统一接口地址
let host = "http://127.0.0.1:8080";

// 统一路由前缀
export const ROUTE_PREFIX = "";   // option /qqGroupNeeds

// 获取QQ群消息列表接口地址
export const getMessageUrl = params => { 
    if ( params && params.status ){
        var status_mapping = {
            "待跟进": 0,
            "已忽略": -1,
            "已跟进": 1
        }
        params.status = status_mapping[params.status];
    }
    return buildUrl( `${host}/message/`, params );
 };

// 更新一条群消息的状态（跟进或忽略）
export const updateMessage = (message_id, params) => { return axios.patch( buildUrl( `${host}/message/`+message_id, params ) ) }

// 获取过滤关键词列表接口地址
export const getFilterKeysUrl = params => { return buildUrl( `${host}/message/filter/keys`, params ) };

// 增加一个过滤关键词
export const postFilterKeys = params => { 
    return axios.post(`${host}/message/filter/keys`, params)
 };

// 更新一个过滤关键词
export const updateFilterKeys = (key_id, params) => { return axios.patch(`${host}/message/filter/keys/` + key_id, params) };

// 删除一个过滤关键词
export const deleteFilterKeys = key_id => { return axios.delete( `${host}/message/filter/keys/`+key_id ) ;}

// 获取过滤QQ群号码列表接口地址
export const getFilterGroupNumberUrl = params => { return buildUrl( `${host}/message/filter/group_numbers`, params ) };

// 增加一个过滤QQ群号码
export const postFilterQqGroup = params => { return axios.post(`${host}/message/filter/group_numbers`, params) };

// 更新一个过滤QQ群号码
export const updateFilterQqGroup = (number_id, params) => { return axios.patch(`${host}/message/filter/group_numbers/` + number_id, params) };

// 删除一个过滤QQ群号码
export const deleteFilterQqGroup = number_id => { return axios.delete( `${host}/message/filter/group_numbers/`+number_id ) };

// 获取过滤QQ号列表接口地址
export const getFilterQqNumberUrl = params => { return buildUrl( `${host}/message/filter/qq_numbers`, params ) };

// 增加一个过滤QQ号
export const postFilterQq = params => { return axios.post(`${host}/message/filter/qq_numbers`, params) };

// 更新一个过滤QQ号
export const updateFilterQq = (number_id, params) => { return axios.patch(`${host}/message/filter/qq_numbers/` + number_id, params) };

// 删除一个过滤QQ号码
export const deleteFilterQq = number_id => { return axios.delete( `${host}/message/filter/qq_numbers/`+ number_id ) };
