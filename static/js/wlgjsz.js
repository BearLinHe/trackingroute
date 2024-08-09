function doSearch() {
  var hwbh = $('#query1').val();
  var cysbh = $('#query2').val();
  layui.use(['layer', 'form'], function(){
    var layer = layui.layer
    ,form = layui.form;
    // 发起AJAX请求
    $.ajax({
      url: '/wlgj', // Django视图的URL
      type: 'GET',
      data: {
        'query1': hwbh,
        'query2': cysbh
      },
      success: function(data) {
        // 假设返回的数据是JSON格式
        layer.msg('搜索成功', {time: 1000});

        // 更新页面的某个部分，比如表格

      },
      error: function() {
        layer.msg('搜索失败', {time: 1000});
      }
    });
  });
}