// function  animate_(){
//  // var list = document.getElementsByClassName('ydzx_lis').item(0);
//      var list1= document.getElementById("l1")
//      var list2= document.getElementById("l2")
//      var list3= document.getElementById("l3")
//      var list4= document.getElementById("l4")
//      var  offset=-300
//      var time = 600;
//      var interval = 10;
//      var speed = offset / (time / interval);
//
//       list1.style.left = parseInt(list2.offsetLeft) + speed + 'px';
//       list2.style.left = parseInt(list2.offsetLeft) + speed + 'px';
//       list3.style.left = parseInt(list3.offsetLeft) + speed + 'px';
//       list4.style.left = parseInt(list4.offsetLeft) + speed + 'px';
//
//      // alert( list1.offsetLeft)
//     // alert( parseInt(list2.style.left))
//     //    list1.style.left = list2.offsetLeft +'px'
//     //    list2.style.left =  list3.offsetLeft +'px'
//     //     list3.style.left = list4.offsetLeft +'px'
//     //     list4.style.left = list1.offsetLeft +'px'
//     //  list2.style.left = -300+'px'
//      // list2.style.left = parseInt(list3.style.left)+'px'
//      // list3.style.left = parseInt(list4.style.left)+'px'
//      // list4.style.left = parseInt(list1.style.left)+'px'
// }
// setInterval(animate_,4000);

   var swiper = new Swiper('.swiper', {

       spaceBetween: 5, //slide之间距——间距30

      // slidesPerView: 'auto', //多列——宽度自动
      slidesPerGroupSkip: 2, //设置 前n个不列入分组 ——前3个不列入分组，将单独出现


      slidesPerView: 1, // 多列——一屏显示4列
      loopFillGroupWithBlank: true, //循环滚动相接处填充空白区分头尾
        loop: true,

		lazy: {
            //loadPrevNext: true,
        },
        autoplay: {
            delay: 2000,
        },
		navigation: {
		  nextEl: '.swiper-button-next',
		  prevEl: '.swiper-button-prev',
		},
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },

        direction:'horizontal'
    });