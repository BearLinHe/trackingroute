
 layui.use(['tree', 'table','form','util'], function(){
  var table = layui.table;
  var tree = layui.tree;
  var $ = layui.jquery;
  var form = layui.form;
  var util = layui.util;
  layer = layui.layer
  var hwbh = $('#loadSearch').val();
  var cysbh = $('#MCSearch').val();
  table.reload('rtTable', {
            where: {} // 设定查询条件为空对象，相当于没有查询条件，从而没有数据返回
        });
  // 发起AJAX请求获取Tree数据
  $.ajax({
    url: '/wlxg/tree/',  // Django后端API的URL
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      // 使用Tree组件初始化
      tree.render({
         elem: '#tree' // 指向树容器的DOM对象
        ,data: data // 树的数据
           ,showCheckbox: true
          ,click: function(obj){
           let json = JSON.stringify(obj);
           var parsedData = JSON.parse(json);
           if (parsedData.data.ismw=='1'){

               let str=parsedData.data.title
               let arr = str.split("|");
                $('#loadSearch').val(arr[0])
                $('#MCSearch').val(arr[1])
                doSearch()

           }
              //

        // 节点点击事件，可以在这里加载表格数据
      }
        // 其他配置项...
      })
    }
  });
   // 发起AJAX请求获取表格数据数据
  $.ajax({
    url: '/wlxg/table/',  // Django后端API的URL
    type: 'GET',
    dataType: 'json',
       data: {
        'hwbh': hwbh,
        'hwbh': cysbh
      },

    success: function(data) {
        console.log(data)
      // 使用Tree组件初始化
      table.render({
          id:'LP13',
         elem: '#rtTable' // 指向树容器的DOM对象
        , data:  data.table2_data,  //data,
      limit:100000,
      page: true, // 开启分页
      event:true,
          cellMinWidth: 100,
    cols: [[
          {type: 'checkbox'},
        {field:'number', title: '序号' , align:'center',type:'numbers'},
        {field: 'LP11', title: '抵达时间',align:"center"},
        {field: 'LP12', title: '终点地址',align:"center"},
        { fixed: 'right', title: '操作', toolbar: '#barDemo', width: 300 }

    ]],
      });
        //事件监听
           //头工具栏事件
                table.on('tool(rtTable)', function (obj) {
                     var data = obj.data;
                      var czlx="";
                    if (obj.event === 'del') {
                        layer.confirm('真的删除行么', function (index) {
                            czlx='del'
                            delFormValue(data,czlx);
                            obj.del();
                            layer.close(index);
                        });
                    } else if (obj.event === 'edit') {
                        czlx='edit'
                        var jsonObj = JSON.stringify(data);
                         layer.open({
                        //layer提供了5种层类型。可传入的值有：0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
                        type: 1,
                        title: "物流路线修改",
                        area: ['420px', '330px'],
                        content: $("#popUpdateTest"),//引用的弹出层的页面层的方式加载修改界面表单

                         success: function (layer, index) {
                             console.log(jsonObj)

                             $('#IdCode').val(data.LP13);
                           $('#neweqptIdCode').val(data.LP08);
                           $('#neweqptName').val(data.LP12);
                        }
                    });
                         setFormValue(obj,data,czlx);

                    }
                    else if (obj.event === 'add') {
                        var jsonObj = JSON.stringify(data);
                        czlx='add'
                         layer.open({
                        //layer提供了5种层类型。可传入的值有：0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
                        type: 1,
                        title: "物流路线增加",
                        area: ['420px', '330px'],
                        content: $("#popUpdateTest"),//引用的弹出层的页面层的方式加载修改界面表单

                         success: function (layer, index) {
                             console.log(jsonObj)

                             $('#IdCode').val(data.LP13);
                        }
                    });
                         setFormValue(obj,data,czlx);

                    }
                    else if (obj.event === 'modify') {
                        var jsonObj = JSON.stringify(data);
                         czlx='modify'
                         layer.open({
                        //layer提供了5种层类型。可传入的值有：0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
                        type: 1,
                        title: "整条物料路线修改",
                        area: ['420px', '330px'],
                        content: $("#popUpdateTest"),//引用的弹出层的页面层的方式加载修改界面表单

                         success: function (layer, index) {
                             console.log(jsonObj)

                             $('#IdCode').val(data.LP13);
                        }
                    });
                         czlx='modify'
                         setFormValue(obj,data,czlx);
                    }


                });

        function setFormValue(obj,data,czlx){
           form.on('submit(demo11)', function(massage) {
               alert(czlx)
               var LP08=$('#neweqptIdCode').val()
               var LP12=$('#neweqptName').val()
               $.ajax({
                   url:'/wlxg/xlxg/',
                   type:'POST',
                   data:{
                       'uuid':data.LP13,
                       'LP08':LP08,
                       'LP12':LP12,
                       'CZLX':czlx},
                   success:function (msg) {
                        //
                       // alert(data.LP13)

                         //alert(msg.returnCode==200)
                       if(msg.returnCode==200){
                           layer.closeAll('loading');
                           layer.load(2);
                       }else{
                            alert('ERR')
                           layer.msg("修改失败", {icon: 5});
                       }
                   }
               })
           })

       }
           table.render({
         elem: '#table1' // 指向树容器的DOM对象
        , data:  data.table1_data,  //data,
    cols: [[

        {field: 'TP01', title: 'Load#',width:155,align:"center"},
        {field: 'TP02', title: 'MC#',width:155,align:"center"},
        {field: 'TP04', title: 'Truck#',width:155,align:"center"},
        {field: 'TP13', title: 'Trailer#',width:155,align:"center"},
         {field: 'TP05', title: 'Driver name',width:155,align:"center"},

    ]]        // 其他配置项...
      });
    }});
},);

function doSearch() {
  layui.use(['layer', 'form','table'], function() {
       var table = layui.table;
      var layer = layui.layer
          , form = layui.form;
       var $ = layui.jquery;
       var hwbh = $('#loadSearch').val();
       var cysbh = $('#MCSearch').val();
       table.reload('rtTable', {
            where: {} // 设定查询条件为空对象，相当于没有查询条件，从而没有数据返回
        });

       $.ajax({
    url: '/wlxg/table/',  // Django后端API的URL
    type: 'GET',
    dataType: 'json',
       data: {
        'hwbh': hwbh,
        'cysbh': cysbh
      },
    success: function(data) {
       // alert( JSON.stringify(data))
      // 使用Tree组件初始化
      table.render({
          id:'LP13',
         elem: '#rtTable' // 指向树容器的DOM对象
        , data:  data.table2_data,  //data,
      limit:100000,
      page: true, // 开启分页
      event:true,
          cellMinWidth: 100,
    cols: [[
          {type: 'checkbox'},
        {field:'number', title: '序号' , align:'center',type:'numbers'},
        {field: 'LP11', title: '抵达时间',align:"center"},
        {field: 'LP12', title: '终点地址',align:"center"},
        { fixed: 'right', title: '操作', toolbar: '#barDemo', width: 300 }

    ]],
      });
        //事件监听
           //头工具栏事件
                table.on('tool(rtTable)', function (obj) {
                     var data = obj.data;
                      var czlx="";


                    if (obj.event === 'del') {
                        layer.confirm('真的删除行么', function (index) {
                            czlx='del'
                            setFormValue(obj,data,czlx);
                            obj.del();
                            layer.close(index);
                        });

                    } else if (obj.event === 'edit') {
                        czlx='edit'
                        var jsonObj = JSON.stringify(data);
                         layer.open({
                        //layer提供了5种层类型。可传入的值有：0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
                        type: 1,
                        title: "单条物料路线修改",
                        area: ['420px', '330px'],
                        content: $("#popUpdateTest"),//引用的弹出层的页面层的方式加载修改界面表单

                         success: function (layer, index) {
                             console.log(jsonObj)

                             $('#IdCode').val(data.LP13);
                           $('#neweqptIdCode').val(data.LP08);
                           $('#neweqptName').val(data.LP12);
                        }
                    });
                         setFormValue(obj,data,czlx);

                    }
                    else if (obj.event === 'add') {
                        var jsonObj = JSON.stringify(data);
                         czlx='add'
                         layer.open({
                        //layer提供了5种层类型。可传入的值有：0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
                        type: 1,
                        title: "物流路线增加",
                        area: ['420px', '330px'],
                        content: $("#popUpdateTest"),//引用的弹出层的页面层的方式加载修改界面表单

                         success: function (layer, index) {
                             console.log(jsonObj)

                             $('#IdCode').val(data.LP13);
                        }
                    });
                         setFormValue(obj,data,czlx);

                    }  else if (obj.event === 'modify') {
                        var jsonObj = JSON.stringify(data);
                        czlx='modify'
                         layer.open({
                        //layer提供了5种层类型。可传入的值有：0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
                        type: 1,
                        title: "整条物料路线修改",
                        area: ['420px', '330px'],
                        content: $("#popUpdateTest"),//引用的弹出层的页面层的方式加载修改界面表单

                         success: function (layer, index) {
                             console.log(jsonObj)

                             $('#IdCode').val(data.LP13);
                        }
                    });
                         czlx='modify'
                         setFormValue(obj,data,czlx);
                    }



                });


function setFormValue(obj,data,czlx){

           form.on('submit(demo11)', function(massage) {
               alert(czlx)
               var LP08=$('#neweqptIdCode').val()
               var LP12=$('#neweqptName').val()

               $.ajax({
                   url:'/wlxg/xlxg/',
                   type:'POST',
                   data:{
                       'uuid':data.LP13,
                       'LP08':LP08,
                       'LP12':LP12,
                       'CZLX':czlx},
                   success:function (msg) {
                        // alert(data.LP13)

                         // alert(msg.returnCode==200)
                       if(msg.returnCode==200){
                           layer.closeAll('loading');
                           layer.load(2);
                             layer.msg("操作成功", {icon: 6});
                       }else{
                            alert('ERR')
                           layer.msg("失败", {icon: 5});
                       }
                   }
               })
           })

       }
           table.render({
         elem: '#table1' // 指向树容器的DOM对象
        , data:  data.table1_data,  //data,
    cols: [[

        {field: 'TP01', title: 'Load#',width:155,align:"center"},
        {field: 'TP02', title: 'MC#',width:155,align:"center"},
        {field: 'TP04', title: 'Truck#',width:155,align:"center"},
        {field: 'TP13', title: 'Trailer#',width:155,align:"center"},
         {field: 'TP05', title: 'Driver name',width:155,align:"center"},

    ]]        // 其他配置项...
      });
    }});


  })


}
function delFormValue(data,czlx){

     layui.use('layer', function() {
         var $ = layui.jquery;
           $.ajax({
              url: '/wlxg/xldel/',
              type: 'POST',
               data: {
                       'uuid': data.LP13,
                   },
               success: function (msg) {
                       layer.msg("删除成功", {icon: 6});
                   }
           })
     })

}
//
// function delFormValue(obj,data,czlx){
//
//            layui.use(['layer', 'form','table'], function() {
//                var $ = layui.jquery;
//                 alert('czlx')
//                $.ajax({
//                    url: '/wlxg/xlxg/',
//                    type: 'POST',
//                    data: {
//                        'uuid': data.LP13,
//                        'LP08': LP08,
//                        'LP12': LP12,
//                        'CZLX': czlx
//                    },
//                    success: function (msg) {
//                        alert(msg)
//                    }
//                })
//         })}