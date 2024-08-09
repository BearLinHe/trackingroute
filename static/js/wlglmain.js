layui.use(['layer', 'element'], function () {

        var layer = layui.layer
            , element = layui.element,
            $ = layui.$;

        element.on('nav(test)', function (elem) {
                $('.popup-menu-items dd a').removeClass('layui-this');

                if ($(this).attr('item-sub-id') != undefined) {
                    var subId = $(this).attr('item-sub-id');
                    $('.popup-menu-items dd a[item-sub-id="' + subId + '"]').addClass('layui-this');

                    $('.thumbnail-nav-item').removeClass('layui-this');
                    $('.thumbnail-nav-item[item-id="' + itemId + '"]').addClass('layui-this');
                }
                var rest=this.text
                var result = rest.split(" ").join("");
                result = result.replace(/\s/g, "");

                switch (result) {
                    case '轨迹查询':
                        // alert('ks1')
                        var address = $(this).attr("data-src");
                        $('#btitle').text('轨迹查询')
                        $('#iframe').attr('src', address);
                        break;
                    case '轨迹设置':
                        // alert('ks1')
                        var address = $(this).attr("data-src");
                        $('#btitle').text('轨迹设置')
                        $('#iframe').attr('src', address);
                        break;
                    case '轨迹修改':

                        var address = $(this).attr("data-src");
                        // alert(address)
                        $('#btitle').text('轨迹修改')
                        $('#iframe').attr('src', address);
                        break;
                        case '员工信息':
                        var address = $(this).attr("data-src");
                        // alert(address)
                        $('#btitle').text('添加用户')
                        $('#iframe').attr('src', address);
                        break;


                }
            }
        )
    }
)
