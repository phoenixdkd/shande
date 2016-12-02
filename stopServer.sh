PID=`ps -ef|grep python|grep usr |grep -v grep|grep manage.py|grep 8001|awk '{print \$2}'`
if [ ! -z $PID ];then
	kill $PID
fi

