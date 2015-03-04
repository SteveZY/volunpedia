function qq_login(){
   QC.Login({
       btnId:"qq_login_btn",
       scope:"all",
       size: "A_M"
   }, function(reqData, opts){
          var dom = document.getElementById(opts['btnId']),
          _logoutTemplate=[
            //icon
            '<span><img src="{figureurl}" class="{size_key}"/></span>',
            //nickname            
            '<span style="margin-left: 6px;">{nickname}</span>',
            //logout
            '<span><a href="javascript:QC.Login.signOut();" style="margin-left: 6px;">logout</a><span>'    
          ].join("");
          dom && (dom.innerHTML = QC.String.format(_logoutTemplate, {
               nickname : QC.String.escHTML(reqData.nickname), 
               figureurl : reqData.figureurl
          }))
        //alert(["Current user's nickname is " + reqData.nickname, "figuerurl is " + reqData.figureurl].join("\n"));  
        if(QC.Login.check()){
            QC.Login.getMe(function(openId, accessToken){
                if(openId){
                    $("#openididentifier").val(openId);
                    $("#loginform").append('<input type="hidden" name="oidstage" value="1" />');  
                    $("#loginform").submit();
                }
            });
        }
   });
}

function wb_login() {
    WB2.anyWhere(function(W){
    W.widget.connectButton({
        id: "wb_connect_btn",
        type:"3,2",
        callback : {
            login:function(o){
                if(o.id){
                    $("#openididentifier").val(o.idstr);
                    $("#loginform").append('<input type="hidden" name="oidstage" value="1" />');
                    $("#loginform").submit();
                }
            },
            logout:function(){
                //alert('logout');
            }
        }
   });
  });
}

function qq_logout() {
    if(QC.Login.check()){
        QC.Login.signOut();
    }
}

function wb_logout() {
    if(WB2.checkLogin()){
        WB2.logout(function(){
        });
    }
}
