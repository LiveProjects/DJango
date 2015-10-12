window.onload=function(){
    var gl={
        spanlist:$("#profile_itemlist").find('span')
    };
    //tab
    $("#profile_main_tablist > ul > li").click(function(){
        var index=$(this).index();
        $("#profile_main_card> ul >li").eq(index).show();
        $("#profile_main_card> ul >li").eq(index).siblings().hide();
    });
    $("#profile_itemlist").delegate('ul > li','click',function(e){
        e.stopPropagation();
        e.cancelBubble = true;
        $(this).find('ul').toggle();
        $(this).find("span").css('display','none');

        if($(this).children("ul").css('display')=="block"){

            $(this).children("span").hide();
        }else{
            $(this).children("span").show();
        }
    });

    //添加model
    $("#profile_addcharacter_modal > div ").eq(1).find('input').focus(function(){
        if($(this).parent().is('label')){
            $(this).parent().css('border','2px solid #39f');
        }
    });
    $("#profile_addcharacter_modal > div").eq(1).find('input').blur(function(){
        if($(this).parent().is('label')){
            $(this).parent().css('border','');
        }
    });

    ////自动加载第一行数据
    //var lis = $("#profile_itemlist").find("li");
    //$.each(lis,function(val,index,arr){
    //    $(this).click();
    //});

    //点击异步加载数据
    //$("#profile_itemlist").delegate('li','click',function(e){
    //    console.log($(this).text());
    //    e.stopPropagation();
    //    e.cancelBubble = true;
    //    var that=$(this);
    //
    //    if($(this).find("li").length==0){//need fix
    //        var value=$(this).attr('id');
    //        $.ajax({
    //            url:"ajaxvalue/ajax/",
    //            data:{
    //                'value':value
    //            },
    //            Type:'get',
    //            dataType:'json',
    //            beforeSend:function(){
    //                console.log(value);
    //            },
    //            success:function(data){
    //                console.log(data);
    //                if(data['list']){
    //                    var ul = document.createElement('ul');
    //                    var ele=document.getElementById(value);
    //                    var hr=document.createElement('hr');
    //                    data['list'].forEach(function(val,index,array){
    //                        for(var key in val){
    //                            var li=document.createElement('li');
    //                            li.className='list-group-item';
    //                            li.setAttribute('id',val[key]);
    //                            var a=document.createElement('a');
    //                            a.setAttribute('href',val[key]+'/');
    //                            var text=document.createTextNode(key);
    //                            a.appendChild(text);
    //                            li.appendChild(a);
    //                            ul.appendChild(li);
    //                        }
    //                    })
    //                    //ele.appendChild(hr);
    //                    ele.appendChild(ul);
    //                    var li_list=that.find("li");
    //                    if(li_list){
    //                        $.each(li_list,function(val,index,arr){
    //                            $(this).click();
    //                        });
    //                    }
    //                }
    //            },
    //            error:function(error){
    //                //console.log("son is mull");
    //            }
    //        })
    //    }
    //});
    //备用右键弹框编辑
    //$("#profile_itemlist").delegate('li','dblclick',function(e){
    //    that=$(this);
    //    var val=that.childNodes[0];
    //    alert(val);
    //    $("#submitadd").click();
    //
    //});
    //备用，封锁右键
    //window.document.oncontextmenu=youji;
    function youji(){
        return false;
    }

    //提交新关系
    $("#submitadd").click(function(){
        var data={};
        var commonvar=$("#profile_addcharacter_modal>div").eq(1).find("input");

        var zh_name=data.zh_name;
        var all=0;
        (function(){
            var num=10000;
            var numval=0;

            var input=$("#lastli").find("input");

            $.each(input,function(index,item){
                if($(this).prop('checked')==true){
                    numval=1
                }else {
                    numval = 0
                }
                all=all+(numval*num);
                num=num/10;
            });
        })();

        data.whichcontent=$("#profile_addcharacter_modal>div").eq(0).find('input:checked').val();
        data.zh_name = commonvar.eq(0).val();
        data.en_name = commonvar.eq(1).val();
        data.defination = commonvar.eq(2).val();
        data.regulation = commonvar.eq(3).val();
        data.parent_name = commonvar.eq(4).val();
        data.child_name = commonvar.eq(5).val();
        data.product_use = all;

        var zh_name=data.zh_name;
        var en_name=data.en_name;

        $.ajax({
            url:'add/new/',
            data:{
                'value':JSON.stringify(data)
            },
            dataType:'text',
            Type:'get',
            success:function(data){
                console.log(data);
                if(data!=0){
                    alert("add is success");

                    if($("#"+data).children("ul").length>0){
                        $("#"+data).children("ul").append("<li class='list-group-item'>"+"<a href='"+en_name+"/'>"+zh_name+"</a>"+"</li>");
                        $("#submitadd").prev().click();
                    }else{
                        $("#"+data).append("<ul><li class='list-group-item'>"+"<a href='"+en_name+"/'>"+zh_name+"</a>"+"</li></ul>");
                        $("#submitadd").prev().click();
                    }

                }
            },
            error:function(error){
                console.log(error);
            }
        })
    });

    //修改定义和规则
    $("#profile_detail_changedefine> button,#profile_detail_changeregular >button").bind('click',function(){
        var that=$(this);
        if($(this).text()=="编辑"){
            $(this).prev().removeAttr('disabled').focus();
            $(this).text('完成');

        }else{

            var val=$(this).prev().val();
            var url=$(this).parent().attr('id').split("_")[2];

            $.ajax({
                url:url+"/",
                Type:'get',
                dataType:'text',
                data:{
                    'value':val
                },
                success:function(data){
                    console.log(data);
                    if(data==1){
                        alert("修改成功");
                        that.text("编辑");
                        that.prev().attr('disabled','disabled');
                    }else{
                        alert("修改失败");
                    }
                },
                error:function(error){
                    console.log(error);
                }
            });
        }

    });

    //产品使用标签显示
    var product_use_num=$("#profile_detail_tag").find("button").text();
    !function(num){
        var str=num.toString();
        var arr=[];
        arr=str.split('');

        var start=5-arr.length;
        for(var i=0;i<start;i++){
            arr.unshift(0);
        }
        $.each(arr,function(index){
            if(arr[index]==1){
                //alert($("#profile_detail_tag").find('li').eq(index).html());
                $("#profile_detail_tag").find('li').eq(index).css({'background':'brown','color':'white'});
            }
        });
    }(product_use_num);

    // 实现和输出方式标签显示
    var achieve_method_num=$("#profile_detail_method > button").text();
    (function(num){
        num=parseInt(num);
        $("#profile_detail_method").find("li").eq(num-1).addClass('mark_tag');
        var detail_outputmethod= $("#profile_detail_outputmethod");
        detail_outputmethod.find("li").eq(detail_outputmethod.children("button").text()).addClass('mark_tag');
    })(achieve_method_num);


    //管理detail
    $("#management").bind('click',function(){
        if($("#profile_detail_outputmethod").find("li[class='mark_tag']").index()==0){
            if($(this).text()=="管理"){
                $("#profile_detail_changedefine").children("button").show().end().next().find("button").show();
                $("#proflie_detail_relation").find("span").show();
                $(this).text("取消");
            }else{
                $("#profile_detail_changedefine").children("button").hide().text("编辑").end().next().find("button").hide().text("编辑");
                $("#profile_detail_changedefine").children("textarea").attr('disabled','disabled').end().next().find("textarea").attr('disabled','disabled');
                $("#proflie_detail_relation").find("span").hide();
                $(this).text("管理");
            }
        }else{
            $(this).css('cursor','not-allowed');
        }
    });

    //修改父级
    $("#fixfather").click(function(){
        var val=$(this).parent().prev().find("input").val();

        var that=$(this);
        if(val!=''){
            data={
                'parent_name':val,
                'my_name':$("#en_name").text()
            };
            $.ajax({
                url:'fix/parent/',
                dataType:'text',
                data:{
                    'value':data.parent_name
                },
                Type:'get',
                success:function(data){
                    console.log(data);
                    if(data!=0){
                        alert("修改成功");
                        that.prev().click();
                        $("#proflie_detail_relation > div").eq(0).find("a").text(val);
                        $("#proflie_detail_relation > div").eq(0).find("a").attr('href',"http://10.4.17.165:9550/crawl/resys/profile/"+data+"/");


                    }else{
                        alert("修改失败");
                    }
                },
                error:function(error){
                    console.log(error);
                }
            })
        }
    });

    //撤回历史记录
    $("#history_show").find("button").click(function(){
        var really = confirm("确认撤回吗？");
        if(really){
            var time = $(this).parent().children("span").text();
            var that=$(this);

            $.ajax({
                url:'drawback/history/',
                datatype:'text',
                Type:'get',
                data:{
                    'value':time
                },
                beforeSend:function(){
                    //alert(time);
                },
                success:function(data){
                    if(data==1){
                        alert("撤回成功");
                        var definition = that.prev().prev().text().substring(3);
                        var regulation = that.prev().text().substring(3);

                        $("#profile_detail_changedefine").find("textarea").text(definition);
                        $("#profile_detail_changeregular").find("textarea").text(regulation);

                        $("#history_model").prev().click();

                    }else{
                        alert("撤回失败");
                    }
                },
                error:function(error){
                    console.log(error);
                }

            })
        }
    });

    //加载完成异步数据获取
    if(window.location.pathname == "/crawl/resys/profile/"){
        $.ajax({
            url:"profile_tree/ajax/",
            dataType:'json',
            Type:'get',
            success:function(data){
                console.log(data);
                data = data[0];
                (function(val){
                    //console.log(data);
                    var doc= document.createDocumentFragment();
                    var a="";
                    var test = document.getElementById("test");
                    function show(data,doc){

                        $.each(data,function(index,item,attr){

                            if(Object.prototype.toString.call(item)!='[object Array]'){
                                var li = document.createElement("li");
                                //console.log(a+item.zh_name);
                                li.setAttribute('id', item.en_name);
                                li.setAttribute('class', item.en_name+" list-group-item");
                                var span = document.createElement("span");
                                span.setAttribute('class','badge');

                                var text = document.createTextNode(item.zh_name);
                                var a = document.createElement('a');
                                if(item.profile_type==0){
                                    a.style.color='black';
                                }else if(item.profile_type==1){
                                    a.style.color='red';
                                }
                                a.setAttribute('href',item.en_name+"/");
                                a.appendChild(text);
                                li.appendChild(a);
                                li.appendChild(span);
                                doc.appendChild(li);
                            }else{
                                var ul =document.createElement("ul");
                                ul.style.display="none";
                                doc.lastElementChild.appendChild(ul);

                                show(item,ul);
                            }
                        });
                    };

                    show(data,test);
                })(data);
                //徽章统计

                $.each($("#profile_itemlist").find('span'),function(index,item){
                    //if($(this).next().children('li').length!=0){
                    //    $(this).text($(this).next().children('li').length)
                    //}else{
                    //    $(this).remove();
                    //}
                    $(this).text($(this).next().children('li').length);
                    $("#news").parent().append($("#news"));
                });
            },
            error:function(error){
                console.log(error);
            }
        })
    };

};

