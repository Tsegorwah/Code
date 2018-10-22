/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
window.onload=function(){
    $("#loading").fadeOut();
};
var head=new Vue({
    el:'#head',
    data:{
        logname:"登陆",
        regname:"注册"
    }
});
var selectmap=new Vue({
    el:'#selectmap',
    data:{
     hotshow:false,
     cityname:''
    },
    methods:{ 
       hotblock:function(){
            this.hotshow=true;
       },
        getcityname:function(e){
            cityname=e.target.innerText;
            this.cityname=cityname;
       },
       hotclose:function(){
           this.hotshow=false;
       }      
    }
});
 $(function(){
 $(".mapbt").mouseover(function(){
  $(this).animate({fontSize: "20px",marginLeft:"10px",marginRight:"10px"},"fast");});
  $(".mapbt").mouseout(function(){
  $(this).animate({fontSize: "16px",marginLeft:"2px",marginRight:"2px"},"fast");});
  $(".ltbt").mouseover(function(){
  $(this).animate({height: "80px",width:"80px",marginLeft:"10px",marginRight:"10px"},"fast");});
  $(".ltbt").mouseout(function(){
  $(this).animate({height: "60px",width:"60px",marginLeft:"2px",marginRight:"2px"},"fast");});
 });
