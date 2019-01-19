<template>
  <div id="app">
    <Header></Header>
    <div class="layui-container">  
      <Search></Search>
      <FilterCom></FilterCom>
      <Message></Message>
    </div>
  </div>
</template>

<script>
// 导入头部组件
import Header from '../components/Header';
// 导入搜索组件
import Search from '../components/Search';
// 导入过滤插件
import FilterCom from '../components/FilterCom';
// 导入消息插件
import Message from '../components/Message';
export default {
  name: 'App',
  components: { // 在app中注册组件
    Header,
    Search,
    FilterCom,
    Message
  }
}
</script>

<style>
</style>
