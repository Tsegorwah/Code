/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
function save(diccenter){
    savecenter=diccenter;
    return savecenter;
}
var map = new AMap.Map('container', {
        resizeEnable: true,
        zoom:11,
        center:[116.397428,39.90923]
 });
 function citycenter(buttonValue){
    var dic=new Array();
    dic["佛山"]=[113.133413,23.030547];
    dic["广州"]=[113.266622,23.130353];
    dic["上海"]=[121.455564,31.222443];
    dic["深圳"]=[114.09144,22.541673];
    dic["沈阳"]=[123.463428,41.678716];
    dic["成都"]=[104.076721,30.568221];
    dic["武汉"]=[114.312305,30.594758];
    dic["北京"]=[116.397428,39.90923];
    map.setCenter(dic[buttonValue]);
 }
 function cname(num){
     var buttonValue= document.getElementById(num).innerHTML;
     citycenter(buttonValue);
 }
 var heatmap;
 var points =[
        {"lng":116.191031,"lat":39.988585,"count":10000},
        {"lng":116.389275,"lat":39.925818,"count":10000}, 
        {"lng":116.287444,"lat":39.810742,"count":12000},
        {"lng":116.481707,"lat":39.940089,"count":13000},
        {"lng":116.410588,"lat":39.880172,"count":14000},
        {"lng":116.394816,"lat":39.91181,"count":15000},
        {"lng":116.416002,"lat":39.952917,"count":16000}
    ];
    map.plugin(["AMap.Heatmap"],function() {      //加载热力图插件
        heatmap = new AMap.Heatmap(map,{
			radius:50,  //给定半径
			opacity: [0,0.8]
		});    //在地图对象叠加热力图
        heatmap.setDataSet({
		data:points,
		max:100
		}); //设置热力图数据集
        //具体参数见接口文档
    }); 
