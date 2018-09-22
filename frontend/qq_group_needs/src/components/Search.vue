<template>
  <div>
    <fieldset class="layui-elem-field layui-field-title" style="margin-top: 30px;">
      <legend>搜索</legend>
    </fieldset>    
    <div class="layui-input-inline">
      <input placeholder="群号码/群名称" autocomplete="on" class="layui-input" v-model="group" >
    </div>
    <div class="layui-input-inline">
      <input placeholder="项目信息" autocomplete="on" class="layui-input" v-model="content" >
    </div>
    <div class="layui-input-inline">
      <input placeholder="发布人QQ" autocomplete="on" class="layui-input" v-model="qq_number" >
    </div>
    <div class="layui-input-inline">
      <input placeholder="状态" autocomplete="on" class="layui-input" v-model="status" >
    </div>
    <div class="layui-input-inline">
      <input placeholder="操作人" autocomplete="on" class="layui-input" v-model="operator" >
    </div>                    
  </div>
</template>

<script>
import event  from '../utils/event.js';
export default {
  name: 'Search',
  data(){
    return {
        group: '',
        content: '',
        qq_number: '',
        status: '',
        operator: ''
    }
  },
  updated(){
    event.$emit( "search", {
      group: this.group,
      content: this.content,
      qq_number: this.qq_number,
      status: this.status,
      operator: this.operator
    } );
  }
}
</script>

<style>

</style>
