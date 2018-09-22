<template>
  <div id="app">
    <Header></Header>
    <div class="layui-container">  
        <fieldset class="layui-elem-field layui-field-title" style="margin-top: 30px;">
        <legend>过滤关键词管理</legend>
        </fieldset>   
        <table class="layui-hide" id="filter_keys" lay-filter="filter_keys"></table>
        
        <script type="text/html" id="toolbar">
        <div class="layui-btn-container">
            <button class="layui-btn layui-btn-sm" lay-event="addKey">添加关键字</button>
            <!--            
            <button class="layui-btn layui-btn-sm" lay-event="getCheckLength">获取选中数目</button>
            <button class="layui-btn layui-btn-sm" lay-event="isAll">验证是否全选</button>
            -->
        </div>
        </script>
        
        <script type="text/html" id="bar">
        <a class="layui-btn layui-btn-xs" lay-event="edit">编辑</a>
        <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="del">删除</a>
        </script>              
    </div>
  </div>
</template>

<script>
import api from "../api";
// 导入头部组件
import Header from '../components/Header';
export default {
  name: 'FilterKeys',
  components: { // 在app中注册组件
    Header,
  },
  methods:{
    flush_table( get_filter_keys_url=null ){
      var that = this;
      layui.use('table', function(){
        var table = layui.table;
        
        table.render({
          elem: '#filter_keys'
          ,url: get_filter_keys_url
          ,toolbar: '#toolbar'
          ,title: '过滤关键词表'
          ,cols: [[
            {type: 'checkbox', fixed: 'left'}
            ,{field:'id', title:'ID', width:80, fixed: 'left', unresize: true, sort: true}
            ,{field: 'key_name', width: 1020, title:'关键字', align: 'center'}
            ,{fixed: 'right', title:'操作', toolbar: '#bar', width:150}
          ]]
          ,page: true
        }); 
        
        // 头工具栏事件
        table.on('toolbar(filter_keys)', function(obj){
          var checkStatus = table.checkStatus(obj.config.id);
          switch(obj.event){
            case 'addKey':
              layer.prompt({
                formType: 2,
                value:""
              }, function(value, index){
                api.postFilterKeys( { "key_name": value } )
                .then(function( res ){
                  layer.alert( res.data.msg );
                  that.flush_table( api.getFilterKeysUrl() );
                  layer.close(index);
                })
                .catch(function( err ){
                  layer.alert( err.toString() );
                  layer.close(index);
                });
              });
            break;
            case 'getCheckLength':
              var data = checkStatus.data;
              layer.msg('选中了：'+ data.length + ' 个');
            break;
            case 'isAll':
              layer.msg(checkStatus.isAll ? '全选': '未全选');
            break;
          };
        });
        
        //监听行工具事件
        table.on('tool(filter_keys)', function(obj){
          var data = obj.data;
          console.log(obj);
          if(obj.event === 'del'){
            layer.confirm('真的删除行么', function(index){
              api.deleteFilterKeys( data.id )
              .then(function(res){
                layer.alert( res.data.msg );
                obj.del();
                layer.close(index);                
              })
              .catch(function( err ){
                layer.alert( err.data.msg );
              })
            });
          } else if(obj.event === 'edit'){
            layer.prompt({
              formType: 2
              ,value: data.key_name
            }, function(value, index){
              api.updateFilterKeys( data.id, { "key_name": value } )
              .then( function(res){
                layer.alert( res.data.msg );
                obj.update({
                  key_name: value
                });
                layer.close(index);
              } )
              .catch(function(err){
                console.log( err )
                layer.alert( err.toString() );
                layer.close(index);
              })
            });
          }
        });
      });    
    },
  },
  mounted(){
    console.log( "FilterKeys is mounted!" );
    this.flush_table( api.getFilterKeysUrl() );
  }
}
</script>

<style>
</style>
