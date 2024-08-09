var  num=1;
var number=1
function  time_() {

    if  (num===7){
        num=1
    }
      var img =document.getElementById("imginfo")
         document.getElementById("imginfo").style.backgroundImage="url('/static/image/"+num+".jpg')"
         document.getElementById("b"+num).style.background="rgb(255,97,3)"
     img.onclick=function (){
        var random1 = Math.floor(Math.random()*6)+1;
         var but=document.getElementById("b"+random1)
          but.click()
    }


    if  (num>=2){
         number=num-1
         // /alert(number)
         document.getElementById("b"+number).style.background="rgb(220,245,245)"

      }
     if  (num===1 & number>1){

         number=6
         document.getElementById("b"+number).style.background="rgb(220,245,245)"
    }
    num++

}




setInterval(time_,4000)


