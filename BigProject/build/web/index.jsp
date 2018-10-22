<%-- 
    Document   : index
    Created on : 2018-9-29, 16:46:30
    Author     : yyznb
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link href="css/mapcss.css" rel="stylesheet" type="text/css"/>
         <script type="text/javascript" src="js/vue.js"></script>
          <script src="https://webapi.amap.com/maps?v=1.4.10&key=69c70ee2c4d2e932f9a8b4ac0b5afb29"></script>
          <script type="text/javascript" src="js/1.9.1jquery.min.js"></script>
          <script type="text/javascript" src="js/jquery-ui.min.js"></script>
        <title>JSP Page</title>
    </head>
    <body>
        <div id="loading">加载中...</div>
        <jsp:include flush="true" page="head.jsp"></jsp:include>
        <div id="selectmap">
            <div id="select" align="center">
                <jsp:include flush="true" page="map-button.jsp"></jsp:include>
            </div>   
            <div id="mapbox">
                 <div id="map" v-show="hotshow"><jsp:include flush="true" page="hot.jsp"></jsp:include></div>
                <div id="luntan">
                <jsp:include flush="true" page="luntan.jsp"></jsp:include>
            </div>
            </div>
        </div>
        <jsp:include flush="true" page="tail.jsp"></jsp:include>
    </body>
     <script type="text/javascript" src="js/mapjs.js"></script>  
     <script type="text/javascript" src="js/hot.js"></script> 
</html>
