<template>
  <div>
    <fieldset class="layui-elem-field layui-field-title" style="margin-top: 30px;">
    <legend>过滤</legend>
    </fieldset>  
    <button class="layui-btn layui-btn-lg layui-btn-primary layui-btn-radius"><router-link :to="{ name: 'FilterKeys' }">管理过滤关键词</router-link></button>
    <button class="layui-btn layui-btn-lg layui-btn-primary layui-btn-radius"><router-link :to="{ name: 'FilterGroupNumbers' }">管理过滤QQ群号码</router-link></button>
    <button class="layui-btn layui-btn-lg layui-btn-primary layui-btn-radius"><router-link :to="{ name: 'FilterQqNumbers' }">管理过滤QQ号码</router-link></button>
  </div>
</template>

<script>
export default {
  name: 'FilterCom'
}
</script>

<style>

</style>
