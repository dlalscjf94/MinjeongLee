package org.techtown.homecctv;

import android.os.AsyncTask;

import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;

public class MyClientTask extends AsyncTask<Void, Void, Void> {
    String dstAddress;
    int dstPort;
    String myMessage = "";

    MyClientTask(String addr, int port, String message){
        dstAddress = addr;
        dstPort = port;
        myMessage = message;
    }

    @Override
    protected Void doInBackground(Void... arg0) {

        Socket socket = null;
        myMessage = myMessage.toString();
        try {
            socket = new Socket(dstAddress, dstPort);
            //송신
            OutputStream out = socket.getOutputStream();
            out.write(myMessage.getBytes());

        } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }finally{
            if(socket != null){
                try {
                    socket.close();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        }
        return null;
    }
}
