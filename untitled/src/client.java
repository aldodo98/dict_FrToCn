
import java.lang.System;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.*;
import java.io.OutputStream;
import java.io.PrintStream;
import java.io.InputStream;

public class client {
    public static void main(String[] args){
        //System.out.println("Hello World!");
        // TODO Auto-generated method stub

        try {
            InetAddress addr = InetAddress.getLocalHost();
            String host=addr.getHostName();
            //String ip=addr.getHostAddress().toString(); //获取本机ip
            //log.info("调用远程接口:host=>"+ip+",port=>"+12345);
            host = "172.17.57.113";
            // 初始化套接字，设置访问服务的主机和进程端口号，HOST是访问python进程的主机名称，可以是IP地址或者域名，PORT是python进程绑定的端口号
            Socket socket = new Socket(host,12345);

            // 获取输出流对象
            OutputStream os = socket.getOutputStream();
            PrintStream out = new PrintStream(os);
            // 发送内容
            out.print("Bob");
            // 告诉服务进程，内容发送完毕，可以开始处理
            //print("哪个词典？accessoires_dict.json,beaute_dict.json,bijoux_dict.json,chaussures_dict.json,pretaporter_dict.json,sac_dict.json")
            out.print(";accessoires_dict.json");
            out.print(";over");
            // 获取服务进程的输入流
            InputStream is = socket.getInputStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(is,"utf-8"));
            String tmp = null;
            StringBuilder sb = new StringBuilder();
            // 读取内容
            while((tmp=br.readLine())!=null)
                sb.append(tmp).append('\n');
            System.out.print(sb);
            // 解析结果
            //JSONArray res = JSON.parseArray(sb.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
