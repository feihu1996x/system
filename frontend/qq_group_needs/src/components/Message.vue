<template>
  <div>
    <fieldset class="layui-elem-field layui-field-title" style="margin-top: 30px;">
    <legend>消息管理</legend>
    </fieldset>  
    <table class="layui-hide" id="Message" lay-filter="Message"></table>
    
    <script type="text/html" id="toolbar">
    <div class="layui-btn-container">
        <!--
        <button class="layui-btn layui-btn-sm" lay-event="getCheckData">获取选中行数据</button>
        <button class="layui-btn layui-btn-sm" lay-event="getCheckLength">获取选中数目</button>
        <button class="layui-btn layui-btn-sm" lay-event="isAll">验证是否全选</button>
        -->
    </div>
    </script>
    
    <script type="text/html" id="bar">
    <a class="layui-btn layui-btn-xs" lay-event="follow">跟进</a>
    <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="ignore">忽略</a>
    </script>    
  </div>
</template>

<script>
    import api from "../api";
    import event  from '../utils/event.js';
    export default {
        name: 'Message',
        methods: {
            flush_table( get_message_url=null ){
                layui.use('table', function(){
                    var table = layui.table;
                    table.render({
                        elem: '#Message'
                        ,url: get_message_url
                        ,toolbar: '#toolbar'
                        ,title: '消息表'
                        ,cols: [[
                        {type: 'checkbox', fixed: 'left'}
                        ,{ field: 'id', title: 'ID', width:80, sort: true }
                        ,{ field: 'group_number', title: 'QQ群号码', width:150 }
                        ,{ field: 'group_name', title: 'QQ群名称', width:150 }
                        ,{ field: 'content', title: '项目信息', width:150 }
                        ,{ field: 'qq_number', title: '发布人QQ', width:150 }
                        ,{ field: 'send_time', title: '消息发布时间', width:150 }
                        ,{ field: 'status', title: '消息处理状态', width:150 }
                        ,{ field: 'operator', title: '操作者', width:150 }
                        ,{fixed: 'right', title:'操作', toolbar: '#bar', width:150}
                        ]]
                        ,page: true
                    });
                
                    // 头工具栏事件
                    table.on('toolbar(Message)', function(obj){
                        var checkStatus = table.checkStatus(obj.config.id);
                        switch(obj.event){
                        case 'getCheckData':
                            var data = checkStatus.data;
                            layer.alert(JSON.stringify(data));
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
                
                    // 监听行工具事件
                    table.on('tool(Message)', function(obj){
                        console.log(obj);
                        var data = obj.data;
                        if(obj.event === 'ignore'){
                            if ( "已忽略" === data.status ){
                                layer.confirm( "当前已经是忽略状态了额～，您是要取消忽略操作吗?", function( index ){
                                    api.updateMessage( data.id, { status: 0 } )
                                    .then( function( res ){
                                        layer.alert( res.data.msg );
                                        obj.update({
                                            status: "待跟进"
                                        });
                                    } )
                                    .catch( function( err ){
                                        layer.alert( err.data.msg );
                                    } )
                                } );
                            }
                            else {
                                layer.confirm('真的要忽略么', function(index){
                                    api.updateMessage( data.id, { status: -1 } )
                                    .then( function( res ){
                                        layer.alert( res.data.msg );
                                        obj.update( {
                                            status: "已忽略"
                                        } );
                                    } )
                                    .catch( function( err ){
                                        layer.alert( err.data.msg );
                                    } )
                                });
                            }
                        } else if(obj.event === 'follow'){
                            if ( "已跟进" === data.status ){
                                layer.confirm("当前已经是跟进状态了，您是要取消跟进吗？", function( index ){
                                    api.updateMessage( data.id, { status: 0 } )
                                    .then( function( res ){
                                        layer.alert( res.data.msg );
                                        obj.update({
                                            status: "待跟进"
                                        });
                                    } )
                                    .catch( function( err ){
                                        layer.alert( err.data.msg );
                                    } )                                    
                                });
                            }
                            else {
                                api.updateMessage( data.id, { status: 1 } )
                                .then(function( res ){
                                    layer.alert( res.data.msg );
                                    obj.update({
                                        status: "已跟进"
                                    });
                                })
                                .catch(function(err){
                                    layer.alert( err.data.msg );
                                })
                            }
                        }
                    });
                });   
            }
        },
        mounted(){
            console.log( "message is mounted!" );       
            this.flush_table( api.getMessageUrl() );
            event.$on( "search", ( params )=>{
                this.flush_table( api.getMessageUrl( params ) );
            } ); // 监听Search组件触发的自定义事件以实时获取搜索字段
        }
    }
</script>

<style>

</style>
